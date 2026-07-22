# Plugin changelog conventions

Reference for changelog management in plugins. Skills use `metadata.version` in
their frontmatter, but do not keep their own changelog files.

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
        └── SKILL.md
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

When updating a skill in a plugin:
1. Update the plugin's root `CHANGELOG.md` with the plugin version when releasing.
2. Bump `version` in `plugin.json` if releasing.
