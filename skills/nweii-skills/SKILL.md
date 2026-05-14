---
name: nweii-skills
description: "Reference for Nathan's agent skills setup: the nweii/agent-stuff and nweii/agent-stuff-private repos, frontmatter conventions, changelog practices, privacy tiers, and migrating locally-developed skills into a repo. Use when creating, editing, migrating, or installing skills in Nathan's environment."
metadata:
  author: nweii
  version: "1.3.0"
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

For Nathan's own skills (in `agent-stuff` or `agent-stuff-private`), **always symlink** the install location to the repo. Repo edits are then immediately live in the install — no commit/push/update cycle, no risk of drift between repo and install.

For third-party skills (vercel-labs, etc.) where there's no local source repo, use bunx as the install mechanism.

### Architecture (read this first)

`~/.claude/skills` is a **symlink** to `~/.agents/skills`. There is only one install root; Claude Code sees it through that parent-level symlink. So:

- A skill at `~/.agents/skills/<name>/` is automatically visible to Claude Code at `~/.claude/skills/<name>/`.
- There are no per-skill hardlinks or copies between the two paths — they're the same dir, two access paths.
- Trashing `~/.claude/skills/<name>/` actually trashes `~/.agents/skills/<name>/` (you only need to do it once, via either path).

### Symlink Nathan's own skills (preferred)

```bash
# Public (agent-stuff)
ln -s ~/Developer/LLMs/agent-stuff/skills/<name> ~/.agents/skills/<name>

# Private (agent-stuff-private)
ln -s ~/Developer/LLMs/agent-stuff-private/skills/<name> ~/.agents/skills/<name>
```

Converting an existing bunx install to a symlink:

```bash
trash ~/.agents/skills/<name>
ln -s ~/Developer/LLMs/agent-stuff/skills/<name> ~/.agents/skills/<name>
```

When folder name differs from the frontmatter `name:`, the symlink takes the frontmatter name and points at the repo folder:

```bash
ln -s ~/Developer/LLMs/agent-stuff-private/skills/lennys-podcast-transcripts-slim ~/.agents/skills/lennys-podcast-transcripts
```

bunx still recognizes symlinked installs in `bunx skills list`, but its agent-tracking metadata may not register them as belonging to Claude Code specifically. That's only relevant for `bunx skills update`, which doesn't apply to symlinked skills anyway — edits are live.

### bunx install (for third-party skills, or initial fetch)

**Always scope installs to `-a claude-code`.** Without it, `bunx skills add` spreads the skill into 27+ agent directories (`~/.codebuddy/skills/`, `~/.cline/skills/`, etc.) for tools that aren't used.

```bash
# Public agent-stuff (initial fetch — convert to symlink afterward)
bunx skills add nweii/agent-stuff --skill <name> -a claude-code -g -y

# Private agent-stuff-private — local path
bunx skills add ~/Developer/LLMs/agent-stuff-private --skill <name> -a claude-code -g -y

# Private agent-stuff-private — SSH URL (HTTPS hangs on credentials, see vercel-labs/skills#12)
bunx skills add git@github.com:nweii/agent-stuff-private.git --skill <name> -a claude-code -g -y

# Third-party
bunx skills add vercel-labs/agent-skills --skill <name> -a claude-code -g -y
```

**HTTPS URLs do not work for private repos** ([vercel-labs/skills#12](https://github.com/vercel-labs/skills/issues/12)) — `bunx skills add` hangs on credentials. Always use SSH form.

`bunx skills update -g` does not work for private repos ([vercel-labs/skills#381](https://github.com/vercel-labs/skills/issues/381)) or for skills with `metadata.internal: true` (silently fails with "Failed to update <name>"). For those, re-run `bunx skills add` over the existing install — it overwrites in place, no `remove` first.

### Cleaning up multi-agent spread

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

When a skill has been developed directly in `~/.agents/skills/` and needs to move into a repo:

1. Decide the tier (public, internal-but-public, or private) and pick the matching repo
2. Move the skill folder to `<repo>/skills/<name>/` (use `mv`, not `cp` — you'll symlink back in step 6)
3. **Fix the description** — wrap it in double quotes if it isn't already
4. Commit and push (private repo: ensure the remote is private)
5. Trash any leftover local copy: `trash ~/.agents/skills/<name>` (this is the same dir as `~/.claude/skills/<name>/` via the parent symlink — only one trash needed)
6. Symlink the install location to the repo:
   ```bash
   # Public
   ln -s ~/Developer/LLMs/agent-stuff/skills/<name> ~/.agents/skills/<name>
   # Private
   ln -s ~/Developer/LLMs/agent-stuff-private/skills/<name> ~/.agents/skills/<name>
   ```

   Future repo edits are immediately live in the install — no reinstall needed.

**Watch for install-side edits.** If you've been editing the install dir (`~/.agents/skills/<name>/SKILL.md`) directly while it was still a bunx-installed copy (not yet symlinked), that version is the real source of truth — diff against the repo before moving and use the install version if it's newer.
