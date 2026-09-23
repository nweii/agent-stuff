---
name: repo-docs
description: "README and other user-facing repo docs (setup guides, docs/ pages, security and contributing notes, release notes). Use when writing, revising, or auditing them, or preparing a repo's docs for public release. Agent-facing files such as AGENTS.md belong to writing-for-agents."
metadata:
  author: nweii
  version: "0.2.0"
  internal: true
---

# Repo docs

User-facing repo docs serve a **stranger**: someone who arrived cold, is deciding whether the project fits, and then sets it up or uses it. Their coding agent often reads the same page and follows its steps. Write every page for that pair, never for the owner.

The guidance has two layers. The content rules apply to every user-facing doc in every repo. The format defaults apply only where the repo, its ecosystem, or its docs site has no convention of its own; when one exists, follow it.

Most rules below are judgments, each with the test that decides it. Apply the test to the case in front of you: the same detail can belong in a reference table and not in a heading, or in a closing section and not in a setup step. Scale the steps to the change as well: a one-line fix needs the facts it touches and their echoes, while a new doc or a public-release pass needs every step in full.

## Steps

### 1. Gather the facts

Read the doc you are changing, its siblings, the code and config behind each claim, and every **echo** of its facts elsewhere (website copy, storefront text, in-app help, installed docs, other docs in the repo). Check the repo's visibility with `gh repo view --json visibility` and look for existing conventions: a docs site, a style the other docs share, README requirements from the plugin or package directory the project ships through.

Done when you can name the audience, the conventions that bind the doc, every echo location, and the code path behind each claim you will touch.

### 2. Place the material

Put each piece of material in the document that owns it, using the map below. Give each fact one canonical home and link to it from everywhere else; copy a fact only where a link cannot reach (a storefront, an app's help text).

### 3. Draft or revise

Apply the content rules, then the repo's conventions, then the format defaults for whatever the conventions leave open. For a README, read [references/readme.md](references/readme.md).

When revising, change only what is awkward, wrong, stale, or misplaced. Keep phrasing that already works, and when feedback names one part, fix that part and keep the rest. When the owner asks for a file-wide fix, apply it to the whole file.

### 4. Verify every claim

Trace each factual sentence you wrote or kept to the code, config, or a command you ran. Fix or cut any claim you cannot trace. Update every echo that states a fact you changed.

Done when every claim in the changed sections is traced and every echo agrees.

### 5. Sweep

Run [references/audit-checklist.md](references/audit-checklist.md) against every changed section. Done when every item that bears on the change has been checked against every changed section.

### 6. Preview before committing

Show the changed prose in chat (or open the file for review) and wait for approval before committing, unless the owner has already approved the wording or asked for a direct commit. Publishing to a public repo needs its own explicit approval.

## Where material belongs

| Material | Home |
|---|---|
| What the project is, who it suits, how to start, its boundaries, where to go next | README |
| One task or topic in depth (a setup path, an integration, a deploy target) | A guide in `docs/`, linked from the README |
| Exhaustive reference (every option, command, tool, or variable) | `docs/` or a docs site; a short table can live in the README |
| Context, conventions, and traps that only an agent hits | `AGENTS.md` (see `writing-for-agents`) |
| A copyable prompt that sets the project up through an agent | A `text` block in the README or its own file, written with `writing-for-agents` |
| Version history and release specifics | `CHANGELOG.md` or release notes |
| Vulnerability reporting; contribution process | `SECURITY.md`; `CONTRIBUTING.md` |
| What a vendored dependency is and why it is committed | A short README in its folder |
| Owner notes, research, plans, audits, handoffs, competitor analysis | Outside a public repo, in the owner's private store; a private repo may keep them in `docs/` |

## Content rules

**Outcome first, then the specific.** Describe a feature or step by what the reader gets. Then weigh each concrete detail (a number, a list, a name) on two questions: does it inform the reader's decision, and how often will it change? Match its position to the answer. Headings, feature lead-ins, and openings are the most prominent and least often revisited lines, so they carry only details that are both decision-relevant and stable (a minimum runtime version, a measured speedup). A detail that is useful but likely to change (how many commands, templates, or integrations ship; which formats this release supports) goes where it is easy to keep current: a reference table, a docs page, or release notes. A detail that only describes internals (control names, implementation terms) goes nowhere.

**Explain what and why.** When a step asks the reader to create an account, a project, a token, or a setting the intended reader may not know, say what that thing is and why the project needs it.

**State the boundary.** For privacy, security, network, and data behaviour, state what the software does and does not touch, and name each external service it contacts and why. Mechanics the reader only needs to trust belong in `docs/` or the code; steps the reader must take belong on the page.

**Durable.** Write sentences that stay true as versions, vendors, and release states change. Release dates, "what's new" sections, listing status, renames, retired components, and provider names that may change belong in release notes or nowhere. Three kinds of time-bound fact earn a place:

- Minimum requirements, which stay true until raised ("Requires Node 20 or later").
- One maturity or maintenance line when it changes whether someone should adopt the project ("This project is no longer maintained").
- A warning that protects the reader now (a known crash, lookalike download sites). Remove it once it no longer applies.

When a reader needs a platform fact that may change, date it ("As of 2026-08, …").

**Inform.** State the value plainly and back it with measured facts. Present paid and free paths, or this project and an alternative, evenly, each with its real cost. Answer the concerns a reader will actually have, including alarming system warnings, which deserve a calm, specific instruction.

**Scoped.** Document what applies to this project and its users. Mention another project when it shaped this one, when readers commonly confuse the two, or as a one-clause anchor to a well-known neighbour ("similar to `grep`"). Keep any fuller comparison measured and even-handed.

**Requirements where the reader starts.** Put a requirement at the start of the path that needs it. A requirement every path needs goes in the first sentence of setup.

**Default path short.** Keep the primary path to the fewest accounts, tokens, and dashboard visits. Advanced setups go in optional sections the reader or their agent can adopt.

**One clear action per step.** When one choice is right, say it. Match each step to the screen the reader actually sees. Write steps an agent can follow mechanically.

**One term per thing.** Choose one name for each concept and use it across every doc. Replace insider shorthand with what the reader will notice.

**Stranger-safe.** Docs in a public repo, or one likely to become public, carry no personal domains, account or deployment IDs, private references, or real personal data in examples. Use placeholders (`example.com`) and fictional sample data. A private repo read by a known team may name the people, hosts, and infrastructure its readers need. A personal collection that says openly it is personal may speak in the first person throughout.

**Content stands alone; meta stays in meta sections.** Content describes the project and how to use it: what it does, setup, usage, configuration, privacy, limits. Meta is material about the project as a project: who maintains it and how to support them, credits, how it was built (including AI usage), contribution stance, maintenance status, license. Write content so it would stay correct and complete if a different person maintained the project, or if the section were read in isolation (linked directly, quoted on a storefront, loaded by an agent). Gather meta into sections that exist for it, usually at the end of a README or in `CONTRIBUTING.md`, where a first-person voice, the maintainer's name, and support links fit. One exception: a maintenance or maturity status that changes whether someone should adopt the project goes where the reader sees it first.

**Built before documented.** Docs on the default branch describe behaviour that exists and works as described. A branch that builds a feature may document it alongside the code.

## Headings

Write each heading for a reader scanning the page, who should be able to predict what the section holds. Choose its form by the section's nature:

- A section that holds reference, a procedure, or a category of material gets a simple, direct label ("Configuration", "Supported file types", "Privacy and network access").
- A section that makes one point or explains one idea gets a succinct summary of that content ("Everything runs locally").

Readers already know the common signposts ("Getting started", "Installation", "Usage", "FAQ", "Troubleshooting", "License"), so use those as readers expect them, whatever their grammar. Use sentence case. Fold a section that would hold one item into a neighbour, or into an FAQ; a signpost section such as License may stay one line.

## Prose

Write plain, conversational sentences in forward order: subject, verb, point. Aim for simple English that still reads like a person talking; when sentences turn clipped, rejoin them. Let paragraphs wrap without hard line breaks. Use parentheses or a new sentence where an em dash might go. For a plain-text file that ships outside the repo (a README.txt in a download), follow the format of its siblings.

## Examples

For before-and-after rewrites that show these rules applied, read [references/examples.md](references/examples.md) when drafting an opening, a feature list, or a privacy section, or when a revision is not converging.
