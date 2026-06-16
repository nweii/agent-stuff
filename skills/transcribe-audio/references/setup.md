# Setup and model selection

Run this when there's no `~/.config/transcribe-audio/config.json` (first run on a machine), or when the user wants to choose, change, or upgrade a model. It has two parts: a staging area, set once, and a model, revisitable any time. The config written at the end is what makes ordinary runs a one-line command.

## Step 1 — Staging area (first time only)

Each job writes an intermediate WAV and a transcript; they need a directory. Pick one that is:

- **Disposable** — WAVs accumulate and are safe to delete. This is scratch space, not an archive.
- **Outside synced and notes locations** — large media in cloud-synced folders (iCloud Desktop & Documents, Dropbox) or note vaults bloats sync and indexing.

Suggest a default, let the user override. On macOS, default to `~/Movies/media-jobs`: `~/Movies` is the native home for video and sits outside iCloud Desktop & Documents sync, so throwaway media isn't uploaded. On Linux, `~/media-jobs` or `~/scratch/media`.

Create the directory and record its absolute path as `staging_dir`.

## Step 2 — Detect the system

Hardware decides which runtimes are viable. Check it:

```bash
uname -s -m        # OS + CPU architecture
```

- **Apple Silicon Mac (arm64 Darwin)** — use MLX builds; they run on the GPU without CUDA. Two options, both run via `uvx` with no install and both need `ffmpeg`:
  - `mlx-whisper` (Whisper on MLX) — broadly multilingual.
  - `parakeet-mlx` (Parakeet on MLX) — fast, English/European, few hallucinations over silence.
- **Linux/Windows with an NVIDIA GPU** — `faster-whisper` / `WhisperX` (CTranslate2), or NVIDIA NeMo for Parakeet/Canary natively.
- **CPU-only** — `whisper.cpp` or `faster-whisper` on a small/medium model, trading away some accuracy or speed.

Confirm `uvx` (or `uv`) and `ffmpeg` are installed; install them if missing (`brew install uv ffmpeg` on macOS).

## Step 3 — Elicit the user's needs

The best model depends on the use. Ask enough to weight the choice:

- **Language** — English only, or multilingual? Some of the most accurate models are English-only.
- **Accuracy vs speed** — one careful transcript, or throughput over many hours?
- **Timestamps** — segment- or word-level timing for captions (SRT/VTT), or plain prose?
- **Privacy** — must it stay fully local? (This skill assumes yes; confirm.)
- **Length** — short memos vs multi-hour recordings change how much speed matters.

## Step 4 — Check the current landscape

Consult the HuggingFace **Open ASR Leaderboard**, which ranks models by word error rate (WER) and speed (RTFx). Read it live; the order shifts as models ship.

The leaderboard Space renders its table in JavaScript, so fetching the page HTML returns nothing. Pull current numbers from the leaderboard's blog or dataset, the paper, or a recent reputable secondary summary.

Map the standings onto three families; the tradeoff among them holds even as names change:

- **Accuracy-first** (e.g. Canary-class) — lowest English WER, heavier, often NVIDIA-stack.
- **Speed-first** (e.g. Parakeet-class) — slightly higher WER, very high throughput, few hallucinations over non-speech.
- **Breadth-first** (Whisper-class) — wide multilingual coverage (~99 languages), mature tooling.

Then filter by what the user's hardware runs well. A top-ranked model that needs a datacenter GPU is wrong for a laptop.

## Step 5 — Recommend and confirm

Give the reasoning, then let the user decide. Apple-Silicon defaults that fit most cases:

- **English or mixed European, wants it fast and clean** → `parakeet-mlx` (default `parakeet-tdt-0.6b-v3`, multilingual across European languages). Small download, fast, few hallucinations over silence.
- **Broad multilingual, or maximum robustness on messy audio** → `mlx-whisper` with `whisper-large-v3` (or `-turbo` for near-equal quality at higher speed).

For general use the two are close; choose for the dominant case.

## Step 6 — Install and verify

Run one short transcription so the weights download and cache (to `~/.cache/huggingface`) and you confirm it works. Use any short clip, or extract ~30s with ffmpeg.

- parakeet-mlx:

  ```bash
  uvx parakeet-mlx /path/to/sample.wav --output-format txt --output-dir /tmp
  ```

- mlx-whisper:

  ```bash
  uvx --from mlx-whisper mlx_whisper /path/to/sample.wav --model mlx-community/whisper-large-v3-turbo -f txt -o /tmp
  ```

The first run downloads the model (parakeet ~0.6 GB; whisper-large-v3-turbo ~1.5 GB); later runs reuse the cache.

## Step 7 — Write the config

Write `~/.config/transcribe-audio/config.json`, creating the directory if needed. `model.command` is a template the transcribe script fills in: `{input}` is the normalized WAV, `{outdir}` the output directory, `{format}` the format. Keep `{input}` even for models that read video directly; the script always passes a WAV.

```json
{
  "version": 1,
  "staging_dir": "/Users/you/Movies/media-jobs",
  "default_output_format": "txt",
  "model": {
    "label": "parakeet-tdt-0.6b-v3 (parakeet-mlx)",
    "command": "uvx parakeet-mlx {input} --output-format {format} --output-dir {outdir}",
    "languages": "English + European (multilingual)",
    "chosen_on": "YYYY-MM-DD",
    "notes": "Apple Silicon MLX; fast, few hallucinations over silence."
  }
}
```

mlx-whisper `command` template:

```
uvx --from mlx-whisper mlx_whisper {input} --model mlx-community/whisper-large-v3-turbo -f {format} -o {outdir}
```

To pin a specific parakeet model, add `--model mlx-community/parakeet-tdt-0.6b-v3` to its command. Set `chosen_on` to today's date; the swap flow reads it to judge staleness.

### Templates for other platforms

The `model.command` contract is the same everywhere: fill `{input}`, `{outdir}`, `{format}`. On non-Apple-Silicon hardware, `faster-whisper` (through the `whisper-ctranslate2` CLI) drops in cleanly and auto-downloads its models:

- NVIDIA GPU:
  ```
  uvx whisper-ctranslate2 {input} --model large-v3 --device cuda --compute_type float16 --output_format {format} --output_dir {outdir}
  ```
- CPU (any platform):
  ```
  uvx whisper-ctranslate2 {input} --model large-v3 --device cpu --compute_type int8 --output_format {format} --output_dir {outdir}
  ```

`whisper.cpp` is the lightest native-CPU option (no Python), but it doesn't reduce to a one-line template: it needs a GGUF model file passed with `-m`, selects formats with output flags (`-otxt`, `-osrt`) rather than a format value, and takes an output-prefix flag. Reach for it through a small wrapper script when the zero-Python footprint matters; otherwise the CPU template above is simpler.

## Swapping models later

When the user wants a different model:

1. Re-run Steps 3–6; skip the staging area, which stays. Re-check the leaderboard, since the landscape may have moved since `chosen_on`.
2. Install and verify the new model.
3. Overwrite the `model` block and update `chosen_on`. Keep a line in `notes` about the previous pick if it's worth remembering.

Ordinary transcription is unaffected; it runs the same command and picks up the new model.

## Config reference

- **Location** — `~/.config/transcribe-audio/config.json` (override with `TRANSCRIBE_AUDIO_CONFIG`).
- `staging_dir` — default directory for WAVs and transcripts.
- `default_output_format` — `txt`, `srt`, `vtt`, or `json`.
- `model.command` — shell template with `{input}`, `{outdir}`, `{format}`.
- `model.label`, `model.languages`, `model.notes`, `model.chosen_on` — metadata; `chosen_on` drives swap-staleness checks.
