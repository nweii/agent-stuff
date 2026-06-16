---
name: transcribe-audio
description: "Transcribe audio or video to text with a locally-run speech-to-text model. Use when the user wants a transcript or captions from a recording, wants to run speech-to-text locally instead of a cloud service, or wants to set up or switch their local transcription model."
compatibility: "Needs a shell, Python 3, and ffmpeg. Default models target Apple Silicon (MLX via uvx); other platforms work but supply their own model command in the config."
metadata:
  author: nweii
  version: "1.0.0"
---

# Transcribe audio

Produce a transcript from an audio or video file using the model configured on this machine.

## Check for a config first

Settings live in `~/.config/transcribe-audio/config.json`.

- **Missing** — the machine isn't set up. Read `references/setup.md` and run setup (staging area, then model choice) before transcribing. Don't pick a model unprompted: the right one depends on the user's hardware, languages, and whether they want speed or accuracy, and a wrong guess wastes a large download.
- **Present** — go straight to transcribing.

When the user asks to change or upgrade their model, route to `references/setup.md` as well.

## Transcribe

Run the bundled script on the file:

```bash
python3 <skill-dir>/scripts/transcribe.py /path/to/recording.mp4
```

The script extracts a 16kHz mono WAV (so audio and video files are handled the same way), runs the configured model, and writes the transcript to the staging area.

- `--outdir DIR` — write the WAV and transcript somewhere other than the staging area.
- `--format srt` — timestamped captions instead of prose; `txt` (default), `vtt`, and `json` also work.

Run it in the foreground and let its output stream. Throughput is high, but a multi-hour file still takes real time, and a silent run reads as stalled.

## Offer to fix errors when accuracy matters

Auto-transcripts fail in predictable spots: proper nouns — names, products, jargon — get misheard, and audio over music or crosstalk garbles. Whether to fix this depends on use. A transcript the user skims once needs nothing; one they'll quote, publish, or keep as a record is worth a pass.

Flag, don't silently correct: you're inferring what was said, and a confident wrong fix buries the error where the user won't catch it. Read the whole transcript first, and ground proper nouns in whatever context exists — project notes, a glossary, the surrounding conversation — rather than substituting a similar-sounding name from your own knowledge. Then triage what you find:

- **A term misheard the same way throughout** (a name rendered as a consistent non-word) — propose one find-and-replace.
- **A garbled clause that context can recover** — propose your reading as a question ("I think this is X — does that match?"), don't just rewrite it.
- **A stretch where several words are nonsense and context doesn't pin it down** — flag it as garbled and leave the original; don't fabricate a clean version.

Surface the flags as a list and let the user confirm; each correction is context for the rest of the pass. A dedicated audit can go further — building a domain glossary, wrapping unrecoverable spans in callouts that preserve the original — but this much is useful on its own.

## Offer to structure a long transcript

Raw output is one unbroken block of text. For anything long, offer to make it navigable: break it into paragraphs at natural shifts in topic, and add brief subheadings that summarize each section. This doesn't change the words, so it's worth doing even on a transcript you don't correct — keep it separate from the error pass.

## Switching models

Follow the "Swapping models later" section of `references/setup.md`. It re-checks the landscape, installs the replacement, and updates the config; the staging area is untouched.
