#!/usr/bin/env python3
# Validates portable manifests against the published schema and Codex metadata against project contracts.
# /// script
# dependencies = ["jsonschema==4.26.0"]
# ///

import argparse
import importlib.util
import json
from pathlib import Path
import sys

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent.parent


def main():
    parser = argparse.ArgumentParser(description="Validate generated plugin metadata and optionally staged archives")
    parser.add_argument("--archives", action="store_true", help="Also check final ZIP membership and bytes against staged sources")
    args = parser.parse_args()
    spec = importlib.util.spec_from_file_location("generate_plugins", ROOT / "scripts/generate-plugins.py")
    generator = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(generator)
    generator.generate(check=True)
    schemas = ROOT / "scripts/schemas"
    targets = [(path, "agent-plugin-1.0.0.schema.json") for path in ROOT.glob("plugins/*/plugin.json")]
    targets.append((ROOT / ".agents/plugins/marketplace.json", "codex-marketplace.contract.schema.json"))
    for path, schema_file in targets:
        schema = json.loads((schemas / schema_file).read_text())
        Draft202012Validator.check_schema(schema)
        Draft202012Validator(schema).validate(json.loads(path.read_text()))
        print(f"Passed {path.relative_to(ROOT)} against {schema_file}")
        if path.parent.parent.name == "plugins" and path.name == "plugin.json":
            extension = json.loads(path.read_text()).get("extensions", {}).get("com.openai")
            contract = json.loads((schemas / "codex-extension.contract.schema.json").read_text())
            Draft202012Validator(contract).validate(extension)
            if (path.parent / ".codex-plugin").exists():
                raise ValueError(f"Obsolete Codex fallback remains: {path.parent.name}")
    if args.archives:
        archive_spec = importlib.util.spec_from_file_location("build_zips", ROOT / "scripts/build-zips.py")
        archives = importlib.util.module_from_spec(archive_spec)
        archive_spec.loader.exec_module(archives)
        print(f"Checked {archives.check_archives()} archive(s) against staged payloads.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
