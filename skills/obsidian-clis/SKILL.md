---
name: obsidian-clis
description: Documents terminal control of Obsidian notes using the Obsidian app CLI (`obsidian`) when it is on PATH, and notesmd-cli when the app CLI is unavailable (headless or synced vault only). Covers note CRUD, search, vault structure (orphans, backlinks, unresolved links), tasks, properties, Bases, and plugin development when the app CLI is available. Use when the user mentions Obsidian CLI, obsidian-clis, notesmd-cli, terminal vault operations, or shell automation of Obsidian notes.
metadata:
  author: nweii
  version: "1.5.1"
  source: kepano/obsidian-cli
---

# Obsidian CLIs

**CLIs** here means two terminal interfaces: the **Obsidian app CLI** (`obsidian`, primary) and **notesmd-cli** (filesystem fallback when `obsidian` is not available). There is no separate invocation mode—pick the binary that exists in the environment.

## Which binary to use

1. If `obsidian` is on PATH, use it for all workflows below (richer surface: links, Bases, tasks, plugin dev).
2. If `obsidian` is missing but `notesmd-cli` is on PATH, follow [notesmd-fallback.md](notesmd-fallback.md) for headless vault operations.
3. If neither is available, say so and fall back to direct file edits, MCP, or other vault tools the user provides.

## CLI availability

!`which obsidian`

!`which notesmd-cli`

---

## Obsidian app CLI

Run `obsidian <command>` to control a running Obsidian instance from the terminal. The app must be running for most commands; the first command will launch Obsidian if not open.

Run `obsidian help` or `obsidian help <command>` for the canonical, always-up-to-date command reference. This skill documents common patterns and non-obvious behaviors.

### Targeting vaults and files

- **Vault**: `vault=<name>` as first parameter. Default: cwd if it's a vault folder, else the active vault.
- **File**: `file=<name>` resolves like a wikilink (name only, no path or extension needed). `path=<path>` for exact path from vault root.
- **TUI**: Run `obsidian` with no args for interactive mode; omit the `obsidian` prefix inside.

### Parameters and flags

- **Parameters**: `param=value`. Quote values with spaces: `content="Hello world"`.
- **Flags**: Boolean, no value: `silent`, `overwrite`, `newtab`.
- **Multiline content**: Use `\n` for newlines, `\t` for tabs in `content=`.

### Search, links, and structure

```bash
obsidian search query="text" [path=folder] [limit=n] [format=text|json] [total] [case]
obsidian search:context query="text" [path=folder] [limit=n]  # includes surrounding context
obsidian links [file=Note] [total]
obsidian backlinks [file=Note] [counts] [total]
obsidian outline [file=Note] [format=tree|md]
obsidian orphans [total] [active]       # notes with no links to or from them
obsidian deadends [total] [active]      # notes with no outgoing links
obsidian unresolved [total] [counts] [verbose]  # broken wikilinks
obsidian tags [active] [file=Note] [total] [counts] [sort=count]
obsidian tag name=project [total] [verbose]
```

### Common patterns

#### Notes and content

To peek at a note without reading its full content, use `property:read` or `properties file=Note`.

```bash
obsidian read file="Note" # Use this to read the content of a wikilink
obsidian create name="Note" content="# Title\n\nBody" [template=Name] [overwrite] [silent]
obsidian append file="Note" content="- [ ] Task"
obsidian prepend file="Note" content="# Header\n"
obsidian move file="Note" to=folder/newpath.md
obsidian rename file="Note" name="New file name"
obsidian delete file="Note"
```

#### Daily notes (Daily notes plugin)

```bash
obsidian daily:read
obsidian daily [paneType=tab|split|window] [open]
obsidian daily:append content="- [ ] Buy groceries" [inline] [open]
obsidian daily:prepend content="- [ ] Morning routine" [inline]  # goes after frontmatter
obsidian daily:path  # returns expected path even if file doesn't exist yet
```

#### Tasks

```bash
obsidian tasks [daily] [file=Note] [todo] [done] [status="x"] [total] [verbose]
obsidian task ref=path:line [toggle] [done] [todo] [daily]
```

#### Properties and frontmatter

```bash
obsidian properties [active] [file=Note] [total] [counts] [format=yaml|json|tsv]
obsidian property:read name=status [file=Note]
obsidian property:set name=status value=done [file=Note]
obsidian property:remove name=status [file=Note]
```

#### Bases (Bases plugin)

```bash
obsidian bases
obsidian base:views [file=base.base]
obsidian base:query [file=base.base] [view=name] [format=json|csv|tsv|md|paths]
obsidian base:create name="Item" content="..." [open] [newtab]
```

### Plugin development

#### Develop/test cycle

After making code changes to a plugin or theme, follow this workflow:

1. **Reload** the plugin to pick up changes:

   ```bash
   obsidian plugin:reload id=my-plugin
   ```

2. **Check for errors** — if errors appear, fix and repeat from step 1:

   ```bash
   obsidian dev:errors
   ```

3. **Verify visually** with a screenshot or DOM inspection:

   ```bash
   obsidian dev:screenshot path=screenshot.png
   obsidian dev:dom selector=".workspace-leaf" text
   ```

4. **Check console output** for warnings or unexpected logs:

   ```bash
   obsidian dev:console level=error
   ```

#### Additional developer commands

Run JavaScript in the app context:

```bash
obsidian eval code="app.vault.getFiles().length"
```

Inspect CSS values:

```bash
obsidian dev:css selector=".workspace-leaf" prop=background-color
```

Toggle mobile emulation:

```bash
obsidian dev:mobile on
```

### Quick reference (Obsidian app CLI)

| Task | Command |
|------|---------|
| List commands | `obsidian help` |
| Open daily note | `obsidian daily` |
| Append to daily | `obsidian daily:append content="- [ ] Task"` |
| Search vault | `obsidian search query="text"` |
| Read active/specified file | `obsidian read` or `obsidian read file=Note` |
| Create from template | `obsidian create name="Title" template=Name` |
| List tags with counts | `obsidian tags counts` |
| List tasks from daily | `obsidian tasks daily` |
| Find broken wikilinks | `obsidian unresolved counts` |
| Find orphan notes | `obsidian orphans` |

For **notesmd-cli**, see [notesmd-fallback.md](notesmd-fallback.md).

### References

- `obsidian help` — full command list (always up to date)
- `obsidian help <command>` — help for a specific command
- [Obsidian CLI docs (Obsidian)](https://raw.githubusercontent.com/obsidianmd/obsidian-help/refs/heads/master/en/Extending%20Obsidian/Obsidian%20CLI.md)
