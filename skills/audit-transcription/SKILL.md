---
name: audit-transcription
description: "Audit auto-generated transcripts for mistranscriptions. Use when the user asks to audit or clean up a Granola, Whisper, or other machine transcript, or to resume pending items in a note's transcription notes."
metadata:
  author: nweii
  version: "1.2.0"
---

# Audit transcription

## Posture

Auto-transcribed text is noisy in domain-specific ways. The user almost always knows what they actually said; you don't. **Your job is to flag, not to correct.** Every interpretation is a hypothesis until the user confirms it.

You will be wrong about some flags even when you're well-grounded in context. That's fine — it's expected. What's not fine is silently applying corrections the user hasn't seen.

## Workflow

### 1. Read the whole transcript before flagging anything

You can't tell what's mangled until you know the topic and shape. Skim end-to-end first.

### 2. Pull in domain context the user has documented

Before guessing at vocabulary, check what's actually in the user's world:

- Project notes, AGENTS.md / CLAUDE.md, glossaries
- Related notes the transcript references
- Recent commits, working logs, specs

If a transcribed proper noun doesn't match anything in their documented vocabulary, **don't substitute a similar-sounding name from your own knowledge** — flag it and ask.

### 3. Triage into three confidence tiers

| Tier | Example | What to do |
|------|---------|------------|
| **High — recurring vocabulary** | A phonetic mishearing of a domain term that appears throughout the transcript (e.g. a tool, product, or library name consistently rendered as a similar-sounding non-word) | Propose find/replace |
| **Medium — sentence-level gist** | A garbled clause whose meaning is recoverable from context | Propose your interpretation **as a question**: "I think you were saying X here — does that match?" |
| **Low — unrecoverable** | A sentence where multiple consecutive words are nonsense and the surrounding context doesn't pin down what was being said | Flag as garbled. Do not reconstruct. |

### 4. Settle the high tier

If the user has already authorized applying high-confidence edits, apply them (step 6) and report what changed in a short list. Otherwise show the high-tier list and wait for their pass. Authorization covers the high tier only; medium and low readings wait for the walkthrough.

Treat every correction the user gives, here or in the walkthrough, as a context update: apply it across the rest of the transcript before continuing.

### 5. Walk through the medium and low tiers

Write for a user who has neither the note open nor the passage in memory. Say how many medium and low items remain and ask whether to walk through them now or set them aside. If they set them aside, go to step 7.

In the walkthrough, send one item per message. Each message stands alone and carries:

- **Where it falls:** who is speaking and what the conversation is about at that point, in a sentence.
- **The passage:** the original span, quoted with the line before and after it.
- **Your reading:** for a medium item, your interpretation and the evidence for it. For a low item, say that nothing in the transcript or the user's notes recovers it.
- **The question:** answerable in a word or two: confirm, correct, leave as transcribed, or delete.

Apply each answer before sending the next item. "Skip" leaves an item pending. "Stop" ends the walkthrough; the remaining items stay pending.

The walkthrough is done when every item has an answer or the user has stopped it.

### 6. Apply edits

- **High tier and confirmed vocabulary:** inline find/replace.
- **Confirmed sentence-level readings:** a callout above the passage, with the original kept intact beneath it:

```markdown
> [!warning] Transcription note (Garbled)
> gist: <the confirmed reading of what was being said>

<original text left intact>
```

- **Deletions:** only where the user asked for one.

Pending items stay as transcribed. Never strip the raw transcript.

### 7. Record the audit after the transcript

Add a `## Transcription notes` section after the transcript. It holds:

- A note that the transcript is auto-generated
- The recurring-vocab glossary
- Each applied correction, with its original span
- Each pending item, with its original span, proposed reading, and evidence
- A pointer to the callout format used for confirmed readings

When nothing is pending, fold the section's body into a collapsed callout (`> [!note]- Transcription audit record`). If the note already has a notes section above the transcript, move it below.

Update the frontmatter `description` to mention auto-transcription, the notes section, and whether items remain pending.

The audit is recorded when the notes section sits after the transcript and every item has an explicit status.

## Anti-patterns

- **Don't guess at proper nouns from your own knowledge.** A name that sounds plausible to you may be invented. Flag, ask.
- **Don't rewrite garbled sentences with confident prose.** Even when you think you know what was said, write the gist as a hypothesis in a callout, not as edited dialogue.
- **Don't keep pushing a guess after the user corrects you.** The correction itself is information about how they think — incorporate it into how you flag the rest.
- **Don't claim you've recovered something you haven't.** If a clause is gone, mark it `[transcription unintelligible]` rather than fabricating.

## When the user is the only source of truth

If you can't ground a flag in any documented context — no glossary, no project notes, nothing in the codebase — say so explicitly when surfacing the flag. Frame it as "no idea what this is, and nothing in your notes resolves it" rather than producing a confident-sounding guess. The user will tell you, and that's the right division of labor.
