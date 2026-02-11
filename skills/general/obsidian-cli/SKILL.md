---
name: obsidian-cli
description: Control Obsidian from the terminal via the obsidian CLI. Use for vault automation, opening/creating notes, searching, daily notes, tasks, tags, and plugin development.
metadata:
  author: nweii
  version: "1.0.0"
---

# Obsidian CLI

Run `obsidian <command>` to control Obsidian from the terminal. The app must be running for most commands; the first command will launch Obsidian if not open.

## Targeting vaults and files

- **Vault**: Add `vault=<name>` to target a specific vault. Default: uses cwd if it's a vault folder, else the active vault.
- **File**: Use `file=<name>` (wikilink resolution, extension optional) or `path=<path>` (exact path from vault root).
- **TUI**: Run `obsidian` with no args for interactive mode; omit the `obsidian` prefix inside.

## Parameters and flags

- **Parameters**: `param=value`. Quote values with spaces: `content="Hello world"`.
- **Flags**: Boolean, no value: `silent`, `overwrite`, `newtab`.
- **Multiline content**: Use `\n` for newlines, `\t` for tabs in `content=`.

## Common commands

### Notes and content

```bash
obsidian create name="Note" content="Hello world"
obsidian create name="Note" template=Travel  # from Templates folder
obsidian create name="Note" content="# Title\n\nBody" overwrite silent
obsidian read [file=Note] [path=folder/note.md]
obsidian open [file=Note] [newtab]
obsidian append [file=Note] content="- [ ] Task"
obsidian prepend [file=Note] content="# Header\n"
obsidian delete [file=Note] [permanent]
obsidian move [file=Note] to=folder/newpath.md
```

### Daily notes

Requires Daily notes plugin. Use `daily:append` / `daily:prepend` for content.

```bash
obsidian daily [paneType=tab|split|window] [silent]
obsidian daily:append content="- [ ] Buy groceries" [inline] [silent]
obsidian daily:prepend content="- [ ] Morning routine" [inline]
obsidian daily:read
```

### Search and navigation

```bash
obsidian search query="meeting notes" [path=folder] [limit=10] [format=text|json]
obsidian search:open query="tag:project"
obsidian files [folder=path] [ext=md] [total]
obsidian recents [total]
obsidian random [folder=path] [newtab] [silent]
```

### Tasks and tags

```bash
obsidian tasks [daily] [file=Note] [todo] [done] [status="x"] [total] [verbose]
obsidian task ref=path:line [toggle] [done] [todo] [daily]
obsidian tags [all] [file=Note] [total] [counts] [sort=count]
obsidian tag name=project [total] [verbose]
```

### Links and structure

```bash
obsidian links [file=Note] [total]
obsidian backlinks [file=Note] [counts] [total]
obsidian outline [file=Note] [format=tree|md]
obsidian orphans [total] [all]
obsidian deadends [total] [all]
obsidian unresolved [total] [counts] [verbose]
```

### Properties and frontmatter

```bash
obsidian properties [all] [file=Note] [total] [counts] [format=yaml|tsv]
obsidian property:read name=status [file=Note]
obsidian property:set name=status value=done [file=Note]
obsidian property:remove name=status [file=Note]
```

### Bases (Bases plugin)

```bash
obsidian bases
obsidian base:views [file=base.base]
obsidian base:query [file=base.base] [view=name] [format=json|csv|tsv|md|paths]
obsidian base:create name="Item" content="..." [silent] [newtab]
```

### Plugins and themes

```bash
obsidian plugins [filter=core|community] [versions]
obsidian plugin:install id=plugin-id [enable]
obsidian plugin:enable id=plugin-id
obsidian plugin:disable id=plugin-id
obsidian plugin:reload id=plugin-id  # for development
obsidian themes [versions]
obsidian theme:install name=Theme [enable]
obsidian theme:set name=Theme
```

### Publish

```bash
obsidian publish:status [total] [new] [changed] [deleted]
obsidian publish:add [file=Note] [changed]
obsidian publish:remove [file=Note]
obsidian publish:list [total]
```

### History and diff

```bash
obsidian history [file=Note]
obsidian history:read [file=Note] version=2
obsidian history:restore [file=Note] version=2
obsidian diff [file=Note] [from=1] [to=3] [filter=local|sync]
```

### Vault and workspace

```bash
obsidian vault [info=name|path|files|folders|size]
obsidian vaults [total] [verbose]
obsidian workspace:save [name=layout]
obsidian workspace:load name=layout
obsidian reload
obsidian restart
```

### Execute Obsidian commands

```bash
obsidian commands [filter=prefix]
obsidian command id=app:open-settings
obsidian hotkey id=app:open-settings [verbose]
```

## Developer commands

```bash
obsidian dev:screenshot path=screenshot.png
obsidian dev:dom selector=".cm-editor" [text] [attr=class]
obsidian dev:css selector=".cm-editor" [prop=color]
obsidian dev:console [clear] [limit=10] [level=log|warn|error]
obsidian dev:errors [clear]
obsidian devtools
obsidian eval code="app.vault.getFiles().length"
```

## Quick reference

| Task                        | Command                                      |
| --------------------------- | -------------------------------------------- |
| List commands               | `obsidian help`                              |
| Open daily note             | `obsidian daily`                             |
| Append to daily             | `obsidian daily:append content="- [ ] Task"` |
| Search vault                | `obsidian search query="text"`               |
| Read active/ specified file | `obsidian read` or `obsidian read file=Note` |
| Create from template        | `obsidian create name="Title" template=Name` |
| List tags with counts       | `obsidian tags counts`                       |
| List tasks from daily       | `obsidian tasks daily`                       |
| Diff file versions          | `obsidian diff file=Note from=1 to=3`        |

## Help

Run `obsidian help` (not `--help`) for the full command list.

## References

For the most up-to-date CLI documentation: [Obsidian CLI (Context7)](https://context7.com/websites/help_obsidian_md/llms.txt?topic=cli&tokens=10000)
