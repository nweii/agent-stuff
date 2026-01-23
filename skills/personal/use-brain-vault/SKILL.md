---
name: use-brain-vault
description: "Navigate this Obsidian vault: metadata (categories, types, tags), Bases for dashboards, and periodic journaling. Use for organizing content, configuring Bases, or journal notes."
alwaysApply: true
metadata:
  author: nweii
  version: "1.0.0"
---

# Brain Vault Skills

You have access to a vault of markdown notes. In this vault you will hardly code at all, instead acting as a knowledge worker and humanities expert.

This skill bundle covers the complete vault system: metadata organization, Base configuration, periodic journaling, and Obsidian documentation.

## Vault Principles

- **Minimal Overhead**: Systems require minimal effort to maintain. The goal is to spend time thinking, not organizing.
- **Durability and Longevity**: Organizational methods are simple and robust, designed to last for years without significant refactoring.
- **KISS & DRY**: Use a small, well-defined set of tags, categories, and types. Avoid creating new metadata for one-off cases. Do not feel obligated to add comprehensive metadata to every note.

## Navigating the Vault

You have access to a trove of context from what is essentially a digital brain vault. For any request, proactively use the tools available to you to gather as much context as possible, following wikilinks and thinking deeply about how the information is connected.

### Vault Folders

Folders provide tidy organization, but the core organizational logic resides within each note's YAML frontmatter. This approach ensures the vault's structure is durable and can be refactored without breaking the system.

- `**01-Days**`: Personal daily, weekly, and quarterly journals (aka periodic notes). See [periodic-notes.md](periodic-notes.md) for details.
- `**02-Evergreen**`: Concept notes.
- `**03-Records**`: Information, web clippings, snippets, topic indexes, working notes, and non-periodic journaling (thinking notes, reflections). Archival and utilitarian notes.
- `**04-Entities**`: Profiles for specific external things: people, places, companies, media (similar to a `References` folder).
- `**98-Spaces**`: Hub notes serving as dynamic dashboards and indexes for categories and types (similar to a `Categories` folder).
- `**99-Admin**`: Obsidian templates and config files.

### Reading Notes Efficiently

Many notes use the `description` frontmatter property to provide an abstract or summary. Read or grep for the description first as a token-efficient way to understand a file without reading its entire contents. This helps determine whether to read a file in full.

Alternatively, use `obsidian-cli frontmatter "Note" --print` to extract just the YAML frontmatter without reading the full note body.

## Wikilink Syntax

Obsidian uses **wikilink** syntax for internal links. Understanding this syntax is essential for navigating the vault.

### Basic Syntax

- `[[Note]]`: Link to a note (Find file named `Note.md` in vault)
- `[[Folder/Note]]`: Link with path (Find `Folder/Note.md` relative to vault root)
- `[[Note|Display Text]]`: Aliased link (Same resolution; text after `|` is display only)
- `[[Note#Heading]]`: Link to heading (Find `Note.md`, locate `## Heading` within it)
- `[[Note#^block-id]]`: Link to block (Find `Note.md`, locate line ending with `^block-id`)

### Embedded Wikilinks (Transclusion)

Adding `!` before a wikilink **embeds** the content instead of linking to it:

| Syntax                    | What It Embeds                         |
| ------------------------- | -------------------------------------- |
| `![[Note]]`               | Entire note content                    |
| `![[Note#Heading]]`       | Content under that heading             |
| `![[Note#^block-id]]`     | Specific block (paragraph, list, etc.) |
| `![[Image.png]]`          | Image file                             |
| `![[Base.base]]`          | All views from a Base file             |
| `![[Base.base#ViewName]]` | Specific view from a Base              |

### File Resolution Rules

When resolving wikilinks to file paths:

1. **Shortest unique match**: Obsidian finds the shortest path that uniquely identifies the file
2. **Case-insensitive on macOS**: `[[note]]` matches `Note.md`
3. **Extension optional for `.md`**: `[[Note]]` and `[[Note.md]]` are equivalent
4. **Other extensions required**: `[[Image.png]]`, `[[Data.base]]`
5. **Search vault-wide**: If no path given, search entire vault for matching filename

## Core Metadata System

The vault uses frontmatter properties to organize notes. These properties are optional, but are used to create self-updating dashboards and to surface emergent relationships between notes.

Here are some of the most common ones:

- `**categories**`: Answers "What _is_ this note?" Fundamental nature (e.g., `[[Projects]]`, `[[Clippings]]`), sometimes corresponds to a note template in `99-Admin/Templates`
- `**type**`: Sub-classification or "flavor" of a category (e.g., "Job interviews", "AI Chats", "Google form"). Use plain text strings. If it needs a hub page, it's a category, not a type.
- `**tags**`: Answers "What does this note _do_?" Functional roles and topical keywords
- `**related**`: Flexible multi-directional connections between notes

### Category semantics and valid combinations

Categories fall into three semantic types:

| Type           | Answers                       | Examples                                            |
| -------------- | ----------------------------- | --------------------------------------------------- |
| **Provenance** | "Where did this come from?"   | `[[Clippings]]`, `[[Web]]`, `[[Messages]]`          |
| **Function**   | "What am I using this for?"   | `[[Applications]]`, `[[Projects]]`, `[[Thinking]]`  |
| **Nature**     | "What kind of thing is this?" | `[[Snippets]]`, `[[Histories]]`, `[[Case studies]]` |

**Valid**: Combining categories from _different_ semantic types. Example: `[[Clippings]], [[Web]], [[Applications]]` (provenance + provenance + function) for a web-clipped application form.

**Anti-pattern**: Combining categories from the _same_ semantic type, which creates ambiguity about the note's identity. Example: `[[Histories]], [[Projects]]` — both are competing to define what the note fundamentally _is_.

When you need cross-category visibility (e.g., showing project-related histories in a Projects dashboard), use `type:` instead of adding another category. Example: a history note uses `categories: [[Histories]]` with `type: Projects` to appear in project-filtered views without claiming `[[Projects]]` as a category.

### Hub notes vs. content

Hub notes (with `#index/trackers` tag) organize and track work but aren't themselves the work product. This affects tagging:

- **Hub notes**: Get minimal, functional tags only (`index`, `domain`, `trackers`)
- **Content notes**: Get topical tags describing what they're about (`log/work`, `career-work/2025`, topic tags)

Examples:

- Project hub: `tags: [index/trackers]`
- Work log about that project: `tags: [thinking, log/work, TALtech]`
- History of that project: `tags: [log/archive, retrospectives, TALtech]`

Don't tag hubs with topics—tag the content that the hub links to.

### Category-specific conventions

Each major category has its own conventions documented in its hub note:

- See `98-Spaces/Projects.md` for project/domain/case study/history patterns
- See `98-Spaces/Applications.md` for application tracking patterns

### Renaming Published Notes

When renaming notes that have `publish: true`, add the old title as an alias in the format `{Folder path(s)}/{old title}`. This preserves SEO redirects in Obsidian Publish and maintains search indexing for existing URLs.

## Vault Tools

You have two tool systems for vault operations: **obsidian-cli** (terminal commands) and **MCP Brain tools** (structured API). Use both strategically based on the operation type.

### When to use which tool

| Operation             | Preferred Tool | Why                                                   |
| --------------------- | -------------- | ----------------------------------------------------- |
| Move/rename notes     | obsidian-cli   | Guarantees wikilink updates across vault              |
| Delete notes          | obsidian-cli   | Link-safe deletion                                    |
| Read frontmatter only | obsidian-cli   | `--print` returns just YAML, token-efficient          |
| Print note content    | obsidian-cli   | Raw stdout, no wrapper overhead                       |
| Graph traversal       | MCP Brain      | Backlinks, neighbors, path-finding, search-traverse   |
| Advanced search       | MCP Brain      | Operators, regex, TF-IDF ranking, fragments           |
| Bases queries         | MCP Brain      | Query, export, analyze `.base` files                  |
| Edit by section       | MCP Brain      | Window/patch editing with fuzzy matching              |
| Content edits         | Either         | Direct file edits work; MCP has structured operations |

### obsidian-cli (basic operations)

[obsidian-cli](https://github.com/Yakitrak/obsidian-cli) provides terminal automation. Its key advantage is **link-safe refactoring**—moves and renames automatically update all wikilinks across the vault.

```bash
# Check availability
command -v obsidian-cli && obsidian-cli print-default --path-only

# Link-safe move/rename (updates all references)
obsidian-cli move "old/path/Note" "new/path/Note"

# Token-efficient reads
obsidian-cli frontmatter "Note" --print   # Just YAML
obsidian-cli print "Note"                  # Raw content

# Create and delete
obsidian-cli create "Folder/Note" --content "..."
obsidian-cli delete "path/Note"

# Frontmatter edits
obsidian-cli frontmatter "Note" --edit --key "status" --value "done"
```

Note: `search` and `search-content` are interactive (fuzzy finder), so they're not useful for AI automation—use MCP search instead.

For additional flags and commands, see [cli-tools.md](cli-tools.md). If not installed, see that file for setup instructions.

### MCP Brain tools (advanced operations)

The MCP plugin (`mcp_Brain_*`) provides richer operations for exploration and complex edits:

- **vault**: list, read, create, search (with operators, regex, ranked results), fragments, split, combine
- **graph**: traverse, neighbors, path-finding, statistics, backlinks, forwardlinks, search-traverse, tag-traverse
- **edit**: window editing with fuzzy matching, append, patch by heading/block/frontmatter
- **bases**: list, read, query, view, export (CSV/JSON/Markdown)
- **view**: file view, window view (centered on line), active note
- **workflow**: contextual suggestions for next actions

Use MCP tools when you need to explore connections, run semantic searches, query Bases, or make structured edits.

### Resolving wikilinks with tools

When you encounter a `[[wikilink]]` and need to follow it:

1. **MCP graph tools** can resolve links directly via backlinks/forwardlinks operations
2. **MCP search** with `file:` operator finds notes by name
3. **obsidian-cli print** outputs content if you know the path
4. **Fall back to file search** (`grep`, `find_by_name`) if tools unavailable

For Bases (`![[Base.base#View]]`), use MCP `bases` action to query directly, or read the `.base` file and manually execute similar searches.

## Context-Aware Dashboards via Bases

The system uses reusable Base files to create self-updating dashboards:

- **Periodic dashboards**: Each daily note embeds a "relative base" using `this.file` filter to link related notes and journal entries
- **Category/type hubs**: Hub notes in `98-Spaces` embed master Bases that auto-populate views by type
- **Entity backlinking**: Author pages, project pages, etc. automatically display all notes that reference them

The pattern works because `categories` serves as the central link between templates → notes → hubs → dashboards.

### Practical Example: Embedded Bases

When you see `![[Period entries.base#Timespan]]` in a note:

1. Find `Period entries.base` (located in `98-Spaces/Engines/Relative Bases/`)
2. The `#Timespan` references a specific view within that Base file
3. The Base uses `this.file` to query relative to the embedding note's context

Use MCP `bases` tools to query directly, or read the `.base` file to understand its filters.

## When to Use This Skill

- Organizing or restructuring vault content
- Designing or troubleshooting Base queries
- Working with periodic notes (daily/weekly/quarterly journals)
- Understanding Obsidian features, syntax, or configuration
- Asking about metadata structure or vault best practices

## Further Reading

- **[periodic-notes.md](periodic-notes.md)** — Daily/weekly/quarterly journal structure
- **[things-integration.md](things-integration.md)** — Things 3 todo management and integration
- **[obsidian-reference.md](obsidian-reference.md)** — Links to official Obsidian documentation (Bases, formatting, syntax, etc.)
- **[cli-tools.md](cli-tools.md)** — Extended obsidian-cli reference (additional flags and commands)
