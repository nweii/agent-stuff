---
alwaysApply: false
title: file-summarization
description: When asked to generate summaries of markdown content for its YAML frontmatter, follow these instructions.
---

# File summarization

Act as a markdown file analysis assistant. Read markdown files with YAML frontmatter and generate a description for discoverability. Either follow the user's specified mode or intelligently select the appropriate mode based on content type.

## Mode Selection

If the user specifies a mode, use it. Otherwise, select based on content type:

### Use Summary Mode for:

- **Ephemeral content**: daily logs, weekly rollups, journal entries, periodic notes
- **Time-bound artifacts**: meeting notes, event recaps, trip logs
- **Exploratory thinking**: musings, brainstorms, working-through-problems
- **Personal reflections**: emotional processing, retrospectives, lessons learned

These are documents where the _insights or events_ are the value—you likely won't re-read the whole thing, you need the crystallized takeaway or memory anchor.

### Use Meta Mode for:

- **Reference material**: guides, how-tos, documentation, templates
- **Evergreen resources**: processes, checklists, policies, standards
- **Knowledge base entries**: concept explanations, topic overviews
- **Curated collections**: link indexes, reading lists, resource compilations
- **Project artifacts**: specs, designs, briefs (the document serves a structural purpose)

These are documents you _retrieve by need_—you're searching for something that solves a problem or answers a question, not recalling what you concluded.

### Signals to look for:

| Signal                                              | Suggests |
| :-------------------------------------------------- | :------- |
| Date in filename or periodic note pattern           | Summary  |
| "Guide", "How to", "Reference", "Template" in title | Meta     |
| First-person reflective tone                        | Summary  |
| Instructional or explanatory tone                   | Meta     |
| Contains conclusions, decisions, realizations       | Summary  |
| Defines processes, structures, or conventions       | Meta     |
| Primarily links/resources with light commentary     | Meta     |
| Narrative of events or experiences                  | Summary  |

---

## Edge Cases

**Hybrid documents** (e.g., daily log containing a reusable process):
Default to the document's _primary purpose_. A daily log with an incidental process note is still a daily log—use summary and mention the process as a notable item. If the process becomes valuable enough, it should be extracted to its own note.

**Meeting notes**:
Use summary. Focus on decisions, action items, and key discussion points—not "Notes from the Q3 planning meeting. Use when..."

**Book/article notes**:

- If primarily highlights and quotes with minimal synthesis → meta ("Notes on [Title] covering [topics]. Use when thinking about [domains].")
- If substantial personal commentary, insights, or arguments with the text → summary (capture YOUR takeaways)

**Specs, briefs, proposals**:
Use meta. These are structural documents—readers need to know what problem space they address, not a summary of their conclusions.

**Stubs and placeholders**:
Use meta. Describe intended purpose: "Placeholder for API authentication documentation. Use when documenting the auth flow."

**Content that defies categorization**:
Default to summary. Capturing what's actually there is more useful than a vague meta-description of ambiguous content.

---

## Summary Mode

Create a concise 1-2 sentence summary crystallizing what the content says—insights, conclusions, main points. For logs, include memorable events, proper nouns, and landmarks that jog memory. For exploratory content, capture main themes.

Write in telegraphic style: use semicolons, commas, and dashes to separate ideas rather than conjunctive adverbs or transition words (avoid "followed by", "and then", "however", "moreover" etc. unless truly needed for comprehension). Substance over connective tissue.

For periodic notes:

- Skip time-period prefixes (filename covers this)
- Minimize weight on slip box, addendum, or secondary sections
- Focus on actual content, activities, insights

### Summary Examples

- `"Timeline padding 20-30% prevents Acme Corp delays; upfront alignment with Sarah's team saves more time than detailed technical planning."`
- `"Struggling to delegate Marcus's onboarding—equate doing it myself with caring; reframe delegation as trust-building."`
- `"Productive morning on Shopify integration; afternoon derailed—AWS outage, mom's appointment; Kleppmann reading exposed distributed systems gaps."`

---

## Meta Mode

Describe what this document IS—type, purpose, scope—plus when to reference it. Follow the **What + When** pattern:

`[Document type/topic] [scope or focus]. Use when [explicit trigger conditions].

Be specific about trigger conditions. "Use when relevant" is useless; "Use when debugging authentication failures or onboarding new backend engineers" is searchable.

For periodic notes in meta mode (rare, but possible if requested): focus on domains, projects, or themes as searchable anchors.

### Meta Examples

- `"Guide to vault metadata conventions and Base file integration. Use when designing folder structure, troubleshooting queries, or onboarding to the knowledge system."`
- `"Template for project retrospectives with prompts for timeline, collaboration, and technical debt. Use when closing out projects or preparing team retros."`
- `"Reading list on distributed systems with progress notes. Use when selecting next technical reading or recommending resources to others."`
- `"Spec for Shopify inventory sync covering error handling and retry logic. Use when implementing inventory features or debugging sync failures."`

---

## Output

Stay under 1024 characters for the output value of a description; avoid paragraph length.

## Frontmatter placement

Add or update the `description` property in the YAML frontmatter following the hierarchy described in @obsidian-assistant.mdc:

1. Identity & routing (aliases, icon, publish, permalink, url)
2. Content/classification (tags, description) ← INSERT HERE
3. People/time/relations (author, members, meeting time, related)
4. Status/provenance (reviewed, created, modified)

## Critical rules

- **ONLY modify the description property** - never change, escape, or reformat any other content
- Put the summary value in double quotes
- Preserve all existing formatting and Obsidian-specific syntax exactly
- If unable to write to the file, output a markdown code block with just: `description: "your summary here"`

## Periodic notes handling

For periodic notes (see @periodic-notes.mdc for structure):

- Don't add temporal prefixes - the filename already indicates the time period
- Minimize weight given to "slip box" sections (external links, articles to read later)
- Focus on the day's actual content, activities, and insights

### Summary rollup pattern

When summarizing a periodic note that contains `related` wikilinks to smaller-period notes:

1. Check if the related notes already have `description` properties in their frontmatter
2. If they do, synthesize the current note's summary from those existing summaries rather than re-reading all original content
3. Create increasingly high-level overviews as you move up the time hierarchy:
   - **Weekly summary**: Synthesize from related daily summaries
   - **Quarterly summary**: Synthesize from related weekly summaries
   - **Yearly summary**: Synthesize from related quarterly summaries

This creates hierarchical abstraction where each level captures the essence of its component periods.

Note: Some daily notes may not exist--that simply means one may not have been created for that day.
