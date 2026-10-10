---
name: archive-conversation
description: "Create analytical archival summaries of AI conversations, capturing intellectual journeys, key insights, and technical logs. Use when archiving, saving, or documenting a chat session."
argument-hint: "[save-location]"
metadata:
  author: nweii
  version: "1.2.0"
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

## Deep Analysis Requirements

Conduct a thorough analysis of the entire conversation:

1. Read through completely first, identifying all conceptual threads, task sequences, and transitions
2. Note patterns in questioning, resistance points, breakthrough moments, or technical hurdles
3. Identify the conversation's nature (technical work session, creative exploration, strategic planning, philosophical inquiry, etc.)
4. Understand what made this particular exchange worth preserving (insight-driven vs. action-documentation)
5. Determine what structure would best capture its unique value (narrative vs. log-formatted)

**Look deeply for:**

- The real question beneath the initial question
- How the problem space was redefined or the technical path was forged
- Moments where assumptions were challenged or implementation details were decided
- Conceptual frameworks or technical patterns that emerged organically
- The emotional/intellectual journey or the step-by-step progress of a work session
- Valuable tangents or "failed" approaches that taught something or informed the final code
- Connections made between seemingly unrelated ideas or system components
- What remained intentionally unresolved or deferred to later tasks

## Creating Descriptive Structure

Instead of using generic headings like "Initial Question" or "Key Findings," create headings that describe the actual content of each section. The heading should give readers immediate context about what happened in that part of the conversation.

**Examples of descriptive headings:**

- "Starting from hourly vs. project pricing questions"
- "Why the recursive function kept hitting memory limits"
- "Exploring whether this needs to be real-time"
- "The confusion about state management"
- "Deciding between complexity and maintainability"

Use sentence-case for headings, not title case. Avoid marketing-speak, dramatic phrasing, or trying to be clever.

## Flexible Documentation Approaches

Let the conversation's natural flow determine your structure:

**For Problem-Solving Sessions:**
Open with what broke/what problem triggered the conversation → Document failed approaches if instructive → Describe the working solution → Note implementation details or next steps

**For Creative Explorations:**
Start with the initial vision or desire → Show how ideas evolved or branched → Capture key decisions and why they were made → Preserve unexplored directions worth revisiting

**For Learning Journeys:**
Begin with what the user didn't understand → Track how understanding built piece by piece → Highlight breakthrough moments → List remaining questions

**For Work Sessions & Implementation Logs:**
Define the session's objective → Document specific actions taken and files modified → Capture technical hurdles and how they were resolved → Summarize the current state of the work and remaining tasks

**For Strategic Thinking:**
Frame the decision that needed making → Explore options considered and their trade-offs → Document the framework or criteria that emerged → Capture action items or next considerations

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

Match the user's system first. Before writing, read two or three of their most similar notes (earlier archives, or recent notes in the likely folder) and follow how those are named, filed, and tagged. Use the defaults below only when there is no system to match.

### Naming

Default format: `{{Type}} - {{topic}} YYYY-MM.md`, with `Thinking` for insight-heavy conversations and `Log` for work sessions.

- Example: `Thinking - Portfolio strategy 2025-08.md`
- Example: `Log - Refactoring auth middleware 2025-01.md`

### Save location

1. **Save-location argument:** use that path directly.
2. **Existing structure:** save next to the user's similar notes, or in the folder that best fits the conversation's subject.
3. **Unclear:** ask the user where to save.
4. **No file access:** output the note as a Markdown code block with the intended path above it.

### Metadata

Fill only the frontmatter fields those similar notes share and this conversation can answer accurately, and reuse tags that already exist. With no system to match, add the date and a few tags for the conversation's topic.

## Remember

- You're documenting intellectual exploration OR technical execution/work sessions
- Perform deep analysis to identify all important threads, transitions, and task sequences
- Use headings that describe what actually happened or what was achieved in that section
- Keep language natural and straightforward - no marketing-speak or forced drama
- Include the messy, human elements - confusion, recognition, technical frustrations, breakthroughs
- When using specific examples repeatedly, vary phrasing or generalize after first mention
- Use third person or neutral documentation style, except in the user's quoted words
