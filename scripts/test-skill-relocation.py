#!/usr/bin/env python3
# Exercises skills CLI relocation through a local Git URL with isolated homes and projects.
# Retains fixture files and command logs for inspection; never touches the caller's installations.

import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cli", type=Path, required=True, help="Pinned skills bin/cli.mjs")
    parser.add_argument("--runtime", default="node")
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    cli = args.cli.resolve(strict=True)
    root = Path(tempfile.mkdtemp(prefix="skill-relocation-", dir="/tmp")).resolve()
    logs, results = [], {}

    def environment(label, internal=False):
        home = root / label / "home"
        home.mkdir(parents=True, exist_ok=True)
        env = {key: value for key, value in os.environ.items()
               if key in ("PATH", "LANG", "LC_ALL", "SYSTEMROOT")}
        # os.homedir(), XDG lock paths, agent detection, and temp clones must all be isolated.
        env.update(HOME=str(home), XDG_CONFIG_HOME=str(home / ".config"),
                   XDG_STATE_HOME=str(home / ".state"), XDG_CACHE_HOME=str(home / ".cache"),
                   CODEX_HOME=str(home / ".codex"), TMPDIR=str(root), CI="1",
                   DISABLE_TELEMETRY="1", DO_NOT_TRACK="1", NO_COLOR="1",
                   GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=str(root / "gitconfig"))
        if internal:
            env["INSTALL_INTERNAL_SKILLS"] = "1"
        return env

    def run(command, cwd, env=None, label="git"):
        proc = subprocess.run(command, cwd=cwd, env=env or environment("git"),
                              capture_output=True, text=True, timeout=120)
        output = re.sub(r"\x1b\[[0-9;]*[A-Za-z]", "", proc.stdout + proc.stderr)
        logs.append({"label": label, "command": command, "cwd": str(cwd),
                     "exit_code": proc.returncode, "output": output})
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps({"fixture": str(root), "commands": logs}, indent=2) + "\n")
        return proc.returncode, output

    repo = root / "source"
    repo.mkdir()
    def git(*argv):
        code, output = run(["git", *argv], repo)
        assert code == 0, output

    git("init", "-b", "main")
    git("config", "user.name", "Fixture")
    git("config", "user.email", "fixture@example.invalid")
    for name, internal in [("public-moved", False), ("internal-moved", True), ("internal-stays", True)]:
        folder = repo / "skills" / name
        folder.mkdir(parents=True)
        (folder / "SKILL.md").write_text(
            f'---\nname: {name}\ndescription: "Use when testing relocation."\nmetadata:\n'
            f'  version: "0.1.0"\n' + ('  internal: true\n' if internal else '') + '---\nFixture v1.\n')
    git("add", ".")
    git("commit", "-m", "Seed skills")
    bare = root / "source.git"
    code, output = run(["git", "clone", "--bare", str(repo), str(bare)], root)
    assert code == 0, output
    # file:// installs do not create global lock entries in skills 1.7.0.
    # An HTTPS Git source with a fixture-only Git rewrite exercises the same clone path.
    source = "https://fixture.invalid/owner/source.git"
    (root / "gitconfig").write_text(
        f'[url "{bare.as_uri()}"]\n\tinsteadOf = {source}\n')

    def skills(label, *argv, internal=False):
        project = root / label / "project"
        project.mkdir(parents=True, exist_ok=True)
        return run([args.runtime, str(cli), *argv], project, environment(label, internal), label)

    version = skills("version", "--version")[1].strip()
    names = ["public-moved", "internal-moved", "internal-stays"]
    for label, scope in [("global", ["-g"]), ("project", [])]:
        code, output = skills(label, "add", source, "--skill", *names,
                              "-a", "claude-code", "zed", *scope, "-y", internal=True)
        assert code == 0, output

    def lock(label):
        path = (root / label / "home" / ".state" / "skills" / ".skill-lock.json"
                if label == "global" else root / label / "project" / "skills-lock.json")
        if not path.exists() and label == "global":
            path = root / label / "home" / ".agents" / ".skill-lock.json"
        return json.loads(path.read_text())

    before = {label: lock(label) for label in ("global", "project")}
    for label in before:
        assert before[label]["skills"]["public-moved"]["sourceType"] == "git"
    target = repo / "plugins" / "fixture-tools" / "skills"
    target.mkdir(parents=True)
    for name in names[:2]:
        git("mv", f"skills/{name}", f"plugins/fixture-tools/skills/{name}")
        (target / name / "SKILL.md").write_text((target / name / "SKILL.md").read_text().replace("v1", "v2"))
        old = repo / "skills" / name
        old.mkdir()
        (old / "README.md").write_text(f"Moved to ../../plugins/fixture-tools/skills/{name}/.\n")
    catalog = repo / ".claude-plugin" / "marketplace.json"
    catalog.parent.mkdir()
    local_catalog = {"name": "fixture", "owner": {"name": "Fixture"}, "plugins": [
        {"name": "fixture-tools", "version": "0.1.0", "source": "./plugins/fixture-tools"}]}
    catalog.write_text(json.dumps(local_catalog))
    git("add", ".")
    git("commit", "-m", "Move skills")
    git("push", str(bare), "main")
    for label, scope in [("global", ["-g"]), ("project", ["-p"])]:
        code, output = skills(label, "update", *scope, "-y")
        after = lock(label)
        results[f"{label}_public_relocated"] = after["skills"]["public-moved"]["skillPath"] == "plugins/fixture-tools/skills/public-moved/SKILL.md"
        installed = root / label / ("home" if label == "global" else "project") / ".agents/skills"
        results[f"{label}_public_payload_updated"] = "Fixture v2." in (installed / "public-moved/SKILL.md").read_text()
        results[f"{label}_internal_false_deletion"] = ("deleted upstream" in output and "internal-stays" in output and "internal-moved" in output)
        results[f"{label}_internal_preserved_noninteractive"] = all(name in after["skills"] for name in names[1:])
        code, output = skills(label, "update", *scope, "-y", internal=True)
        after_internal = lock(label)
        results[f"{label}_internal_relocated_with_opt_in"] = after_internal["skills"]["internal-moved"]["skillPath"] == "plugins/fixture-tools/skills/internal-moved/SKILL.md"
        results[f"{label}_internal_payload_updated"] = "Fixture v2." in (installed / "internal-moved/SKILL.md").read_text()
        results[f"{label}_internal_stays_with_opt_in"] = after_internal["skills"]["internal-stays"]["skillPath"] == "skills/internal-stays/SKILL.md" and "deleted upstream" not in output
    code, output = skills("fresh-local-catalog", "add", source, "--skill", "public-moved", "-a", "claude-code", "zed", "-y")
    results["fresh_named_local_catalog"] = (root / "fresh-local-catalog/project/.agents/skills/public-moved/SKILL.md").exists()
    git("tag", "fixture-tools--v0.1.0")
    git("push", str(bare), "refs/tags/fixture-tools--v0.1.0")
    local_catalog["plugins"][0]["source"] = {"source": "git-subdir", "url": source,
        "path": "plugins/fixture-tools", "ref": "fixture-tools--v0.1.0"}
    catalog.write_text(json.dumps(local_catalog))
    git("add", ".")
    git("commit", "-m", "Pin catalog")
    git("push", str(bare), "main")
    code, output = skills("fresh-pinned-catalog", "add", source, "--skill", "public-moved", "-a", "claude-code", "zed", "-y")
    results["fresh_named_tag_pinned_catalog"] = (root / "fresh-pinned-catalog/project/.agents/skills/public-moved/SKILL.md").exists()
    code, output = skills("fresh-pinned-full-depth", "add", source, "--skill", "public-moved", "--full-depth", "-a", "claude-code", "zed", "-y")
    results["fresh_named_tag_pinned_full_depth"] = (root / "fresh-pinned-full-depth/project/.agents/skills/public-moved/SKILL.md").exists()
    report = {"cli_version": version, "fixture": str(root), "source": source,
              "git_rewrite_target": bare.as_uri(),
              "before_locks": before, "results": results, "commands": logs}
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"cli_version": version, "fixture": str(root), "results": results}, indent=2))
    assert all(value for key, value in results.items() if key != "fresh_named_tag_pinned_catalog"), "Unexpected relocation result; inspect report"


if __name__ == "__main__":
    main()
