#!/usr/bin/env python3
# ABOUTME: Builds per-skill .zip files into zips/ for drag-into-Claude.ai from standalone and plugin skills,
# ABOUTME: plus one upload archive per plugin in zips/plugins/ (latest version only).
# ABOUTME: Deterministic (fixed timestamps, sorted entries) so unchanged skills produce byte-identical zips and no git churn.

import json
import os
import re
import subprocess
import sys
import zipfile
from pathlib import Path
from typing import List
from skill_sources import read_index_file, tracked_skill_files

# Public repo: zip general-purpose skills only. The private copy sets this True (all its skills are personal).
ZIP_INCLUDE_INTERNAL = False

REPO_ROOT = Path(__file__).parent.parent
SKILLS_DIR = REPO_ROOT / "skills"
ZIPS_DIR = REPO_ROOT / "zips"
PLUGIN_ZIPS_DIR = ZIPS_DIR / "plugins"

# Fixed timestamp for every entry → reproducible archives. (Earliest value zip allows.)
FIXED_DATE_TIME = (1980, 1, 1, 0, 0, 0)

# Defensive name skips, in case an untracked stray slips past the git-tracked filter.
JUNK_NAMES = {".DS_Store", "Thumbs.db", "Desktop.ini"}


def is_internal(skill_md: Path) -> bool:
    content = read_index_file(REPO_ROOT, skill_md).decode()
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
    return [f for f in files if f.name not in JUNK_NAMES]


def build_zip(skill_dir: Path, prefix: str = None) -> bytes:
    """Build a folder's zip as bytes, deterministic. Entries nest under the folder name unless prefix is ""."""
    name = skill_dir.name if prefix is None else prefix
    import io

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for f in sorted(tracked_files(skill_dir), key=lambda p: p.relative_to(skill_dir).as_posix()):
            relative = f.relative_to(skill_dir).as_posix()
            arcname = f"{name}/{relative}" if name else relative
            info = zipfile.ZipInfo(arcname, date_time=FIXED_DATE_TIME)
            info.external_attr = 0o644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(info, read_index_file(REPO_ROOT, f))
    return buf.getvalue()


def skills_to_zip() -> List[Path]:
    dirs = []
    for skill_md in tracked_skill_files(REPO_ROOT):
        if skill_md.parent.name == "private":
            continue
        if not ZIP_INCLUDE_INTERNAL and is_internal(skill_md):
            continue
        dirs.append(skill_md.parent)
    return sorted(dirs, key=lambda p: p.name)


def plugins_to_zip() -> List[tuple]:
    """(plugin folder, archive name) for each plugin, versioned from its staged plugin-source.json."""
    found = []
    for source in sorted((REPO_ROOT / "plugins").glob("*/plugin-source.json")):
        try:
            data = json.loads(read_index_file(REPO_ROOT, source))
        except subprocess.CalledProcessError:
            continue  # not staged or tracked yet
        found.append((source.parent, f"{data['name']}-{data['version']}.zip"))
    return found


def rebuild() -> List[str]:
    """Regenerate tracked archives and trash stale ones. Returns the names written."""
    ZIPS_DIR.mkdir(exist_ok=True)
    written = []
    for skill_dir in skills_to_zip():
        (ZIPS_DIR / f"{skill_dir.name}.zip").write_bytes(build_zip(skill_dir))
        written.append(skill_dir.name)
    for old in ZIPS_DIR.glob("*.zip"):
        if old.stem not in written:
            subprocess.run(["trash", str(old)], check=True)
    # Plugin upload archives: the plugin folder's files at the archive root, one current version per plugin.
    plugin_archives = []
    for plugin_dir, archive_name in plugins_to_zip():
        PLUGIN_ZIPS_DIR.mkdir(exist_ok=True)
        (PLUGIN_ZIPS_DIR / archive_name).write_bytes(build_zip(plugin_dir, prefix=""))
        plugin_archives.append(archive_name)
    for old in PLUGIN_ZIPS_DIR.glob("*.zip") if PLUGIN_ZIPS_DIR.is_dir() else []:
        if old.name not in plugin_archives:
            subprocess.run(["trash", str(old)], check=True)
    return written + plugin_archives



def check_archives(plugin=None):
    """Check final archive membership and bytes against staged payloads, without rewriting files."""
    targets = {}
    if plugin is None:
        for folder in skills_to_zip():
            targets[ZIPS_DIR / f"{folder.name}.zip"] = (folder, folder.name)
    for folder, name in plugins_to_zip():
        if plugin is None or folder.name == plugin:
            targets[PLUGIN_ZIPS_DIR / name] = (folder, "")
    if plugin is not None and not targets:
        raise ValueError(f"No staged plugin payload for {plugin}")
    if plugin is None:
        actual = set(ZIPS_DIR.glob("*.zip")) | set(PLUGIN_ZIPS_DIR.glob("*.zip"))
        if actual != set(targets):
            missing = sorted(str(p.relative_to(REPO_ROOT)) for p in set(targets) - actual)
            stale = sorted(str(p.relative_to(REPO_ROOT)) for p in actual - set(targets))
            raise ValueError(f"Archive inventory differs: missing={missing}, stale={stale}")
    for path, (folder, prefix) in targets.items():
        expected = {}
        for file in tracked_files(folder):
            relative = file.relative_to(folder).as_posix()
            expected[f"{prefix}/{relative}" if prefix else relative] = read_index_file(REPO_ROOT, file)
        if not prefix:
            required = {"plugin.json", ".claude-plugin/plugin.json"}
            if not required <= expected.keys():
                raise ValueError(f"Missing staged plugin manifest: {folder.name}")
            if any(name.startswith(".codex-plugin/") for name in expected):
                raise ValueError(f"Codex settings must use root plugin.json: {folder.name}")
            manifest = json.loads(expected["plugin.json"])
            extension = manifest.get("extensions", {}).get("com.openai", {})
            interface = extension.get("interface", {})
            claude = json.loads(expected[".claude-plugin/plugin.json"])
            declared = [interface.get("logo"), interface.get("composerIcon"), extension.get("apps"),
                        claude.get("icon"), claude.get("mcpServers")]
            for relative in declared:
                if relative is None:
                    continue
                if not isinstance(relative, str) or not relative.startswith("./") or relative[2:] not in expected:
                    raise ValueError(f"Declared file is absent from staged plugin payload: {folder.name}:{relative}")
        try:
            with zipfile.ZipFile(path) as archive:
                names = archive.namelist()
                if len(names) != len(set(names)) or set(names) != set(expected):
                    raise ValueError(f"Archive membership differs from staged payload: {path.name}")
                for name, content in expected.items():
                    if archive.read(name) != content:
                        raise ValueError(f"Archive content differs from staged payload: {path.name}:{name}")
        except (OSError, zipfile.BadZipFile) as error:
            raise ValueError(f"Cannot read archive {path.name}: {error}") from error
    return len(targets)


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
    if "--check" in sys.argv:
        try:
            print(f"Checked {check_archives()} archive(s) against staged payloads.")
        except ValueError as error:
            print(str(error), file=sys.stderr)
            sys.exit(1)
    elif "--selfcheck" in sys.argv:
        selfcheck()
    else:
        names = rebuild()
        print(f"Built {len(names)} zip(s) into {ZIPS_DIR.relative_to(REPO_ROOT)}/")
