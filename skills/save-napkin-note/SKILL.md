---
name: save-napkin-note
description: "Turn raw capture material into a properly structured Brain vault note (template, frontmatter, folder, related links), or integrate a fragment into an existing note after user confirmation. Use when filing a quick capture into the vault. Triggers: 'save this as a note', 'file this', 'turn this into a note', 'napkin note', 'process this dump'."
argument-hint: "[optional note-title-or-path when source is a file]"
metadata:
  author: nweii
  version: "1.1.0"
  internal: true
---

# Save napkin note

Turn capture material into a vault-ready note: right template, frontmatter, destination folder, and related links. The source may be:

1. **An existing note** — inbox dump, partial draft, or rough file that needs finishing.
2. **Inline content** — text the user pastes, dictates, or dumps in the conversation (no file yet).

In both cases, fill in what is missing without overwriting work the user has already done. Do not summarize away or discard ideas unless they ask you to.

## Tooling (any agent)

Vault conventions live in **AGENTS.md** (and CLAUDE.md). **Obsidian CLI commands in this skill are examples** for environments where `obsidian` is installed and wired to this vault.

Use whatever you actually have:

- Obsidian CLI (`obsidian read`, `obsidian move`, `obsidian properties`, …) when available — prefer link-safe moves/renames when the toolchain supports them.
- Vault MCP tools, notesmd-cli, IDE file operations, or direct filesystem reads/writes when CLI is not available.
- In MCP-only setups, stay within the server's exposed capabilities; do not assume shell or Obsidian CLI.

Map each illustrative `obsidian …` step to your environment's equivalent (read note, list properties, write file, move/rename with wikilink updates if possible).

## Arguments

- **`$ARGUMENTS`**: When the source is a **file**, pass the note title or path so you can load it. If the user only dumped text in chat and named no file, **omit arguments** and treat the message (or the clearly marked paste block) as the source.
- If it is ambiguous whether they mean a vault file vs. chat text, ask once before proceeding.

---

## Analyzing the source

**From a file:** Read the full note (via your vault tools).

**From chat:** Use the user's message (or the section they identify as the capture) as the full body to structure.

Then parse for:

- Subject matter and content type
- Any people, places, projects, dates, or URLs mentioned
- Implicit intent (record of something that happened? Concept? Reference? Project note?)
- Tone signals: rough thought, decision log, meeting record, creative fragment?

**Candidate home note:** For short fragments or clearly continuation-style captures, search the vault (wikilinks, titles, `related`, topic indexes, semantic search) for an **existing note** that this material would naturally extend or belong in. If you find a plausible match, **do not merge or append without explicit user confirmation** — see **Integrate vs. new note** below.

---

## Processing heuristics

Apply these based on what the note actually needs.

### 1. Respect what exists

Only generate what is missing.

- **Folders (existing file):** If the note is already outside a generic inbox/dump location (e.g. not `00-Inbox/` or vault root), assume placement is intentional; do not move unless clearly wrong.
- **Folders (inline-only):** There is no prior path — choose destination from the mapping below.
- **Titles:** If the material already has a descriptive title (not "Untitled", "Quick note", or a bare timestamp), keep it; otherwise propose one in the filing plan.
- **Frontmatter:** If fields (e.g. `tags`, `categories`) are already populated, append or leave them alone — do not blindly overwrite.

### 2. Integrate vs. new note

When the capture is a **fragment** (or reads like an addendum to a topic you already have a note for), you may propose **integrating** into `[[Existing note]]` instead of creating a separate file.

**Rule:** If integration is a reasonable option, **always** pause and get **explicit confirmation** before editing that existing note. Never silently fold chat text or inbox content into another note because it "fits."

Present clearly:

- **Option A — New note:** default filing plan (title, folder, template, frontmatter).
- **Option B — Integrate into existing:** which note (`[[Title]]` or path), *where* the new material would go (section/heading), and what frontmatter you would adjust (e.g. `description`, `last`, `related`, tags).

Ask which option they want (or a different target). Only after they confirm **Option B** (or explicitly ask you to merge into a named note) may you append or restructure the existing file.

If they decline integration, proceed with Option A only.

### 3. Templates

If the content already matches a specific template (frontmatter, headings, structure), use that as the base.

Otherwise pick the best template by inspecting files under `99-Admin/Templates/`.

Example (Obsidian CLI):

```bash
obsidian properties file="{Template name}"
```

If you cannot run that, read the template `.md` file directly (or via MCP). Use template `categories` for note kind, `tags` for defaults, and **`Note template.md`** when unsure.

### 4. Folders

Templates do not always imply a folder. When moving or when creating from inline content, use this mapping:

- Concept / evergreen idea → `02-Evergreen/`
- Personal reflection, journal, thinking → `03-Records/Journaling/`
- Meeting or conversation → `03-Records/Talks/`
- Web clipping or saved content → `03-Records/Clippings/`
- Short reference fragment → `03-Records/Snippets/`
- Active project working notes → `03-Records/Working/`
- Person, place, company, media → `04-Entities/` (matching subfolder)
- General note with no strong signal → `03-Records/` (best-fit subfolder)

### 5. Frontmatter

Synthesize missing frontmatter per **AGENTS.md**.

**Fields to always ensure exist:**

- `description`: Summary mode (events, meetings, reflections) or Meta mode (concepts, references, specs). Under ~200 characters, telegraphic. Leave good existing descriptions alone unless they are placeholders.
- `tags`: Template defaults plus 2–5 topical tags from the content. Prefer existing vault tags.
- `related`: Wikilinks to connected notes — from explicit mentions, search, or `03-Records/Topics/`. Aim for 2–5.

**Add if meaningful and missing:**

- `aliases`, `categories` (existing hub notes only — e.g. `[[Clippings]]`, `[[Projects]]`), `icon` (`Li{TitleCaseIconName}`), `date` / `people` / `url`, `last` where conventions apply.

**Omit:**

- `created` / `modified`: Templater (or equivalent) usually fills these; do not add them by hand unless the user or template explicitly requires it.
- `publish`: only add `publish: false` when the base template includes it.

### 6. Filenames

If the filename is generic or you are creating a new file, propose a clean name:

- Sentence case: `Designing for trust over efficiency.md`
- Omit dates unless the note is inherently date-anchored.
- Keep under ~60 characters.
- Evergreens: declarative or noun-phrase titles.

---

## Output and approval

Before writing files, show a **filing plan**. If a plausible **integration target** exists, show **both** a new-note plan and an integration option, and **do not apply** either until the user chooses (and, for integration, explicitly confirms the target note).

**New note (default shape):**

```
**Filing plan — new note**
- Title: [current or proposed filename without .md]
- Destination: [folder path]
- Template: [template name]
- Source: [existing file path | inline chat capture]
- Key frontmatter additions:
  - description: "[generated description]"
  - tags: [tag1, tag2] (merging with existing if any)
  - related: [[Note A]] (merging with existing if any)
  - [any other generated fields]
```

**If integration is plausible, also show (still require confirmation):**

```
**Alternative — integrate into existing**
- Target: [[Note title]] (path if helpful)
- Placement: [e.g. new section under "## …", or after paragraph about …]
- Edits to target frontmatter: [e.g. refresh description, bump `last`, add `related`]
- [Omit this block if no credible existing note — do not invent a weak merge just to avoid a new file]
```

Ask: For a single path, "Does this look right, or should we adjust…?" When two paths exist: "**Should this become a new note, or should we fold it into [[X]]?**" Wait for an explicit choice before editing.

Once approved:

1. **Write or update** using your vault tools: create the file at the destination, or update in place, or perform a link-safe move/rename if your stack supports it (e.g. `obsidian move file="Note" to=folder/newpath.md` when Obsidian CLI is available). For **integration**, only modify the **confirmed** target note plus any agreed `related` updates elsewhere.
2. Preserve substantive content — restructure or lightly clean; do not replace with a summary unless asked.
3. Add backlinks from `related` targets when clearly appropriate; ask if uncertain.
4. If you **duplicated** from a temp path (e.g. `00-Inbox/`) into a new canonical file, confirm before deleting the original.

### Frontmatter ordering

Canonical order when you control the block; omit unused fields:

```yaml
---
aliases:
categories:
type:
icon:
publish:
description:
date:
url:
author:
people:
location:
related:
tags:
created:
modified:
---
```

---

## Output

1. The vault note at its final path (**new**, **updated in place**, or **existing note** after confirmed integration).
2. One-line confirmation: what changed (path or `[[title]]`) and any `related` notes you touched.
