# Changelog

## [1.2.0] - 2026-02-20

### Changed

- Restructured after reviewing Kepano's official version of this skill, adopting its concise patterns-first approach
- Grouped search, links, and structure commands (orphans, dead ends, unresolved wikilinks, backlinks) into a dedicated section
- Trimmed from 190 to ~120 lines by cutting sections easily discoverable via `obsidian help` (Publish, History/Diff, Execute Commands, Vault/Workspace)
- Reframed skill as a patterns guide rather than an exhaustive command manual, with explicit delegation to `obsidian help` for the canonical reference
- Updated frontmatter description to mention vault structure commands, Bases, and plugin development
- Added properties-peek tip under Notes as a lightweight alternative to reading full note content
- Linked directly to the raw markdown source of Obsidian CLI docs on GitHub, which is more agent-friendly than the main, hosted help site

### Added

- "Find broken wikilinks" and "Find orphan notes" rows in the quick reference table

## [1.0.0] - 2026-02-10

### Added

- Initial version, created independently before Kepano's official obsidian-cli skill
- Comprehensive command reference covering all CLI subcommands with inline `[optional]` parameter signatures
- Sections for Bases, Publish, History/Diff, Vault/Workspace, and Execute Commands
- Quick reference table
- Was thorough but verbose (~190 lines); tried to be an exhaustive manual rather than a practical guide
