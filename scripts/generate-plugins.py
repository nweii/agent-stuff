#!/usr/bin/env python3
# Generates portable and host manifests and marketplace catalogs from per-plugin metadata.
# Membership comes from the skills folder; generation never copies or rewrites skill files.

import argparse
import json
from pathlib import Path
import re
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent
AGENT_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
NAME_PATTERN = r"(?!.*(?:--|\.\.))[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?"
VERSION_PATTERN = r"(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)"
COMMON_FIELDS = ("name", "version", "description", "author", "homepage", "repository", "license", "keywords")


def read_sources(root=REPO_ROOT):
    sources = []
    seen = {}
    skill_files = list((root / "skills").glob("*/SKILL.md")) + list((root / "plugins").glob("*/skills/*/SKILL.md"))
    for skill in sorted(skill_files):
        text = skill.read_text()
        match = re.match(r"---\n(.*?)\n---", text, re.DOTALL)
        name = re.search(r"^name:\s*([a-z0-9-]+)\s*$", match[1], re.MULTILINE) if match else None
        if not name or name[1] != skill.parent.name:
            raise ValueError(f"Skill name/folder mismatch: {skill.relative_to(root)}")
        if name[1] in seen:
            raise ValueError(f"Duplicate skill {name[1]}: {seen[name[1]]} and {skill.relative_to(root)}")
        seen[name[1]] = skill.relative_to(root)
    for folder in sorted((root / "plugins").glob("*")):
        if not folder.is_dir():
            continue
        source = folder / "plugin-source.json"
        data = json.loads(source.read_text())
        name = data.get("name", "")
        if len(name) > 64 or not re.fullmatch(NAME_PATTERN, name) or folder.name != name:
            raise ValueError(f"Invalid plugin name or folder: {source.relative_to(root)}")
        if not re.fullmatch(VERSION_PATTERN, data.get("version", "")):
            raise ValueError(f"Use a stable semantic version in {source.relative_to(root)}")
        if data.get("audience") not in ("public", "personal"):
            raise ValueError(f"Declare public or personal audience in {source.relative_to(root)}")
        if not data.get("description") or not data.get("author", {}).get("name"):
            raise ValueError(f"Description and author are required: {source.relative_to(root)}")
        members = sorted((folder / "skills").glob("*/SKILL.md"))
        if not members:
            raise ValueError(f"Plugin has no skill payload: {name}")
        for member in members:
            internal = bool(re.search(r"^\s+internal:\s*true\s*$", member.read_text().split("---", 2)[1], re.MULTILINE))
            if data["audience"] == "public" and internal:
                raise ValueError(f"Internal member breaks public audience: {member.relative_to(root)}")
            if data["audience"] == "personal" and not internal:
                raise ValueError(f"General member needs review for personal audience: {member.relative_to(root)}")
        if any(path.is_symlink() for path in folder.rglob("*")):
            raise ValueError(f"Plugin payload must be self-contained without symlinks: {name}")
        sources.append(data)
    return sources


def generated_documents(root=REPO_ROOT):
    documents = {}
    claude_entries, codex_entries = [], []
    for data in read_sources(root):
        name = data["name"]
        common = {key: data[key] for key in COMMON_FIELDS if key in data}
        folder = Path("plugins") / name
        documents[folder / "plugin.json"] = {"$schema": AGENT_SCHEMA, **common}
        documents[folder / ".claude-plugin/plugin.json"] = common
        documents[folder / ".codex-plugin/plugin.json"] = {**common, "skills": "./skills/", "interface": data["interface"]}
        codex_source = {"source": "git-subdir", "url": data["repository"],
                        "path": f"plugins/{name}", "ref": f"{name}/v{data['version']}"}
        claude_entries.append({"name": name, "version": data["version"],
                               "description": data["description"], "author": data["author"],
                               "source": f"./plugins/{name}"})
        codex_entries.append({"name": name, "version": data["version"], "source": codex_source,
                              "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
                              "category": data["interface"]["category"]})
    documents[Path(".claude-plugin/marketplace.json")] = {
        "name": "agent-stuff", "owner": {"name": "Nathan Cheng"},
        "metadata": {"description": "Reusable agent plugins for working with your own tools and conventions."},
        "plugins": claude_entries}
    documents[Path(".agents/plugins/marketplace.json")] = {
        "name": "agent-stuff", "interface": {"displayName": "Agent Stuff"}, "plugins": codex_entries}
    return documents


def generate(root=REPO_ROOT, check=False):
    stale = []
    for path, data in generated_documents(root).items():
        target = root / path
        content = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
        if check:
            if not target.is_file() or target.read_text() != content:
                stale.append(str(path))
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            if not target.is_file() or target.read_text() != content:
                target.write_text(content)
    if stale:
        raise ValueError("Generated metadata is stale: " + ", ".join(stale))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Refuse stale generated manifests or catalogs")
    args = parser.parse_args()
    try:
        generate(check=args.check)
    except (ValueError, KeyError, OSError) as error:
        print(str(error), file=sys.stderr)
        return 1
    print("Plugin manifests and catalogs are current." if args.check else "Generated plugin manifests and catalogs.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
