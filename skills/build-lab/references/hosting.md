# Hosting other work in a lab

Read this when a lab will hold something other than a tuning panel: a state machine, a model of a flow, a round of variants, a prototype, or any artifact another skill or tool produces. Read it too when the project or the session brings a skill that produces such an artifact.

The lab section stays the same whatever a lab holds. This skill owns the parts every lab shares: the folder, the page and its metadata, the sidebar, exposure, and the freeze lifecycle. The skill or tool that produces the artifact owns the artifact: its procedure, its vocabulary, its rules for what makes it correct, and its definition of done. Follow that skill for the work itself, and use this reference only to fit the result into a lab.

## The adapter

Before building, write down four mappings between the artifact and the lab. Keep them in the lab's description or a comment at the top of its client component, in the other skill's terms.

| Lab part | The question it answers | Tuning panel (the default) |
| --- | --- | --- |
| Canvas | What does the page render, at full size? | The production component |
| Controls | What can someone change, and in whose terms? | Visual values from the production module |
| Outcome | What did the lab decide, stated the way the artifact's skill would state it? | The accepted values |
| Capture | What does a frozen record keep so the decision still reads without the code? | A screenshot at the accepted values |

Some guidance for filling it in:

- **Canvas.** Render the real thing when one exists. When the artifact describes a component, put the two side by side so the reader can check one against the other.
- **Controls.** Expose the inputs the artifact's skill treats as variable, such as a model's constants, a variant's axis, or a guard switched on or off. Leave out anything that skill treats as fixed. When the artifact comes from a tool that can't run in the page, precompute its outputs at build time or serve it from a development-only route, and say which in the lab.
- **Outcome.** Use the artifact's own language, such as "variant B adopted" or "rules 1–3 hold, rule 4 breaks on the retry path". A reader of the frozen record should not need this skill to understand it.
- **Capture.** Pick what still makes sense once the code is gone. That might be a screenshot, a short clip, or the artifact's own text form, such as a chart's source. The record page shows captures, so when a text form is the clearer capture, extend the formats the record and its page accept rather than flattening the text into an image.

## Where the artifact's files live

- If production uses it, it stays in production and the lab imports it. Defaults flow from production, the same as a tuning lab.
- If only the lab uses it, it lives in the lab folder. Freezing then removes it with the lab, and the pinned commit keeps it.

## What stays with the host

Rules about which kinds of work belong in the lab section, and what each kind must state, are the project's editorial choice. Record them in the host's agents file next to the lab conventions. The adapter makes such rules checkable, because every lab answers the same four questions. This skill doesn't define the kinds themselves.
