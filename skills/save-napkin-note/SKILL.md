---
name: save-napkin-note
description: "Turn raw capture material into a properly structured Brain vault note (template, frontmatter, folder, related links), or integrate a fragment into an existing note after user confirmation. Use when filing a quick capture into the vault. Triggers: 'save this as a note', 'file this', 'turn this into a note', 'napkin note', 'process this dump'."
argument-hint: "[optional note-title-or-path when source is a file]"
metadata:
  author: nweii
  version: "1.2.0"
  internal: true
---

# Save napkin note

Turn capture material into a vault-ready note: template, frontmatter, folder, and related links. Sources:

1. **An existing note** — inbox dump, partial draft, or rough file that needs finishing.
2. **Inline content** — pasted or dictated text in the conversation (no file yet).

Fill in what is missing without overwriting work the user already did. Do not summarize away or discard ideas unless they ask.

## Defer to AGENTS.md / CLAUDE.md

**Canonical rules live there:** vault layout, folder purposes, metadata semantics (including categories vs tags, `date` vs `last`, `prev`/`next`), hub vs content notes, and how to choose tools (Obsidian CLI, MCP, IDE, etc.).

This skill only adds **procedure** for one task: filing a capture. When in doubt on *what a field means* or *where a note type belongs*, read AGENTS.md rather than guessing.

Illustrative `obsidian …` commands below are **examples** for vaults where the CLI is wired; map them to your environment (read, properties, link-safe move/rename).

## Arguments

- **`$ARGUMENTS`**: If the source is a **file**, pass title or path. If the user only dumped text in chat, **omit** and use the message (or marked paste) as the body.
- If vault file vs chat is ambiguous, ask once.

---

## Analyzing the source

**From a file:** Read the full note with your vault tools.

**From chat:** Use the user’s message or the section they label as the capture.

Parse lightly: subject, entities (people, places, projects, dates, URLs), intent (event record vs concept vs reference vs active work), tone (fragment, decision log, meeting-shaped, etc.).

**Candidate home note:** For fragments or clear continuations, search the vault for a note this could extend. **Never merge or append without explicit confirmation** — see **Integrate vs. new note**.

---

## Processing heuristics

### 1. Respect what exists

Only generate what is missing.

- **Path (existing file):** If the note is already outside a generic inbox/dump location, assume placement is intentional; do not move unless clearly wrong.
- **Path (inline-only):** No prior path — route using **Routing captures** below and AGENTS.md.
- **Title:** Keep a descriptive title; replace placeholders (`Untitled`, bare timestamps) in the filing plan.
- **Frontmatter:** If `tags`, `categories`, etc. are already set, merge or leave alone — do not blindly replace.

### 2. Integrate vs. new note

For fragments or addendum-shaped captures, you may offer **integration** into `[[Existing note]]` instead of a new file.

**Rule:** If integration is plausible, **pause** for **explicit confirmation** before editing the target. Never silently fold content into another note because it “fits.”

Present:

- **Option A — New note:** filing plan (title, folder, template, frontmatter).
- **Option B — Integrate:** target `[[Title]]` or path, where material goes (section/heading), frontmatter updates (`description`, `last`, `related`, tags).

Proceed with B only after they confirm (or explicitly name a merge target). If they decline, Option A only.

### 3. Templates

If content already matches a template’s shape, use it. Otherwise inspect `99-Admin/Templates/` and pick the best fit; use **`Note template.md`** when unsure. Read template frontmatter for default `categories` / `tags`.

Example (when Obsidian CLI is available):

```bash
obsidian properties file="{Template name}"
```

Otherwise open the template `.md` via MCP or filesystem.

### 4. Routing captures (apply AGENTS.md here)

AGENTS.md lists each area’s **purpose**. Use this workflow lens when choosing a folder:

- **Durable concept / evergreen** → match to `02-Evergreen/` intent in AGENTS.
- **Personal reflection, letters, life writing** → `03-Records/Journaling/` (per AGENTS).
- **Meeting or conversation record** → `03-Records/Talks/`.
- **Saved web or external material** → `03-Records/Clippings/` (or provenance categories AGENTS allows).
- **Short reference fragment** → `03-Records/Snippets/`.
- **Active project work** → `03-Records/Working/` (project subfolders, `STATUS.md` cross-cuts — see AGENTS).
- **Entity profile** (person, place, company, media) → `04-Entities/` and the subfolder pattern your vault uses.
- **Weak signal** → best-fit under `03-Records/` per AGENTS descriptions, not vault root.

Templates do not always imply folder; if the template and content disagree with AGENTS routing, **content + AGENTS win**.

### 5. Frontmatter

Follow **AGENTS.md** for property meanings, category semantics, and what not to duplicate across category types.

For this task: ensure a solid **`description`**, **`tags`**, and **`related`** when missing (prefer existing vault tags and 2–5 related links from mentions or `03-Records/Topics/`). Add `aliases`, `categories` (hub wikilinks only, per AGENTS), `icon`, `date`, `people`, `url`, `last` when the note type calls for them.

Do not hand-add `created` / `modified` unless the user or template requires it. For `publish`, only mirror what the chosen template does.

Use **set-note-description** when you want a structured pass at `description` specifically.

### 6. Filenames

For generic names or new files: sentence case, declarative or noun-phrase for evergreens, omit dates unless the note is date-anchored, keep roughly under 60 characters.

---

## Output and approval

Before writing, show a **filing plan**. If integration is plausible, show **both** options and **do not edit** until the user chooses (and confirms the merge target for B).

**New note:**

```
**Filing plan — new note**
- Title: [current or proposed filename without .md]
- Destination: [folder path]
- Template: [template name]
- Source: [existing file path | inline chat capture]
- Key frontmatter additions:
  - description: "[…]"
  - tags: […] (merge with existing if any)
  - related: [[…]] (merge with existing if any)
  - [other fields per AGENTS.md]
```

**If integration is plausible (omit if none):**

```
**Alternative — integrate into existing**
- Target: [[Note title]] (path if helpful)
- Placement: [section / heading / after …]
- Edits to target frontmatter: [e.g. description, last, related]
```

Ask once for approval; for two paths, ask whether to create new or fold into `[[X]]`.

**After approval:**

1. Create, update in place, or link-safe move/rename (e.g. `obsidian move file="Note" to=folder/newpath.md` when available). For integration, only touch the **confirmed** target and agreed `related` updates elsewhere.
2. Preserve substance — light structure/cleanup only unless they ask to summarize.
3. Update `related` backlinks when clearly right; ask if unsure.
4. If you copied out of an inbox/temp path into a canonical file, confirm before deleting the original.

When rewriting frontmatter wholesale, keep a consistent property order matching nearby notes or the template you used.

---

## Output

1. The note at its final path (**new**, **in place**, or **integrated** after confirmation).
2. One line: what changed (path or `[[title]]`) and any `related` notes you touched.
