---
name: save-term
description: "Save a term, phrase, or coined concept as a Term note in the Brain vault under 02-Evergreen/Terms/. Two modes: capturing a nice term encountered in reading (with source quote) or recording one coined during conversation (with brief gloss). Triggers: '/save-term <term>', 'save this term', 'add this to my terms'."
argument-hint: "[term or phrase]"
disable-model-invocation: true
metadata:
  author: nweii
  version: "1.0.0"
  internal: true
---

# Save term

Save a term or phrase as a Term note in `02-Evergreen/Terms/`. Two modes:

1. **Encountered** — a term lifted from a book, article, conversation, or other external source. Body anchors on a source citation + quote.
2. **Coined** — a term that emerged during conversation (often a compact replacement for a wordy phrase, or a fresh concept the user wants to lock in). Body is a brief gloss with a usage example or context.

This skill is **not** for general note-taking. It writes one specific shape of note — short, atomic, and aligned with the existing vault Term convention. For broader capture, use `save-napkin-note`.

## Defer to AGENTS.md / CLAUDE.md

Vault layout, metadata semantics, and tool-choice rules live in the vault's `AGENTS.md` and `CLAUDE.md`. This skill only adds the procedure for writing one note type. When unsure about a field's meaning or which tool to use for vault writes, read those first.

## Arguments

- **`$ARGUMENTS`**: the term or phrase to save. If omitted, ask. If the term contains punctuation tricky for filenames (`/`, `:`, etc.), confirm a filesystem-safe variant before writing.

## Process

### 1. Determine mode

Ask if not obvious from context:

- **Encountered** — user is referencing something external (a book, article, person they're quoting, web clipping). Need a source.
- **Coined** — emerged in this conversation, no external source. Likely came out of a phrase-revision pass or a fresh framing.

### 2. Gather what the body needs

For **encountered** terms:

- **Source citation** — wikilink to an existing vault note if possible (`[[Source note title]]`), otherwise a markdown link to the URL with the article/book title as link text. Check `04-Entities/` and `03-Records/Clippings/` for an existing source note before defaulting to a raw URL.
- **Quote** — verbatim passage from the source that defines or illustrates the term. Use a blockquote (`>`). Don't paraphrase.
- Optional: brief framing sentence above the quote if needed for context, though most existing Term notes go straight to the quote.

For **coined** terms:

- **Gloss** — 1–2 sentences defining the term in plain language. The user's own wording is preferable to your phrasing — pull from the conversation if a clean definition already exists there.
- **Usage example or context** — optionally, the wordy phrase it replaces (if it came from a phrase-revision pass) or a sentence showing it in use.
- **Optional source** — if it was inspired by something external, link or cite it lightly.

### 3. Pick an icon (optional but encouraged)

Existing Term notes usually have a Lucide icon in frontmatter (e.g., `icon: LiFilter`, `icon: LiWaves`). If you can suggest a fitting one, do — otherwise leave the field blank rather than guessing badly. The `suggest-lucide-icons` skill is the right tool when the user wants help picking one.

### 4. Find related notes

Search the vault briefly for adjacent Term notes or concept notes (`02-Evergreen/`) that this term connects to. Two or three is plenty — these populate `## See also`. Don't force connections; if nothing obvious comes up, leave the section empty or omit it.

### 5. Write the note

Path: `02-Evergreen/Terms/{term}.md`

**Filename casing**: match the user's preference if they specified one; otherwise default to sentence case for multi-word terms (`Bottleneck optimization.md`) and lowercase for single common-noun terms (`burnout.md`). Existing examples are mixed — don't agonize over it.

**Filename collision**: before writing, check if the file exists. If it does, surface to the user — don't silently overwrite. Options: append to the existing note, pick a more specific filename, or abort.

**Frontmatter shape** (matching existing Term notes):

```yaml
---
icon: Li{LucideIconName}     # optional
publish: true
related:                      # optional, omit if empty
  - "[[Adjacent term]]"
tags:
  - {topical tags}
  - evergreen
  - terms
created: {ISO timestamp}
modified: {ISO timestamp}
---
```

`evergreen` and `terms` tags are required — they're how the vault identifies these notes.

**Body shape — encountered mode**:

```markdown
[[Source note]]:
> Verbatim quote that defines or illustrates the term. Multiple paragraphs of the source can be stacked as separate blockquote lines.
> Another excerpt if relevant.

## See also
- [[Related term]]
- [[Related concept]]
```

**Body shape — coined mode**:

```markdown
1–2 sentence gloss in plain language. The phrase or context that prompted it can sit below as a usage example or as a quoted line.

> Optional: original phrase being replaced, or a sentence using the term.

## See also
- [[Related term]]
```

### 6. Confirm

Show the resulting wikilink (`[[Term name]]`) and a one-line summary of what was saved. If a daily-log bullet is warranted (per the vault's write-back discipline), mention it but don't auto-write — that's a separate decision.

## Tool choice

Per `AGENTS.md`, prefer Obsidian CLI when the desktop app is running. For new file creation in a known location, the `Write` tool is fine and direct. Read existing Term files with `obsidian read file="<term>"` to check for collisions and to study tone/length when in doubt.

## Examples

**Encountered**:

```
User: /save-term affordance
[skill asks for source]
User: From Don Norman's Design of Everyday Things — there's a clipping at [[The Design of Everyday Things - Norman]]
[skill drafts the note with that source + a quote pulled from the clipping]
```

**Coined (post phrase-revision)**:

```
User: /save-term ambient drafting
[skill confirms it's coined, asks for a quick gloss]
User: writing in the background while doing other things — the prose accretes rather than gets composed
[skill drafts a short coined-mode note, suggests `LiPenLine` for icon]
```

## What not to do

- Don't paraphrase source quotes in encountered mode. Verbatim only.
- Don't invent metadata fields not in the existing convention (no `category`, no `type`, etc.) — keep frontmatter minimal.
- Don't write ambient prose around the term. Term notes are tight scrapbook entries, not essays.
- Don't flip `publish: true` to anything else — Term notes are typically published. (If the user says don't publish, set `publish: false` explicitly.)
- Don't auto-update STATUS or other vault state. This skill writes one file.
