---
name: archive-conversation
description: Create analytical archival summaries of AI conversations, capturing intellectual journeys, key insights, and technical logs. Use when archiving, saving, or documenting a chat session.
metadata:
  author: nweii
  version: "1.0.0"
---

# AI Conversation Archival Summary

Create an archival summary of an AI conversation that captures its intellectual journey, key insights, or technical work session logs. Document either how thinking evolved throughout the discussion or the specific actions and technical decisions made during a work session.

## Deep Analysis

Perform a deep, analytical reading of the entire conversation:

- **Conceptual Threads**: Identify all conceptual threads, task sequences, and transitions.
- **Patterns**: Note patterns in questioning, resistance points, breakthrough moments, or technical hurdles.
- **Nature of Exchange**: Identify if the session was technical work, creative exploration, strategic planning, or philosophical inquiry.
- **Value**: Understand what made this particular exchange worth preserving (insight-driven vs. action-documentation).
- **Structure**: Determine what structure best captures its unique value (narrative vs. log-formatted).

## Documentation Guidelines

### Descriptive Headings

Create headings that describe the actual content of each section. The heading should give readers immediate context about what happened in that part of the conversation.

- Use sentence-case.
- Be straightforward and specific (e.g., "Starting from hourly vs. project pricing questions", "Why the recursive function kept hitting memory limits").
- Avoid generic labels like "Introduction" or "Key Findings".

### Flexible Approaches

- **Problem-Solving Sessions**: Open with the problem → Document failed approaches → Describe the working solution → Note implementation details.
- **Creative Explorations**: Start with the initial vision → Show evolution/branching → Capture key decisions → Preserve unexplored directions.
- **Learning Journeys**: Begin with gaps in understanding → Track building blocks → Highlight breakthroughs → List remaining questions.
- **Work Sessions & Technical Execution**: Define objective → Document specific actions (files modified) → Capture technical hurdles → Summarize current state and remaining tasks.

### Excerpts

Include conversation excerpts that show thinking in action - moments where thinking actually changed, not just where information was exchanged. Be generous in excerpt lengths.

> Nathan: "[moment of recognition or confusion]"
> AI: "[response that shifted understanding or articulated key insight]"

## Output and Archival

### Metadata and Naming

- **Frontmatter**: Include metadata (like `#thinking` tag) as appropriate for the user's system.
- **Naming Convention**: `{{Type}} - {{topic}} YYYY-MM.md`
  - Use `Thinking` for insight-heavy journeys.
  - Use `Log` for action-leaning work sessions.
  - Example: `Thinking - career portfolio strategy 2025-08.md`

### Output Logic (Portable/Mobile Support)

1. **Identify Target Vault**: Detect if the user has a known notes vault or storage system (e.g., Obsidian, Google Drive, iCloud, Notion).
2. **Confirm Location**: Unless a default saving location is already established in the current session's context, always ask the user to confirm where to save the file (e.g., "Should I save this to your `03-Records/Working` folder, or elsewhere?").
3. **Default (Save to File System)**: If the environment supports file operations and a target location is confirmed, save the summary directly to the user's vault.
4. **Fallback (Markdown Block)**: If vault access is unavailable, restricted, or the user prefers manual saving (common in mobile chat contexts), output the complete archival summary within a single markdown code block for the user to copy/save manually.
