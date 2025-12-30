# Periodic notes and Bases

Periodic notes are journal entries organized by time period. This vault uses four periodic note types, identified by filename:

- Daily: `YYYY-MM-DD-ddd`
- Weekly: `YYYY-[W]WW`
- Quarterly: `YYYY-[Q]n`
- Yearly: `YYYY`

IMPORTANT: Be thoughtful about the recency of notes, always understand the datedness of these notes relative to the current date, as more recent notes better reflect Nathan's current mind and recent pre-occupations.

## Locations

- Daily: `01-Days/YYYY-MM-DD-DayName.md` (file ex. `2025-05-08-Thu.md`)
- Weekly: `01-Days/Weeks/YYYY-Www.md` (file ex. `2025-W02.md`)
- Quarterly: `01-Days/Quarters/YYYY-Q#.md` (file ex. `2025-Q1.md`)
- Yearly: `01-Days/Years/YYYY.md`

## Frontmatter used by periodic notes Bases

- `description`: single-line synopsis
- `related`: array of wikilinks connecting periods (dailies↔weeks↔quarters↔year)
- `reviewed`: boolean for daily checkoffs -- only used for daily notes

## Embedded Bases scope and columns

- When you see embed wikilink syntax such as `![[Period entries.base#ViewName]]`, you're seeing a reference to another .base file in the vault. That's a sign to view that base's query information and column information.
- Weekly notes embed a Daily view scoped to the week using either `related.contains(this.file)` or `this.related.contains(file.asLink())`. Columns: `reviewed`, `file.name`, `summary`. Sort by `file.name`.
- Quarterly notes embed a Weekly view and define lightweight formulas to label the week range from linked dailies:
  - `period_start`, `period_end` (from linked daily filenames)
  - `week_range` (displayed as column `range`)
    Columns: `file.name`, `range` (`formula.week_range`), `summary`.
- Yearly notes embed a Quarterly view and define:
  - `q_num` (from `file.name`)
  - `month_span` (displayed as column `months`)
    Columns: `months` (`formula.month_span`), `file.name`, `summary`.

## Global overview Base for periodic notes

- `98-Spaces/Periodic notes.base` provides vault-wide Daily/Weekly/Quarterly/Annual tables.
- Each view mirrors the columns of its embedded counterpart and always includes `description`.
- Views identify notes by filename patterns (not paths) and may sort ascending or descending by `file.name` as preferred.
- Formulas are defined once at the top level only when a view needs them (`week_range`, `month_span`).
