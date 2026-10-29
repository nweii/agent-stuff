# Skill authoring

Use this reference before creating or substantially editing a skill.

## Structure and writing

Start skills in the private canonical library using its `templates/SKILL_TEMPLATE.md`. Keep the procedure operational: lead with actions, keep decisions and gotchas beside the step they affect, and move branch-specific detail into a reference with a conditional pointer.

Follow `writing-for-agents` for structure and pruning. Remove instructions that repeat what the agent already knows or can find in the referenced skill. Keep project-specific choices, known pitfalls, permission limits, and conditions for completion. Read the draft a second time for unnecessary clauses, awkward sentence structure, and shorthand that makes the reader decode the meaning. Preserve precise terms, make clear who does what, and cut explanations that merely repeat the instruction.

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
  source: owner/repo
  credit: "Prose attribution"
---
```

- Names use lowercase letters, digits, and hyphens, with a 64-character maximum.
- Descriptions state concrete user intent and discriminating triggers. Keep detailed capability lists in the body.
- Add `metadata.internal: true` when the skill addresses Nathan's personal environment or conventions. General skills omit it even in the private repository. The flag describes audience; repository visibility describes access.
- Set top-level `compatibility` for required apps, tools, or runtime access. Keep conditional dependencies beside the branch that needs them.
- Keep developing skills in `0.y.z`; use `1.0.0` when mature. After 1.0, bump minor for capability and patch for fixes.
- Use `metadata.source` for one canonical upstream pointer. Use `metadata.credit` for provenance that needs prose. Preserve the original author when packaging someone else's work.

## Validation

Run the canonical repository's existing skill validator when available. For an approved public export, also run `scripts/check-mirrors.py` to verify the private counterpart, approved membership, fixed public path, and mirror agreement. At minimum, parse frontmatter, confirm the folder matches `name`, scan for unfinished placeholders, and resolve every relative Markdown link. Run new or changed scripts against a safe fixture or temporary directory.

Validation is complete when every changed skill passes structural checks and every added branch can reach its supporting reference.
