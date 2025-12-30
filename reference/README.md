# Reference Documentation

This directory contains reference materials and documentation about different agent skill systems and platforms.

## Contents

- **Agent Skills - Claude Code Docs.md** - Official Claude Code documentation on Agent Skills
- **Equipping agents for the real world with Agent Skills - @AnthropicAI.md** - Engineering deep dive from Anthropic
- **Claude code components - when to use what.md** - Decision guide for Skills vs Commands vs Rules
- **Rules _ Cursor Docs - Cursor Documentation.md** - Cursor's rules system documentation

## Purpose

These files provide background on:
- The Claude/Anthropic Agent Skills architecture
- Progressive disclosure and context management
- Platform-specific implementations (Claude Code vs Cursor)
- Best practices for authoring skills

## Platform Comparison

### Claude/Anthropic System

**Architecture**: Progressive disclosure with layered context loading
- Level 1: Skill metadata (always loaded)
- Level 2: Full SKILL.md (loaded when relevant)
- Level 3+: Additional files (loaded as needed)

**Key Features**:
- Model-invoked (autonomous)
- Effectively unbounded skill complexity
- Code execution support
- Tool restriction via `allowed-tools`

### Cursor System

**Architecture**: Rules-based with immediate context inclusion
- Rules are loaded into context when applied
- Can be always-applied, agent-decided, file-pattern, or manual

**Key Features**:
- Can import Claude skills
- Multiple rule scopes (Project, User, Team)
- AGENTS.md simple alternative
- GitHub remote rules support

## When to Use What

| Need | Use |
|------|-----|
| Autonomous expertise application | **Skill** (Claude) |
| Quick user-invoked shortcuts | **Command** |
| Persistent instructions | **Rule** (Cursor) or **Skill** (Claude) |
| Bundle multiple components | **Plugin** |

## Further Reading

- [Claude Skills Documentation](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview)
- [Claude Code Skills Guide](https://code.claude.com/docs/en/skills)
- [Cursor Rules Documentation](https://cursor.com/docs/context/rules)
- [Agent Skills Engineering Blog](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
