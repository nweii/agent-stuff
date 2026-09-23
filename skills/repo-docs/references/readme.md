# README defaults

Use these where the repo has no README convention of its own. A README does three jobs, in order: help a stranger decide whether the project fits, get them to a first working result, and point them to everything else.

## Opening

Start with an H1 carrying the project's display name as the product spells it, or the lowercase slug when the slug is what people type (a CLI command or package name).

Follow it with one or two short paragraphs:

1. What kind of thing it is and what it gives the reader. Name the category when one exists ("a command-line JSON formatter", "a date picker component for React"), or anchor to a tool the reader knows ("a better `npm publish`"). Then state the outcome. When no category fits, the outcome carries the sentence alone.
2. Where and how it runs, and its scope boundary ("One deployment serves one account.").

A one-line tagline above the paragraphs is optional. Keep one only when it states the outcome more directly than the paragraph under it.

When a reader's first question is how the project differs from a well-known neighbour, answer it here in a clause ("similar to `ag` and `grep`, but respects your gitignore").

## Show it working

Showing the project doing its job, right after the opening, is strongly recommended and rarely required. A project with a UI benefits most; a small utility, an early release, or an owner without time to capture visuals can ship without one. When a README lacks a visual, suggest the specific shot that would help most and where it would go, and let the owner decide. Never add a placeholder image or a link to a file that does not exist.

- For anything with a UI, use a screenshot, a short GIF, or a short video when the feature is motion (transitions, drag interactions). Give each image alt text that says what it shows. Supply light and dark variants with `<picture>` when the image has a background.
- For a CLI, library, or MCP server, a code block does the job: a command or call and the real output it returns, in a `console` block for terminal sessions.
- Caption any benchmark or chart with its conditions (hardware, cache state, data size).
- Give each key feature its own captioned image when a single hero shot cannot show them.

## Section order by project type

Choose the list that matches the project and use only the sections it needs. License is always last.

**App or plugin** (desktop utility, editor or note-app plugin, browser extension):

1. Opening and visual
2. Features (optional)
3. Install: the primary path first with the minimum OS or app version, alternates as subsections, "Let an agent set it up" last
4. Usage: defaults, input-to-result tables (such as shortcut → action)
5. Configuration
6. Uninstall, mirroring the install paths and listing what the app leaves behind
7. Troubleshooting or FAQ
8. Privacy
9. Limits
10. Relation to a named project, only for a real lineage
11. How it works, briefly
12. Development
13. Meta sections (see Section conventions)

**Library or component:** opening, visual or demo, install, the smallest working code sample, a link to full docs, FAQ, credits, license.

**CLI:** opening, a terminal demo, install (primary command, labelled alternates, a try-without-installing one-liner such as `uvx` or `npx` when available), usage, when not to use it, a link to full docs, troubleshooting, development, license.

**Service, MCP server, or template:** opening, "When to use it" (including when a platform-native option fits better), features, what you need, deploy or set up, connect, verify the connection, reference tables (tools, variables), optional setups, security, troubleshooting, develop locally, license.

**Personal collection** (skills, dotfiles, snippets): may open in the first person and say plainly that it is personal; explain how a stranger can use or adapt the pieces.

**Fork:** a one-sentence notice at the top naming the upstream project and what this fork changes, then the type's usual order.

## When a docs site exists

Once a second doc or a docs site exists, the README becomes a front door. Keep the identity, the visual, install, the smallest working example, and a link to the docs for each topic. Move exhaustive reference, option lists, and version history out. Keep enough real text that a person, a search engine, or an agent reading the raw file learns what the project is and how to start; an image-only README fails that.

## Section conventions

**Features.** Optional; skip it when the opening already carries the differentiator. Three to five bullets. Each opens with a bold sentence stating the outcome, ending in a period, followed by one plain sentence of support. Short concrete fragments work for a library ("Zero dependencies", "Works with server rendering"). Lead with the feature that sets the project apart.

**Install.** Label each alternate path with its real cost ("needs a rebuild for every update", "updated less often"). When a path stops working well, say so plainly and point to the better one.

**Limits.** State what the project does not do and who should use something else, in plain sentences. When a gap is a known issue, link it. For a CLI or library whose limits decide adoption, place this right after Features.

**Troubleshooting and FAQ.** Key each entry to what the reader sees: quote the literal error text or dialog, then give the fix. For operating-system permissions, name the exact settings path and the command that resets them. Order fixes from easiest to hardest.

**Privacy and security.** State what the software collects, sends, and touches, then name each external service it contacts and why. When the reader must act (rotating a secret, reviewing a crash report before sending it), give the steps.

**Platform disclosures.** Plugin, extension, and package directories often set README requirements; check the directory's developer policy and meet it. Obsidian's community plugin policy, for example, requires naming each remote service and why it is used, and disclosing payments, required accounts, file access outside the vault, and telemetry.

**Agent setup prompt.** Put a copyable prompt in a `text` block under "Let an agent set it up". Write it with the `writing-for-agents` skill: steps an agent can follow mechanically, each ending on a checkable result. It works with every install path, stays conditional about optional steps, and tells the agent to guide the user through secrets rather than receive them.

**Badges.** Functional and self-updating only: a deploy button, an install badge, a live package version. Never a hard-coded version.

The next five conventions are meta sections (see the content and meta rule in `SKILL.md`). Place them together near the end, in this order.

**Credits.** Name what the project borrows and from whom, with one line of purpose each (an algorithm adapted from another project, an icon by a designer, a parser library). Contributor handles are fine.

**Contribution stance.** For a solo-maintained project, one line on whether and how contributions are accepted, or a link to `CONTRIBUTING.md`.

**Maintainer and support.** A maintainer credit, a link to their site, and a support link (sponsor, "Buy me a coffee") go together in one short closing section.

**AI usage.** One to three sentences near the end stating how the project was built with AI tools and who directed and reviewed the work. Write it in the voice of whoever the project presents as its author: "I" for a solo maintainer, "we" for a team, the organization's name for a project published under one. The other meta sections use the same voice.

**License.** The last section, in the form `MIT. See [LICENSE](LICENSE).` A license may add a permission or an exclusion in a sentence (attribution requested for ports; trademarks and icons not covered).
