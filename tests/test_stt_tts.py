"""Loopback STT: Whisper MLX transcrie mostra generată de Supertonic (data/test_ro.wav).
Verifică recunoașterea românei + latența (3 rulări warm)."""
import os
import sys
import time

import mlx_whisper  # noqa: E402

MODEL = "mlx-community/whisper-small-mlx-q4"
SAMPLE = os.path.join(os.path.dirname(__file__), "..", "data", "test_ro.wav")

if not os.path.exists(SAMPLE):
    print("Lipsește data/test_ro.wav — rulează întâi test_e2e.py (generează TTS ro).")
    sys.exit(1)

mlx_whisper.transcribe(SAMPLE, path_or_hf_repo=MODEL, language="ro")  # warm
for i in range(3):
    t0 = time.time()
    r = mlx_whisper.transcribe(SAMPLE, path_or_hf_repo=MODEL, language="ro")
    el = time.time() - t0
    print(f"run {i+1}: STT {el:.2f}s (RTF {el/8.57:.2f}x) → {r['text'].strip()[:100]}")
    time.sleep(0.3)
