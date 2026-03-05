---
name: archive-to-brain
description: "Save an archival summary of an AI conversation to Nathan's Obsidian vault, using Nathan's Thinking note template and vault folder conventions to capture intellectual journeys, key insights, and technical logs. Use when archiving a chat session to Nathan's Obsidian vault."
compatibility: "The skill inherits the full analytical approach from the `archive-conversation` skill and adds vault-specific save logic."
metadata:
  author: nweii
  version: "1.1.0"
  variants: nweii/archive-conversation
  internal: true
---

# Archive conversation to Brain vault

Create an archival summary of an AI conversation and save it to Nathan's Obsidian vault (Brain).

## Deep analysis requirements

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

## Creating descriptive structure

Instead of using generic headings like "Initial Question" or "Key Findings," create headings that describe the actual content of each section. The heading should give readers immediate context about what happened in that part of the conversation.

**Examples of descriptive headings:**

- "Starting from hourly vs. project pricing questions"
- "Why the recursive function kept hitting memory limits"
- "Exploring whether this needs to be real-time"
- "The confusion about state management"
- "Deciding between complexity and maintainability"

Use sentence-case for headings, not title case. Avoid marketing-speak, dramatic phrasing, or trying to be clever.

## Flexible documentation approaches

Let the conversation's natural flow determine your structure:

**For problem-solving sessions:**
Open with what broke/what problem triggered the conversation → Document failed approaches if instructive → Describe the working solution → Note implementation details or next steps

**For creative explorations:**
Start with the initial vision or desire → Show how ideas evolved or branched → Capture key decisions and why they were made → Preserve unexplored directions worth revisiting

**For learning journeys:**
Begin with what the user didn't understand → Track how understanding built piece by piece → Highlight breakthrough moments → List remaining questions

**For work sessions & implementation logs:**
Define the session's objective → Document specific actions taken and files modified → Capture technical hurdles and how they were resolved → Summarize the current state of the work and remaining tasks

**For strategic thinking:**
Frame the decision that needed making → Explore options considered and their trade-offs → Document the framework or criteria that emerged → Capture action items or next considerations

## Excerpt guidelines

Include conversation excerpts that show thinking in action:

> Nathan: "[moment of recognition or confusion]"
> AI: "[response that shifted understanding or articulated key insight]"

Choose excerpts that reveal intellectual movement — the moments where thinking actually changed, not just where information was exchanged. Be generous in your excerpt lengths.

## Naming convention

- **Format**: `{{Type}} - {{topic}} YYYY-MM.md`
- Use `Thinking` for insight-heavy, reflective, or exploratory conversations
- Use `Log` for action-leaning work sessions, implementation logs, or technical sessions
- Example: `Thinking - Portfolio strategy 2025-08.md`
- Example: `Log - Refactoring auth middleware 2025-01.md`

## Vault save logic

### 1. Fetch the live template

If running locally with access to terminal tools where Obsidian is running, fetch the live template from the vault:

```bash
obsidian read file="Thinking note template"
```

If running in a cloud or sandboxed environment without shell access, skip this step and use the fallback frontmatter below directly.

### 2. Compose the frontmatter

Use today's date for `created`, `modified`, and `last`.

**Fallback template** (if `obsidian read` fails):

```yaml
---
aliases:
categories: "[[Thinking]]"
type:
icon: LiBrainCircuit
publish: false
description:
last: YYYY-MM-DD
tags:
  - thinking
related: []
created: YYYY-MM-DD
modified: YYYY-MM-DDTHH:mm
---
```

For `Log` notes, change the `tags` entry to `log` and update `categories` to `"[[Log]]"` if appropriate.

### 3. Determine the save folder

- Personal life, emotions, identity, relationships, dreams, health → `03-Records/Journaling`
- Work, projects, productivity (including personal productivity), technical sessions, client work → `03-Records/Working`

Within `03-Records/Working`, check for existing subfolders that match the conversation topic (e.g., by running `obsidian search` or listing the directory if local tools are available). Use a matching subfolder if one clearly fits; otherwise save to the root of `03-Records/Working`. Don't assume which subfolders exist — they change over time.

If a specific save location was provided, use it directly.

### 4. Save to vault

Use the Obsidian CLI to create the note:

```bash
obsidian create name="{{filename}}" path="{{folder}}/{{filename}}.md" content="{{full content with frontmatter}}"
```

Pipe multiline content via stdin or use `\n` escaping as needed.

If the Obsidian CLI is unavailable, fall back in this order:

1. **Write the file directly** to the vault path on disk if file system access is available
2. **Output as a downloadable file** if the environment supports it
3. **Output as a markdown code block** for manual saving, with the intended vault path noted above the block

## Remember

- You're documenting intellectual exploration OR technical execution/work sessions
- Perform deep analysis to identify all important threads, transitions, and task sequences
- Use headings that describe what actually happened or what was achieved in that section
- Keep language natural and straightforward — no marketing-speak or forced drama
- Capture why this journey or work session matters, and what was actually produced or decided
- Include the messy, human elements — confusion, recognition, technical frustrations, breakthroughs
- Preserve what would be valuable to revisit months or years later
- Use third person or neutral documentation style, not first person (except when quoting)
