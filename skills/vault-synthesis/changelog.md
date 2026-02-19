# Changelog

All notable changes to the `vault-synthesis` skill.

Format: [Keep a Changelog](https://keepachangelog.com)

## [1.0.1] - 2026-01-28

### Changed

- Add `internal: true` to metadata; hides this skill from normal discovery in the skill store unless `INSTALL_INTERNAL_SKILLS=1` is set. This is because this skill is specific to my personal vault system.

## [1.0.0]

### Added

- Initial skill consolidating brain-vault synthesis commands
- `references/history-rollup.md`: Compile periodic mentions into History notes
- `references/summarize-frontmatter.md`: Generate description properties for notes
- `references/periodic-rollup.md`: Synthesize child descriptions into parent notes
- `references/topic-note.md`: Create topic hub notes with backlinking
