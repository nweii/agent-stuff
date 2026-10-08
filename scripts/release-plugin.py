#!/usr/bin/env python3
# Checks per-plugin release versions across all manifests and both marketplace entries.
# Updates release metadata on request and creates a plain Git tag only from committed, matching artifacts.

import argparse
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("generate_plugins", ROOT / "scripts/generate-plugins.py")
generator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(generator)


def check_release(name, root=ROOT):
    sources = {data["name"]: data for data in generator.read_sources(root)}
    if name not in sources:
        raise ValueError(f"Unknown plugin: {name}")
    data = sources[name]
    version = data["version"]
    expected = generator.generated_documents(root)
    for relative in (Path(f"plugins/{name}/plugin.json"), Path(f"plugins/{name}/.claude-plugin/plugin.json"),
                     Path(f"plugins/{name}/.codex-plugin/plugin.json")):
        actual = json.loads((root / relative).read_text())
        if actual != expected[relative]:
            raise ValueError(f"Manifest disagrees with source version {version} or metadata: {relative}")
    for relative in (Path(".claude-plugin/marketplace.json"), Path(".agents/plugins/marketplace.json")):
        actual = json.loads((root / relative).read_text())
        entries = [entry for entry in actual["plugins"] if entry.get("name") == name]
        wanted = next(entry for entry in expected[relative]["plugins"] if entry["name"] == name)
        if len(entries) != 1:
            raise ValueError(f"Catalog must contain exactly one entry for {name}: {relative}")
        if entries[0].get("source") != wanted["source"]:
            raise ValueError(f"Catalog source disagrees with the vendor's local path or release tag: {relative}")
        if entries[0] != wanted:
            raise ValueError(f"Catalog entry disagrees with source version {version} or metadata: {relative}")
    return f"{name}/v{version}"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("plugin")
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--version", help="Prepare a release version and regenerate metadata; commit before tagging")
    action.add_argument("--tag", action="store_true", help="Check committed metadata and create a local lightweight Git tag")
    action.add_argument("--check", action="store_true", help="Check without changing metadata or Git refs (default)")
    args = parser.parse_args()
    try:
        # Resolve the declared plugin first; the argument cannot select a path outside plugins/.
        sources = {data["name"]: data for data in generator.read_sources(ROOT)}
        if args.plugin not in sources:
            raise ValueError(f"Unknown plugin: {args.plugin}")
        if args.version:
            if not re.fullmatch(generator.VERSION_PATTERN, args.version):
                raise ValueError("Release version must be MAJOR.MINOR.PATCH")
            source = ROOT / "plugins" / args.plugin / "plugin-source.json"
            data = sources[args.plugin]
            data["version"] = args.version
            source.write_text(json.dumps(data, indent=2) + "\n")
            generator.generate()
        tag = check_release(args.plugin)
        if args.tag:
            dirty = subprocess.check_output(["git", "status", "--porcelain", "--untracked-files=normal"], cwd=ROOT, text=True)
            if dirty:
                raise ValueError("Commit or set aside working-tree changes before tagging; a tag must identify the checked files")
            # No host-specific tag helper: one lightweight tag for one plugin release.
            subprocess.run(["git", "tag", tag], cwd=ROOT, check=True)
        print(f"{'Tagged' if args.tag else 'Checked'} {tag}; no push performed.")
    except (ValueError, KeyError, OSError, subprocess.CalledProcessError) as error:
        print(str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
