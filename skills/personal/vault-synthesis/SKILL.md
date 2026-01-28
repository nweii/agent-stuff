---
name: vault-synthesis
description: "Synthesize information across vault notes: history rollups, frontmatter summaries, periodic rollups, and topic note creation. Use when aggregating, summarizing, or organizing content across multiple notes."
metadata:
  author: nweii
  version: "1.0.1"
  internal: true
---

# Vault Synthesis

Operations that synthesize, aggregate, or organize information across multiple notes in the Brain vault. This skill provides a unified framework for various synthesis patterns.

## When to Use

Use this skill when you need to:

- Compile periodic note mentions into a History note
- Generate or update `description` frontmatter for notes
- Roll up child note summaries into parent periodic notes
- Create topic hub notes that group related content

## Core Principles

All synthesis operations share these principles:

1. **Preserve source links**: Always maintain wikilinks back to source notes for traceability
2. **Respect hierarchy**: Understand the relationship between daily → weekly → quarterly notes
3. **Minimal overhead**: Synthesis should reduce cognitive load, not add organizational complexity
4. **Token efficiency**: Use description frontmatter and hierarchical summaries to enable efficient navigation

## Synthesis Operations

### History Rollup

Compile periodic note mentions of a project/domain into a consolidated [[Histories]] note.

**Triggers**: "Roll up history for [[Project]]", "Compile mentions of [[Topic]]"

See [references/history-rollup.md](references/history-rollup.md) for detailed workflow.

---

### Summarize to Frontmatter

Generate a `description` property for a note's YAML frontmatter based on content analysis.

**Triggers**: "Summarize this note", "Generate description for [[Note]]", "Add frontmatter summary"

See [references/summarize-frontmatter.md](references/summarize-frontmatter.md) for mode selection and guidelines.

---

### Periodic Rollup

Synthesize child note descriptions into a parent periodic note's description (e.g., weekly from dailies, quarterly from weeklies).

**Triggers**: "Roll up my weekly summary", "Summarize this quarter from weeks"

See [references/periodic-rollup.md](references/periodic-rollup.md) for the hierarchical synthesis process.

---

### Topic Note Creation

Create a Commentary topic note that groups related notes under a common theme, with automatic backlinking.

**Triggers**: "Group these under a topic about X", "Create topic note for [[A]], [[B]], [[C]]"

See [references/topic-note.md](references/topic-note.md) for the creation workflow.

---

## General Synthesis Guidance

If you encounter a synthesis need not covered by the specific workflows above, apply these general principles:

1. **Identify the scope**: What notes are being synthesized? What's the output format?
2. **Preserve provenance**: Link back to sources so the synthesis is traceable
3. **Level of abstraction**: Match the abstraction level to the purpose (detailed for working notes, high-level for indexes)
4. **Update related metadata**: If the synthesis creates new relationships, update `related` properties bidirectionally
5. **Use existing conventions**: Follow the vault's metadata system (categories, types, tags) when creating new notes
