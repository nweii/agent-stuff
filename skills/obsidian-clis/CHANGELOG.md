# Changelog

## [1.5.2] - 2026-03-29

### Changed

- Removed autocommand hooks that ran `which` when the skill loaded; agents now use `command -v` / `which` only when they need to verify install, for a cleaner security review posture.

## [1.5.1] - 2026-03-29

### Changed

- Renamed `NOTESMD.md` to `notesmd-fallback.md` so the filename reads as the notesmd-cli fallback guide, not generic Markdown notes.

## [1.5.0] - 2026-03-29

### Changed

- Renamed skill to `obsidian-clis` (folder + frontmatter `name`). Reason: the upstream Obsidian skill already uses the slug `obsidian-cli`, so a distinct `name` avoids clashes when both are installed. The plural `clis` reflects multiple terminal paths (Obsidian app CLI and notesmd-cli when `obsidian` is missing), keeps the `obsidian-*` convention, and stays close to the official name for recognition.

### Added

- Headless path via **notesmd-cli** when `obsidian` is not on PATH; details in `NOTESMD.md`.
- Third-person `description` and explicit “Obsidian first, then notesmd-cli” routing (no separate invocation mode).

## [1.3.1] - 2026-03-20

### Added

- Include autocommand to verify CLI install with `which obsidian`

## [1.3.0] - 2026-03-03

### Changed

- Removed compatibility frontmatter note
- Sharper language about the CLI controlling a running instance of the app.

### Added

- Plugin development section from Steph Ango's 2026-02-10 update to his version of this skill.

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
