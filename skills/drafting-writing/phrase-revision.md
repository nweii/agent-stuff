# Phrase revision

Targeted help for tightening a specific wordy phrase or sentence. Invoke when the user has a draft and points at a particular limp phrase, or when they ask for "a better way to say this." For broader passes (whole paragraph, section, piece), stay in the main `drafting-writing` flow.

## When to use

- User pastes a sentence and asks for a tighter version
- User flags a specific phrase as wordy or weak
- User is mid-draft and asks "what's a better word for…"
- User wants to consider alternatives before locking a phrasing

## Process

### 1. Identify the target phrase

If the user named a phrase to focus on, use that. Otherwise pick the wordiest phrase that could be made more concise — usually a multi-word adverbial or prepositional construction doing the work of a single verb.

Classify lightly: adverbial (`in a very quick manner`), prepositional (`with great care`), adjectival (`of a complicated nature`), nominalization (`carry out an investigation` → `investigate`).

### 2. Generate 3–5 candidate replacements

Each candidate gets a short rationale — one clause is enough. Vary the register: at least one candidate that's a near-literal swap, one that leans on a sharper verb, one that shifts the rhythm.

Account for any context the user provided:

- **Genre** — match conventions (noir verbs differ from technical verbs)
- **Emotion** — capture both obvious and subtle ways to convey the feeling
- **Technical level** — precision vs accessibility
- **Audience** — adjust vocabulary and complexity

If the user gave no context, skim the surrounding sentence for register cues before suggesting.

### 3. Recommend a top choice + show the revised sentence

Pick one. Show the full sentence with the replacement substituted in, so the user can read it in flow.

### 4. Iterate if asked

If the user wants more options, more in a particular direction (more formal, punchier, more technical), or pushback on your top pick, refine.

## Output format

```
Targeted phrase: [the wordy phrase]
Type: [adverbial / prepositional / adjectival / nominalization / other]

Candidates:
1. [replacement] — [brief rationale]
2. [replacement] — [brief rationale]
3. [replacement] — [brief rationale]
[optional 4–5]

Top pick: [your choice]
Revised: [full sentence with replacement]
```

## Notes

- Single words beat short phrases beat longer phrases, all else equal
- Don't trade wordiness for jargon — `bottlenecked` is fine, `optimally throughputted` is not
- Preserve the original sentence's tone; a noir thriller doesn't want a corporate verb
- If the user has a recurring weak construction (lots of `in a [adj] manner`), surface the pattern so they can fix others themselves

## Related

- If the user discovers a replacement worth keeping (a coined term, a phrase worth remembering), offer to save it wherever they keep such things — a terms note, a snippets file, or whatever their system provides.
