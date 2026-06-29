#!/usr/bin/env python3
# ABOUTME: Builds per-skill .zip files into zips/ for drag-into-Claude.ai, mirroring the skills/ folder.
# ABOUTME: Deterministic (fixed timestamps, sorted entries) so unchanged skills produce byte-identical zips and no git churn.

import os
import re
import subprocess
import sys
import zipfile
from pathlib import Path
from typing import List

# Public repo: zip general-purpose skills only. The private copy sets this True (all its skills are personal).
ZIP_INCLUDE_INTERNAL = False

REPO_ROOT = Path(__file__).parent.parent
SKILLS_DIR = REPO_ROOT / "skills"
ZIPS_DIR = REPO_ROOT / "zips"

# Fixed timestamp for every entry → reproducible archives. (Earliest value zip allows.)
FIXED_DATE_TIME = (1980, 1, 1, 0, 0, 0)

# Defensive name skips, in case an untracked stray slips past the git-tracked filter.
JUNK_NAMES = {".DS_Store", "Thumbs.db", "Desktop.ini"}


def is_internal(skill_md: Path) -> bool:
    content = skill_md.read_text()
    fm = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not fm:
        return False
    match = re.search(r'^\s*internal:\s*["\']?(.*?)["\']?\s*$', fm.group(1), re.MULTILINE)
    return bool(match) and match.group(1).strip().lower() == "true"


def tracked_files(skill_dir: Path) -> List[Path]:
    """Git-tracked + staged files under a skill dir. Excludes anything gitignored (.DS_Store, __pycache__, etc.)."""
    rel = skill_dir.relative_to(REPO_ROOT).as_posix()
    out = subprocess.run(
        ["git", "ls-files", "-z", "--", rel],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    files = [REPO_ROOT / p for p in out.split("\0") if p]
    return [f for f in files if f.name not in JUNK_NAMES and f.is_file()]


def build_zip(skill_dir: Path) -> bytes:
    """Build one skill's zip as bytes: entries nested under the skill-name folder, deterministic."""
    name = skill_dir.name
    import io

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for f in sorted(tracked_files(skill_dir), key=lambda p: p.relative_to(skill_dir).as_posix()):
            arcname = f"{name}/{f.relative_to(skill_dir).as_posix()}"
            info = zipfile.ZipInfo(arcname, date_time=FIXED_DATE_TIME)
            info.external_attr = 0o644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(info, f.read_bytes())
    return buf.getvalue()


def skills_to_zip() -> List[Path]:
    dirs = []
    for skill_md in SKILLS_DIR.glob("*/SKILL.md"):
        if skill_md.parent.name == "private":
            continue
        if not ZIP_INCLUDE_INTERNAL and is_internal(skill_md):
            continue
        dirs.append(skill_md.parent)
    return sorted(dirs, key=lambda p: p.name)


def rebuild() -> List[str]:
    """Wipe zips/ and regenerate. Returns the list of skill names written."""
    ZIPS_DIR.mkdir(exist_ok=True)
    for old in ZIPS_DIR.glob("*.zip"):
        old.unlink()

    written = []
    for skill_dir in skills_to_zip():
        (ZIPS_DIR / f"{skill_dir.name}.zip").write_bytes(build_zip(skill_dir))
        written.append(skill_dir.name)
    return written


def selfcheck() -> None:
    """Determinism guarantee: building the same skill twice yields byte-identical output."""
    targets = skills_to_zip()
    if not targets:
        print("selfcheck: no skills to zip (nothing to verify)")
        return
    sample = targets[0]
    a, b = build_zip(sample), build_zip(sample)
    assert a == b, f"non-deterministic zip for {sample.name}"
    assert a[:2] == b"PK", "output is not a valid zip"
    print(f"selfcheck OK — deterministic zip for '{sample.name}' ({len(a)} bytes)")


if __name__ == "__main__":
    if "--selfcheck" in sys.argv:
        selfcheck()
    else:
        names = rebuild()
        print(f"Built {len(names)} zip(s) into {ZIPS_DIR.relative_to(REPO_ROOT)}/")
