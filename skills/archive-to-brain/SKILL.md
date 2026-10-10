---
name: archive-to-brain
description: "Save an archival summary of an AI conversation to Nathan's Obsidian vault, using the Thinking note template and vault folder conventions to capture intellectual journeys, key insights, and technical logs. Use when archiving a chat session to the vault."
compatibility: "Brain vault access through Obsidian CLI or the Vault MCP."
disable-model-invocation: true
metadata:
  author: nweii
  version: "1.9.0"
  source: nweii/archive-conversation
  internal: true
---

# Archive conversation to Brain vault

Create an archival summary of an AI conversation and save it to Nathan's Obsidian vault (Brain). Read Brain's `AGENTS.md` before accessing notes.

## What the note is for

The note is a record for a reader coming back without the conversation at hand. A good note lets that reader recover:

- what was decided, and why
- how the thinking moved through the back-and-forth
- Nathan's own thinking, in his words
- what was produced and where it lives
- what stayed open

The note is done when everything on that list the conversation contains is recoverable from the note alone.

## Analyze the whole conversation

Read the entire conversation before writing. Name its nature (work session, creative exploration, learning, strategy) and what made it worth saving. Look for:

- the real question beneath the first one
- where assumptions changed or decisions were made
- frameworks or patterns that emerged along the way
- dead ends that taught something
- connections between ideas or system parts
- the human texture: confusion, recognition, frustration, breakthroughs

## Shape the note

Let the conversation's flow set the structure. Common shapes:

- **Problem-solving:** what broke → instructive failed approaches → the working solution → next steps
- **Creative exploration:** the initial vision → how ideas branched → key decisions and why → directions worth revisiting
- **Learning:** what wasn't understood → how understanding built → breakthroughs → remaining questions
- **Work session:** the objective → actions taken and files changed → hurdles and fixes → current state and remaining tasks
- **Strategy:** the decision → options and trade-offs → criteria that emerged → next considerations

Give each section a sentence-case heading that says what happened in it, such as "Starting from hourly vs. project pricing questions" or "Why the recursive function kept hitting memory limits." Write in plain, third-person documentation style; first person appears only in Nathan's quoted words.

## Preserve Nathan's own words

Quote Nathan **verbatim** wherever he states a decision, reasoning, opinion, worry, excitement, or an idea he wants to pursue. His words record his thinking at the time, close to a journal entry; a paraphrase flattens his voice and the back-and-forth in which ideas took shape.

- Open the section a quote informs with the quote; analysis follows.
- Keep his wording and casing; correct only typos and dictation errors.
- Quote whole thoughts.
- Keep the AI's contributions in the AI's voice.
- Be selective about which moments, not about how much of each.

When an exchange shows thinking changing, quote both sides:

> Nathan: "[moment of recognition, doubt, or decision]"
> AI: "[response that shifted understanding or articulated a key insight]"

## Naming

Format: `{{Type}} - {{topic}} YYYY-MM.md`. Use `Thinking` for insight-heavy, reflective, or exploratory conversations and `Log` for work sessions. Examples: `Thinking - Portfolio strategy 2025-08.md`, `Log - Refactoring auth middleware 2025-01.md`.

## Save to the vault

### 1. Compose the frontmatter

```yaml
---
aliases:
  - [1-2 alternative titles in sentence case]
categories: "[[Thinking]]"
type:
icon: [Lucide icon name prefixed with "Li", e.g. LiBrainCircuit]
publish: false
description: [1–2 sentences on what the conversation covered and why it was worth saving]
# Optional: start (multi-day threads only, see below)
last: YYYY-MM-DD
tags:
  - thinking
  - [2-3 tags for the topic, domain, or people]
related:
  - "[[Note name]]" # confirmed vault notes only
# Optional: prev / next (continuity, see below)
created: YYYY-MM-DD
modified: YYYY-MM-DDTHH:mm
---
```

Set `created` and `modified` to today and `last` to the day the conversation happened. Draw aliases, description, icon, and tags from the conversation so they aid recall beyond the filename.

- **Category:** a note carries one of `[[Thinking]]`, `[[Logs]]` (with the `logs` tag), or `[[Journal]]`. One note is the default. When the session also produced a durable artifact of another kind (a spec, a project's working record, a system map), save that as its own note in its category, as defined by its hub in `98-Spaces/`, and link the two through `related`. Personal life writing belongs in a `[[Journal]]` note, which the `personal-processing` skill maintains.
- **Extend or start new:** follow the editorial rules in `98-Spaces/Thinking.md`, which also govern Logs. The default is a new note per session; extend an existing note only when the session continues its scope and the note is still current.
- **Dates:** a single-session archive has only `last`. Add `start` when the thread spans more than one day; then `start` is the first day and `last` the most recent. When extending a note that had only `last`, move that date to `start` and set `last` to today.
- **Continuity:** when another Thinking or Log note is the immediate predecessor or successor (the conversation surfaces it, or Nathan names one), set `prev` / `next` per the vault's `AGENTS.md` and patch the other note so the chain stays bidirectional. Usually the new archive's `prev` is the prior session's note, whose `next` then points here. When work forks, branches may share a `prev`; the origin's `next` names the main continuation. A note linked through `prev` or `next` stays out of `related`.
- **Related:** only notes confirmed to exist in the vault; leave the array empty otherwise.

### 2. Choose the folder

Use a provided save location directly. Otherwise:

- Personal life, emotions, identity, relationships, dreams, health → `03-Records/Journaling`
- Work, projects, productivity, technical sessions, client work → `06-Working`, in a matching subfolder when one clearly fits (list the folder to check; subfolders change over time), or its root

### 3. Write the note

Use the first write path the machine supports:

1. **Obsidian CLI** (Obsidian running): `obsidian vault=Brain create name="{{filename}}" path="{{folder}}/{{filename}}.md" content="{{note}}"`, and `obsidian vault=Brain property:set file="{{note}}" name=prev value='[[Prior note]]'` for continuity links. Pipe multiline content via stdin or escape newlines as `\n`.
2. **notesmd-cli** (headless host with a synced vault): its create/update commands per `--help`; edit frontmatter directly for `prev` / `next`.
3. **Direct file write** when the vault root is known and writable.
4. **Vault MCP** when it is the only vault access.
5. **Manual handoff:** the full note in a Markdown code block with the intended path above it.

### 4. Log to the daily note

Append one bullet to the `## Log` section of the daily note for the day the conversation happened (usually today), at `01-Days/YYYY-MM-DD-ShortDayName.md` (e.g. `01-Days/2025-08-14-Thu.md`). Skip this step if that note doesn't exist.

```
- [[Area/domain]] / [[Note filename without extension]]: plain one- or two-sentence summary
```

Lead with the area note Nathan named, or an existing `[[Domains]]` or `[[Projects]]` note that matches; omit the prefix when no real note fits. The bullet jogs memory and points to the archive: one or two plain sentences on the gist, in the voice Nathan would jot it, drawn from the archive's `description`.

### 5. Surface an Obsidian link

After a completed save, give both a markdown link and the bare URI on the next line, since some clients render `obsidian://` links as plain text. URI-encode only the `file=` value; the bare filename without folder or `.md` is enough.

```
[Thinking - Some topic 2025-08](obsidian://open?vault=Brain&file=Thinking%20-%20Some%20topic%202025-08)
obsidian://open?vault=Brain&file=Thinking%20-%20Some%20topic%202025-08
```
