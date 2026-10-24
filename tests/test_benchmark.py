"""Benchmark: 5 ture end-to-end + simulare failover (primar invalid → xKiro).
Raportează mediană/p90 TTFT și total, și dovedește failover-ul."""
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from llm_adapter import chat_stream  # noqa: E402

PROMPTS = [
    "Spune-mi o anecdotă scurtă despre o pisică hacker.",
    "Ce vreme e potrivită pentru o plimbare în București în octombrie?",
    "Explică-mi într-o propoziție ce e un raycaster.",
    "Dă-mi o idee de biz care costă 0 lei să pornesc.",
    "Cum fac cafea bună cu un Moka pot? Scurt.",
]


def run_turn(i, prompt):
    t0 = time.time()
    gen, st = chat_stream(
        [{"role": "system", "content": "Ești asistent vocal în română. Răspunzi în max 2 propoziții."},
         {"role": "user", "content": prompt}],
        max_tokens=300,
    )
    pieces = list(gen)
    return {
        "i": i,
        "ttft_s": st["ttft_s"],
        "total_s": time.time() - t0,
        "provider": st["provider"],
        "fallback": st["used_fallback"],
        "chars": len(st["text"] or ""),
    }


def main():
    print("== Benchmark 5 ture, primar GonkaRouter ==")
    rows = []
    for i, p in enumerate(PROMPTS, 1):
        st = run_turn(i, f"{i}. {p}")
        ttft = st["ttft_s"]
        print(f"  tura {i}: ttft={ttft:.2f}s" if ttft is not None else
              f"  tura {i}: ttft=None (răspuns gol)", end="")
        print(f" total={st['total_s']:.2f}s provider={st['provider']} chars={st['chars']}")
        rows.append(st)
        time.sleep(0.3)
    tts_list = sorted(r["ttft_s"] for r in rows if r["ttft_s"] is not None)
    med = tts_list[len(tts_list) // 2]
    print(f"  mediană TTFT: {med:.2f}s | p90: {tts_list[-1]:.2f}s")

    print("\n== Simulare failover (primar cu base URL invalid) ==")
    os.environ["GONKAROUTER_BASE_URL"] = "https://primul-căzut.example/v1"
    t0 = time.time()
    gen, st = chat_stream([{"role": "user", "content": "Spune doar: fallback funcționează."}],
                          max_tokens=30)
    text = "".join(gen)
    print(f"  fallback OK: provider={st['provider']} ttft={st['ttft_s']:.2f}s "
          f"total={st['total_s']:.2f}s used_fallback={st['used_fallback']}")
    print(f"  răspuns fallback: {text[:80]}")


if __name__ == "__main__":
    main()
