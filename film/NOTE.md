# NOTE — film explicativ romanian-s2s (draft)

## Ideea
Un singur lucru pe care doar acest proiect îl poate filma: **filmul e narat chiar de vocea
proiectului** (Supertonic 3, română, generat local pe M4). Explică pipeline-ul cu datele
reale de benchmark și se declară onest „în dezvoltare, nu real-time".

## Beats (VO Supertonic F1, ro)
1. **Hook** (0-3.4s): waveform accent + „Salut. Asta nu vorbește om." — vocea e sintetică.
2. **Turn** (3.4-9.6s): pipeline real STT→LLM→TTS, carriers: banda de waveform.
3. **Proof STT** (9.6-16.9s): screenshot real HF whisper-small-mlx-q4 + linia REALĂ din
   `tests/test_stt_tts.py` (`run 1: STT 0.35s (RTF 0.04x)`), typewriter pe terminalul propriu.
4. **Proof LLM** (17.0-23.2s): config REAL (env vars) + TTFT măsurat 0.93s + failover real xKiro.
5. **Proof TTS** (23.4-28.9s): screenshot Supertonic + counter real 8.57s→1.68s (RTF 0.20x).
6. **Onestitate** (29.5-36.1s): „Încă nu e real-time." + TTFT mediană reală 3.76s + „în dezvoltare".
7. **CTA** (36.45-42.85s): screenshotul real al repo-ului GitHub + URL; meta-reveal: „Narat
   chiar de vocea proiectului."

## Ce e real vs. ilustrativ
- Real: TOATE numerele (RTF 0.04x, TTFT 0.93s, 3.76s mediană, 1.68s TTS, HTTP 200 fallback),
  liniile de terminal, config-ul, screenshoturile (repo GitHub live, HF whisper, GitHub Supertonic),
  vocea (Supertonic 3 F1, română).
- Ilustrativ: diagrama pipeline-ului (B2) și waveform-ul — reprezentări ale arhitecturii reale.

## Note de producție
- VO generat local cu `supertonic` 1.3.1 (voce F1, lang=ro, speed 1.05) — 7 linii, mix adelay+amix.
- Fără ElevenLabs: fără muzică/SFX; filmul e vocea proiectului + tăceri (potrivit temei).
- G5 lint: PASS (D1 la WARN după recentrare; C5/T1 = warn-uri pe terminalul real / accent).
- G0/G2/G3: de rulat pe draft cu look.py (secțiunea de mai jos se completează cu cifre).

## Ce aș îmbunătăți
- Barge-in demo real (faza 2 a proiectului) ca proof beat suplimentar.
- Muzică de fundal + SFX subtil pe hit-uri (acum doar VO).
