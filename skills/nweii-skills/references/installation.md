# Installation and maintenance

Use this reference before discovering or using a repository skill on demand, or installing, updating, repairing, removing, or diagnosing a skill installation.

## Source choice

Install public skills from `nweii/agent-stuff`, private skills from `nweii/agent-stuff-private`, and third-party skills from their GitHub slug unless they ship a supported plugin. Prefer the plugin when it provides the requested skill.

For private repositories, confirm `gh auth status` first. Do not use a local clone path or SSH URL as the recorded source. Treat tokens as credentials.

If a vendored third-party set has licensed and free skills with the same names, follow its private vendor README and pass explicit `--skill` names. An unscoped install can overwrite fuller copies without leaving a version trace.

## Discovery and use without installation

`bunx skills list -g --json` lists installed global skills; omit `-g` for project installations. It does not list uninstalled repository skills.

Browse a repository without installing anything:

```bash
INSTALL_INTERNAL_SKILLS=1 bunx skills add nweii/agent-stuff --list --full-depth
INSTALL_INTERNAL_SKILLS=1 bunx skills add nweii/agent-stuff-private --list --full-depth
```

`INSTALL_INTERNAL_SKILLS=1` includes skills marked `internal: true` in the listing; `--full-depth` includes nested vendor packages. Use repository catalogs or local source folders to narrow the search when the listing is large.

Load one named skill for the current task:

```bash
bunx skills use nweii/agent-stuff --skill <name>
bunx skills use nweii/agent-stuff-private --skill <name>
```

Pass the frontmatter name; an explicit selector includes internal skills. Add `--full-depth` for nested vendor packages. Remote commands fetch the published repository state. For authorized local work on an unpublished skill, read its canonical local `SKILL.md` and supporting files directly; retain the GitHub repository as its recorded source.

`use` prints an instruction prompt and downloads supporting files to a temporary directory. Read that output, follow the skill for the user's task, and resolve relative references and scripts from the reported directory. Fetching alone does not execute the task. Omit `--agent`: that option starts a separate interactive agent rather than loading instructions into the current conversation. This workflow creates temporary files without adding a persistent skill installation.

Before removing an infrequently used installation, compare its full directory with canonical source and preserve useful drift. Confirm the source can be loaded on demand, then remove only the authorized skill and agent targets. Keep `nweii-skills` discoverable as the entry point for named repository skills.

## Canonical layout

`bunx skills add` uses `~/.agents/skills/<name>/` as the real copy when at least two compatible agent targets are supplied. Nathan's MacBook may expose this through a directory-level `~/.claude/skills -> ~/.agents/skills` symlink.

Check `readlink ~/.claude/skills` before diagnosing per-skill directories. If the parent is that symlink, a real-looking child directory is canonical, deleting it deletes the skill, and adding a per-skill symlink can create a loop.

Install with explicit skill and agent targets:

```bash
bunx skills add nweii/agent-stuff --skill <name> -a claude-code zed -g -y
bunx skills add nweii/agent-stuff-private --skill <name> -a claude-code zed -g -y
bunx skills add <owner/repo> --skill <name> -a claude-code zed -g -y
```

Pass the frontmatter `name:` to `--skill`; a differing folder name can silently install nothing. A single `-a claude-code` target uses copy mode and bypasses `~/.agents/skills`. Without `-a`, the tool may spread the skill to unrelated agent directories.

## Updating and repair

Use `bunx skills update <name> -g` only for public, non-internal skills and compatible third-party skills. Private-repository and `internal: true` skills can fail tree discovery; refresh those by rerunning the matching `bunx skills add` command.

When `~/.claude/skills` is not a parent symlink and a per-skill entry is a copied directory, reinstall with the two-agent command. Reinstallation replaces downstream drift, so reconcile useful changes into canonical source first.

Remove accidental spread with one space-separated agent list:

```bash
bunx skills remove --skill <name> -a augment codebuddy cursor -g -y
```

Installation work is complete only after the real copy, relevant symlinks, and recorded source match the intended layout.
