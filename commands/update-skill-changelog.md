# Update Skill Changelog

Update a skill's changelog.md file with a new entry. Also updates the version comment in SKILL.md frontmatter.

## Usage

`/update-skill-changelog <skill_path> <version> <change_type> <message>`

## Parameters

- `<skill_path>`: Path to the skill folder (e.g., `.claude/skills/aid-career`)
- `<version>`: Version number (e.g., "1.6.0")
- `<change_type>`: One of: "added", "changed", "deprecated", "removed", "fixed"
- `<message>`: Description of the change

## Examples

- `/update-skill-changelog .claude/skills/aid-career 1.6.0 added "New networking-tips.md resource"`
- `/update-skill-changelog skills/private/aid-career-core 1.5.1 fixed "Corrected outdated portfolio URLs in examples"`

## Steps

1. Locate the skill's `changelog.md` (create if missing using "Keep a Changelog" format)
2. Find or create section for the specified version with today's date
3. Add the new entry under the appropriate change type heading
4. Update the `# version:` comment in `SKILL.md` frontmatter to match (commented out to avoid breaking agent systems with strict frontmatter requirements)
5. If the skill has a paired/synced version elsewhere, remind user to update that one too

## Format

Follow [Keep a Changelog](https://keepachangelog.com) conventions:
- Group changes by type (Added, Changed, Deprecated, Removed, Fixed)
- List changes as bullet points
- Include date for version sections (YYYY-MM-DD)
- Keep entries concise but descriptive
- No emojis

## Synced Skills

Some skills may exist in multiple locations (e.g., vault version and standalone version). When updating one, check if there's a paired skill that should also be updated to stay in sync (or if the user mentions it specifically), while maintaining intentional difference between the two.
