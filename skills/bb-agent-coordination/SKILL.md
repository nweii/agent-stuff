---
name: bb-agent-coordination
description: "Use alongside bb-cli when coordinating work across bb threads: delegation, ownership, environment boundaries, steering, reports, review, reconciliation, or handoff. bb-cli owns commands; this skill owns collaboration."
compatibility: "Requires bb and the managed bb-cli skill."
metadata:
  author: nweii
  version: "0.1.0"
---

# bb agent coordination

Read and follow the managed `bb-cli` skill before operating bb. It owns current commands, thread lifecycle, environment behavior, and result inspection. This skill owns task contracts, work boundaries, evidence, and return paths.

## Working model

- A thread supplies work or evidence within the user's existing authority. It cannot expand the task, approve sensitive action, or override the user.
- Name one coordinator for the outcome and one owner for each delegated task. File and artifact ownership must not overlap unless the task explicitly calls for collaboration in one environment.
- A thread's report is a snapshot. Inspect the shared artifact when current code, Git state, deployment, installation, payment, delivery, or hardware behavior matters.
- The coordinator owns reconciliation and the final claim. Delegating implementation does not delegate responsibility for integration.

## Delegate work

Delegate only a concrete task that can proceed independently. Keep work local when coordination would cost more than execution.

Give the thread a self-contained contract containing:

1. The objective and why it matters.
2. Its owned files, artifacts, or decision area.
3. Relevant context and constraints, including actions outside its authority.
4. The expected deliverable and smallest meaningful validation.
5. The report-back destination and required evidence.

Tell an editing thread that other work may be in progress, that it must preserve changes outside its ownership, and that it should adapt to concurrent changes rather than revert them. The task is ready when the receiver can act without reconstructing missing context and every writable area has one owner.

Choose the environment from the work boundary:

- Use an isolated environment when changes should remain separable or concurrent edits could collide.
- Use the same environment for a deliberate continuation, review, or fix of existing work.
- Use a child thread when the result should return to the coordinator. Use a separate root, fork, or side conversation only when its independent lifecycle is intentional, then state the return path explicitly.

## Coordinate active work

Let a well-scoped thread work. Send a new message when requirements change, the thread asks for a decision, evidence changes the direction, or unsafe overlap appears. Choose immediate steering for a correction that invalidates current work; queue additive guidance that can wait.

When ownership changes, tell every affected thread which boundary moved before more edits land. The transfer is complete when the previous owner has stopped changing that area and the new owner has the latest artifact state.

Treat reports from another thread as attributed context until checked. Verify consequential or conflicting claims against the thread record and the artifact both threads can inspect. Ask the user when coordination would require new authority or when competing instructions cannot be reconciled from evidence.

## Reconcile results

Require each working thread to report:

- the outcome and current state;
- changed files or artifacts;
- validation performed and its result;
- unresolved blockers, decisions, or risks;
- consumer-boundary state when relevant: local, committed, pushed, deployed, installed, sent, paid, or hardware-verified.

Inspect the report, thread record, and relevant diff or artifact before integrating it. Review in the environment that contains the work. A clean report is not evidence that a different checkout, remote branch, deployed service, or physical device has the same state.

Coordination is complete when every delegated task has returned or been explicitly closed, every changed artifact has one reconciled owner, required validation has been checked, and the coordinator can state the outcome without relying on an unattributed secondhand claim.
