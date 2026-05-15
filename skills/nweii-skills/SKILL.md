---
name: nweii-skills
description: "Reference for Nathan's agent skills setup: the nweii/agent-stuff and nweii/agent-stuff-private repos, frontmatter conventions, changelog practices, privacy tiers, and migrating locally-developed skills into a repo. Use when creating, editing, migrating, or installing skills in Nathan's environment."
metadata:
  author: nweii
  version: "1.4.0"
  internal: true
---

# nweii-skills

Reference context for Nathan's skills ecosystem. Read this before creating, editing, or migrating any skill in his environment.

## The repos

Skills live in two paired repos:

- **[nweii/agent-stuff](https://github.com/nweii/agent-stuff)** — public + internal-but-public skills. Cloned at `~/Developer/LLMs/agent-stuff/`.
- **`nweii/agent-stuff-private`** — truly private skills (career materials, personal workflows, confidential content). Cloned at `~/Developer/LLMs/agent-stuff-private/`. Pushed to a private GitHub remote; never made public.

Both repos use the same layout:

```
<repo>/
├── skills/          # Skill folders
├── commands/        # Slash commands (agent-stuff only)
├── templates/       # SKILL_TEMPLATE.md, RULE_TEMPLATE.md (agent-stuff only)
└── reference/       # Platform docs (agent-stuff only)
```

`agent-stuff` has a git hook that auto-updates `README.md` with a skills catalog on every commit. `agent-stuff-private` does not (kept simple).

## Source of truth: the repos, not the install dir

**All edits to a skill happen in the repo working copy** (`~/Developer/LLMs/agent-stuff/skills/<name>/` or `~/Developer/LLMs/agent-stuff-private/skills/<name>/`). The install at `~/.agents/skills/<name>/` is a **downstream copy** placed there by `bunx skills add`, and gets overwritten on the next install or update.

Never edit the install dir directly. If you find yourself reaching for `~/.agents/skills/<name>/SKILL.md`, stop — find the matching repo folder and edit there instead, then reinstall to sync the change down.

Why this matters: `~/.agents/skills/` is not version-controlled, not synced across machines, and not the artifact that gets pushed to GitHub. Edits there are silently ephemeral. The repo is the source; everything else is a render of it.

## Installing and updating skills

Always install via `bunx skills add`. The source differs by repo:

- **Public (`agent-stuff`)** → install from the GitHub slug `nweii/agent-stuff`. Cloud route, gets updates via `bunx skills update`.
- **Private (`agent-stuff-private`)** → install from the **local clone path** `~/Developer/LLMs/agent-stuff-private`. The cloud route is blocked by known bunx bugs with private repos.
- **Third-party** → install from their GitHub slug.

Symlinking the install location to the repo is **not** the workflow. It bypasses bunx's install machinery (agent-tracking, scoping, manifest entries) and creates inconsistency with the rest of the collection. If you find a symlinked install for one of Nathan's skills, treat it as drift to repair — see "Repairing a symlinked install" below.

### Architecture (read this first)

`~/.claude/skills` is a **symlink** to `~/.agents/skills`. There is only one install root; Claude Code sees it through that parent-level symlink. So:

- A skill at `~/.agents/skills/<name>/` is automatically visible to Claude Code at `~/.claude/skills/<name>/`.
- There are no per-skill hardlinks or copies between the two paths — they're the same dir, two access paths.
- Trashing `~/.claude/skills/<name>/` actually trashes `~/.agents/skills/<name>/` (you only need to do it once, via either path).

### Install commands

**Always scope installs to `-a claude-code`.** Without it, `bunx skills add` spreads the skill into 27+ agent directories (`~/.codebuddy/skills/`, `~/.cline/skills/`, etc.) for tools that aren't used.

```bash
# Public agent-stuff — from GitHub
bunx skills add nweii/agent-stuff --skill <name> -a claude-code -g -y

# Private agent-stuff-private — from local clone path
bunx skills add ~/Developer/LLMs/agent-stuff-private --skill <name> -a claude-code -g -y

# Third-party
bunx skills add vercel-labs/agent-skills --skill <name> -a claude-code -g -y
```

**Why local path for private?** HTTPS URLs hang on credentials for private repos ([vercel-labs/skills#12](https://github.com/vercel-labs/skills/issues/12)), and `bunx skills update -g` doesn't work against private repos either ([vercel-labs/skills#381](https://github.com/vercel-labs/skills/issues/381)). Installing from the local clone sidesteps both. The SSH URL form (`git@github.com:nweii/agent-stuff-private.git`) is a last-resort alternative if the local clone isn't available.

### Updating an installed skill

For private skills (and any skill with `metadata.internal: true`), `bunx skills update` silently fails with "Failed to update <name>". Re-run `bunx skills add` over the existing install — it overwrites in place, no `remove` first:

```bash
bunx skills add ~/Developer/LLMs/agent-stuff-private --skill <name> -a claude-code -g -y
```

For public/third-party skills without the `internal` flag, `bunx skills update <name> -g` works normally.

### Repairing a symlinked install

If `~/.agents/skills/<name>` is a symlink pointing into `~/Developer/LLMs/agent-stuff*/skills/`, replace it with a real bunx install:

```bash
trash ~/.agents/skills/<name>          # removes the symlink, not the repo source
# Then install via the appropriate source for the skill's repo:
bunx skills add nweii/agent-stuff --skill <name> -a claude-code -g -y                          # public
bunx skills add ~/Developer/LLMs/agent-stuff-private --skill <name> -a claude-code -g -y       # private
```

`--skill` takes the **frontmatter `name:`**, not the repo folder name. When the two differ (e.g. repo folder `lennys-podcast-transcripts-slim` with frontmatter `name: lennys-podcast-transcripts`), pass the frontmatter name. Bunx will silently install nothing if you pass the folder name in this case.

### Cleaning up multi-agent spread

If a previous install spread to multiple agents, scope the cleanup with repeated `-a` flags (the comma-separated form does not parse):

```bash
bunx skills remove --skill <name> -a augment -a codebuddy -a cursor -g -y
```

## Pushing changes

Commit freely in either repo working copy — that's local-only. Pushing is where the gate is:

- **`agent-stuff` (public)** — **always get explicit user confirmation before `git push`.** Public commits are world-readable on GitHub and feed the auto-generated catalog. Don't push opportunistically.
- **`agent-stuff-private`** — push as needed, no extra gate.

## Frontmatter conventions

```yaml
---
name: skill-name           # lowercase-with-hyphens, max 64 chars
description: "..."         # Always quoted. Max ~1024 chars. Describe what it does AND when to use it.
metadata:
  author: nweii
  version: "1.0.0"         # semver, always quoted
  internal: true           # only include when true
---
```

**Description quoting is required** — always wrap in double quotes. YAML chokes on unquoted descriptions that contain `: ` (colon-space), em dashes, or other special characters. This is a silent failure: the skill file appears valid but bunx can't parse the name and won't find the skill.

`metadata.internal: true` marks personal workflows that are pushed to GitHub but not intended for general use. Use it on any skill that's specifically tuned to Nathan's setup, regardless of which repo it lives in.

## Privacy tiers

Three tiers, two repos:

| Tier | Repo | Visibility | Use for |
|---|---|---|---|
| Public | `agent-stuff` | Public on GitHub, no `internal` flag | Skills genuinely useful to others |
| Internal-but-public | `agent-stuff` | Public on GitHub, `metadata.internal: true` | Personal workflows that aren't sensitive but aren't general-purpose either |
| Private | `agent-stuff-private` | Private GitHub remote, `metadata.internal: true` | Career materials, project-specific assistants, anything that shouldn't leave Nathan's environment |

The previous `skills/private/` (gitignored subfolder of agent-stuff) tier is retired — that pattern was fragile (one stray `git add -A` and content leaks) and made cross-machine sync impossible. All formerly-private skills now live in `agent-stuff-private`.

## Changelogs

Only add a `changelog.md` when a skill has meaningful versioned history worth preserving — significant behavioral changes, deprecated patterns, or decisions future maintainers should understand. Omit it for simple or stable skills. When present, increment `metadata.version` alongside it.

## Migrating a locally-developed skill into a repo

When a skill has been developed directly in `~/.agents/skills/` and needs to move into a repo:

1. Decide the tier (public, internal-but-public, or private) and pick the matching repo
2. Copy the skill folder to `<repo>/skills/<name>/`
3. **Fix the description** — wrap it in double quotes if it isn't already
4. Commit and push (private repo: ensure the remote is private)
5. Trash the local install: `trash ~/.agents/skills/<name>`
6. Reinstall via bunx from the appropriate source:
   ```bash
   # Public
   bunx skills add nweii/agent-stuff --skill <name> -a claude-code -g -y
   # Private
   bunx skills add ~/Developer/LLMs/agent-stuff-private --skill <name> -a claude-code -g -y
   ```

   Future edits happen in the repo, then re-run `bunx skills add` (private) or `bunx skills update` (public) to sync the install.

**The install dir is downstream, not source.** Edits to `~/.agents/skills/<name>/SKILL.md` get overwritten on the next `bunx skills add`. Always edit in the repo working copy. If you suspect drift before migrating, diff the install against the repo and reconcile to the repo before reinstalling.
