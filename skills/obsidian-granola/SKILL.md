---
name: obsidian-granola
description: Syncs meetings from Granola to Obsidian notes. Fetches notes and transcripts from Granola, and imports them into formatted meeting and transcript notes in Obsidian. Use when the user says "sync my last granola meeting", "get my granola meeting with X", "make a note for my last meeting", or asks to pull in a Granola transcript.
compatibility: Designed for a system that has Granola MCP and an Obsidian vault configured.
context: fork
model: haiku
metadata:
  author: nweii
  version: "1.2.0"
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
3. `mcp_granola_get_meeting_transcript` to get the verbatim raw transcript (NOTE: This tool may require a paid Granola tier. If the call fails with a paid-tier error, continue the workflow and still create the transcript note so the user can fill it in manually.)

## 3. Generate the Title (If creating a new note)

Generate a title using the user's specific naming convention:
`[Meeting / Kickoff / Interview / etc] with [Person] [more concise context if relevant] [YYYY-MM]`

_Examples:_

- `Meeting with Matt 2, 2025-10`
- `Intro call with Acme 2026-01`
- `Interview - Acme Corp design rol with Grace 2024-05`
- `Kickoff with Carol for assistance work 2026-02`

**Crucial Step:** Present the generated title to the user for approval before creating the files. The user may want to tweak it or provide their own.

## 4. Prepare and Save the Transcript Note

The transcript note uses the `Transcript template.md` format and _must_ follow this naming convention: `Transcript - [Meeting Title]`.

1. **Frontmatter:**

   - If you need the transcript template, `obsidian read file="Transcript template"` to read the latest properties for the template.
   - Use the retrieved properties as the base for the new note's frontmatter.
   - Inject the dynamic values from the meeting:
     - `date`: `YYYY-MM-DD` of the meeting.
     - `people`: Add any identified attendees as wikilinks (e.g., `"[[Jane Doe]]"`).
     - `aliases`: Generate a list of 1-2 short, alternative titles for the meeting to improve searchability. Make sure these aliases are highly specific to this exact meeting (e.g. mentioning specific project names, unique topics, or dates) so they don't broadly apply to other notes (e.g., `["Project Phoenix Q3 roadmap sync", "Stripe API integration planning 2024-10"]`).
     - `related`: Add a wikilink back to the main meeting note (e.g., `"[[Meeting Title]]"`).
     - Generate a `description` property summarizing the meeting. Write a 1-2 sentence concise summary directly (like "Summary mode" in the `set-note-description` skill); do not use filler phrases like "This note is about" or "A summary of".
     - _If the template contains dynamic scripts or variables (e.g. `<% tp.file.creation_date(...) %>`), evaluate them into actual dates._

2. **Content:**

   - Add a `## Transcript` header below the frontmatter.
   - Append the verbatim raw transcript below the header.
   - Granola transcript logs have speaker labels like ` Them:` and `Me:`. You must format the transcript text, inserting blank newlines to separate speakers into distinct paragraphs.
   - Replace "Me: " with "**Nathan:** ". If you know the other speaker, replace "Them: " with the bolded first name of the speaker. If this is a multi-speaker meeting and speaker assignment isn't certain, leave the original label but bold it (e.g. "**Them:** "). Note the colon should be included in the bolding.

3. **Save Location:**
   - Save to @03-Records/Talks/Transcript - [Meeting Title].md

## 5. Prepare and Save the Meeting Note

If the user provided an existing note:

- Read their existing note.
- Retain their frontmatter and title.
- Ensure the `related` property in their frontmatter includes a link to the transcript (`"[[Transcript - [Meeting Title]]]"`).
- Intelligently append the Granola notes and AI summary into their document where it makes sense (e.g., under a `## Notes` header).

If creating a new note:

1. **Frontmatter:**

   - If you need the meeting template, `obsidian read file="Meeting template"` to read the latest properties for the template.
   - Use the retrieved properties as the base for the new note's frontmatter.
   - Inject the dynamic values from the meeting:
     - Follow the same rules for `date`, `people`, `aliases`, and `description` as defined above.
     - `related`: `"[[Transcript - [Meeting Title]]]"`
     - _If the template contains dynamic scripts or variables (e.g. `<% tp.file.creation_date(...) %>`), evaluate them into actual dates._

2. **Content:**

   - Add a `## Notes` or `## Summary` header.
   - Insert the AI-generated summary, private notes, and action items from Granola. Make sure it is nicely formatted in Markdown.

3. **Save Location:**
   - Save to @03-Records/Talks/[Meeting title].md

4. **Bidirectional prev/next linking:**
   - If the new note has a `prev` frontmatter field pointing to an earlier meeting in a series, open that previous note and add (or append to) its `next` frontmatter field with a wikilink back to the new note (e.g., `next: "[[New Meeting Title]]"`). This keeps the chain navigable in both directions.

## 6. (Desktop environment only) Open in Obsidian

Note: This only works if the agent has Obsidian CLI access in the current environment. If the command fails or is unavailable, skip it silently and report the file paths to the user instead.

After saving both notes, try to open them in Obsidian using the CLI:

```bash
# If you have Obsidian running in your environment
obsidian open file="[Meeting Title]"
```

## 7. Log to the daily note

After saving the notes, append a bullet to the daily note for the meeting's date.

**Format:**
```
- Synced [[Meeting Title]] from Granola — [one sentence: who the meeting was with and what it covered]
```

Resolve the daily note for the meeting's `date` using the vault's standard daily note conventions and whatever tools are available. Read the note, find a suitable log section, and append the bullet after the last existing bullet in that section. Use the Obsidian CLI, direct file edit, or vault MCP — whichever is available.

Skip silently if: the daily note doesn't exist, or no suitable log section is found.

If multiple meetings were synced on different dates, log to each respective daily note.

## 8. Review

Confirm with the user that the notes have been successfully created and linked together!
