#!/usr/bin/env python3
# Checks cross-platform skill metadata without rejecting supported vendor-specific fields.
# /// script
# dependencies = ["pyyaml==6.0.3"]
# ///

import argparse
import json
import re
import sys
from pathlib import Path

import yaml


def inspect(content, folder, private=False):
    """Return metadata defects and advisory review items for one skill."""
    errors, review = [], []
    match = re.match(r"\A---\n(.*?)\n---(?:\n|$)", content, re.DOTALL)
    if not match:
        return {}, ["Missing YAML frontmatter"], review
    try:
        data = yaml.safe_load(match[1])
    except yaml.YAMLError:
        return {}, ["Invalid YAML frontmatter"], review
    if not isinstance(data, dict):
        return {}, ["Frontmatter must be a mapping"], review
    name, description = data.get("name"), data.get("description")
    if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) > 64:
        errors.append("Name must be lowercase hyphenated text, at most 64 characters")
    elif name != folder:
        errors.append("Folder differs from frontmatter name")
    if not isinstance(description, str) or not description.strip():
        errors.append("Description must be nonempty text")
    else:
        if len(description) > 1024:
            errors.append("Description exceeds 1024 characters")
        elif len(description) > 300:
            review.append("Description exceeds the 300-character routing guideline")
        if not re.search(r'^description: "', match[1], re.MULTILINE):
            errors.append("Description must be double-quoted")
    if "argument-hint" in data and not isinstance(data["argument-hint"], str):
        errors.append("argument-hint must be text, not a YAML list or mapping")
    metadata = data.get("metadata", {})
    if not isinstance(metadata, dict):
        errors.append("metadata must be a mapping")
        metadata = {}
    version = metadata.get("version")
    if not isinstance(version, str) or not re.fullmatch(r"\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?", version):
        errors.append("metadata.version must be a quoted semantic version")
    if private and metadata.get("internal") is not True:
        errors.append("Private skills require metadata.internal: true")
    if not metadata.get("author"):
        review.append("Authorship is unrecorded; check provenance before editing")
    return data, errors, review


def self_test():
    valid = '---\nname: sample\ndescription: "Use when testing."\ncontext: fork\nmodel: sonnet\ndisable-model-invocation: true\nmetadata:\n  author: owner\n  version: "1.0.0"\n  internal: true\n---\nBody\n'
    assert inspect(valid, "sample", private=True)[1] == []
    assert inspect(valid.replace('description: "Use when testing."', 'description: [test]'), "sample")[1]
    assert inspect(valid.replace("context: fork", "argument-hint: [title]"), "sample")[1]
    assert inspect(valid, "different")[1]
    assert inspect(valid.replace("  internal: true\n", ""), "sample", private=True)[1]
    assert inspect("---\n[broken\n---\n", "sample")[1]
    assert inspect(valid.replace("  version: \"1.0.0\"", "  version: 1.0"), "sample")[1]
    print("Skill metadata self-test passed.")


def main():
    parser = argparse.ArgumentParser(description=__doc__ or "Check skill metadata; emit JSON without skill body contents.")
    parser.add_argument("paths", nargs="*", type=Path, help="Skill directories or a directory containing skills")
    parser.add_argument("--private", action="store_true", help="Require the private-skill marker")
    parser.add_argument("--owner", help="Validate only skills explicitly attributed to this owner; report others as skipped")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return 0
    if not args.paths:
        parser.error("Provide at least one skill directory")
    files = set()
    for path in args.paths:
        if not path.is_dir():
            parser.error(f"Not a directory: {path}")
        found = [path / "SKILL.md"] if (path / "SKILL.md").is_file() else list(path.glob("*/SKILL.md"))
        if not found:
            parser.error(f"No skills found: {path}")
        files.update(found)
    results, skipped, names = [], [], {}
    for path in sorted(files):
        data, errors, review = inspect(path.read_text(), path.parent.name, args.private)
        metadata = data.get("metadata", {})
        owner = metadata.get("author") if isinstance(metadata, dict) else None
        if args.owner and data and owner != args.owner:
            skipped.append(str(path))
            continue
        name = data.get("name")
        if isinstance(name, str):
            if name in names:
                errors.append(f"Duplicate skill name also present at {names[name]}")
            names[name] = str(path)
        results.append({"path": str(path), "errors": errors, "review": review})
    print(json.dumps({"checked": len(results), "results": results, "skipped": skipped}, indent=2))
    return int(any(item["errors"] for item in results))


if __name__ == "__main__":
    sys.exit(main())
