# romanian-s2s — Agent Speech-to-Speech în română (Mac mini M4)

Pipeline S2S românesc: **STT local → LLM cloud (streaming) → TTS local**, cu failover
de provider și metrici reale de latență. Documentația cerințelor: PDF-ul de la user
("Instrucțiuni actualizate pentru Hermes").

## Arhitectura implementată

| Etapă | Implementare | Status verificat |
|---|---|---|
| STT | Whisper MLX `mlx-community/whisper-small-mlx-q4`, limbă `ro` forțată | RTF 0.04x (8.6s audio în 0.35s), transcriere corectă cu diacritice |
| LLM primar | GLM-5.3-Flash prin GonkaRouter (`chat_template_kwargs.enable_thinking=false`) | live, streaming SSE OK |
| LLM fallback | xKiro `qwen/qwen3.7-flash:free` | failover dovedit în test (primar invalid → xKiro preia, TTFT 2.3s) |
| TTS | Supertonic 3 (`supertonic` pypi 1.3.1, ONNX), limbă `ro`, voci M1–M5/F1–F5 | RTF ~0.19–0.20x, diacritice corecte |

**Divergență față de PDF (verificată live):** xKiro **NU publică GLM-5.3-Flash** (catalog
97 modele, zero GLM — verificat live `/v1/models`). Fallback configurat: `qwen/qwen3.7-flash:free`
(planul Free al contului xKiro; modelele plătite dau 403 permission_denied).

## Setup

```bash
cd ~/AI/romanian-s2s
python3.12 -m venv .venv
.venv/bin/pip install -r requirements.txt
cp .env.example .env   # completează cheile local; .env e în .gitignore
set -a; source .env; set +a
```

Chei: `GONKAROUTER_API_KEY` (sau `GONKA_API_KEY`, numele folosit deja de Hermes),
`XKIRO_API_KEY`. Niciodată în cod, git sau loguri.

## Rulare

```bash
.venv/bin/python tests/test_e2e.py        # LLM streaming → TTS → data/e2e_reply.wav
.venv/bin/python tests/test_benchmark.py  # 5 ture + failover simulat
.venv/bin/python tests/test_stt_tts.py    # STT transcrie mostra TTS (loopback)
```

## Numere măsurate (M4 24GB, 24.10.2026)

- STT (whisper-small-mlx-q4): **RTF 0.04x** — 8.57s audio transcris în 0.34–0.39s
- TTS (Supertonic 3, ro): RTF ~0.2x — 8.57s audio în 1.68s; 19.9s audio în 3.8s
- LLM primar (gonka GLM-5.3-Flash, stream): **TTFT median 3.76s, p90 5.95s**
  (TTFT = până la primul token de conținut; GLM mai „gândește" 0–4s în ciuda enable_thinking=false)
- LLM fallback (xKiro qwen3.7-flash:free): TTFT ~2.3s, $0
- Latență estimată tur vocal complet: STT ~0.35s + TTFT ~3.8s + TTS prima frază ~0.5s ≈ **4.5–5s**

**Verdict: NU e real-time/full-duplex** — e turn-taking cu ~4–7s până la primul audio.
Bottleneck: reasoning-ul GLM-5.3-Flash. Următoarea optimizare: TTS pe fraze (sintetizezi
prima propoziție cât LLM continuă) și/sau model non-reasoning pentru tură vocală.

## Licențe & versiuni (verificate la instalare)

- `supertonic` 1.3.1 — MIT (pip metadata); model Supertonic 3, 31 limbi + `ro`, ONNX on-device
- `mlx-whisper` — MIT (ecosistem MLX); model `whisper-small-mlx-q4` (derivat Whisper MIT)
- `openai`, `requests`, `numpy` — licențe standard PyPI
- LLM: GonkaRouter GLM-5.3-Flash (cont propriu), xKiro qwen3.7-flash:free (plan Free)
- Limitare cunoscută: xKiro Free nu permite modele plătite (403); GonkaRouter e obligatoriu primar

## Rollback / dezinstalare

```bash
rm -rf ~/AI/romanian-s2s          # șterge tot proiectul (venv + modele cache în ~/.cache/huggingface)
```
Nu s-au modificat setări globale Hermes/OpenClaw. Cheile rămân doar în `~/.hermes/.env`.

## Înapoi la Hermes: ce NU e încă

- VAD + barge-in pe microfon live (fază 2 — cere permisiune microfon macOS)
- Streaming TTS frază-cu-frază (reduce latența percepută sub TTFT + prima frază)
- Nu declara „real-time" până la testele de barge-in — conform documentului de specificații
