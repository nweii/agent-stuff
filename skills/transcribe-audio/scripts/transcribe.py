#!/usr/bin/env python3
"""Normalize an audio or video file to 16kHz mono WAV and transcribe it with the
locally configured ASR model. Model and staging settings come from the
transcribe-audio config (~/.config/transcribe-audio/config.json)."""

import argparse
import json
import os
import shlex
import subprocess
import sys
from pathlib import Path

CONFIG_PATH = Path(
    os.environ.get(
        "TRANSCRIBE_AUDIO_CONFIG",
        Path.home() / ".config" / "transcribe-audio" / "config.json",
    )
)


def load_config():
    if not CONFIG_PATH.exists():
        sys.exit(
            f"No config at {CONFIG_PATH}.\n"
            "This machine hasn't been set up yet — work through the skill's "
            "references/setup.md (pick a staging area and a model) before transcribing."
        )
    try:
        cfg = json.loads(CONFIG_PATH.read_text())
    except json.JSONDecodeError as e:
        sys.exit(f"Config at {CONFIG_PATH} is not valid JSON: {e}")
    for key in ("staging_dir", "model"):
        if key not in cfg:
            sys.exit(f"Config is missing required key '{key}'. See references/setup.md.")
    if "command" not in cfg["model"]:
        sys.exit("Config 'model' is missing a 'command' template. See references/setup.md.")
    return cfg


def main():
    ap = argparse.ArgumentParser(
        description="Transcribe an audio or video file with the configured local model."
    )
    ap.add_argument("input", help="Path to an audio or video file")
    ap.add_argument("--outdir", help="Output directory (default: staging_dir from config)")
    ap.add_argument(
        "--format",
        help="Output format: txt, srt, vtt, json (default: config default_output_format or txt)",
    )
    args = ap.parse_args()

    cfg = load_config()
    src = Path(args.input).expanduser()
    if not src.exists():
        sys.exit(f"Input not found: {src}")

    outdir = Path(args.outdir).expanduser() if args.outdir else Path(cfg["staging_dir"]).expanduser()
    outdir.mkdir(parents=True, exist_ok=True)
    fmt = args.format or cfg.get("default_output_format", "txt")

    wav = outdir / (src.stem + ".wav")
    print(f"[1/2] Extracting 16kHz mono audio -> {wav}", flush=True)
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(src), "-ar", "16000", "-ac", "1", str(wav)],
        check=True,
    )

    model = cfg["model"]
    cmd = model["command"].format(
        input=shlex.quote(str(wav)),
        outdir=shlex.quote(str(outdir)),
        format=fmt,
    )
    print(f"[2/2] Transcribing with {model.get('label', 'configured model')}", flush=True)
    print(f"      $ {cmd}", flush=True)
    subprocess.run(cmd, shell=True, check=True)

    produced = [p for p in outdir.glob(src.stem + ".*") if p.suffix.lstrip(".") == fmt]
    if produced:
        print("\nTranscript:")
        for p in sorted(produced):
            print(f"  {p}")
    else:
        print(f"\nDone. Check {outdir} for the {fmt} output.")


if __name__ == "__main__":
    main()
