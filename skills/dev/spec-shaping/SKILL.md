---
name: spec-shaping
description: "Shape product ideas into actionable specs and sprint plans. Use when interviewing about a product plan, breaking specs into sprints, or turning vague ideas into well-scoped work."
metadata:
  author: nweii
  version: "1.0.0"
---

# Spec Shaping

Transform product ideas into well-scoped specs and actionable sprint plans. This skill supports two complementary phases:

1. **Interview phase**: Probe the problem space until a clear, narrow spec emerges
2. **Sprint breakdown phase**: Decompose a spec into atomic tasks and demoable sprints

## When to Use

- User has a rough product plan or idea that needs scoping
- User needs help thinking through implementation details, UI/UX, or tradeoffs
- User has a spec ready to break into sprints and tasks
- User wants to validate whether a problem is well-framed before building

---

## Phase 1: Spec Interview

Read the plan file and interview the user in detail about technical implementation, UI & UX, concerns, tradeoffs, etc. Make sure questions are not obvious.

### Interview Principles

1. **Narrow before expanding**: Push to narrow the problem until it can be described in one clear sentence. Vague scope ("build a calendar") leads to endless shaping. Precise scope ("show empty time slots between existing events") enables real solutions.

2. **Surface complexity early**: Ask "what could make this harder than it sounds?" and "where are the hidden dependencies?" The goal is to reveal time bombs before they're in the middle of a build, not after.

3. **Distinguish understanding from justification**: Watch for the anti-pattern where someone has already decided what to build and is looking for data to justify it. Ask why this problem matters *before* discussing solutions.

4. **Probe the adjacent user**: If this is user-facing, ask who the *next* user is — the one just outside the current target. What would need to be different for them?

### Interview Process

Be very in-depth. Continue interviewing until you're confident the problem is well-framed and the key risks are surfaced. Then write the spec to the file.

A good spec should be **shapeable** — someone should be able to read it and describe the solution in ≤9 major components. If they can't, the problem isn't narrow enough yet.

---

## Phase 2: Spec to Sprints

Read the spec file and break the project down into sprints and tasks.

### Core Principles

1. **Atomic tasks**: Every task should be an atomic, committable piece of work that can be completed, reviewed, and merged independently.

2. **Demoable sprints**: Every sprint should result in a demoable piece of software that can be run, tested, and built on top of previous sprints.

3. **Clear validation**: Each task must include explicit validation criteria — tests where applicable, or another concrete verification method (e.g., "Validation: API returns 200 with expected payload", "Validation: Component renders correctly in Storybook").

4. **Dependencies first**: Order tasks so dependencies are completed before the work that relies on them.

5. **Fixed time, variable scope**: Sprints are time-boxed *appetites*, not scope commitments. If something doesn't fit, shape it smaller — don't extend the timeline.

6. **Budget for understanding**: Reserve ~10-20% of sprint capacity for de-risking future work — spikes, research, or validation that will speed up the *next* sprint.

### Output Structure

Structure your output so it remains malleable as the project evolves:

- **Stable identifiers**: Give tasks IDs (T1, T2, etc.) so they can be referenced and reshuffled between sprints without losing context.
- **Traceability**: Link tasks back to spec sections so changes to the spec can be traced to affected tasks.
- **Visible dependencies**: Make it clear which tasks depend on others.

Adapt the specific format to what makes sense for this project — a simple list may suffice for small projects, while complex projects might benefit from a task registry table with sprint groupings. Use your judgment.

### Sprint Breakdown Process

1. Read the spec thoroughly. Identify natural section boundaries for traceability.

2. Create the task registry first — focus on atomicity and dependencies.

3. Group tasks into sprints, ensuring each sprint is demoable.

4. Self-review with these lenses:
   - Are any tasks too large to complete in a single focused session?
   - Are there missing or circular dependencies?
   - Is each validation criteria concrete and verifiable?
   - Could a developer pick up any task and know exactly what "done" looks like?
   - Does each sprint have a clear demo scenario?
   - **Shaping smell test**: Can you describe the entire sprint in ≤9 major scopes? If not, the spec may need more narrowing before breaking it into tasks.

5. Revise based on your review.

6. Write the final sprint plan to a markdown file alongside the spec (e.g., if spec is `docs/spec.md`, write to `docs/sprints.md`).

### Explicitly Out of Scope

- **Time estimates**: Do not estimate duration. The human will layer in timeline context.
- **Resource allocation**: Do not assign tasks to people or roles.
