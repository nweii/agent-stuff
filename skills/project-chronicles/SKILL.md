---
name: project-chronicles
description: Sets up and maintains a two-track documentation system for any project: a working log (implementation decisions, what changed) and usage notes (product/process thinking, what we're learning). Handles both fresh projects and existing ones — detects current structure and adapts rather than clobbing. Use this skill when starting a new project, when adding structured documentation to an ongoing project, when writing a session's working log entry or usage note, or when the user says "set up project docs", "add a working log", "track sessions", or anything about capturing ongoing project context for future sessions.
metadata:
  author: nweii
  version: 1.0.0
---

# Project Chronicles

A two-track documentation system that preserves both implementation history and product/process
thinking across sessions. Built for the reality that future-you (or a future AI session) needs
to orient fast — and that these two kinds of knowledge decay differently.

## The core distinction

**Working log** — what changed and why. Tied to specific files, decisions, commits. Becomes
outdated when the code changes; that's fine, it's a record.

**Usage notes** — what you're learning about the problem, the product, the process. Observations
about how the system behaves, where friction surfaces, what the work wants to be. Stays true
(or worth thinking about) regardless of what's in the code.

**The litmus test:** "Would this note become wrong when the code changes?"
- Yes → working log
- No → usage note

A single session often produces both. Write to each when the session warrants it.

---

## Phase 1: Detect existing structure

Before proposing anything, look at what's already there. Scan the project root for:

- Config files: `CLAUDE.md`, `AGENTS.md`, `.cursor/rules`, or similar agent/session config
- Existing docs directories: `docs/`, `notes/`, `journal/`, `log/`, `.notes/`, or any folder
  that looks like it's collecting session or project context
- Any files that resemble working logs or usage notes (common names: `CHANGELOG.md`,
  `working-log.md`, `notes.md`, `decisions.md`, `ADR/`)

Present what you found. Be specific: name the files and folders, describe what they appear to
contain, and explain how you'd integrate rather than replace.

If an existing docs structure is close to this pattern (even with different names), say so and
ask whether to adapt it or set up alongside it.

---

## Phase 2: Confirm configuration

Propose defaults based on what you found, then confirm with the user. The questions that matter:

1. **Docs root** — where should the working log and usage notes live?
   Default: `docs/`. If something like `notes/` already exists and makes more sense, propose that.

2. **Working log structure** — single file or subfolder?
   The right choice depends on how much the project will accumulate over time.
   - **Single file** (`{docs-root}/working-log.md`) — good default for most projects. Simple,
     low friction, easy to scan. Fine until it gets long enough to be unwieldy.
   - **Subfolder** (`{docs-root}/working-logs/YYYY-QN.md`) — worth it when you expect many
     sessions over months or years and want to avoid one enormous file. One file per quarter
     is a natural cadence. Could also be monthly or per-major-version.
   Ask the user which fits their project's expected lifespan and pace. Default to single file
   unless they know this will be a long-running project.
   If there's an existing changelog or decisions log, ask if it should be converted or kept separate.

3. **Usage notes location** — subfolder name.
   Default: `{docs-root}/usage/`.
   These are typically named by topic or session, not by date — propose freeform naming here.

4. **Session-start config** — which file gets the "read these first" instructions?
   Look at what exists: if there's a `CLAUDE.md` or `AGENTS.md`, propose injecting a section.
   If nothing exists, offer to create one. Ask which they prefer.

5. **Naming conventions** — are there project-specific naming patterns to follow?
   If the project already has a README with style conventions, or a CLAUDE.md with rules,
   inherit those rather than inventing new ones.

Present the proposed config clearly (a simple list is fine) and ask for confirmation or changes
before writing anything.

---

## Phase 3: Scaffold

Create only what doesn't exist. Never overwrite.

### Directories

Create whatever directories are needed based on the agreed structure. If using a subfolder for
working logs, create it. If using a single file, no extra directory needed — just the docs root.
Usage notes always get their own subfolder. Skip creation for anything that already exists.

### Initial working log file

Create the working log file if none exists. The structure is the same regardless of whether
you're using a single file or a subfolder — the difference is just the path:

- Single file: `docs/working-log.md`
- Subfolder: `docs/working-logs/2026-Q2.md` (or whatever period is current)

Use this structure:

```markdown
# Working log — [project name], [period]

Living source of truth for implementation decisions. Read when starting work; append when
finishing a significant block. Any agent or human collaborator should include their signature.

## Entry template

---

## YYYY-MM-DD — Sentence-case summary of what happened

**Agent**: [agent name + model, e.g. Claude Code / Sonnet 4.6, Cursor / GPT-4o, human]
**Scope**: [brief area, e.g. auth, schema, UI, infra]

What was done, decided, or changed. Keep it concise — link to files or commits where details
live. Note any open questions or follow-ups.

---
```

If a working log file already exists for the current period, leave it alone.

### Usage notes directory

Create the folder. No initial file needed — usage notes are written as they emerge, named
by topic. Include a brief `README.md` so the purpose is clear to anyone landing there:

```markdown
# Usage notes

Product and process observations: how sessions feel, where friction surfaces, what the work
wants to be. Distinct from the working log — these stay relevant regardless of code state.

Name files by topic, not date. Write when a session produces insight worth keeping.
```

### Session-start injection

If injecting into an existing config file (`CLAUDE.md`, `AGENTS.md`), add a clearly delimited
section. Don't touch surrounding content. Something like:

```markdown
## Session start

Before replying substantively to the first message in any session, orient from:

1. The most recent working log entry in `{working-logs-path}/` — what changed recently.
2. The last one or two files in `{usage-notes-path}/` — what we're learning about the work.
   Scan filenames first; read the most recent in full.

If a usage note flags unresolved questions or thinking that's ahead of implementation,
carry that forward rather than re-deriving it.
```

Adapt the language to match the existing file's tone and conventions.

If creating a new config file, use the above as the session-start section and keep the rest
minimal — don't over-architect a config file for a project that doesn't need one yet.

---

## Phase 4: Ongoing use

Once the scaffold exists, this skill also guides session behavior going forward.

### Writing a working log entry

Append after completing a significant block of work — a feature, a bug fix, a design decision,
a meaningful refactor. Not after every small edit.

Format:

```markdown
## YYYY-MM-DD — Sentence-case summary of what happened

**Agent**: [agent name + model, e.g. Claude Code / Sonnet 4.6, Cursor / GPT-4o, human]
**Scope**: [brief area, e.g. auth, schema, UI, infra]

What was done, decided, or changed. Note any open questions or follow-ups.
```

The `Agent` field matters: when multiple tools or people contribute to a project, knowing
who wrote what helps future sessions understand the provenance of a decision. Always fill it
in — use "human" if the entry is written directly, or name the specific tool + model if an
AI agent is writing it.

`Scope` is a fast triage label. It should be glanceable — one or two words that let someone
scanning headings know whether this entry is relevant to what they're working on.

Keep entries tight. If you're writing more than a few bullets, you're probably capturing too
much — distill to what a future session actually needs.

### Writing a usage note

Write when a session produces insight about the work itself: friction you hit, something
that worked surprisingly well, a question about where the project is headed, an observation
about how the system behaves in practice.

Name the file for the topic, not the date (`auth-flow-friction.md`, `onboarding-observations.md`).
Dates go inside the file if needed.

No fixed format — these are freeform observations. But include:
- What you observed or what question surfaced
- Why it matters to how the work should proceed
- Any open questions it raises

### Session-start reading

The session-start section in the config file tells agents what to read. The intent is fast
orientation, not comprehensive review. A few minutes of reading should be enough to carry
context from the previous session.

If the working log has grown long, scan headings and read only the last few entries. If usage
notes have accumulated, scan filenames and read the most recent one or two in full.

---

## What not to do

- Don't create a docs structure and then never write to it. The value is in ongoing use.
- Don't write working log entries that are just git commit summaries — those belong in git.
  The working log is for decisions and context that don't fit in commit messages.
- Don't write usage notes about implementation specifics — those belong in the working log.
- Don't let the two tracks collapse into one. The distinction matters: one record is time-bound
  to the code, the other is durable.
- Don't force the quarterly naming convention if it doesn't fit the project's rhythm. Monthly,
  feature-based, or a single rolling file can all work — match the project's cadence.
