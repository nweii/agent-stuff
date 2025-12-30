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

Good description:

```yaml
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
```

Bad description:

```yaml
description: Helps with documents
```

## Creating commands

Commands go in `commands/`. Use `templates/COMMAND_TEMPLATE.md`. Commands are user-invoked shortcuts—make them specific and actionable.

## Style

- Forward slashes for all paths
- Valid YAML frontmatter (no tabs)
- Well-formatted markdown with language-tagged code blocks

## Security

Never commit credentials, API keys, or proprietary code.
