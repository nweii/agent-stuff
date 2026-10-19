---
name: better-work
description: "Use when improving a prompt before execution or revisiting work the user finds too shallow."
metadata:
  author: nweii
  version: "0.3.2"
  credit: "Inspired by Josh’s (@jjpcodes) prompt for deepening a task."
---

# Better work

Deepen the approach within the task's existing goal and scope. Identify what would materially affect the result:

1. **Expertise:** Identify the missing domain practice and explain what it would resolve. If the approach is already sufficient, say so.
2. **Source material:** Identify the original material needed to address the gap, such as code, transcripts, records, or observed behavior. Use it directly where available; state any access limits.
3. **Methods:** Name the specific methods and tools suited to the gap and explain what each would establish.
4. **Evidence:** Define an observable check tied to the intended outcome and what would count as success. If no independent check is available, state the remaining uncertainty.

Present these findings briefly, then follow the applicable branch.

## Improve a prompt before execution

Rewrite the supplied prompt to include the identified source material, methods, and success criteria. Preserve the user's goal and constraints. End with the rewritten prompt; leave execution to a separate request.

## Revisit work in progress

1. Rewrite the task brief using the original request, the user's feedback, and the findings above.
2. If the brief changes the goal, widens the scope, or requires a decision, spending, or access beyond existing authorization, show the brief and wait for the user's go-ahead. Otherwise continue.
3. Revise or extend the existing work to satisfy the brief. Use the identified source material and methods, preserving work that already meets the brief.
4. Run the outcome check defined under **Evidence**. Report what it showed and any remaining uncertainty. If the check cannot run, state the specific blocker and leave verification open.
