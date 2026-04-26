# Changelog

## 1.1.0

### Changed

- Install commands now default to `-a claude-code` scope. Without this flag, `bunx skills add` spreads the skill into 27+ agent directories for tools that aren't used. Claude Code is the only target that matters in this environment.
- Corrected the symlink claim: repo edits do NOT propagate live to installed skills. The install copies SKILL.md into `~/.claude/skills/<name>/`, hardlinked from `~/.agents/skills/<name>/`, but neither side links back to the repo. `bunx skills update -g` is required to pick up edits after a commit — except for internal skills (see below).
- Documented that `bunx skills update -g` does not refresh skills with `metadata.internal: true`. The update silently fails with "Failed to update <name>" and no further detail. Workaround: `bunx skills remove --skill <name> -a claude-code -g -y` followed by `bunx skills add nweii/agent-stuff --skill <name> -a claude-code -g -y`. Since most nweii skills are internal, this is the typical refresh path.
- Added cleanup pattern using repeated `-a <agent>` flags. The comma-separated form (`-a a,b,c`) does not parse — each agent must be its own flag occurrence.

## 1.0.0

- Initial version.
