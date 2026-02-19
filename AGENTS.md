# Agent Instructions

Instructions for AI assistants working on this repository.

## What this repo is

A personal collection of AI agent skills, plugins, commands, and rules. It follows the Claude/Anthropic Agent Skills format.

## Directory structure

```
agent-stuff/
├── skills/           # Agent Skills (Claude format)
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

| Field                      | Type     | Purpose                                                                     |
| -------------------------- | -------- | --------------------------------------------------------------------------- |
| `name`                     | required | Lowercase with hyphens, max 64 chars                                        |
| `description`              | required | What skill does + when to use it, max 1024 chars                            |
| `argument-hint`            | optional | Hint shown after `/name`, e.g. `[issue-number]`                             |
| `disable-model-invocation` | optional | If `true`, only user can invoke via `/name`                                 |
| `user-invocable`           | optional | If `false`, only Claude can invoke (not shown as `/command`)                |
| `allowed-tools`            | optional | Comma-separated list of tools, e.g. `Read, Grep, Glob`                      |
| `model`                    | optional | Model to use for this skill                                                 |
| `context`                  | optional | `fork` runs in subagent; `agent` specifies agent type                       |
| `agent`                    | optional | Agent type for `context: fork` (e.g., `Explore`, `Plan`)                    |
| `hooks`                    | optional | [Hooks](https://docs.anthropic.com/docs/en/hooks) integration               |
| `metadata`                 | custom   | Author/version tracking — see [Metadata conventions](#metadata-conventions) |

### Metadata conventions

`metadata` is a custom field (not part of the official spec) used for author and version tracking:

```yaml
metadata:
  author: nweii # GitHub username; use someone else's username if this is primarily their work
  version: "1.0.0" # semver, matched to the skill's changelog.md if one exists
  source:
    skills/some-skill # relative GitHub path to skill folder if using their username as author;
    # full URL if using your own username as author
  internal: true # only include if true; marks private skills or public workflows not meant for others
```

- `author` — typically a GitHub username. Use the original author's username if the skill is primarily their work.
- `version` — semver string. Increment it alongside the skill's `changelog.md` when one exists.
- `source` — attribution link to the upstream skill. Use a GitHub-relative path when `author` is set to the upstream author's username; use the full URL when `author` is set to your own username.
- `internal` — boolean flag; **only include this key when the value is `true`**. Applies to anything in the gitignored `skills/private/` subfolder, or public skills that are really internal workflows not intended for outside use.

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
