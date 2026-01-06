---
name: use-brain-vault
description: "Navigate and develop this Obsidian vault—metadata system (categories, types, tags, related), Bases for dynamic dashboards, and periodic notes structure. Use when organizing vault content, configuring Bases, or working with journal notes."
alwaysApply: true
---

# Brain Vault Skills

You have access to a vault of markdown notes. In this vault you will hardly code at all, instead acting as a knowledge worker and humanities expert.

This skill bundle covers the complete vault system: metadata organization, Base configuration, and periodic journaling.

## Quick Navigation

- See **[periodic-notes.md](periodic-notes.md)** for Daily/weekly/quarterly journal structure
- See **[things-integration.md](things-integration.md)** for Things 3 todo management and integration
- See **[obsidian-reference.md](obsidian-reference.md)** for links to official Obsidian documentation (Bases, formatting, syntax, etc.). Consult these when helping with Obsidian configuration or note refactoring.
- See **[cli-tools.md](cli-tools.md)** for extended obsidian-cli reference (additional flags and commands)

## Navigating the Vault

You have access to a trove of context from what is essentially a digital brain vault. For any request, proactively use the tools available to you to gather as much context as possible, following wikilinks and thinking deeply about how the information is connected.

### Vault Folders

Folders provide tidy organization, but the core organizational logic resides within each note's YAML frontmatter. This approach ensures the vault's structure is durable and can be refactored without breaking the system.

- **`01-Days`**: Personal daily, weekly, and quarterly journals (aka periodic notes). See [periodic-notes.md](periodic-notes.md) for details.
- **`02-Evergreen`**: Concept notes.
- **`03-Records`**: Information, web clippings, snippets, topic indexes, working notes, and non-periodic journaling (thinking notes, reflections). Archival and utilitarian notes.
- **`04-Entities`**: Profiles for specific external things: people, places, companies, media (similar to a `References` folder).
- **`98-Spaces`**: Hub notes serving as dynamic dashboards and indexes for categories and types (similar to a `Categories` folder).
- **`99-Admin`**: Obsidian templates and config files.

### Reading Notes Efficiently

Many notes use the `description` frontmatter property to provide an abstract or summary. Read or grep for the description first as a token-efficient way to understand a file without reading its entire contents. This helps determine whether to read a file in full.

Alternatively, use `obsidian-cli frontmatter "Note" --print` to extract just the YAML frontmatter without reading the full note body.

## Vault Principles

- **Minimal Overhead**: Systems require minimal effort to maintain. The goal is to spend time thinking, not organizing.
- **Durability and Longevity**: Organizational methods are simple and robust, designed to last for years without significant refactoring.
- **KISS & DRY**: Use a small, well-defined set of tags, categories, and types. Avoid creating new metadata for one-off cases. Do not feel obligated to add comprehensive metadata to every note.

## Core Metadata System

The vault uses frontmatter properties to organize notes. These properties are optional, but are used to create self-updating dashboards and to surface emergent relationships between notes.

Here are some of the most common ones:

- **`categories`**: Answers "What _is_ this note?" Fundamental nature (e.g., `[[Projects]]`, `[[Clippings]]`), sometimes corresponds to a note template in `99-Admin/Templates`
- **`type`**: Sub-classification or "flavor" of a category (e.g., "Job interviews", "AI Chats"). Use plain text strings. If it needs a hub page, it's a category, not a type.
- **`tags`**: Answers "What does this note _do_?" Functional roles and topical keywords
- **`related`**: Flexible multi-directional connections between notes

### Renaming Published Notes

When renaming notes that have `publish: true`, add the old title as an alias in the format `{Folder path(s)}/{old title}`. This preserves SEO redirects in Obsidian Publish and maintains search indexing for existing URLs.

## obsidian-cli

[obsidian-cli](https://github.com/Yakitrak/obsidian-cli) provides terminal automation for Obsidian vaults. The key advantage over raw file operations is **link-safe refactoring**—moves and renames automatically update all wikilinks and markdown links across the vault.

### Availability

Check if the CLI is available and configured:

```bash
command -v obsidian-cli && obsidian-cli print-default --path-only
```

If not installed, see [cli-tools.md](cli-tools.md) for installation instructions, or fall back to direct file operations (with the caveat that moves/renames won't auto-update links).

Obsidian tracks vaults in `~/Library/Application Support/obsidian/obsidian.json`—avoid hardcoding vault paths.

### Essential commands

```bash
# Move/rename with automatic link updates
obsidian-cli move "old/path/Note" "new/path/Note"

# Search by filename (fuzzy) or content
obsidian-cli search
obsidian-cli search-content "query"

# Create notes
obsidian-cli create "Folder/Note" --content "..." --open

# Token-efficient note preview via frontmatter
# Read the description property to grok a note without reading the full file
obsidian-cli frontmatter "Note" --print

# Edit frontmatter properties
obsidian-cli frontmatter "Note" --edit --key "status" --value "done"

# Delete
obsidian-cli delete "path/Note"
```

### When to use vs direct file edits

- **Use obsidian-cli**: Moving, renaming, or deleting notes (preserves link integrity)
- **Use direct edits**: Modifying note content (Obsidian picks up changes automatically)

If you need additional commands and flags, see [cli-tools.md](cli-tools.md).

## Context-Aware Dashboards via Bases

The system uses reusable Base files to create self-updating dashboards:

- **Periodic dashboards**: Each daily note embeds a "relative base" using `this.file` filter to link related notes and journal entries
- **Category/type hubs**: Hub notes in `98-Spaces` embed master Bases that auto-populate views
- **Entity backlinking**: Author pages, project pages, etc. automatically display all notes that reference them

The pattern works because `categories` serves as the central link between templates → notes → hubs → dashboards.

## Wikilinks for AI Agents

Obsidian uses **wikilink** syntax for internal links. AI agents working with this vault must understand how to resolve these links to actual file paths.

### MCP tools

If you have access to any vault-specific MCP tools for browsing the file structure, searching content semantically, following backlinks, and working with the bases system, you should use them. These will enhance your ability to proactively gather your own context for the user and their queries.

### Basic Wikilink Syntax

- `[[Note]]`: Link to a note (Find file named `Note.md` in vault)
- `[[Folder/Note]]`: Link with path (Find `Folder/Note.md` relative to vault root)
- `[[Note\|Display Text]]`: Aliased link (Same resolution; text after `\|` is display only)
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

### Resolving Wikilinks as an AI Agent

If you have access to **vault-aware tools** (MCP tools, graph traversal, or search tools that understand Obsidian structure), think about how best to use them to resolve wikilinks. If you can, prefer tools that can resolve wikilinks for:

- Following wikilinks to their target files
- Exploring backlinks/forwardlinks between notes
- Querying Bases or executing their filters
- Traversing the vault's link graph

Otherwise, fall back to file operations like:

- Filename search (`find_by_name`, `grep_search`, etc.) to locate linked files
- Reading `.base` files to understand their queries, then manually executing similar searches

### Practical Example: Embedded Bases

When you see `![[Period entries.base#Timespan]]` in a note:

1. Find `Period entries.base` (located in `98-Spaces/Engines/Relative Bases/`)
2. The `#Timespan` references a specific view within that Base file
3. The Base uses `this.file` to query relative to the embedding note's context

If you have vault-aware tools that can query Bases directly, use those. Otherwise, read the `.base` file to understand its filters and manually search for matching notes.

## When to Use This Skill

- Organizing or restructuring vault content
- Designing or troubleshooting Base queries
- Working with periodic notes (daily/weekly/quarterly journals)
- Understanding Obsidian features, syntax, or configuration
- Asking about metadata structure or vault best practices
