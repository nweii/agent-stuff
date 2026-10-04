# notesmd-cli (headless fallback)

Use **notesmd-cli** when `obsidian` is not on PATH (no Obsidian app CLI). It operates on vault files directly. Authoritative syntax: `notesmd-cli --help` and `notesmd-cli <command> --help`.

## Contents

- Vault selection
- Rough mapping from Obsidian-style tasks
- Automation (non-interactive search)
- Not available vs Obsidian app CLI

## Vault selection

- `notesmd-cli list-vaults` (optional `--json`, `--path-only`)
- `notesmd-cli print-default` / `notesmd-cli set-default`
- `-v` / `--vault <name>` on subcommands when no default is set

## Rough mapping

| Intent | notesmd-cli |
|--------|-------------|
| Read note | `notesmd-cli print "<note-or-path>"` |
| Create note | `notesmd-cli create "<path-or-title>" [-c "body"] [-o]` |
| Append body | `notesmd-cli create "<path>" -a -c "more text"` |
| List folder | `notesmd-cli list [path]` |
| Search inside files | `notesmd-cli search-content "<term>" --no-interactive` (optional `--format text` or `json`) |
| Fuzzy pick by title | `notesmd-cli search` (interactive; avoid for agents) |
| Daily note | `notesmd-cli daily` |
| Frontmatter | `notesmd-cli frontmatter "<note>" --print` / `--edit -k key --value val` / `--delete -k key` |
| Move/rename | `notesmd-cli move "<from>" "<to>"` |
| Delete | `notesmd-cli delete "<path-or-title>"` |
| Open in Obsidian/editor | `notesmd-cli open "<note>"` (often unnecessary for agents) |

Note names/paths are tool-specific; quote paths with spaces.

## Automation

For scripted or agent use, prefer **`search-content`** with **`--no-interactive`** (and `--format json` when structured output helps). Do not rely on **`search`** for unattended runs—it targets interactive selection.

## Not available via notesmd-cli

There is no substitute here for Obsidian app features such as **`obsidian` backlinks/orphans/deadends/unresolved**, **tasks** integration, **Bases** queries, **plugin dev** commands, or **`obsidian eval`**. For those, the Obsidian app CLI must be available, or approximate with ripgrep/MCP/manual graph logic.
