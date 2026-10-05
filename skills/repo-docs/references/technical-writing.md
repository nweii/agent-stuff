# Technical writing

Use this reference when choosing a document's purpose, drafting prose, or reviewing sentences. Apply all four layers: document mode, reader address, one thought at a time, and unambiguous syntax. PR descriptions and commit messages use every layer except document mode.

The reader should understand the text on the first read, even when tired. Cut words that add nothing and choose familiar words unless a technical term adds precision. Keep a sentence that serves the reader better than a mechanical rewrite. Use the codebase's actual symbols, filenames, flags, and commands as the vocabulary for technical details.

## Choose the document mode (Diátaxis)

Choose by the reader's purpose and whether the reader is learning or working:

| Reader's purpose | Learning | Working |
|---|---|---|
| Doing something | Tutorial | How-to |
| Understanding something | Explanation | Reference |

Keep a focused document in one mode. Apply the same test to individual sentences: a sentence that serves another purpose may belong in a linked page. A README or RFC can contain distinct sections with explicit purposes, as described in `SKILL.md`.

### Tutorial

Guide the learner to build something concrete. Open with the thing they will build, then provide a path that succeeds without unstated knowledge. Take responsibility for the learner's success.

Each step produces an observable result. State the expected output, prompt, or log message early and throughout the lesson. Use concrete commands and a shared “we” voice when guiding the learner. Keep necessary explanation to a short clause and link to the full explanation. Put exhaustive reference elsewhere so the lesson keeps moving.

### How-to

Solve a problem the reader has. Name the guide for that task, such as “How to restore a backup.” Assume the reader knows the basics and give the actions needed to reach the goal.

Allow decisions and branches when the task requires them. Put the relevant condition before its action. Link to background, teaching material, and exhaustive options rather than interrupting the procedure.

### Reference

Describe facts, options, limits, and errors for lookup. Match the structure of the API, configuration, command, or other thing being described. Put information where readers expect it and generate it from code when practical.

State verified facts directly and completely. Keep procedures, persuasion, and opinion in their own documents. State an actual limit or uncertainty when evidence requires it; certainty comes from verification.

### Explanation

Answer a real why question about one bounded topic. Use a concept title that makes sense after “About,” and make the explanation readable away from the product.

Explain design decisions, constraints, alternatives, and relevant history when the history helps explain the design. Weigh tradeoffs and give a reasoned view rather than a bare list of advantages and disadvantages. Keep instructions and exhaustive lookup material in linked guides. Historical context belongs here when needed for understanding; adoption and setup copy follow the durability rules in `SKILL.md`.

## Address the reader (Google developer style)

Apply these rules when writing instructions and descriptive prose:

- Address the reader as “you” and use the present tense. Use the future tense for events that happen later. Tutorials may use “we” for shared actions.
- Name the actor when the actor matters. Use passive voice when the actor is unknown or irrelevant.
- Write instructions as direct commands. State facts directly rather than describing what “should be done.”
- Put the condition or goal before the action so readers can skip a step that does not apply. Present the common case before exceptions.
- Use a knowledgeable, conversational voice. Remove buzzwords, figurative language, ceremonial “please,” and claims that a procedure is “simple,” “easy,” or “quick.”
- Document available behavior. Put future plans in the repository's planning material and avoid pre-announcements in user docs.
- Give links the destination's title or a short description. Include enough context on the page for readers to understand the link without opening it.
- Use the heading rules in `SKILL.md`. Write lists in parallel form and introduce each list with a complete sentence. Number sequences and use bullets for unordered items.
- Format code identifiers, paths, and commands as code. Format UI labels in bold. Use serial commas. State that a list is partial instead of ending with “etc.”

## Limit each sentence's load (STE)

Use Simplified Technical English principles to make instructions easy to follow:

- Give each instruction its own sentence and each other sentence one main thought. A condition and its consequence can form one thought.
- Review instructions over about 20 words and other sentences over about 25. Split where a sentence carries separate thoughts or obscures the action. Retain a longer sentence when it stays clear.
- Put a warning before the action it guards, with the consequence stated plainly.
- Keep articles such as “a” and “the” when they make an instruction precise.
- Give each term one meaning and grammatical role, and use one verb consistently for the same action. Use actual code names unchanged.
- Write procedures as commands rather than narration or passive requirements.
- Replace an ambiguous “-ing” form with a direct verb or an explicit clause. Keep an unambiguous form when it reads naturally.

## Resolve ambiguity (Global English)

Check each sentence for competing readings:

- Place “only,” “not,” and similar modifiers next to the words they modify.
- Break long noun chains into explicit relationships. For example, write “the script that checks the import limit.”
- Give “it,” “they,” “this,” and “which” one clear antecedent. Repeat the noun if the pronoun could refer to several things or an entire clause.
- Give each clause its verb. Keep structural words such as “that” when they make the sentence easier to parse.
- Repeat articles when needed to distinguish separate things, such as “the client and the host.”
- Make the grouping of “and” and “or” explicit. Use “both,” “either,” or “if … then” where the grouping is otherwise unclear.
- Prefer periods to semicolons. Use a new sentence instead of an em dash, or a grammatical parenthetical where appropriate.
- Make parentheses a complete phrase or sentence. Write singular and plural forms directly rather than using “(s).”
- Spell out alternatives as “a, b, or both” rather than using slashes in prose. Preserve literal paths, symbols, and names that contain slashes.
- Use one name for each thing across the docs. Keep working wording unchanged when the underlying meaning has not changed.
- Replace idioms, colloquialisms, Latin abbreviations, and metaphors with literal language that a non-native reader, translator, or agent can parse.

## Preserve a natural voice

Read the draft aloud and check for these patterns:

- Mix sentence lengths. A short sentence can establish a point; a longer sentence can carry its condition or consequence. Rejoin clipped sentences when the result stays clear.
- Vary sentence openings without substituting synonyms for established technical terms.
- Prefer specific consequences to vague warnings. Say what fails and under which condition.
- Use literal developer language and define a named pattern when first introducing it. Replace invented jargon with a direct description of the action or constraint.
- Cut filler, AI stock phrases, redundant qualifiers, repetitive framing, and formatting that adds emphasis without meaning. Use the repo-docs audit checklist for the review.

When a revision exposes a recurring jargon or filler pattern absent from the checklist, propose the offending phrase and a concrete replacement in the handoff. Include a proposed checklist diff for a separately scoped update.

## Apply repository conventions

Make PR descriptions a briefing a reviewer can read in under a minute. Explain the problem, the resulting behavior, and relevant validation. Link to detailed run logs, commit lists, or metric tables when needed. Commit messages state the change and its reason in the repository's format. Keep private coordination details out of public artifacts.

Use real paths and symbols in examples, and verify commands against their stated output. Match code indentation to the language and repository so snippets can be copied and run. Where neither sets a convention and the language permits it, use tabs. Counts and directory trees follow the verification step in `SKILL.md`.

Product UI strings follow the product's copy guidelines. Agent-facing instructions follow `writing-for-agents`.

## Worked example

Before:

> Configuration of the export retention enforcement script is performed via exports.json. Note that it is important to remember that running with --prune, which deletes expired exports, should only be done after a preview. If expired, files are removed.

After:

> `prune-exports.mjs` reads the retention period from `exports.json` and lists expired exports. Review the list before you run `prune-exports.mjs --prune`. The command deletes the listed files.

The revision names the actor, preserves the prerequisite, and states the deletion boundary. This fictional example illustrates prose; use commands and behavior verified against the actual project.
