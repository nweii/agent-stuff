# Skill & Plugin Changelog Conventions

Reference for changelog management in skills and plugins.

## Skill Changelog Mode

When updating a skill's changelog, additional steps apply.

### Skill-Specific Steps

1. Locate the skill's `changelog.md` in the skill folder
2. Find or create section for the specified version
3. Add the new entry under the appropriate change type
4. Update the `metadata.version` field in `SKILL.md` frontmatter to match

### SKILL.md Metadata Format

Use YAML block format under a `metadata:` key:

```yaml
metadata:
  author: nweii
  version: "1.2.0"
```

### Synced Skills

Some skills may exist in multiple locations (e.g., vault version and standalone version). When updating one, check if there's a paired skill that should also be updated to stay in sync.

---

## Plugin Changelog Mode

When the skill is part of a Claude Code plugin, follow plugin conventions.

### Plugin Structure

Plugins bundle skills in a `skills/` directory alongside `plugin.json`:

```
my-plugin/
├── plugin.json
├── CHANGELOG.md       # Plugin-level changelog
└── skills/
    └── my-skill/
        ├── SKILL.md
        └── changelog.md  # Skill-level changelog (optional)
```

### Plugin Changelog Conventions

For **plugin-level** changelogs (root `CHANGELOG.md`):

- Use version headers like `### v1.2.0` (matching `plugin.json` version)
- Use short bullet points with optional context tags: `[SDK]`, `[skill-name]`
- Group by features, fixes, improvements
- Keep entries concise for rapid iteration

Example:
```markdown
### v1.2.0 - 2025-01-24

- [my-skill] Added new PDF extraction feature
- Fixed content layout shift in command list
- Added automatic skill hot-reload support
```

### Plugin vs Skill Changelogs

- **Plugin changelog** (root): Aggregate changes across all bundled skills, use plugin version
- **Skill changelog** (in skill folder): Detailed changes for that skill, use skill's own version

When updating a skill in a plugin:
1. Update the skill's `changelog.md` with skill version
2. Update the plugin's root `CHANGELOG.md` with plugin version
3. Bump `version` in `plugin.json` if releasing
