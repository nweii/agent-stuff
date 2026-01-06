# Things 3 Integration

Manage todos and project tasks directly from the vault using the `things` CLI. This allows you to bridge the gap between thinking (Obsidian) and doing (Things 3).

## Core Concepts

- **Thinking vs. Doing**: Use Obsidian for drafting ideas, meeting notes, and project planning. Use Things 3 for actionable todos with specific dates and deadlines.
- **CLI-First**: Use the `things` command to add tasks without leaving the chat or your notes.
- **Contextual Tasks**: When summarizing a meeting or a project note, proactively identify "inklings" or action items and offer to send them to Things.

## Auth Token

The CLI requires an auth token for update operations.
- **Environment**: You should set `THINGS_AUTH_TOKEN` in your shell profile (e.g., `~/.zshrc`) to persist it.

## Common Workflows

### 1. Adding Tasks from Daily Notes
When a task is mentioned in a daily note or during a session, add it to Things:
```bash
# Add to Today with notes
things add "Follow up with [Name]" --notes "Context: [2026-01-06-Tue](obsidian://open?vault=Brain&file=01-Days%2F2026-01-06-Tue)" --when today
```

### 2. Project Task Extraction
When working on a project note (`categories: [[Projects]]`), extract action items:
```bash
# Add to a specific project list in Things
things add "Draft initial spec" --list "Product Launch" --notes "Reference: [Project Alpha](obsidian://open?vault=Brain&file=02-Evergreen%2FProject%20Alpha)"
```

### 3. Reviewing Tasks
Use read-only commands to provide context during planning:
```bash
# See what's on the plate for today
things today

# Get a sense of existing Areas and Projects
things areas
things projects

# See what's inside a specific Area or Project
things show "Area Name"
things tasks --project "Project Name"

# Search for existing tasks to avoid duplicates
things search "query"
```

## Integration Principles

- **Discovery First**: Before adding new projects or areas, use `things areas` and `things projects` to see if a suitable container already exists. This keeps your Things structure tidy.
- **Obsidian URIs in Notes**: When adding tasks from the vault, include a clickable Markdown link with an Obsidian URI in the Things `notes` field.
  - Format: `[Note Name](obsidian://open?vault=Brain&file=URL_ENCODED_PATH)`
  - This allows you to jump directly back to the original context in Obsidian from within Things.
- **Dry Run First**: If a task description is complex, use `things --dry-run add "..."` to show the user what will be sent before executing.
- **Cleanup**: If a task is completed in Things, you don't necessarily need to update the Obsidian note, as Things is the source of truth for "doing".
