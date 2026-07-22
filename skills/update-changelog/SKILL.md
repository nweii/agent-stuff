---
name: update-changelog
description: "Add or revise a project's Keep-a-Changelog-format changelog, including version bumps and change-type groupings. Use when the user says 'update the changelog', 'log this change', or 'bump the changelog' for a project or plugin."
metadata:
  author: nweii
  version: "1.2.0"
---

# Update Changelog

Update changelog files following [Keep a Changelog](https://keepachangelog.com) conventions.

## Usage

```
/update-changelog <version> <change_type> <message>
```

## Parameters

- `<version>`: Version number (e.g., "1.1.0")
- `<change_type>`: One of: "added", "changed", "deprecated", "removed", "fixed", "security"
- `<message>`: Description of the change

## Process

1. Check for existing changelog (CHANGELOG.md or changelog.md), create if missing
2. Find or create section for the specified version with today's date
3. Add the new entry under the appropriate change type heading
4. Format according to Keep a Changelog conventions
5. Write the updated changelog back to file

## Format Conventions

- Group changes by type (Added, Changed, Deprecated, Removed, Fixed, Security)
- List changes as bullet points
- Include date for version sections (YYYY-MM-DD)
- Keep entries concise but descriptive
- No emojis

## Example Output

```markdown
## [1.2.0] - 2025-01-24

### Added
- New markdown to BlockDoc conversion feature

### Fixed
- Bug in HTML renderer causing incorrect output
```

---

## Plugin changelogs

For plugin changelog formats, see [skill-plugin-conventions.md](skill-plugin-conventions.md).
