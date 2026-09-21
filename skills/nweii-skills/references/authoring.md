# Skill authoring

Use this reference before creating or substantially editing a skill.

## Structure and writing

Use `templates/SKILL_TEMPLATE.md` in `agent-stuff` when starting a skill. Keep the procedure operational: lead with actions, keep decisions and gotchas beside the step they affect, and move branch-specific detail into a reference with a conditional pointer.

Read the `writing-for-agents` skill for context pointers, information hierarchy, completion criteria, leading words, and pruning. Add project conventions and non-obvious failure modes; omit generic knowledge and facts available cheaply from the environment or live `--help`.

Scripts must be non-interactive, safe under retry, and explicit about errors. Put structured data on stdout and diagnostics on stderr. Provide `--dry-run` for destructive operations where practical. Add a script only when deterministic reuse earns its maintenance cost.

## Frontmatter

Use double-quoted descriptions written for routing:

```yaml
---
name: skill-name
description: "Use when..."
metadata:
  author: nweii
  version: "1.0.0"
  internal: true
  source: owner/repo
  credit: "Prose attribution"
---
```

- Names use lowercase letters, digits, and hyphens, with a 64-character maximum.
- Descriptions state concrete user intent and discriminating triggers. Keep detailed capability lists in the body.
- `metadata.internal: true` marks Nathan-specific skills, including internal-but-public skills.
- Keep developing skills in `0.y.z`; use `1.0.0` when mature. After 1.0, bump minor for capability and patch for fixes.
- Use `metadata.source` for one canonical upstream pointer. Use `metadata.credit` for provenance that needs prose. Preserve the original author when packaging someone else's work.

## Validation

Run the repository's existing skill validator when available. At minimum, parse frontmatter, confirm the folder matches `name`, scan for unfinished placeholders, and resolve every relative Markdown link. Run new or changed scripts against a safe fixture or temporary directory.

Validation is complete when every changed skill passes structural checks and every added branch can reach its supporting reference.
