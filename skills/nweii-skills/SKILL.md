---
name: nweii-skills
description: "Reference for Nathan's agent skills setup: the nweii/agent-stuff and nweii/agent-stuff-private repos, frontmatter conventions, changelog practices, privacy tiers, and migrating locally-developed skills into a repo. Use when creating, editing, migrating, or installing skills in Nathan's environment."
metadata:
  author: nweii
  version: "1.2.0"
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

## Installing and updating skills

**Always scope installs to `-a claude-code`.** Without it, `bunx skills add` spreads the skill into 27+ agent directories (`~/.codebuddy/skills/`, `~/.cline/skills/`, etc.) for tools that aren't used. Claude Code is the only target that matters here.

### From `agent-stuff` (public)

```bash
# Specific skill
bunx skills add nweii/agent-stuff --skill <name> -a claude-code -g -y

# All skills
bunx skills add nweii/agent-stuff -a claude-code -g -y

# Update non-internal skills (does NOT touch metadata.internal: true skills)
bunx skills update -g
```

### From `agent-stuff-private` (private)

Two install paths, depending on whether the GitHub remote is set up:

```bash
# Local path — works pre-remote, or for the same machine that has the clone
bunx skills add ~/Developer/LLMs/agent-stuff-private --skill <name> -a claude-code -g -y

# SSH URL — works on any machine with SSH access to the private remote
bunx skills add git@github.com:nweii/agent-stuff-private.git --skill <name> -a claude-code -g -y
```

**HTTPS URLs do not reliably work for private repos** ([vercel-labs/skills#12](https://github.com/vercel-labs/skills/issues/12)) — `bunx skills add` hangs on credentials. Always use SSH form for private remotes.

`bunx skills update -g` also does not work for private repos ([vercel-labs/skills#381](https://github.com/vercel-labs/skills/issues/381)). To refresh a private skill: full reinstall (see below).

### Common: install pitfalls and refresh

Repo edits do NOT propagate live — `bunx skills add` copies the SKILL.md into `~/.claude/skills/<name>/`, hardlinked from `~/.agents/skills/<name>/`, but neither side is linked back to the repo source.

**Two cases where `bunx skills update -g` doesn't work**:

- Skills with `metadata.internal: true` — silently fails with "Failed to update <name>"
- Skills installed from private repos

For both: full reinstall to refresh:

```bash
bunx skills remove --skill <name> -a claude-code -g -y
bunx skills add <source> --skill <name> -a claude-code -g -y
```

For public, non-internal skills, `bunx skills update -g` is the right refresh path.

### Skill name vs folder name

`bunx skills add --skill <name>` matches against the **`name:` field in frontmatter**, not the folder name. If a skill folder is `lennys-podcast-transcripts-slim/` but its frontmatter says `name: lennys-podcast-transcripts`, install with the frontmatter name. Mismatches surface as "No matching skills found".

If a previous install spread to multiple agents, scope the cleanup with repeated `-a` flags (the comma-separated form does not parse):

```bash
bunx skills remove --skill <name> -a augment -a codebuddy -a cursor -g -y
```

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

When a skill has been developed directly in `~/.agents/skills/` (or edited in `~/.claude/skills/` without populating up) and needs to move into a repo:

1. Decide the tier (public, internal-but-public, or private) and pick the matching repo
2. Copy the skill folder to `<repo>/skills/<name>/`
3. **Fix the description** — wrap it in double quotes if it isn't already
4. Commit and push (private repo: ensure the remote is private)
5. Trash the local copy: `trash ~/.agents/skills/<skill-name>` and `trash ~/.claude/skills/<skill-name>` if both exist
6. Reinstall from the repo:
   - Public: `bunx skills add nweii/agent-stuff --skill <name> -a claude-code -g -y`
   - Private: `bunx skills add git@github.com:nweii/agent-stuff-private.git --skill <name> -a claude-code -g -y` (or local path if remote not set up)

The reinstalled version is a copy at `~/.claude/skills/<name>/`, hardlinked from `~/.agents/skills/<name>/`. To pick up subsequent repo edits, see "Common: install pitfalls and refresh" above.

**Watch for install-side edits.** If you've been editing the install copy (`~/.claude/skills/<name>/SKILL.md`) directly without populating back to the repo, those edits are the real source of truth — copy that version into the repo, not whatever stale version is sitting there. Diff before moving when in doubt.
