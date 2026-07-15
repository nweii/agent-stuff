---
name: semantic-compression
description: "Compress wordy language or loosely expressed thinking into a smaller, sharper form without flattening its meaning. Use when revising an explanation, phrase, sentence, paragraph, concept, label, or coined term whose nuance, implication, or texture must survive the edit."
metadata:
  author: nweii
  version: "0.1.0"
---

# Semantic compression

Find the smallest expression that carries the meaning the user needs. Compression may produce a tighter explanation, a vivid phrase, one concrete word, an established term, or a coined expression. Success means preserving the distinctions, implications, and texture that matter in context.

## Process

### 1. Establish the semantic payload

Read the surrounding conversation, source material, and writing guidelines before asking questions. Identify:

- what the expression must literally mean
- what it should imply without stating outright
- its emotional texture and degree of force
- the relationships it must preserve, such as direction, causality, reciprocity, or recursion
- its audience, register, and role in the larger passage
- any distinctions that nearby words or concepts already carry

Infer only what the available context supports. If a missing detail could materially change the result, ask one specific question at a time until the required payload is clear. Do not ask the user to repeat context already available.

This step is complete when you can state what the compressed expression must preserve and what it may discard.

### 2. Separate meaning from wording

Restate the payload internally without borrowing the source construction. Identify accidental bulk: modifiers compensating for a weak noun or verb, repeated implications, abstractions hiding a concrete action, qualifications that no longer change the claim, or several adjacent words pointing at one available concept. Look for a word whose ordinary associations absorb the work of a modifier or explanation.

Keep genuine qualifications. A shorter expression that broadens, hardens, sanitizes, or prettifies the claim is a mistranslation.

This step is complete when every removable part has been distinguished from meaning-bearing detail.

### 3. Generate candidates at useful scales

Search beyond synonyms. Depending on the material, try:

- a direct, tighter explanation
- a concrete verb or noun that absorbs its modifiers
- a vivid phrase that recruits familiar associations
- an established term that names the full concept
- a coined expression when existing language misses an important combination

Generate three to five meaningfully different candidates. Fewer are enough when one established term clearly dominates. Match the surrounding voice; do not import technical, literary, or promotional language merely because it is compact.

This step is complete when the candidates represent distinct compression strategies rather than cosmetic variations.

### 4. Test for semantic loss

For each serious candidate, compare it with the payload from step 1. Note briefly what it preserves, sharpens, changes, or loses. Reject candidates that require the reader to infer something implausible or that erase a distinction the passage depends on.

Prefer the shortest candidate only after fidelity, clarity, voice, and usefulness are satisfied. Stop compressing when the next reduction would make the expression less exact or less alive.

This step is complete when every surviving candidate carries the required payload and its tradeoffs are explicit.

### 5. Recommend in context

Choose the strongest candidate and show it in the full sentence, passage, label, or conceptual statement where it will live. Explain the choice in one or two concrete sentences. Include alternatives only when they preserve different worthwhile shades of meaning.

If the source thought itself is still confused, say what remains unresolved and return to context gathering instead of polishing the confusion.

This step is complete when the user can judge the recommendation in its real context and see any meaningful loss or shift.

## Scale and interaction

For a small phrase with ample context, move through the process silently and answer directly. For a paragraph, recurring explanation, or loosely formed idea, make the semantic payload visible so the user can correct your reading before you compress it. Ask questions when the answer changes the language, not as a ritual.

Compression can also produce a clean sentence that makes an implicit relationship explicit. Sometimes that is the smallest faithful form. Semantic density serves understanding.

## Examples

### A verb that absorbs its modifiers

Source: “She looked over the figures slowly and with great care.”

Payload: Close, deliberate examination rather than a casual glance.

Candidates: “studied,” “scrutinized,” “checked.”

Recommendation: “She studied the figures.” “Studied” absorbs the pace and care without adding the suspicion implied by “scrutinized.”

### Conceptual compression

Source: “The tendency for old instructions and exceptions to accumulate because adding another rule feels safer than removing one.”

Payload: Accumulation caused by asymmetric caution, with an image of layers building over time.

Recommendation: “prompt sediment.” The geological image carries accumulation and age; the surrounding text should define the causal mechanism once if readers will not know it.

### When shorter is worse

Source: “A role across design, engineering, and systems.”

Candidate: “a multidisciplinary role.”

Reject it when the three named domains are the point. The shorter phrase loses the unusual combination that makes the claim useful.

### Preserving a relationship

Source: “Research changed the proposal, and the revised proposal changed what the team researched next.”

Candidate: “Research informed the proposal.”

Reject it when the feedback loop matters. The candidate preserves influence in one direction while erasing the return path. A faithful compression must encode reciprocal or iterative influence, even if that requires more words.
