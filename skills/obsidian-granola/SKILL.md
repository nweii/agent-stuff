---
name: obsidian-granola
description: Sync meetings from Granola to Obsidian — pulls notes and transcripts and imports them as formatted meeting/transcript notes. Use when the user says "sync my last granola meeting", "note for my last meeting", or asks to pull in a Granola transcript.
compatibility: Designed for a system that has Granola MCP and an Obsidian vault configured.
context: fork
model: haiku
disable-model-invocation: true
metadata:
  author: nweii
  version: "1.3.0"
  internal: true
---

This skill helps the user extract meeting data from Granola (via the Granola MCP) and turn it into properly formatted Obsidian notes in their vault.

## 1. Capture Intent & Context

First, determine which meeting the user wants to sync.

- If they say "my last meeting", you will need to list recent meetings to find it.
- If they specify a person or topic, search or list recent meetings to identify the correct one.
- If the user says they already have an existing prepared note for this meeting in Obsidian, append the Granola contents to their existing note, and create a separate transcript note.
- Otherwise, you will generate a new title and create both the meeting note and transcript note from scratch.

## 2. Fetch Granola Data

Use the Granola MCP tools:

1. `mcp_granola_list_meetings` to find the meeting ID if you don't already have it.
2. `mcp_granola_get_meetings` to get the AI-generated summary, action items, and private notes.
3. `mcp_granola_get_meeting_transcript` to get the verbatim raw transcript (NOTE: This tool may require a paid Granola tier, and may not be exposed at all in some environments. If the call fails or the tool is unavailable, continue the workflow and still create the transcript note as a staging note so the user can paste the transcript in manually.)

## 3. Generate the Title (If creating a new note)

Generate a title using the user's specific naming convention:
`[Meeting / Kickoff / Interview / Review / etc] with [Person] [more concise context if relevant] [YYYY-MM]`

_Examples:_

- `Meeting with Matt 2, 2025-10`
- `Intro call with Acme 2026-01`
- `Interview - Acme Corp design rol with Grace 2024-05`
- `Kickoff with Carol for assistance work 2026-02`

**Crucial Step:** Present the generated title to the user for approval before creating the files. The user may want to tweak it or provide their own.

## Destination folder

Meeting notes are no longer filed into a single `Talks` folder by default. They live **alongside the working notes for whatever project or context the meeting belongs to**, with the transcript note colocated in the same folder as its meeting note.

Determine the destination before saving:

- Identify the project/context the meeting belongs to (a freelance gig, a job-search thread, a TALtech project, etc.).
- Map it to the relevant folder under `03-Records/Working/<Area>/`. For example, freelance/client gigs go in `03-Records/Working/Gigs/`; the folder is flat (no per-project subfolders) — meeting notes and transcripts sit directly in it. Browse the candidate folder (`vault_read` in list mode, or the CLI) to confirm it exists and to match sibling naming.
- If no project-specific folder fits, ask the user where it should go rather than defaulting to `Talks` (offer the most likely candidate). `Talks` is only a fallback for genuinely context-free meetings, and only if the user confirms.

Both the meeting note and its transcript note save to this same destination folder.

## 4. Prepare and Save the Transcript Note

The transcript note uses the `Transcript template.md` format and _must_ follow this naming convention: `Transcript - [Meeting Title]`.

1. **Frontmatter:**

   - If you need the transcript template, `obsidian read file="Transcript template"` (or read `99-Admin/Templates/Transcript template.md` with whatever vault tool is available) to get the latest properties.
   - Use the retrieved properties as the base for the new note's frontmatter.
   - Inject the dynamic values from the meeting:
     - `date`: `YYYY-MM-DD` of the meeting.
     - `people`: Add identified attendees as wikilinks (e.g., `"[[Jane Doe]]"`). Include attendees the user names even if they aren't in Granola's participant list.
     - `aliases`: Generate a list of 1-2 short, alternative titles for the meeting to improve searchability. Make sure these aliases are highly specific to this exact meeting (e.g. mentioning specific project names, unique topics, or dates) so they don't broadly apply to other notes.
     - `related`: Add a wikilink back to the main meeting note (e.g., `"[[Meeting Title]]"`).
     - Generate a `description` property summarizing the meeting. Write a 1-2 sentence concise summary directly (like "Summary mode" in the `set-note-description` skill); do not use filler phrases like "This note is about" or "A summary of".
     - _If the template contains dynamic scripts or variables (e.g. `<% tp.file.creation_date(...) %>`), evaluate them into actual dates._

2. **Content:**

   - Add a `## Transcript` header below the frontmatter.
   - If you have the verbatim transcript: append it below the header. Granola transcript logs have speaker labels like `Them:` and `Me:`. Format the transcript text, inserting blank newlines to separate speakers into distinct paragraphs. Replace `Me: ` with `**Nathan:** `. If you know the other speaker, replace `Them: ` with the bolded first name of the speaker. If this is a multi-speaker meeting and speaker assignment isn't certain, leave the original label but bold it (e.g. `**Them:** `). The colon should be included in the bolding.
   - If you do NOT have the transcript (tool unavailable/paid-tier): leave a short italic staging placeholder under the header telling the user to paste the Granola transcript and noting the speaker-label formatting to apply.

3. **Save Location:**
   - Save to the **destination folder** determined above (see "Destination folder"), as `[destination]/Transcript - [Meeting Title].md`.

## 5. Prepare and Save the Meeting Note

If the user provided an existing note:

- Read their existing note.
- Retain their frontmatter and title.
- Ensure the `related` property in their frontmatter includes a link to the transcript (`"[[Transcript - [Meeting Title]]]"`).
- Intelligently append the Granola notes and AI summary into their document where it makes sense (e.g., under a `## Notes` header).

If creating a new note:

1. **Frontmatter:**

   - If you need the meeting template, read `99-Admin/Templates/Meeting template.md` (via CLI or vault tool) for the latest properties.
   - Use the retrieved properties as the base for the new note's frontmatter.
   - Inject the dynamic values from the meeting:
     - Follow the same rules for `date`, `people`, `aliases`, and `description` as defined above.
     - `related`: `"[[Transcript - [Meeting Title]]]"`. Add the project's hub/parent note too if there's an obvious one (e.g. `"[[BPL work]]"`).
     - _If the template contains dynamic scripts or variables (e.g. `<% tp.file.creation_date(...) %>`), evaluate them into actual dates._

2. **Content:**

   - Add a `## Summary` (or `## Notes`) header.
   - Insert the AI-generated summary, private notes, and action items from Granola, cleanly formatted in Markdown — preserve the substance and any decision-bearing quotes; trim throwaway asides.

3. **Save Location:**
   - Save to the **destination folder** determined above, as `[destination]/[Meeting title].md` (same folder as the transcript note).

4. **Bidirectional prev/next linking:**
   - If the new note has a `prev` frontmatter field pointing to an earlier meeting in a series, open that previous note and add (or append to) its `next` frontmatter field with a wikilink back to the new note. This keeps the chain navigable in both directions.

## 6. Provide Obsidian links

After saving, output a tappable Obsidian URI for each created note directly in the chat, so the user can open them manually on any platform (desktop or mobile). Don't rely on the desktop-only `obsidian open` CLI.

Construct each link as:

```
obsidian://open?vault=Brain&file=<URL-encoded note name>
```

URL-encode the note name (spaces → `%20`, etc.). The note basename is sufficient — Obsidian resolves it like a wikilink. Present them as markdown links labeled with the note titles, e.g.:

```
**Main note:** [<title>](obsidian://open?vault=Brain&file=<encoded>)
**Transcript:** [Transcript - <title>](obsidian://open?vault=Brain&file=<encoded>)
```

## 7. Log to the daily note

After saving the notes, append a bullet to the daily note for the meeting's date.

**Format:**

```
- Synced [[Meeting Title]] from Granola — [one sentence: who the meeting was with and what it covered]
```

Resolve the daily note for the meeting's `date` using the vault's standard daily note conventions. Read the note, find the `## Log - <Weekday>` section, and append the bullet after the last existing bullet there.

Note on creating a missing daily: a bare `vault_daily_note`/create call produces a stub WITHOUT the user's Templater structure (Log section, Base embeds, prev/next). If the daily for the meeting's date doesn't exist, either skip the log silently, or — if you create it — rebuild it from `99-Admin/Templates/Daily Note.md` with the Templater values resolved (prev/next dailies, the ISO week / quarter / year links, the `## Log - <Weekday>` header) so it isn't a broken stub. Never edit a past daily other than this — they're frozen as of their day.

If multiple meetings were synced on different dates, log to each respective daily note.

## 8. Review

Confirm with the user that the notes have been created, linked together, and filed in the right folder.
