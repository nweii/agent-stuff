# Agent Instructions

Instructions for AI assistants working on this repository.

## What this repo is

A personal collection of AI agent skills, plugins, commands, and rules. It follows the Claude/Anthropic Agent Skills format.

## Directory structure

```
agent-stuff/
├── skills/           # Agent Skills (Claude format), organized by category
├── commands/         # Slash commands, organized by context
├── templates/        # Templates for new components
├── reference/        # Platform docs and guides
└── obsidian/         # Obsidian-related configs
```

## Creating skills

Use `templates/SKILL_TEMPLATE.md` as a starting point. Key requirements:

- **Description is critical** — Must clearly state what the skill does and when to use it
- Keep `SKILL.md` under 500 lines; split complex content into referenced files
- Include concrete examples
- Test that the description triggers the skill appropriately

## Frontmatter reference

All frontmatter fields for `SKILL.md`:

| Field | Type | Purpose |
|-------|------|---------|
| `name` | required | Lowercase with hyphens, max 64 chars |
| `description` | required | What skill does + when to use it, max 1024 chars |
| `argument-hint` | optional | Hint shown after `/name`, e.g. `[issue-number]` |
| `disable-model-invocation` | optional | If `true`, only user can invoke via `/name` |
| `user-invocable` | optional | If `false`, only Claude can invoke (not shown as `/command`) |
| `allowed-tools` | optional | Comma-separated list of tools, e.g. `Read, Grep, Glob` |
| `model` | optional | Model to use for this skill |
| `context` | optional | `fork` runs in subagent; `agent` specifies agent type |
| `agent` | optional | Agent type for `context: fork` (e.g., `Explore`, `Plan`) |
| `hooks` | optional | [Hooks](https://docs.anthropic.com/docs/en/hooks) integration |
| `metadata` | custom | Author/version tracking (custom, not in spec) |

### Invocation control

- **Model-invoked (default)**: Claude decides when to use based on description
- **`disable-model-invocation: true`**: User-only via `/name` — use for side effects like deploy, commit
- **`user-invocable: false`**: Model-only — use for background knowledge Claude should know

### Arguments

Use `$ARGUMENTS` in skill content to receive user input:

```yaml
---
name: fix-issue
description: Fix a GitHub issue
disable-model-invocation: true
---
Fix GitHub issue $ARGUMENTS following our coding standards.
```

Invoked as: `/fix-issue 123`

### Subagent execution

Use `context: fork` to run in isolated context:

```yaml
---
name: deep-research
description: Research a topic thoroughly
context: fork
agent: Explore
---
Research $ARGUMENTS thoroughly...
```

### Dynamic context injection

Prefix commands with `!` to execute before Claude sees the content:

```yaml
---
name: pr-summary
description: Summarize PR changes
context: fork
---
PR diff: !`gh pr diff`
Summarize this pull request...
```

## Style

- Forward slashes for all paths
- Valid YAML frontmatter (no tabs)
- Well-formatted markdown with language-tagged code blocks

## Security

Never commit credentials, API keys, or proprietary code.
