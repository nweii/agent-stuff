---
name: obsidian-granola
description: "Import Granola meetings into Obsidian, or process an imported meeting through a saved transcription audit and reviewed enrichment. Resume after a transcript is pasted or corrections are confirmed."
compatibility: "Requires readable and writable Obsidian notes. Fetching needs a Granola connection; processing an existing transcript does not. Local audio transcription is optional."
disable-model-invocation: true
metadata:
  author: nweii
  version: "1.4.0"
  internal: true
---

# Granola meeting notes

Import meeting data into linked meeting and transcript notes. Read the vault's instructions before note work and use its available CLI or connector; tool names vary by environment.

## Choose the workflow

- **Import:** requests to sync or fetch a meeting follow the steps below. Finish after the notes are saved, linked, and read back; auditing and enrichment are separate unless requested.
- **Process:** requests to process a meeting, audit and enrich it, or resume after pasting a transcript follow [Process a meeting](references/processing.md). Reuse existing notes before importing anything.
- **Recording:** when the input is an audio/video file, use `transcribe-audio` only if local transcription is requested and the runtime supports it. Feed the resulting transcript into processing; the other branches need no local transcription runtime.

An ambiguous meeting needs identifying before any writes. Carry supplied titles, destinations, and earlier approvals forward.

## 1. Capture Intent & Context

First, determine which meeting the user wants to sync.

- If they say "my last meeting", you will need to list recent meetings to find it.
- If they specify a person or topic, search or list recent meetings to identify the correct one.
- If the user says they already have an existing prepared note for this meeting in Obsidian, append the Granola contents to their existing note, and create a separate transcript note.
- Otherwise, you will generate a new title and create both the meeting note and transcript note from scratch.

## 2. Fetch Granola Data

Use the connected Granola tools to list or search meetings, read the selected meeting's summary/action items/private notes, and fetch its verbatim transcript. Discover the tools actually exposed rather than requiring one provider's identifiers.

If transcript access fails or is unavailable, continue importing the meeting and save an empty transcript staging note for manual paste. Check the returned data and saved note; plan restrictions are a possible reason, not a fact to assume.

## 3. Generate the Title (If creating a new note)

Generate a title using the user's specific naming convention:
`[Meeting / Kickoff / Interview / Review / etc] with [Person] [more concise context if relevant] [YYYY-MM]`

_Examples:_

- `Meeting with Matt 2, 2025-10`
- `Intro call with Acme 2026-01`
- `Interview - Acme Corp design role with Grace 2024-05`
- `Kickoff with Carol for assistance work 2026-02`

Present a generated title for approval before creating files, unless the user already supplied or approved it.

## Destination folder

Meeting notes live **alongside the working notes for whatever project or context the meeting belongs to**, with the transcript note colocated in the same folder as its meeting note.

Determine the destination before saving:

- Identify the project/context the meeting belongs to (a freelance gig, a job-search thread, an internal work project, etc.).
- Map it to the relevant folder under `06-Working/<Area>/`. For example, freelance/client gigs go in `06-Working/Gigs/`; the folder is flat (no per-project subfolders) — meeting notes and transcripts sit directly in it. Browse the candidate folder (`vault_read` in list mode, or the CLI) to confirm it exists and to match sibling naming.
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
- Ensure the `related` property in their frontmatter includes a link to the transcript (`"[[Transcript - <Meeting Title>]]"`).
- Intelligently append the Granola notes and AI summary into their document where it makes sense (e.g., under a `## Notes` header).

If creating a new note:

1. **Frontmatter:**

   - If you need the meeting template, read `99-Admin/Templates/Meeting template.md` (via CLI or vault tool) for the latest properties.
   - Use the retrieved properties as the base for the new note's frontmatter.
   - Inject the dynamic values from the meeting:
     - Follow the same rules for `date`, `people`, `aliases`, and `description` as defined above.
     - `related`: `"[[Transcript - <Meeting Title>]]"`. Add the project's hub/parent note too if there's an obvious one (e.g. `"[[Project work]]"`).
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

URL-encode the note path from the vault root without `.md` (spaces → `%20`, etc.). Show the title, a Markdown link, and the bare URI so it remains usable when a client cannot render the link. For example:

```
**Main note:** [<title>](obsidian://open?vault=Brain&file=<encoded>)
**Transcript:** [Transcript - <title>](obsidian://open?vault=Brain&file=<encoded>)
```

## 7. Log to the daily note

After saving the notes, append a bullet to the daily note for the meeting's date. The log records Nathan's day, so the bullet describes the meeting as an event that happened, not the import. Never write "synced", "imported", or "from Granola" in it.

**Format:**

```
- [[Meeting Title]]: [one sentence: who the meeting was with and what it covered]
```

Example: `- [[Design review with Acme 2026-09]]: reviewed the onboarding flow and agreed which prototype to test`

Resolve the daily note for the meeting's `date` using the vault's standard daily note conventions. Read the note, find the `## Log - <Weekday>` section, and append the bullet after the last existing bullet there.

Note on creating a missing daily: a bare `vault_daily_note`/create call produces a stub WITHOUT the user's Templater structure (Log section, Base embeds, prev/next). If the daily for the meeting's date doesn't exist, either skip the log silently, or — if you create it — rebuild it from `99-Admin/Templates/Daily Note.md` with the Templater values resolved (prev/next dailies, the ISO week / quarter / year links, the `## Log - <Weekday>` header) so it isn't a broken stub. Never edit a past daily other than this — they're frozen as of their day.

If multiple meetings were synced on different dates, log to each respective daily note.

## 8. Verify and return

Read both saved notes back. Confirm the transcript or staging placeholder is in place, both related links resolve, the destination matches the approved context, and any daily-log entry appears once. On a repeated import, reuse existing notes and update only missing material rather than duplicating summaries, transcripts, or daily bullets.

Report the meeting and transcript links, whether transcript fetching succeeded, and any incomplete step. For import-only work, stop here. For requested processing, continue through the processing reference.
