# Changelog

All notable changes to the `spec-shaping` skill.

Format: [Keep a Changelog](https://keepachangelog.com)

## [1.2.0] - 2026-02-02

### Added

- **Compositional clarity** principle: Atomic tasks should "compose up" into a clear sprint goal. Suggests adding a "Sprint Goal" statement when the relationship isn't obvious.
- **Optional: Subagent Review** section: For large or complex specs, option to use a subagent for a fresh-context audit of the sprint plan.

## [1.1.0] - 2026-01-27

### Added

- **Evergreen Document Management**: Logic to treat specs as living documents.
- **Smart Synchronization**:
  - **Update by Default**: Renames existing files to current date + revises content.
  - **Identity Heuristic**: Explicit guidance on when to _Update_ (same core identity) vs. _Fork_ (fundamental pivot).
- **Metadata**:
  - **YAML Frontmatter**: `status` and `last` date for machine readability.
  - **Context Header**: Visible "Context" callout for human readers.
- **Adaptive Output Path**: Scans for existing directories (`specs/`, `planning/`, `docs/`) before defaulting to `specs/`.
- **Standardized Naming**: Space-delimited conventions (`Checkout flow spec - 2024-03-25.md`) for both Specs and Sprint Plans.
- **Minimal Changelog**: Instructions to maintain a lightweight in-file changelog, recording only significant changes.
- **Vault Awareness**: Checks for `agents.md`/`claude.md` in external vaults.

## [1.0.0]

### Added

- Initial skill combining `spec-interview` and `spec-to-sprints` commands
- Two-phase workflow: interview → sprint breakdown
- Shape Up-aligned principles for scoping and task atomicity
