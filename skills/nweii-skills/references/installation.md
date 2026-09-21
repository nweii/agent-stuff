# Installation and maintenance

Use this reference before installing, updating, repairing, removing, or diagnosing a skill installation.

## Source choice

Install public skills from `nweii/agent-stuff`, private skills from `nweii/agent-stuff-private`, and third-party skills from their GitHub slug unless they ship a supported plugin. Prefer the plugin when it provides the requested skill.

For private repositories, confirm `gh auth status` first. Do not use a local clone path or SSH URL as the recorded source. Treat tokens as credentials.

If a vendored third-party set has licensed and free skills with the same names, follow its private vendor README and pass explicit `--skill` names. An unscoped install can overwrite fuller copies without leaving a version trace.

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

Use `bunx skills use <owner/repo> -s <name>` to try a public skill without installing it. Installation work is complete only after the real copy, relevant symlinks, and recorded source match the intended layout.
