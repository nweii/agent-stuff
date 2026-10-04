# Locates canonical standalone and plugin skills in the Git index.
# Generated catalogs and archives use staged content so unrelated work stays out of a commit.

from pathlib import Path
import subprocess


def tracked_skill_files(root):
    paths = subprocess.check_output(["git", "ls-files", "-z", "--", "skills/", "plugins/"], cwd=root).decode().split("\0")
    found = []
    for text in paths:
        path = Path(text)
        parts = path.parts
        if ((len(parts) == 3 and parts[0] == "skills" and parts[1] != "private") or
                (len(parts) == 5 and parts[0] == "plugins" and parts[2] == "skills")) and path.name == "SKILL.md":
            found.append(root / path)
    return sorted(found)


def read_index_file(root, path):
    return subprocess.check_output(["git", "show", f":{path.relative_to(root).as_posix()}"], cwd=root)
