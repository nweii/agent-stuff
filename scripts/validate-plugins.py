#!/usr/bin/env python3
# Validates portable manifests against the published schema and Codex metadata against project contracts.
# /// script
# dependencies = ["jsonschema==4.26.0"]
# ///

import importlib.util
import json
from pathlib import Path
import sys

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent.parent


def main():
    spec = importlib.util.spec_from_file_location("generate_plugins", ROOT / "scripts/generate-plugins.py")
    generator = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(generator)
    generator.generate(check=True)
    schemas = ROOT / "scripts/schemas"
    targets = [(path, "agent-plugin-1.0.0.schema.json") for path in ROOT.glob("plugins/*/plugin.json")]
    targets.extend((path, "codex-plugin.contract.schema.json") for path in ROOT.glob("plugins/*/.codex-plugin/plugin.json"))
    targets.append((ROOT / ".agents/plugins/marketplace.json", "codex-marketplace.contract.schema.json"))
    for path, schema_file in targets:
        schema = json.loads((schemas / schema_file).read_text())
        Draft202012Validator.check_schema(schema)
        Draft202012Validator(schema).validate(json.loads(path.read_text()))
        print(f"Passed {path.relative_to(ROOT)} against {schema_file}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
