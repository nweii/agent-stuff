# agents

A couple of subagent definitions I use. These are not installed by `bunx skills` — they're plain `*.md` files you copy into your own agents directory.

Claude Code reads subagents from `~/.claude/agents/`. My agent-agnostic convention is to keep them in `~/.agents/agents/` and symlink `~/.claude/agents` to it (same layout as `~/.agents/skills`).

- **vault-reader** — read-only Obsidian vault exploration. Navigates the link graph, triages by frontmatter, and synthesizes context across notes. Reads each vault's `AGENTS.md`/`CLAUDE.md` for its conventions.
- **vault-writer** — creates and edits notes following each vault's established conventions, via the `obsidian` CLI with shell-tool fallbacks.
