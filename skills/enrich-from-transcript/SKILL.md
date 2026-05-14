---
name: enrich-from-transcript
description: "Enrich an existing meeting/interview note from its transcript, or scaffold one when only a transcript exists. Captures granular narrative, exact phrases, mechanics, casual context, and implicit signals. Run on thin auto-summary notes or transcripts that warrant close reading."
disable-model-invocation: true
metadata:
  author: nweii
  version: "1.0.0"
---

# Enrich from transcript

Two modes, decided from how the user invoked the skill and what they pointed you at:

- **Enrich mode** — there's an existing note (often an AI-summary version) and a transcript. Add depth without overwriting what's there.
- **Scaffold mode** — there's only a transcript. Build a new note from scratch.

If both an existing note and a transcript are referenced, default to enrich mode. If unclear, ask.

## 1. Read the whole transcript first

Read it end to end before writing anything. Skimming misses repeated phrasings, hesitations, and asides, which often matter most.

If there's an existing note, read it too so the enrichment complements rather than duplicates it.

**Auto-generated transcripts** (i.e., from Whisper, Granola, Otter, etc.) may contain mistranscription errors. Don't quote, bold, or read significance into phrases that look garbled or contain weird word choices that may be transcription artifacts. Flag clearly corrupted passages rather than building interpretation around them. If the transcript needs systematic cleanup, treat that as separate work and surface it to the user rather than mixing it into enrichment.

## 2. Apply the six dimensions

Work through these as you read. Not every transcript will yield every dimension — surface what's actually there, do not pad to fill all six.

Whenever your interpretation hinges on something specific in the transcript — a phrase you'd quote verbatim, a number or name, an unusual word choice that seems significant — the auto-transcription may be wrong. Verify against surrounding context before building interpretation around it, and when in doubt, flag rather than interpret confidently.

### Granular narrative detail

Capture the reasoning, examples, and stories shared in the transcript, rather than summarizing them. If someone explained their pricing approach by walking through three customer profiles, write the three profiles, not "we discussed pricing."

A useful check: could the user recall the substance from your notes alone, or would they need to revisit the transcript?

### Personal impressions and takeaways

Where the user felt a parallel, where something felt compelling or surprising, where they sensed flexibility or subtext beneath what was said directly. Write these in first person from the user's POV, marked as impressions, not facts.

If the user hasn't told you their impressions, **ask before writing them in their voice**. You can independently note "the speaker's tone here suggested X" when it's clearly visible in the transcript (long pauses, qualifiers, deflections), but putting words in the user's mouth about how they felt is out of bounds.

### Exact phrases worth preserving

When the other person uses crisp framing — a short phrase that captures something well — quote it verbatim and **bold it**.

Be selective: 2-3 per conversation is often right, rarely more than 5. Bolding everything trains the eye to ignore it. Verify the phrase against the transcript if it sounds awkward — it may be a mistranscription rather than a notable framing.

### Mechanics and specifics

When the conversation describes how something works — sequences, timelines, quantities, conditional rules, named procedures — capture it with enough fidelity that the user could act on the information later without revisiting the transcript. Vague restatements ("they review applications regularly") strip detail the transcript usually contains in concrete form.

Specifics are hardest to reconstruct from memory and most worth being literal about: numbers, dates, names, ordered steps, conditional logic ("if X then Y, unless Z"). They're also the highest-risk mistranscription targets — auto-transcription tools most often mishear specific figures and proper nouns. If a number or name reads as arbitrary or contextually off, flag it as uncertain rather than asserting it.

### Casual and contextual moments

Include relationship-building tangents, origin stories, and social context. The 90 seconds where someone explained how they got into the field, mentioned their kid, or recommended a restaurant often matters as much as the formal agenda.

Thread these in where they belong narratively rather than relegating them to a "miscellaneous" bucket.

### Implicit signals

Note where tone, hesitation, or framing revealed something beyond the literal content. Examples:

- "She was careful not to make promises but the flexibility felt real."
- "He answered the question I asked with the answer to a different question."
- "They brought up X twice in different contexts — felt important to them."
- "The pause before the salary number was the longest pause in the call."

Ground these in something observable in the transcript when you can. If you're inferring from absence ("never mentioned the previous role"), say so.

## 3. Output

### Enrich mode

Edit the existing note in place. Add the enriched material in a way that fits the note's structure — usually as a new section (e.g. `## Beyond the summary`, `## What was actually said`), or threaded into existing sections where it belongs (bolded exact phrases inline within the relevant context).

Treat the existing note as material to preserve, not to rewrite. The enrichment is mostly additive — leave existing content in place. The exception is when a richer entry you're adding fully subsumes a shallower one; you can replace it, but flag the removal so the user can confirm. The bar is no loss of substance, not literal preservation of every bullet.

If the note has a description, summary, or similar metadata field and the enrichment substantively changes what the note is "about," propose a revision and confirm with the user before editing it. Otherwise leave existing metadata alone.

### Scaffold mode

Create a new note. Before inventing structure, look for the user's existing conventions for meeting/interview/transcript notes — naming patterns, where they save them, what metadata format they use. Match what's already there.

If you can't find a clear precedent, ask the user where to save the note and what to call it before generating it.

At minimum, the note needs:

- **Title** that identifies what the transcript is of and when (e.g., `Interview with Jane Doe 2026-05`)
- **Date** of the conversation
- **Participants**
- **A short description or summary** (1-2 sentences) so the note's purpose is clear at a glance
- **Body** organized either by the dimensions above where useful, or in a flowing structure that follows the transcript's actual arc — whichever serves the substance better

Format the metadata according to whatever convention the user's other notes use (frontmatter, no frontmatter, header block, plain prose, etc.).

## 4. Don't fabricate

The interpretive dimensions (impressions, implicit signals) require restraint. Don't invent evidence the transcript doesn't contain, and never put words in the user's mouth about what they felt or noticed.

When in doubt, ask. "I noticed she paused before answering the salary question — did you read that as hesitation or just thinking?" is better than guessing.

## 5. Confirm before committing

For **scaffold mode**, present the note to the user before saving so they can adjust title, scope, or framing.

For **enrich mode**, show the user what you propose to add (and where you propose to thread it in) before committing the edit. The user almost always has impressions of their own — things they noticed at the time that the transcript doesn't show — that they'll want to fold in. Make space for that.
