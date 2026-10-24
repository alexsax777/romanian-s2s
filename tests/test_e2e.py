"""Test end-to-end: LLM streaming (cu metrici) -> TTS local -> wav.
Măsoară: TTFT LLM, timp total LLM, timp TTS, durata audio."""
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from llm_adapter import chat_stream  # noqa: E402
from supertonic import TTS  # noqa: E402


def main():
    t0 = time.time()

    gen, st = chat_stream(
        [{"role": "system",
          "content": "Ești un asistent vocal în română. Răspunzi scurt, conversațional, fără emoji."},
         {"role": "user", "content": "Ce pot face cu un Mac mini M4 ca server de acasă? 2-3 propoziții."}],
        max_tokens=250,
    )
    pieces = []
    first = None
    for piece in gen:
        if first is None:
            first = time.time() - t0
        pieces.append(piece)
    el_llm = time.time() - t0

    text = st["text"]
    print(f"LLM: provider={st['provider']} ttft={st['ttft_s']:.2f}s total={st['total_s']:.2f}s "
          f"({len(text)} chars)")
    print(f"răspuns: {text[:180]}")

    # TTS pe răspuns
    tts = TTS()
    style = tts.get_voice_style("F1")
    t1 = time.time()
    audio, _ = tts.synthesize(text, voice_style=style, lang="ro")
    el_tts = time.time() - t1
    dur_audio = audio.shape[-1] / 44100
    tts.save_audio(audio, "data/e2e_reply.wav")
    print(f"TTS: {el_tts:.2f}s pt {dur_audio:.1f}s audio (RTF {el_tts/dur_audio:.2f}x)")

    total = time.time() - t0
    print(f"E2E (text part): LLM {el_llm:.2f}s + TTS {el_tts:.2f}s = {total:.2f}s "
          f"→ primul audio ar porni după ~{st['ttft_s'] + el_tts:.2f}s de la sfârșitul vorbirii userului (+STT)")


if __name__ == "__main__":
    main()
