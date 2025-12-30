---
aliases:
  - "Cursor docs about rule structure"
  - "Cursor rules structure"
categories:
  - "[[Clippings]]"
  - "[[Web]]"
icon: "LiSquareBottomDashedScissors"
publish: false
excerpt: "Configure persistent instructions with Project, Team, and User Rules, plus AGENTS.md. Learn best practices for effective coding guidelines."
url: "https://cursor.com/docs/context/rules"
author:
  - "[[Anysphere]]"
tags:
  - "clippings"
  - "full-text"
  - "documentation"
  - "ai"
  - "prompts/agents"
  - "file-management"
  - "docs"
  - "dev"
  - "best-practices"
created: 2025-12-17
---
Core

## Rules

Rules provide system-level instructions to Agent. They bundle prompts, scripts, and more together, making it easy to manage and share workflows across your team.

Cursor supports four types of rules:

Project Rules

Stored in `.cursor/rules`, version-controlled and scoped to your codebase.

User Rules

Global to your Cursor environment. Used by Agent (Chat).

Team Rules

Team-wide rules managed from the dashboard. Available on Team and [Enterprise](https://cursor.com/docs/enterprise) plans.

AGENTS.md

Agent instructions in markdown format. Simple alternative to`.cursor/rules`.

## How rules work

Large language models don't retain memory between completions. Rules provide persistent, reusable context at the prompt level.

When applied, rule contents are included at the start of the model context. This gives the AI consistent guidance for generating code, interpreting edits, or helping with workflows.

## Project rules

Project rules live in `.cursor/rules`. Each rule is a folder containing a `RULE.md` file and is version-controlled. They are scoped using path patterns, invoked manually, or included based on relevance.

Use project rules to:

- Encode domain-specific knowledge about your codebase
- Automate project-specific workflows or templates
- Standardize style or architecture decisions

### Rule folder structure

Each rule folder can contain:

- **`RULE.md`** — The main rule file with frontmatter metadata and instructions
- **Scripts and prompts** — Additional files referenced by the rule

```
.cursor/rules/

  my-rule/

    RULE.md           # Main rule file

    scripts/          # Helper scripts (optional)
```

### Rule anatomy

Each rule is a folder containing a `RULE.md` file with frontmatter metadata and content. Control how rules are applied from the type dropdown which changes properties `description`, `globs`, `alwaysApply`.

| Rule Type | Description |
| --- | --- |
| `Always Apply` | Apply to every chat session |
| `Apply Intelligently` | When Agent decides it's relevant based on description |
| `Apply to Specific Files` | When file matches a specified pattern |
| `Apply Manually` | When @-mentioned in chat (e.g., `@my-rule`) |

```
---

globs:

alwaysApply: false

---

- Use our internal RPC pattern when defining services

- Always use snake_case for service names.

@service-template.ts
```

### Creating a rule

Create rules using the `New Cursor Rule` command or going to `Cursor Settings > Rules, Commands`. This creates a new rule folder in `.cursor/rules`. From settings you can see all rules and their status.

## Best practices

Good rules are focused, actionable, and scoped.

- Keep rules under 500 lines
- Split large rules into multiple, composable rules
- Provide concrete examples or referenced files
- Avoid vague guidance. Write rules like clear internal docs
- Reuse rules when repeating prompts in chat

## RULE.md file format

The `RULE.md` file is a markdown file with frontmatter metadata and content. The frontmatter metadata is used to control how the rule is applied. The content is the rule itself.

```
---

description: "This rule provides standards for frontend components and API validation"

alwaysApply: false

---

...rest of the rule content
```

If alwaysApply is true, the rule will be applied to every chat session. Otherwise, the description of the rule will be presented to the Cursor Agent to decide if it should be applied.

## Examples

  

Examples are available from providers and frameworks. Community-contributed rules are found across crowdsourced collections and repositories online.

## Team Rules

Team and [Enterprise](https://cursor.com/docs/enterprise) plans can create and enforce rules across their entire organization from the [Cursor dashboard](https://cursor.com/dashboard?tab=team-content). Admins can configure whether or not each rule is required for team members.

Team Rules work alongside other rule types and take precedence to ensure organizational standards are maintained across all projects. They provide a powerful way to ensure consistent coding standards, practices, and workflows across your entire team without requiring individual setup or configuration.

### Managing Team Rules

Team administrators can create and manage rules directly from the Cursor dashboard:

Once team rules are created, they automatically apply to all team members and are visible in the dashboard:

### Activation and enforcement

- **Enable this rule immediately**: When checked, the rule is active as soon as you create it. When unchecked, the rule is saved as a draft and does not apply until you enable it later.
- **Enforce this rule**: When enabled, the rule is required for all team members and cannot be disabled in their Cursor settings. When not enforced, team members can toggle the rule off in `Cursor Settings → Rules` under the Team Rules section.

### Format and how Team Rules are applied

- **Plain text**: Team Rules are free‑form text. They do not use the folder structure of Project Rules and do not support metadata such as `globs`, `alwaysApply`, or rule types.
- **Where they apply**: When a Team Rule is enabled (and not disabled by the user, unless enforced), it is included in the model context for Agent (Chat) across all repositories and projects for that team.
- **Precedence**: Rules are applied in this order: **Team Rules → Project Rules → User Rules**. All applicable rules are merged; earlier sources take precedence when guidance conflicts.

## Importing Rules

You can import rules from external sources to reuse existing configurations or bring in rules from other tools.

### Remote rules (via GitHub)

Import rules directly from any GitHub repository you have access to—public or private.

1. Open **Cursor Settings → Rules, Commands**
2. Click `+ Add Rule` next to `Project Rules`, then select Remote Rule (Github)
3. Paste the GitHub repository URL containing the rule
4. Cursor will pull and sync the rule into your project

Imported rules stay synced with their source repository, so updates to the remote rule are automatically reflected in your project.

### Claude skills and plugins

Cursor can load rules from Claude's skills and plugins system. These imported rules are always applied as agent-decided rules, meaning Cursor determines when they are relevant based on context.

To enable or disable Claude skills and plugins:

1. Open **Cursor Settings → Rules**
2. Find the **Import Settings** section
3. Toggle **Claude skills and plugins** on or off

## AGENTS.md

`AGENTS.md` is a simple markdown file for defining agent instructions. Place it in your project root as an alternative to `.cursor/rules` for straightforward use cases.

Unlike Project Rules, `AGENTS.md` is a plain markdown file without metadata or complex configurations. It's perfect for projects that need simple, readable instructions without the overhead of structured rules.

Cursor supports AGENTS.md in the project root and subdirectories.

```
# Project Instructions

## Code Style

- Use TypeScript for all new files

- Prefer functional components in React

- Use snake_case for database columns

## Architecture

- Follow the repository pattern

- Keep business logic in service layers
```

### Improvements

## User Rules

User Rules are global preferences defined in **Cursor Settings → Rules** that apply across all projects. They are used by Agent (Chat) and are perfect for setting preferred communication style or coding conventions:

```
Please reply in a concise style. Avoid unnecessary repetition or filler language.
```

## Legacy Cursor Rules

### .cursorrules

The `.cursorrules` (legacy) file in your project root is still supported but **will be deprecated**. We recommend migrating to Project Rules or to `AGENTS.md`.

### .mdc cursor rules

As of 2.2, `.mdc` cursor rules will remain functional however all new rules will now be created as folders in `.cursor/rules`. This is to improve the readability and maintainability of rules.