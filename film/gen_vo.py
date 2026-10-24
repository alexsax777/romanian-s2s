"""Generează liniile VO în română cu Supertonic 3 (vocea proiectului) + măsoară duratele."""
import asyncio
import os
import subprocess

from supertonic import TTS

BASE = os.path.expanduser("~/AI/romanian-s2s/film")
OUT = os.path.join(BASE, "audio", "vo")
os.makedirs(OUT, exist_ok=True)

with open(os.path.join(BASE, "vo.txt"), encoding="utf-8") as f:
    LINES = [l.strip() for l in f if l.strip()]


async def main():
    tts = TTS()
    style = tts.get_voice_style("F1")
    for i, line in enumerate(LINES, 1):
        path = os.path.join(OUT, f"line{i:02d}.wav")
        if not (os.path.exists(path) and os.path.getsize(path) > 10000):
            audio, _ = tts.synthesize(line, voice_style=style, lang="ro", speed=1.05)
            tts.save_audio(audio, path)
        d = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "csv=p=0", path],
            capture_output=True, text=True,
        ).stdout.strip()
        print(f"line{i:02d}: {float(d):.2f}s | {line[:64]}")


if __name__ == "__main__":
    asyncio.run(main())
