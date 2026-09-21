# Agent-stuff

This public repository contains reusable agent skills and a small set of subagent examples.

## Required context

- Read `nweii-skills` before creating, editing, migrating, or installing skills. It defines skill structure, frontmatter, privacy tiers, installation, and source ownership.
- Read `nweii-loops` before working on scheduled tasks, routines, or recurring automations.
- Use `templates/SKILL_TEMPLATE.md` when starting a skill.

## Public boundary

- Everything tracked here is public. Keep general skills vendor-neutral and user-neutral.
- A skill marked `metadata.internal: true` may describe Nathan's non-sensitive setup, but it must remain understandable and adaptable to a public reader.
- Keep private names, confidential material, credentials, and private-repository details out of this repository.
- Treat `skills/<name>/` as the source. Installed copies under `~/.agents/skills/` are downstream.
- `agents/` contains examples that users copy manually; skill installers do not install them.

## Generated files

- The pre-commit hook rebuilds the skill catalog in `README.md` and the per-skill archives in `zips/` when tracked skill files change.
- Do not hand-edit generated catalog entries or archives. Update the skill source or generator instead.
- Generated archives use tracked files only. An untracked file does not enter a release archive.

## Publishing

Local commits are allowed. Get Nathan's explicit confirmation before pushing this public repository.
