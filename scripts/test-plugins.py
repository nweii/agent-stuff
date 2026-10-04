#!/usr/bin/env python3
# Tests generated metadata, audience/name guards, and release refusal using isolated plugin fixtures.
# A temporary Git repository exercises lightweight tagging without changing this repository's refs.

import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent.parent


def module(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / filename)
    loaded = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loaded)
    return loaded


generator = module("generate_plugins", "generate-plugins.py")
release = module("release_plugin", "release-plugin.py")


class PluginTests(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp(prefix="plugin-metadata-", dir="/tmp"))
        self.folder = self.root / "plugins/example"
        self.member = self.folder / "skills/sample/SKILL.md"
        self.member.parent.mkdir(parents=True)
        self.member.write_text('---\nname: sample\ndescription: "Use when testing."\n---\nBody.\n')
        self.data = json.loads((ROOT / "plugins/obsidian-tools/plugin-source.json").read_text())
        self.data["name"] = "example"
        self.write_source()
        generator.generate(self.root)

    def write_source(self):
        (self.folder / "plugin-source.json").write_text(json.dumps(self.data))

    def test_generation_preserves_payload_and_is_deterministic(self):
        before = self.member.read_bytes()
        docs = {path: (self.root / path).read_bytes() for path in generator.generated_documents(self.root)}
        generator.generate(self.root)
        self.assertEqual(before, self.member.read_bytes())
        self.assertEqual(docs, {path: (self.root / path).read_bytes() for path in docs})
        self.assertFalse((self.root / "skills/sample").exists())

    def test_release_rejects_each_manifest_and_catalog_version_mismatch(self):
        self.assertEqual(release.check_release("example", self.root), "example--v0.1.0")
        for path in generator.generated_documents(self.root):
            with self.subTest(path=str(path)):
                target = self.root / path
                data = json.loads(target.read_text())
                if path.name == "marketplace.json":
                    data["plugins"][0]["version"] = "9.9.9"
                else:
                    data["version"] = "9.9.9"
                target.write_text(json.dumps(data))
                with self.assertRaises(ValueError):
                    release.check_release("example", self.root)
                generator.generate(self.root)

    def test_split_catalog_sources_and_refusal_of_wrong_sources(self):
        claude = self.root / ".claude-plugin/marketplace.json"
        codex = self.root / ".agents/plugins/marketplace.json"
        self.assertEqual(json.loads(claude.read_text())["plugins"][0]["source"], "./plugins/example")
        source = json.loads(codex.read_text())["plugins"][0]["source"]
        self.assertEqual(source, {"source": "git-subdir", "url": self.data["repository"],
                                  "path": "plugins/example", "ref": "example--v0.1.0"})
        for path, wrong in ((claude, source), (claude, "./plugins/wrong"),
                            (codex, "./plugins/example"), (codex, {**source, "ref": "wrong"})):
            with self.subTest(path=str(path), source=wrong):
                data = json.loads(path.read_text())
                data["plugins"][0]["source"] = wrong
                path.write_text(json.dumps(data))
                with self.assertRaisesRegex(ValueError, "Catalog source disagrees"):
                    release.check_release("example", self.root)
                generator.generate(self.root)

    def test_release_rejects_duplicate_entry(self):
        path = self.root / ".claude-plugin/marketplace.json"
        data = json.loads(path.read_text())
        data["plugins"].append(data["plugins"][0])
        path.write_text(json.dumps(data))
        with self.assertRaises(ValueError):
            release.check_release("example", self.root)

    def test_invalid_names_internal_members_and_duplicate_skills_fail(self):
        for name in ("Uppercase", "bad--name", "bad..name", "-bad", "bad."):
            self.data["name"] = name
            self.write_source()
            with self.assertRaises(ValueError):
                generator.generate(self.root)
        self.data["name"] = "example"
        self.write_source()
        self.member.write_text('---\nname: sample\nmetadata:\n  internal: true\n---\n')
        with self.assertRaises(ValueError):
            generator.generate(self.root)
        duplicate = self.root / "skills/sample/SKILL.md"
        duplicate.parent.mkdir(parents=True)
        duplicate.write_bytes(self.member.read_bytes())
        with self.assertRaises(ValueError):
            generator.generate(self.root)

    def test_release_script_tags_only_committed_matching_metadata(self):
        scripts = self.root / "scripts"
        scripts.mkdir()
        for filename in ("generate-plugins.py", "release-plugin.py"):
            (scripts / filename).write_bytes((ROOT / "scripts" / filename).read_bytes())
        (self.root / ".gitignore").write_text("__pycache__/\n")
        def git(*argv):
            return subprocess.check_output(["git", *argv], cwd=self.root, stderr=subprocess.STDOUT, text=True)
        git("init", "-b", "main")
        git("config", "user.name", "Fixture")
        git("config", "user.email", "fixture@example.invalid")
        git("add", ".")
        git("commit", "-m", "Fixture")
        subprocess.run(["python3", str(scripts / "release-plugin.py"), "example", "--tag"], cwd=self.root, check=True)
        self.assertEqual(git("cat-file", "-t", "example--v0.1.0").strip(), "commit")
        self.member.write_text(self.member.read_text() + "Dirty.\n")
        refused = subprocess.run(["python3", str(scripts / "release-plugin.py"), "example", "--tag"], cwd=self.root, capture_output=True, text=True)
        self.assertNotEqual(refused.returncode, 0)
        self.assertIn("before tagging", refused.stderr)


if __name__ == "__main__":
    unittest.main()
