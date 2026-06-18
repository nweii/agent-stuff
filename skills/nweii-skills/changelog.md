# Changelog

## 1.10.0

### Added

- "Skill content craft" section condensing the agentskills.io guides: add-what-the-agent-lacks, defaults-not-menus, match-specificity-to-fragility, progressive disclosure (when-to-load triggers), and gotchas sections; a bundled-scripts subsection (non-interactive, `--help`, structured stdout/stderr, retry-safe, inline deps); and on-demand reference links to the three agentskills.io pages.
- Description guidance expanded with imperative/user-intent phrasing, being pushy about implicit triggers, the "agents skip trivial tasks" nuance, and a pointer to the description-optimization eval loop.

## 1.9.0

### Added

- "Keep procedure skills operational" guidance in Writing conventions: skills that *do* something get written as ordered steps with gotchas inline, deferring what the agent can read elsewhere; reference skills that *explain* can carry more exposition.
- "Write the description for routing, not summary" guidance in Frontmatter conventions: descriptions spend their words on concrete triggers over content summary; ~200–300 chars is a ceiling, not a target, and shouldn't be undercut at the expense of routing-relevant triggers or distinctions.

## 1.8.0

### Added

- "Writing conventions" section: after the substance is settled, make a separate succinctness pass over the draft — succinctness over raw brevity, never compressing prose into something terse or cryptic at the expense of human readability.

## 1.7.1

### Changed

- Agent flags take space-separated values on a single `-a` (`-a claude-code zed`); install commands updated from the repeated-flag form. Comma-separated still does not parse.
- Documented `bunx skills use <owner/repo> --skill <name>` for trying a skill without installing.

## 1.7.0

### Added

- Attribution conventions: `metadata.source` for a single canonical upstream pointer (slug or URL) when a skill derives from one specific artifact; `metadata.credit` for prose attribution when provenance doesn't reduce to a pointer (multi-source adaptations, inspiration, or a person as author). Both can coexist; wholesale outside authorship goes in `author` with elaboration in `credit`.

## 1.6.0

### Changed

- Reversed 1.5.0's architecture correction: on Nathan's MacBook, `~/.claude/skills` IS a directory-level symlink to `~/.agents/skills` (verified via `readlink`). Per-skill symlinks never appear under this layout — every `~/.claude/skills/<name>` is the canonical copy seen through the parent link and lists as a real directory. Misdiagnosing this as copy-mode drift and "repairing" it deletes the real skill, so the repair section now gates on `readlink ~/.claude/skills` first.
- Consolidated the source-of-truth rule (edit in the repo, install dir is downstream) from three statements into one strong statement in its own section plus one reminder in the migration steps.

## 1.5.0

### Changed

- Install commands now target two agents (`-a claude-code -a zed`) so bunx uses symlink mode. A single-agent install (`-a claude-code` alone) falls back to copy mode, writing a real folder into `~/.claude/skills/` and skipping the canonical `~/.agents/skills/`. The second agent maps to `~/.agents/skills`, so the real copy lands there and Claude Code gets a symlink, with no stray agent dir.
- Private skills install from the `nweii/agent-stuff-private` slug, the same form as public skills, rather than the local clone path or an SSH URL. Cloning a private repo works through an authenticated `gh`. This keeps the recorded source portable across machines.
- Corrected the architecture description: `~/.claude/skills` is not a parent-level symlink to `~/.agents/skills`. bunx keeps one real copy per skill in `~/.agents/skills/<name>/` and symlinks each agent's skills dir to it per-skill.
- Clarified update behavior: `bunx skills update` cannot refresh private-repo skills (its tree check is unauthenticated and can't see a private repo) or `internal: true` skills (filtered out of the update handoff). Refresh both by re-running `bunx skills add`, which installs internal skills because naming one with `--skill` opts it in.
- Reframed "repairing a symlinked install" as repairing a copied (non-symlink) install — a real directory under `~/.claude/skills/<name>` is the drift to fix, by reinstalling with the two-agent command.

## 1.1.0

### Changed

- Install commands now default to `-a claude-code` scope. Without this flag, `bunx skills add` spreads the skill into 27+ agent directories for tools that aren't used. Claude Code is the only target that matters in this environment.
- Corrected the symlink claim: repo edits do NOT propagate live to installed skills. The install copies SKILL.md into `~/.claude/skills/<name>/`, hardlinked from `~/.agents/skills/<name>/`, but neither side links back to the repo. `bunx skills update -g` is required to pick up edits after a commit — except for internal skills (see below).
- Documented that `bunx skills update -g` does not refresh skills with `metadata.internal: true`. The update silently fails with "Failed to update <name>" and no further detail. Workaround: `bunx skills remove --skill <name> -a claude-code -g -y` followed by `bunx skills add nweii/agent-stuff --skill <name> -a claude-code -g -y`. Since most nweii skills are internal, this is the typical refresh path.
- Added cleanup pattern using repeated `-a <agent>` flags. The comma-separated form (`-a a,b,c`) does not parse — each agent must be its own flag occurrence.

## 1.0.0

- Initial version.
