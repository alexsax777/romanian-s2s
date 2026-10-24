"""Adaptor LLM OpenAI-compatible cu failover GonkaRouter -> xKiro.

- Streaming SSE cu metrici: TTFT (time-to-first-token), total, provider folosit.
- Failover: primar GonkaRouter (GLM-5.3-Flash) → fallback xKiro, o singură reîncercare.
- Fără chei în cod sau loguri — se citesc din env la fiecare call.
- requests, nu urllib (WAF-ul providerilor blochează user-agent urllib).

Folosire:
    from llm_adapter import chat_stream
    gen, state = chat_stream([{"role": "user", "content": "Salut"}])
    for piece in gen:
        print(piece, end="", flush=True)
    print(state["provider"], state["ttft_s"], state["total_s"])
"""
import json
import os
import sys
import time

import requests


def _providers():
    """Ordinea failover. Cheile se citesc din env la call-time; nu se loghează."""
    return [
        ("gonkarouter",
         os.environ.get("GONKAROUTER_BASE_URL", "https://api.gonkarouter.io/v1"),
         os.environ.get("GONKAROUTER_API_KEY") or os.environ.get("GONKA_API_KEY", ""),
         os.environ.get("GONKAROUTER_MODEL", "zai-org/GLM-5.3-Flash")),
        ("xkiro",
         os.environ.get("XKIRO_BASE_URL", "https://api.xkiro.com/v1"),
         os.environ.get("XKIRO_API_KEY", ""),
         os.environ.get("XKIRO_MODEL", "qwen/qwen3.7-flash:free")),
    ]


def _stream_once(base_url, api_key, model, messages, max_tokens,
                 connect_timeout=10, read_timeout=60, disable_thinking=False):
    """Un request SSE; yields bucăți de conținut. Ridică la erori HTTP/rețea."""
    payload = {"model": model, "stream": True, "max_tokens": max_tokens, "messages": messages}
    if disable_thinking:
        # vLLM: scurtează/elimină reasoning-ul GLM la nivel de chat template
        payload["chat_template_kwargs"] = {"enable_thinking": False}
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json",
               "User-Agent": "romanian-s2s/1.0"}
    r = requests.post(base_url.rstrip("/") + "/chat/completions", json=payload,
                      headers=headers, timeout=(connect_timeout, read_timeout), stream=True)
    if r.status_code != 200:
        raise RuntimeError(f"HTTP {r.status_code}: {r.text[:200]}")
    # SSE decodat manual: requests decodează altfel per-chunk cu latin-1 → mojibake diacritice
    r.encoding = "utf-8"
    buf = ""
    with r:
        for chunk in r.iter_content(chunk_size=None, decode_unicode=True):
            buf += chunk
            while "\n" in buf:
                line, buf = buf.split("\n", 1)
                line = line.strip()
                if not line or not line.startswith("data:"):
                    continue
                data = line[5:].strip()
                if data == "[DONE]":
                    return
                obj = json.loads(data)
                delta = (obj.get("choices") or [{}])[0].get("delta", {})
                piece = delta.get("content")
                if piece:
                    yield piece


def chat_stream(messages, max_tokens=300,
                connect_timeout=10, read_timeout=60, max_fallback_retries=1):
    """Returnează (generator_text, state_dict).

    state: {provider, ttft_s, total_s, used_fallback, error, text}
    Comportament failover (obligatoriu):
    - primarul se încearcă la fiecare cerere;
    - la timeout / 5xx / 429 / conexiune întreruptă → fallback o singură dată;
    - niciodată cereri paralele (fără duplicate / cost dublu);
    - dacă fallback-ul și el pică, raise cu ambele erori.
    TTFT = timp până la primul token de CONȚINUT (reasoning-ul nu se numără).
    """
    state = {"provider": None, "ttft_s": None, "total_s": None,
             "used_fallback": False, "error": None, "text": None}

    def gen():
        parts = []
        providers = _providers()
        for attempt, (name, base, key, model) in enumerate(providers):
            if not key:
                state["error"] = (state["error"] or "") + f" | {name}: lipsă API key"
                continue
            t0 = time.time()
            first = None
            try:
                for piece in _stream_once(base, key, model, messages, max_tokens,
                                          connect_timeout, read_timeout,
                                          disable_thinking=(name == "gonkarouter")):
                    if first is None:
                        first = time.time() - t0
                        state["ttft_s"] = first
                    parts.append(piece)
                    yield piece
                state["provider"] = f"{name}:{model}"
                state["total_s"] = time.time() - t0
                state["used_fallback"] = attempt == 1
                state["text"] = "".join(parts)
                return
            except Exception as e:
                err = f"{name}({model}): {type(e).__name__}: {str(e)[:180]}"
                state["error"] = (state["error"] or "") + " | " + err
                print(f"[llm] {err}", file=sys.stderr)
                if attempt == len(providers) - 1:
                    raise
        raise RuntimeError("toți providerii au căzut" + str(state["error"] or ""))

    return gen(), state
