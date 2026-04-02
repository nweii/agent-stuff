---
name: obsidian-sync-people
description: Creates or enriches entity notes for people in /04-Entities/ from available context — current conversation, Granola meetings, Gmail threads. Use when someone is mentioned and worth noting, or when explicitly asked to create or update a person note.
argument-hint: "[Person name | 'all']"
compatibility: Designed for use with the Brain Obsidian vault.
metadata:
  author: nweii
  version: "1.0.0"
  internal: true
---

Creates or enriches `/04-Entities/` notes for people using whatever context is available in the current session.

## 1. Identify people to sync

- If `$ARGUMENTS` names a person, target that person.
- If `$ARGUMENTS` is `all` or empty, target all people meaningfully mentioned in the current conversation — skip passing references (e.g. a name dropped once with no context).
- If invoked mid-conversation ("make a note about X"), use the context already established.

## 2. Check for an existing note

Search `/04-Entities/` for a file matching the person's name or known aliases. A match means any file whose title, `aliases`, or body contains the name.

- **If a note exists**: enrich it (step 4). Do not recreate it.
- **If no note exists**: create one (step 3).

## 3. Create a new note

First, read `99-Admin/Templates/Person template.md` using available vault tools to get the current base frontmatter. Use the retrieved frontmatter as the base. Evaluate any Templater expressions (e.g. `<% tp.file.creation_date(...) %>`) into actual values. Then inject:

- `aliases`: first name and any other common short names
- `description`: 1-2 sentence bio — omit if insufficient context
- `urls`: LinkedIn or other profile URLs if known
- `related`: wikilinks to orgs, companies, or places the person is associated with — only link entities that already exist in `/04-Entities/`
- `tags`: start with `people`; add topical tags based on context (e.g. `people/networking`, `VFA`, `close-friends`, `recruiters`)

**Body:**

Add a short paragraph (1-3 sentences) only if there is meaningful context — who they are, how Nathan knows them, what's notable. Skip it entirely if the frontmatter already captures the substance. Do not write generic filler.

The template already includes `![[Related.base#Person]]` — preserve it at the end of the note.

**Save to:** `04-Entities/[Full Name].md`

## 4. Enrich an existing note

Only add, never overwrite. In order of priority:

1. **`description`**: Add if missing and you have enough context for a solid 1-2 sentence bio.
2. **`related`**: Add wikilinks to orgs or places not yet listed — only if those entities already exist in `/04-Entities/`.
3. **`urls`**: Add a LinkedIn or profile URL if discovered.
4. **`tags`**: Add topical tags if context reveals roles or relationships not yet tagged.
5. **Body paragraph**: Add only if there is meaningful new context not captured elsewhere in the note.

## 5. Pull from available sources

Check each in parallel; skip gracefully if unavailable:

- **Current conversation** (primary) — use context already established in this session.
- **Granola MCP**: `list_meetings` → `get_meetings` to find recent meetings involving this person. Extract role, org, and any relationship context.
- **Gmail MCP**: Search sent + received for threads with this person. Read for context, not just subject lines. Skip if not available or if the person is only a newsletter/transactional sender.

## 6. Open in Obsidian

After saving, open the note using available vault tools if possible. Skip silently if not supported in the current environment. Report the file path to the user instead.

## 7. Confirm

Report briefly: which notes were created, which were enriched, and what was added or changed.

## Important

- **Never fabricate.** If you can't trace a claim to a specific source, use "Unknown" or omit it.
- **`description` is the most valuable field.** It surfaces in search and frontmatter peeks. Prioritize getting this right.
- **Respect existing content.** Do not reorganize, rewrite, or remove what's already there.
- **Only link entities that exist.** Don't create `related` wikilinks to orgs or places that don't yet have a note in `/04-Entities/`.
- **Tags should be reusable.** Prefer existing tag patterns (`people/networking`, `people/advisors`, `close-friends`, `VFA`) over one-off tags.
