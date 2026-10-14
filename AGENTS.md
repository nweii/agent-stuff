# Agent-stuff

This public repository is a curated distribution of reusable agent skills and plugins.

## Required context

- Read `nweii-skills` before creating, editing, migrating, or installing skills. It defines skill structure, frontmatter, privacy tiers, installation, and source ownership.
- Read `nweii-loops` before working on scheduled tasks, routines, or recurring automations.
- Use `templates/SKILL_TEMPLATE.md` when starting a skill.

## Public boundary

- Everything tracked here is public. Keep general skills vendor-neutral and user-neutral.
- A skill marked `metadata.internal: true` may describe Nathan's non-sensitive setup, but it must remain understandable and adaptable to a public reader.
- Keep private names, confidential material, credentials, and private-repository details out of this repository.
- For Nathan's paired-repository workflow, author in the complete private library, then export approved public copies here after privacy review. Preserve public skill names and install paths; `nweii-skills` describes export validation and deliberate variants.
- Installed copies under `~/.agents/skills/` are downstream of repository source.
- `archive/agents/` preserves retired subagent definitions; keep them outside the active catalog.

## Generated files

- The pre-commit hook rebuilds the skill catalog in `README.md`, per-skill archives in `zips/`, and plugin manifests/catalogs when their sources change.
- Do not hand-edit generated catalog entries or archives. Update the skill source or generator instead.
- Generated archives use tracked files only. An untracked file does not enter a release archive.

## Plugin packaging

Standalone source is `skills/<name>/`; bundled source is `plugins/<id>/skills/<name>/` on the default branch. The folder defines membership, with exactly one copy per skill name in this distribution. Self-contained payloads follow fixed skill discovery in [Agent Plugins 1.0.0](https://agent-plugins.org/specification#6-component-discovery) and [Claude's path rules](https://code.claude.com/docs/en/plugins-reference#path-rules) (checked with Claude Code 2.1.288).

Edit `plugin-source.json` for metadata; the generator writes portable and Claude manifests and both catalogs, never skill copies. Each member must keep the name/description's audience promise: public tools work with another user's conventions; personal plugins are personal throughout. Flag mismatches.

Presentation lives in each plugin's `plugin-source.json` `interface` block: `displayName`, `shortDescription`, `longDescription`, `developerName`, `category`, `websiteURL` (the repository), and `logo`/`composerIcon` pointing at an image under the plugin's `assets/`. The generator refuses a missing image. It writes this block to root `plugin.json` under `extensions.com.openai`, following [OpenAI’s portable packaging format](https://developers.openai.com/plugins/build/plugins#plugin-structure). Claude's manifest gets `displayName` and `icon`; Claude Code ignores `icon`, which Anthropic's plugin directory reads for submitted plugins ([directory listing fields](https://code.claude.com/docs/en/plugins-reference#directory-listing-fields), checked 2.1.288). A presentation change is a plugin change: cut a release so tag-pinned Codex installs receive it.

ChatGPT's plugin page shows only the catalog entry (name, category, source) before install, because a `git-subdir` source isn't fetched until install; OpenAI catalog entries have no description or icon fields. The display name, descriptions, icon, and website appear after install.

Claude's catalog uses `./plugins/<id>` so [skills CLI 1.7.0 discovers bundled skills](https://github.com/vercel-labs/skills/blob/v1.7.0/src/plugin-manifest.ts). Claude follows the marketplace checkout (normally the default branch): Git-hosted installed plugins stay on their version until it changes, while new installs can get unreleased edits at that version ([version behavior](https://code.claude.com/docs/en/plugins-reference#version), checked 2.1.288). Codex uses tag-pinned `git-subdir` + `ref` ([parser checked at de3721a7](https://github.com/openai/codex/blob/de3721a7be07054c8c2a41102b5a501f34155361/codex-rs/core-plugins/src/marketplace.rs); installed CLI 0.155.1). Revisit this split if pending [skills PR 1334, remote marketplace sources](https://github.com/vercel-labs/skills/pull/1334) ships (open/unmerged when checked October 4, 2026).

Migrate within the same repo, preserve the frontmatter name, and leave one copy plus a README-only pointer at the old path. [Relocation](https://github.com/vercel-labs/skills/blob/v1.7.0/src/skill-relocation.ts) requires skills CLI >=1.5.24 (fixture checked 1.7.0). Its [update discovery](https://github.com/vercel-labs/skills/blob/v1.7.0/src/update.ts) falsely calls moved and unmoved internal skills deleted; use `INSTALL_INTERNAL_SKILLS=1` or decline removal.

Follow [Package and release plugins](docs/plugin-packaging.md) when generating catalogs, validating packages, or cutting a release. It owns the staged-source build, automated archive checks, client validation, and distribution workflow.

Each plugin's `README.md` is for people installing it: a hand-written intro above `<!-- PLUGIN:START -->`, then install commands and a skills table that `update-catalog.py` generates from each member's frontmatter. The table's requirements column reads the Agent Skills `compatibility` field; set it on any member that needs an app, extension, or tool.

## Publishing

Local commits are allowed. Get Nathan's explicit confirmation before pushing this public repository.
