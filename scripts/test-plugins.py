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
        self.data["version"] = "0.1.0"  # fixed so tests don't track the real plugin's releases
        for key in generator.ASSET_FIELDS:
            if key in self.data["interface"]:
                asset = self.folder / self.data["interface"][key]
                asset.parent.mkdir(parents=True, exist_ok=True)
                asset.write_bytes(b"png")
        self.write_source()
        generator.generate(self.root)

    def write_source(self):
        (self.folder / "plugin-source.json").write_text(json.dumps(self.data))

    def test_pre_commit_packages_regenerated_readme(self):
        import zipfile
        scripts = self.root / "scripts"
        scripts.mkdir()
        for filename in ("generate-plugins.py", "release-plugin.py", "update-catalog.py",
                         "build-zips.py", "skill_sources.py"):
            (scripts / filename).write_bytes((ROOT / "scripts" / filename).read_bytes())
        if (ROOT / "scripts/check-mirrors.py").exists():
            (scripts / "check-mirrors.py").write_bytes((ROOT / "scripts/check-mirrors.py").read_bytes())
            (scripts / "public-exports.json").write_text("{}\n")
            (scripts / "public-variants.txt").write_text("")
        hooks = self.root / ".githooks"
        hooks.mkdir()
        (hooks / "pre-commit").write_bytes((ROOT / ".githooks/pre-commit").read_bytes())
        (self.root / ".gitignore").write_text("__pycache__/\n")
        (self.root / "README.md").write_text(
            "# Fixture\n\n<!-- CATALOG:START -->\n<!-- PLUGINS:START -->\n"
            "<!-- PLUGINS:END -->\n<!-- CATALOG:END -->\n")
        readme = self.folder / "README.md"
        readme.write_text("# Example\n\n<!-- PLUGIN:START -->\nOld metadata.\n<!-- PLUGIN:END -->\n")
        self.member.write_text('---\nname: sample\ndescription: "Updated description."\n---\nBody.\n')
        subprocess.run(["git", "init", "-b", "main"], cwd=self.root, check=True, capture_output=True)
        subprocess.run(["git", "add", "."], cwd=self.root, check=True)
        subprocess.run(["bash", str(hooks / "pre-commit")], cwd=self.root,
                       check=True, capture_output=True, text=True)
        staged = subprocess.check_output(["git", "show", ":plugins/example/README.md"], cwd=self.root)
        self.assertIn(b"Updated description.", staged)
        with zipfile.ZipFile(self.root / "zips/plugins/example-0.1.0.zip") as archive:
            self.assertEqual(archive.read("README.md"), staged)

    def test_catalog_membership_uses_staged_local_paths(self):
        catalog = module("catalog_membership", "update-catalog.py")
        self.data["interface"]["displayName"] = "Example.tools"
        self.write_source()
        outside = self.root / "skills/outside/SKILL.md"
        outside.parent.mkdir(parents=True)
        outside.write_text('---\nname: outside\ndescription: "Standalone description."\nmetadata:\n  internal: true\n---\n')
        subprocess.run(["git", "init", "-b", "main"], cwd=self.root, check=True, capture_output=True)
        subprocess.run(["git", "add", "."], cwd=self.root, check=True)
        self.data["interface"]["displayName"] = "Unstaged name"
        self.write_source()
        self.member.write_text(self.member.read_text().replace("Use when testing.", "Unstaged description."))
        untracked = self.folder / "skills/stray/SKILL.md"
        untracked.parent.mkdir()
        untracked.write_text('---\nname: stray\ndescription: "Untracked."\n---\n')
        catalog.REPO_ROOT = self.root
        rendered = catalog.generate_catalog()
        self.assertIn('<a id="plugin-example"></a>[Example.tools](plugins/example/)', rendered)
        self.assertIn('- [sample](plugins/example/skills/sample/) — Use when testing. '
                      '*Included in [Example.tools](#plugin-example).*', rendered)
        outside_line = next(line for line in rendered.splitlines() if line.startswith('- [outside]'))
        self.assertNotIn('Included in', outside_line)
        self.assertEqual(rendered.count('Included in'), 1)
        self.assertNotIn('Unstaged', rendered)
        self.assertNotIn('stray', rendered)
        subprocess.run(["git", "add", "plugins/example/plugin-source.json"], cwd=self.root, check=True)
        renamed = catalog.generate_catalog()
        self.assertIn('*Included in [Unstaged name](#plugin-example).*', renamed)
        self.assertIn('<a id="plugin-example"></a>', renamed)

    def test_missing_interface_asset_is_refused(self):
        self.data["interface"]["logo"] = "./assets/missing.png"
        self.write_source()
        with self.assertRaisesRegex(ValueError, "Missing logo asset"):
            generator.generate(self.root)

    def archive_fixture(self):
        archives = module("archive_checks", "build-zips.py")
        archives.REPO_ROOT = self.root
        archives.ZIPS_DIR = self.root / "zips"
        archives.PLUGIN_ZIPS_DIR = self.root / "zips/plugins"
        subprocess.run(["git", "init", "-b", "main"], cwd=self.root, check=True, capture_output=True)
        subprocess.run(["git", "add", "."], cwd=self.root, check=True)
        archives.rebuild()
        return archives

    def test_archive_check_rejects_missing_hidden_files_stale_bytes_and_duplicates(self):
        import warnings, zipfile
        archives = self.archive_fixture()
        self.assertGreater(archives.check_archives(), 0)
        path = archives.PLUGIN_ZIPS_DIR / "example-0.1.0.zip"
        for defect in ("hidden manifest", "contents", "wrapper", "duplicate", "extra"):
            with self.subTest(defect=defect):
                archives.rebuild()
                with zipfile.ZipFile(path) as archive:
                    members = {name: archive.read(name) for name in archive.namelist()}
                if defect == "hidden manifest":
                    members.pop(".claude-plugin/plugin.json")
                elif defect == "contents":
                    members["skills/sample/SKILL.md"] = b"Stale body."
                elif defect == "wrapper":
                    members = {"example/" + name: content for name, content in members.items()}
                elif defect == "extra":
                    members["../unexpected.txt"] = b"Outside package."
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", UserWarning)
                    with zipfile.ZipFile(path, "w") as archive:
                        for name, content in members.items():
                            archive.writestr(name, content)
                        if defect == "duplicate":
                            archive.writestr("plugin.json", members["plugin.json"])
                with self.assertRaisesRegex(ValueError, "Archive (membership|content) differs"):
                    archives.check_archives()

    def test_archive_check_rejects_declared_but_unstaged_asset(self):
        archives = self.archive_fixture()
        self.data["interface"]["logo"] = "./assets/new-icon.png"
        (self.folder / "assets").mkdir(exist_ok=True)
        (self.folder / "assets/new-icon.png").write_bytes(b"png")
        self.write_source()
        generator.generate(self.root)
        subprocess.run(["git", "add", "plugins/example/plugin-source.json", "plugins/example/plugin.json",
                        "plugins/example/.claude-plugin/plugin.json"], cwd=self.root, check=True)
        archives.rebuild()
        with self.assertRaisesRegex(ValueError, "Declared file is absent"):
            archives.check_archives()
        subprocess.run(["git", "add", "plugins/example/assets/new-icon.png"], cwd=self.root, check=True)
        archives.rebuild()
        self.assertGreater(archives.check_archives(), 0)

    def test_archive_check_uses_index_even_when_working_file_is_missing(self):
        archives = self.archive_fixture()
        staged = self.member.read_bytes()
        self.member.rename(self.member.with_suffix(".saved"))
        archives.rebuild()
        self.assertGreater(archives.check_archives(), 0)
        import zipfile
        with zipfile.ZipFile(archives.PLUGIN_ZIPS_DIR / "example-0.1.0.zip") as archive:
            self.assertEqual(archive.read("skills/sample/SKILL.md"), staged)

    def test_archive_check_rejects_missing_stale_archives_and_staged_fallback(self):
        archives = self.archive_fixture()
        path = archives.PLUGIN_ZIPS_DIR / "example-0.1.0.zip"
        path.rename(path.with_suffix(".saved"))
        with self.assertRaisesRegex(ValueError, "Archive inventory differs"):
            archives.check_archives()
        path.with_suffix(".saved").rename(path)
        extra = archives.PLUGIN_ZIPS_DIR / "example-9.9.9.zip"
        extra.write_bytes(path.read_bytes())
        with self.assertRaisesRegex(ValueError, "Archive inventory differs"):
            archives.check_archives()
        extra.rename(extra.with_suffix(".saved"))
        fallback = self.folder / ".codex-plugin/plugin.json"
        fallback.parent.mkdir()
        fallback.write_text("{}")
        subprocess.run(["git", "add", str(fallback.relative_to(self.root))], cwd=self.root, check=True)
        archives.rebuild()
        with self.assertRaisesRegex(ValueError, "Codex settings must use root"):
            archives.check_archives()

    def test_generation_preserves_payload_and_is_deterministic(self):
        before = self.member.read_bytes()
        docs = {path: (self.root / path).read_bytes() for path in generator.generated_documents(self.root)}
        generator.generate(self.root)
        self.assertEqual(before, self.member.read_bytes())
        self.assertEqual(docs, {path: (self.root / path).read_bytes() for path in docs})
        self.assertFalse((self.root / "skills/sample").exists())

    def test_release_rejects_each_manifest_and_catalog_version_mismatch(self):
        self.assertEqual(release.check_release("example", self.root), "example/v0.1.0")
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
                                  "path": "plugins/example", "ref": "example/v0.1.0"})
        for path, wrong in ((claude, source), (claude, "./plugins/wrong"),
                            (codex, "./plugins/example"), (codex, {**source, "ref": "wrong"}),
                            (codex, {**source, "ref": "example--v0.1.0"})):
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
        for filename in ("generate-plugins.py", "release-plugin.py", "build-zips.py", "skill_sources.py"):
            (scripts / filename).write_bytes((ROOT / "scripts" / filename).read_bytes())
        (self.root / ".gitignore").write_text("__pycache__/\n")
        def git(*argv):
            return subprocess.check_output(["git", *argv], cwd=self.root, stderr=subprocess.STDOUT, text=True)
        git("init", "-b", "main")
        git("config", "user.name", "Fixture")
        git("config", "user.email", "fixture@example.invalid")
        git("add", ".")
        subprocess.run(["python3", str(scripts / "build-zips.py")], cwd=self.root, check=True, capture_output=True)
        git("add", "zips")
        git("commit", "-m", "Fixture")
        import zipfile
        path = self.root / "zips/plugins/example-0.1.0.zip"
        valid = path.read_bytes()
        with zipfile.ZipFile(path) as archive:
            members = {name: archive.read(name) for name in archive.namelist()}
        members["skills/sample/SKILL.md"] = b"Wrong committed archive body."
        with zipfile.ZipFile(path, "w") as archive:
            for name, content in members.items():
                archive.writestr(name, content)
        git("add", "zips")
        git("commit", "-m", "Invalid archive fixture")
        refused = subprocess.run(["python3", str(scripts / "release-plugin.py"), "example", "--tag"], cwd=self.root, capture_output=True, text=True)
        self.assertNotEqual(refused.returncode, 0)
        self.assertIn("Archive content differs", refused.stderr)
        path.write_bytes(valid)
        git("add", "zips")
        git("commit", "-m", "Restore matching archive")
        subprocess.run(["python3", str(scripts / "release-plugin.py"), "example", "--tag"], cwd=self.root, check=True)
        self.assertEqual(git("cat-file", "-t", "example/v0.1.0").strip(), "commit")
        self.member.write_text(self.member.read_text() + "Dirty.\n")
        refused = subprocess.run(["python3", str(scripts / "release-plugin.py"), "example", "--tag"], cwd=self.root, capture_output=True, text=True)
        self.assertNotEqual(refused.returncode, 0)
        self.assertIn("before tagging", refused.stderr)


if __name__ == "__main__":
    unittest.main()
