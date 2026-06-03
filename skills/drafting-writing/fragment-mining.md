# Fragment mining

Run a grilling session that produces fragments i.e., raw material for a future piece. Interview the user relentlessly about whatever they want to write about. Do not impose phases, outlines, or structure; structure comes later (see [shaping-session.md](shaping-session.md)).

As fragments emerge from either side of the conversation, append them to a single markdown file. If the user did not pass a path, ask once where to save. Capture fragments from the very first thing the user says, including the initial prompt. Only append; cutting is the user's call.

## What is a fragment

A fragment is any piece of text that might survive into the final piece. It must be readable by the author — they can tell what it means — but it does not need to define its terms or be comprehensible to a cold reader. The bar is "is this a piece of good writing?", not "is this a self-contained argument?"

Fragments are deliberately heterogeneous:

- A sharp sentence to deploy somewhere, destination unknown.
- A claim with a one-line justification.
- A vignette: a thing that happened, a code snippet, a scenario, an analogy.
- A half-thought: "something about how X feels like Y, work this out later."
- A quote, a piece of dialogue, an overheard line.
- A cluster of related observations that hang together by feel.
- A complaint, a confession, a punchline.

It's like a novelist's diary: years of unstructured noticings, mined later for raw material.

## Grilling

Use the questioning tactics from [question-modes.md](question-modes.md) weighted toward Concretizing, Adding heft, and Exploring; use Clarifying only to make a fragment capturable, not to resolve it — half-thoughts are valid fragments. Skip the Structural and Prioritizing tactics; those belong to shaping.

## File format

```markdown
# Working title

A first fragment lives here.

It can be multiple paragraphs. It can include lists, code, quotes — whatever
shape the fragment naturally takes.

---

A second fragment.

---

> A quoted line the user wants to keep around.

A reaction to it.
```

On first write, start the file with just an H1 working title (it can change later). Separate fragments with a horizontal rule (`\n---\n`); skip metadata, headings, and tags, and keep fragments in the order they arrived.

