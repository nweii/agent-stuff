# Reflection mode

Review the current session for durable changes to the skills that own its workflows. Prefer an existing skill over another entry point. A valid outcome is no proposed edits.

Adapted from [Lauren Tan (poteto)'s pstack reflect](https://github.com/cursor/plugins/blob/e5a8186d7b43be8d6ac4452440fbead5f1a51c70/pstack/skills/reflect/SKILL.md), including its judgment, tooling, divergent, and synthesis prompts. The [upstream MIT notice](../LICENSE.pstack) accompanies this adaptation. This mode uses the active agent's tools and source ownership rules, with a local backlog instead of automatic external filing.

## 1. Establish the session evidence

Use the current conversation and its exact transcript path when the environment provides one. Verify transcript identity against the active session ID and opening user request before sharing it. Keep transcript lookup within the active session; unrelated chats and project transcripts are outside scope.

If the exact transcript is unavailable, write a digest containing the relevant requests, corrections, decisions, tool results, and skill paths actually read. Preserve short evidence quotes and state omissions. Reviewers must distinguish digest evidence from facts they cannot check.

Identify the skills and tools actually used, plus visible skills that should have triggered. Resolve each skill to its canonical source and privacy tier before proposing an edit. Installed copies provide execution evidence, not the edit destination.

Completion: the evidence belongs to this session, every candidate skill has a source owner, and any evidence gaps are explicit.

## 2. Review through three lenses

Read [reflect-reviewers.md](reflect-reviewers.md). Spawn three independent reviewers in parallel using its shared contract and the judgment, tooling, and divergent lens respectively. Give each the same transcript or digest and the candidate source paths. Reviewers return findings without editing files, committing, or writing to external systems. Read access to referenced tools remains available.

Use the active environment's supported subagent APIs and configured models. Prefer model diversity when available. Preserve independent reviews even when only one model is available, and disclose that limitation. If subagents are unavailable, perform three separately labeled passes and report that independent review was unavailable.

Completion: each lens returned evidence-backed findings or an explicit no-findings result; failed reviews are named.

## 3. Synthesize and check the target guidance

Have a separate synthesizer use the synthesis contract in [reflect-reviewers.md](reflect-reviewers.md), with all reviewer findings and the session evidence. If a separate agent is unavailable, synthesize inline and disclose it.

Read the canonical target skill and the specific reference or script each proposed change would affect. Classify every finding:

- **Proposed edits:** a durable gap or weak instruction with an exact target and concrete replacement text or patch. A visible skill that failed to trigger may need its description tuned rather than more body text.
- **Rejected:** transient facts, speculation, duplication, unrelated targets, or guidance that already says the right thing clearly. Name the reason. Execution failure alone does not justify adding the same rule again.
- **Backlog:** a correction better enforced by a lint rule, script, metadata flag, or runtime check; a tooling limitation; or a dependency the current scope cannot settle. State the mechanism and owning artifact.

Apply the durability, decision-changing, existing-skill-first, and structural-enforcement checks from the synthesis contract to every row. Findings echoed by multiple reviewers carry more confidence; a single reviewer's finding must stand on strong evidence. The parent checks the synthesized proposals against the actual target files before presenting them.

Completion: every finding has a disposition, every proposed edit has reviewed source text, and structural fixes have a concrete owner rather than a prose substitute.

## 4. Present a reviewable result

Return three compact groups: Proposed edits, Rejected, and Backlog. For each proposal, give the observed problem, session evidence, canonical file and section, and exact proposed edit. Keep confidential evidence in private artifacts; public skill text must stand alone without private quotes, paths, or project details.

Present the proposals before changing reusable instructions. Wait for approval of the selected edits unless Nathan already authorized applying session learnings within this scope. An invocation of reflection alone authorizes review, not application. Keep backlog items in the response or an authorized local planning artifact. File external issues only when Nathan requests it.

Completion: Nathan can approve or reject individual concrete edits without needing another drafting pass. If no proposals survive, say why and stop.

## 5. Apply the authorized subset

Re-read each approved target before editing, preserve unrelated changes, and apply only the authorized findings to canonical source. Read [authoring.md](authoring.md) for skill changes and [privacy-and-migration.md](privacy-and-migration.md) when placement changes. Substantial changes use writing-for-agents and the repository's existing validation workflow. A new skill needs recurring evidence and a distinct responsibility no existing skill owns.

When installation is authorized, follow [installation.md](installation.md). A reflection request does not itself authorize installation or publication. Keep this skill's publish boundaries in force.

Completion: approved changes pass structural checks, relative references resolve, and generated artifacts follow their repository workflow. Report applied files, unapplied proposals, and verified commit, publish, and installation states separately.
