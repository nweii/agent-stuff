# History rollup command

Compiles periodic note mentions of a project into a consolidated [[Histories]] note.

## Invocation

```
Roll up history for [[Project Name]]
Roll up history for [[Project Name]] from 2025-01 to 2025-06
Roll up history for [[Project Name]] starting 2025-Q3
```

## Inputs

- **Project wikilink** (required): The project domain to search for (e.g., `[[Acme client work]]`, `[[Side project]]`)
- **Timespan** (optional): Start date, end date, or range. Accepts:
  - Single date: `2025-01`, `2025-Q2`, `2025-W15`
  - Range: `from 2025-01 to 2025-06`
  - Open-ended: `starting 2025-Q3`, `until 2025-06`
  - Default: Earliest uncovered mention to present

## Workflow

### 1. Find existing coverage

Search for History notes already linked to this project:

```bash
# Using ripgrep
rg -l "related:.*\[\[Project Name\]\]" "01-Days" "03-Records" --glob "*.md"

# Using obsidian-cli (preferred)
obsidian-cli search-content "related:.*\[\[Project Name\]\]"
```

Or use MCP vault search:

```
vault search: related.contains(link("Project Name")) AND categories.containsAny(link("Histories"))
```

Extract `start:` and `end:` frontmatter from found histories to determine covered periods. You can use `obsidian-cli frontmatter "Note" --print` to extract these fields efficiently.

### 2. Search periodic notes for mentions

```bash
# Using ripgrep
rg "\[\[Project Name\]\]" "01-Days" -l

# Using obsidian-cli
obsidian-cli search-content "[[Project Name]]"
```

For each matching file, the AI reads the note and extracts entries mentioning the project. Extraction is **context-aware**, not purely pattern-based:

- Bullet points containing the wikilink
- Surrounding context if the mention is part of a larger narrative
- Section headings if the project is discussed under a dedicated heading
- Related entries on the same date even if they don't repeat the wikilink

### 3. Filter by timespan

- Parse filenames to determine dates (`2025-01-15-Wed.md` → 2025-01-15)
- Exclude entries already covered by existing History notes
- Apply user-specified date bounds if provided

### 4. Generate the History note

**Filename**: `Retro - {Project short name} {timespan description}.md`

- Example: `Retro - Acme client work from 2025-Q3 to 2025-Q4.md`

**Frontmatter**:

```yaml
---
categories:
  - "[[Histories]]"
type: Projects
description: { AI-generated one-line summary of the period's work }
start: { YYYY-MM-DD of earliest entry }
end: { YYYY-MM-DD of latest entry }
related:
  - "[[Project Name]]"
tags:
  - log/archive
  - { project-specific tag if one exists }
created: { current date }
modified: { current date }
---
```

**Body structure**:

```markdown
## {Project short name} Log

### [[YYYY-Qn]]

- [[YYYY-MM-DD-Day]]: Entry text extracted from periodic note
- [[YYYY-MM-DD-Day]]: Another entry...

### [[YYYY-Qn]]

- ...
```

Entries are:

- Grouped by quarter
- Sorted chronologically within each quarter
- Linked to source dates via wikilinks
- Preserved with original wording (light cleanup for consistency)

### Entries that link to dedicated notes

When a periodic note mentions the project but links to a dedicated working note (e.g., a Log, Thinking note, or Spec), include the entry as a brief pointer rather than duplicating the detail:

```markdown
- [[YYYY-MM-DD-Day]]: Built data migration script for legacy database → [[Log - Database migration script YYYY-MM]]
- [[YYYY-MM-DD-Day]]: Drafted revised project scope → [[Thinking - Project scope revision YYYY-MM]]
```

The History serves as a **chronological index**—the wikilink provides drill-down depth. This avoids duplication while preserving navigability. The arrow notation (`→`) signals that the linked note contains the substantive work.

### 5. Create the note

```bash
obsidian-cli create "03-Records/Working notes/Retro - Project timespan.md" \
  --content "..." \
  --open
```

Or use MCP vault create if available.

## Overlap handling

The command checks existing History notes' `start`/`end` frontmatter to avoid duplication:

- If a period is fully covered → skip those dates
- If partially covered → only include uncovered dates
- If the user specifies a range overlapping existing coverage → warn and ask whether to proceed (may create duplicate entries)

### Weekly note observations

If weekly notes contain relevant reflections or context about the project (not discrete work items), include them in a separate section at the end:

```markdown
### Weekly observations

- [[YYYY-Www]]: Felt the project ramping up this week; harder to context-switch to other priorities
```

This captures mood, pacing, or thematic observations that don't fit the date-entry format but provide useful context for the period.

## Edge cases

- **No periodic mentions found**: Report this and suggest checking the wikilink spelling or looking in non-periodic notes
- **Project has no existing History notes**: Create the first one covering all found mentions
- **Mentions span multiple years**: Use quarter-based grouping; consider splitting into multiple History notes if the span is very long (2+ years)
- **Dense mention periods**: Preserve detail; don't over-summarize. The History is an archive, not a summary.

## Example output

For `Roll up history for [[Acme client work]] from 2025-07 to 2025-12`:

```markdown
---
categories:
  - "[[Histories]]"
type: Projects
description: Website redesign project covering initial discovery, wireframing, and development handoff
start: 2025-07-01
end: 2025-12-31
related:
  - "[[Acme client work]]"
tags:
  - log/archive
  - client-work
created: YYYY-MM-DD
modified: YYYY-MM-DD
---

## Acme client work Log

### [[2025-Q3]]

- [[2025-07-15-Tue]]: Kickoff meeting with stakeholders; defined project scope
- [[2025-08-03-Sun]]: Completed first round of wireframes → [[Log - Acme wireframe review 2025-08]]
- ...

### [[2025-Q4]]

- [[2025-10-22-Wed]]: Handed off final designs to dev team
- ...
```
