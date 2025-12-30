# Agent Stuff

Personal prompts, skills, and commands I use with Claude and Cursor. Some are highly specific to my own setup (like my Obsidian vault). Sharing publicly in case any of it's useful or interesting to others.

## What's here

**Skills** — Instructions that Claude/Cursor automatically apply based on context. These are located in `skills/` and categorized by use case, such as personal knowledge management and technical optimizations.

**Commands** — User-invoked slash commands. Located in `commands/`, these include workflows for information processing and general-purpose technical tools.

**Reference** — Documentation on Agent Skills, Cursor rules, and how the different components work together.

**Templates** — Starting points for creating new skills, commands, and rules.

## The format

This repo uses the [Claude Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) [format](https://agentskills.io). Skills are folders containing a `SKILL.md` with YAML frontmatter and instructions. The `description` field tells AI agents when to load and apply the skill.

```
skill-name/
├── SKILL.md              # Metadata + instructions
├── reference.md          # Optional: detailed docs
└── supporting-file.md    # Optional: additional context
```

Commands are standalone markdown files with prompts that get invoked via `/command-name`.

## Using these

Copy whatever looks useful into your own `.claude/skills/` or `.cursor/rules/` directory. Adapt as needed.

Note: Some skills reference personal vault notes not included in this repo.

## License

MIT — do whatever you want with it.
