---
name: nweii-skills
description: "Reference context for Nathan's agent skills setup: the nweii/agent-stuff repo, frontmatter conventions, changelog practices, privacy tiers, and how to migrate locally-developed skills into the repo. Use when creating, editing, migrating, or installing skills in Nathan's environment."
metadata:
  author: nweii
  version: "1.1.0"
  internal: true
---

# nweii-skills

Reference context for Nathan's skills ecosystem. Read this before creating, editing, or migrating any skill in his environment.

## The repo

Skills live at [nweii/agent-stuff](https://github.com/nweii/agent-stuff), cloned locally at `~/Developer/LLMs/agent-stuff/`.

```
agent-stuff/
├── skills/          # Public and internal skills
│   └── private/     # Gitignored — truly private skills (sensitive content)
├── commands/        # Slash commands
├── templates/       # SKILL_TEMPLATE.md, RULE_TEMPLATE.md
└── reference/       # Platform docs
```

A git hook auto-updates `README.md` with a skills catalog on every commit.

## Installing and updating skills

**Always scope installs to `-a claude-code`.** Without it, `bunx skills add` spreads the skill into 27+ agent directories (`~/.codebuddy/skills/`, `~/.cline/skills/`, etc.) for tools that aren't used. Claude Code is the only target that matters here.

```bash
# Install a specific skill globally, scoped to claude-code only
bunx skills add nweii/agent-stuff --skill <name> -a claude-code -g -y

# Install all skills, scoped to claude-code only
bunx skills add nweii/agent-stuff -a claude-code -g -y

# Update non-internal skills (does NOT touch metadata.internal: true skills)
bunx skills update -g
```

Repo edits do NOT propagate live — `bunx skills add` copies the SKILL.md into `~/.claude/skills/<name>/`, hardlinked from `~/.agents/skills/<name>/`, but neither side is linked back to the repo source.

**`bunx skills update -g` does not work on skills with `metadata.internal: true`.** The update will appear to run but silently fail with "Failed to update <name>" and no further detail. To refresh an internal skill after pushing repo changes, do a full reinstall:

```bash
bunx skills remove --skill <name> -a claude-code -g -y
bunx skills add nweii/agent-stuff --skill <name> -a claude-code -g -y
```

For non-internal skills, `bunx skills update -g` is the right refresh path.

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

`metadata.internal: true` marks personal workflows that are pushed to GitHub but not intended for general use. It's distinct from `skills/private/` (gitignored, never pushed).

## Privacy tiers

| Location | Pushed | Use for |
|---|---|---|
| `skills/` | Yes | Public skills and personal workflows (`internal: true`) |
| `skills/private/` | No (gitignored) | Sensitive or confidential content |

## Changelogs

Only add a `changelog.md` when a skill has meaningful versioned history worth preserving — significant behavioral changes, deprecated patterns, or decisions future maintainers should understand. Omit it for simple or stable skills. When present, increment `metadata.version` alongside it.

## Migrating a locally-developed skill into the repo

When a skill has been developed directly in `~/.agents/skills/` and needs to move into the repo:

1. Copy the skill folder to `skills/` (or `skills/private/` if truly private)
2. **Fix the description** — wrap it in double quotes if it isn't already
3. Commit and push
4. Trash the local copy: `trash ~/.agents/skills/<skill-name>`
5. Reinstall from the repo: `bunx skills add nweii/agent-stuff --skill <name> -a claude-code -g -y`

The reinstalled version is a copy at `~/.claude/skills/<name>/`, hardlinked from `~/.agents/skills/<name>/`. To pick up subsequent repo edits: `bunx skills update -g` for non-internal skills, or `remove` + `add` for `metadata.internal: true` skills (which `update` skips).
