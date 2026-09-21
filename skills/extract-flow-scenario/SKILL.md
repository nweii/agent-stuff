---
name: extract-flow-scenario
description: "Use when extracting an actual workflow, user journey, or operational scenario from a conversation into a sequence of actors, state changes, and pain points."
argument-hint: "[flow-scenario]"
disable-model-invocation: true
metadata:
  author: nweii
  version: "1.0.1"
---

When asked to document a workflow or scenario, output a fenced markdown code block containing a numbered list. Rules:

- **Title:** Begin with a concise descriptive heading capturing the subject, action, and key conditions (e.g., "[Entity/Subject] [Specific Action] ([Key Context/Condition])").
- **Specificity:** Document the _actual, specific_ scenario that occurred. Do NOT generalize or abstract into a generic workflow. This is a single building block. Include real names, identifiers, tool/platform names, and exact values where known.
- **Inline Structure:** Make retrieval easier by using bold formatting or inline tags (e.g., `Trigger:`, `Actor:`, `Outcome:`, `State Change:`) to call out when the flow starts, who does what, and when a state handoff occurs.
- **Optional Metadata:** If the user explicitly asks for a metadata block (or "properties"), include a brief block at the top of the flow detailing the `Trigger`, `Actors`, and `Outcome`. Ignore this block unless requested.
- **Structure:** Use nested indents (4 spaces) for sub-steps, alternative paths, and conditional branches (e.g., "If X... / If Y..."). Keep step language terse and direct.
- **Epistemological Honesty:** Document _only_ what was described. If you notice a logical gap or missing technical step in the context, do not silently invent it. Instead, **pause and ask the user for clarification in the conversation** before generating the final markdown block. This saves tokens, makes the process more collaborative, and prevents the need to continuously regenerate complex outputs.
- **Pending States:** Leave open-ended flows with a final pending step noting exactly what input or event is awaited before the flow can continue.
