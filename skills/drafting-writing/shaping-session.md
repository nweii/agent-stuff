# Shaping session

Take a markdown file of raw material and shape it into a finished piece through a conversational session. The input pile can be anything — a fragments file from [fragment-mining.md](fragment-mining.md), a wall of unstructured prose, a transcript, tidy notes. Read it end-to-end before doing anything else.

The session produces a separate document. The raw material file is read-only — never edit it. If the user did not say where to save the piece, ask once. When the input is itself a draft the user is revising, rework it in place (still block by block) unless they want a fresh piece grown from it.

## Two stances

Pick the stance with the user before starting; it sets how the piece grows.

- **Argument-led** (default): the piece builds a case. Openings imply theses; each block must earn its place in the argument.
- **Journey-led**: the piece is a narrative. It moves beat by beat, choose-your-own-adventure style, and ends when the journey feels complete — not when the pile is empty.

## Argument-led loop

1. **Read the pile.** Form a sense of what's in it.
2. **Discuss 2–3 candidate openings.** Each should imply a different thesis or angle — a sketch or a quoted fragment from the pile is enough. Each candidate is really a question: is *this* what the piece is about? The user picks one, composes a hybrid, or writes their own version. The chosen opening defines what the rest of the piece must do.
3. **Grow paragraph by paragraph.** After the opening lands, ask "given this opening, what does the reader need to hear next?" Pull material from the pile to answer. Argue about whether the next beat is a paragraph, a list, a table, a callout, a quote, a code block — each format choice deliberate and defensible.
4. **Append to the piece as you go.** Don't batch. Write each agreed block immediately so the user can see the piece taking shape.
5. **Loop step 3 until done.** The user decides when it's done.

## Journey-led loop

A beat can set a scene, land a point, pose a question, drop an aside, twist the angle, etc. A beat is sized by what it needs: a single sentence, a short paragraph, or several paragraphs if it's a self-contained vignette. If a "beat" needs five paragraphs and three subheadings, it's two beats glued together — split it.

1. **Discuss 2–3 candidate starting beats** drawn from the raw material, each a different entry point. Prod the user for where each might lead, as if the user is seeing a little way down the path. The user picks one or gives their input.
2. **That beat gets written — only that beat, never ahead.** The user writes it with you questioning, or you draft it for them to rework.
3. **Re-read the file, then consider 2–3 candidate next beats**
4. **Loop until the journey reaches a natural end.** Leftover fragments are fine; that is the point of having more raw material than you need. If the user substantially edits a previous beat, let it change what comes next.

## Conversational feel

This is the grilling session inverted. What is this piece actually arguing (or where is this journey going), and in what order does the reader need it? Push back. Be wary of weak transitions. If a block doesn't earn its place, cut it.

Consider things like:

- "What does this paragraph do for the reader that the previous one didn't?"
- "If I cut this, what breaks?"
- "Is this prose, or should it be a list? Why prose?"
- "This sentence is doing two jobs — split it or pick one."
- "The opening promised X. We've drifted to Y. Either re-thread it or change the opening."

## Ordering by dependency

When asking "what does the reader need to hear next?", check the candidate block's dependencies against what the piece has already established. When restructuring, sketch the section order, confirm it with the user, then grow within it. Splitting an overlong paragraph often reveals a hidden dependency that wants its own block.

## Pulling from the pile

Treat the raw material as a quarry, not a script. Prefer the pile's own sentences over paraphrase.

If the piece needs something the pile doesn't have — an example, a transition, setup for a concept — name the gap explicitly and let the user fill it: "We need an example here and the pile doesn't have one — give me one now or we cut this section."

## Format arguments 

When choosing how to render a block, weigh these tradeoffs out loud with the user, not silently:

- **Prose vs. list.** Prose carries argument; lists carry parallel items. If items aren't truly parallel, prose is better. If they are, a list is faster to scan.
- **Inline vs. callout.** Tips, warnings, and asides go in callouts (`> [!TIP]`, `> [!NOTE]`) — but only if they'd genuinely derail the main argument inline. Otherwise leave them inline.
- **Table vs. repeated structure.** If the same shape repeats 3+ times with the same fields, a table. Otherwise prose with bold leads.
- **Quote vs. paraphrase.** Quote when the original wording is the point. Paraphrase when only the idea matters.
- **Code block vs. inline code.** Multi-line, runnable, or illustrative → block. Single token or identifier → inline.