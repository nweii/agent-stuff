---
name: archive-conversation
description: "Create analytical archival summaries of AI conversations, capturing intellectual journeys, key insights, and technical logs. Use when archiving, saving, or documenting a chat session."
argument-hint: "[save-location]"
metadata:
  author: nweii
  version: "1.3.0"
---

# AI Conversation Archival Summary

Create an archival summary of an AI conversation that captures its intellectual journey, key insights, or technical work session logs. Document either how thinking evolved throughout the discussion or the specific actions and technical decisions made during a work session.

## What the Note Is For

The note is a record for a reader coming back without the conversation at hand. A good note lets that reader recover:

- what was decided, and why
- how the thinking moved through the back-and-forth
- the user's own thinking, in their words
- what was produced and where it lives
- what stayed open

The note is done when everything on that list the conversation contains is recoverable from the note alone.

## Analyze the Whole Conversation

Read the entire conversation before writing. Name its nature (work session, creative exploration, learning, strategy) and what made it worth saving. Look for:

- the real question beneath the first one
- where assumptions changed or decisions were made
- frameworks or patterns that emerged along the way
- dead ends that taught something
- connections between ideas or system parts
- the human texture: confusion, recognition, frustration, breakthroughs

## Shape the Note

Let the conversation's flow set the structure. Common shapes:

- **Problem-solving:** what broke → instructive failed approaches → the working solution → next steps
- **Creative exploration:** the initial vision → how ideas branched → key decisions and why → directions worth revisiting
- **Learning:** what wasn't understood → how understanding built → breakthroughs → remaining questions
- **Work session:** the objective → actions taken and files changed → hurdles and fixes → current state and remaining tasks
- **Strategy:** the decision → options and trade-offs → criteria that emerged → next considerations

Give each section a sentence-case heading that says what happened in it, such as "Starting from hourly vs. project pricing questions" or "Why the recursive function kept hitting memory limits." Write in plain, third-person documentation style; first person appears only in the user's quoted words.

## Preserve the User's Own Words

Quote the user **verbatim** wherever they state a decision, reasoning, opinion, worry, excitement, or an idea they want to pursue. Their words record their thinking at the time, close to a journal entry; a paraphrase flattens their voice and the back-and-forth in which ideas took shape.

- Open the section a quote informs with the quote; analysis follows.
- Keep their wording and casing; correct only typos and dictation errors.
- Quote whole thoughts.
- Keep the AI's contributions in the AI's voice.
- Be selective about which moments, not about how much of each.

When an exchange shows thinking changing, quote both sides:

> [User's first name, if known]: "[moment of recognition, doubt, or decision]"
> AI: "[response that shifted understanding or articulated a key insight]"

## File Output Requirements

Match the user's system first. Use what you already know of their conventions from their instructions, memory, or this conversation. Otherwise, before writing, read two or three of their most similar notes (earlier archives, or recent notes in the likely folder) and follow how those are named, filed, and tagged. Use the defaults below only when there is no system to match.

### Naming

Default format: `{{Type}} - {{topic}} YYYY-MM.md`, with `Thinking` for insight-heavy conversations and `Log` for work sessions.

- Example: `Thinking - Portfolio strategy 2025-08.md`
- Example: `Log - Refactoring auth middleware 2025-01.md`

### Save Location

1. **Save-location argument:** use that path directly.
2. **Existing structure:** save next to the user's similar notes, or in the folder that best fits the conversation's subject.
3. **Unclear:** ask the user where to save.
4. **No file access:** output the note as a Markdown code block with the intended path above it.

### Metadata

Fill only the frontmatter fields those similar notes share and this conversation can answer accurately, and reuse tags that already exist. With no system to match, add the date and a few tags for the conversation's topic.
