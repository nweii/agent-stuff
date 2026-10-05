# Agent Stuff

[![skills.sh](https://skills.sh/b/nweii/agent-stuff)](https://skills.sh/nweii/agent-stuff)

Agent skills, plugins, and subagent examples I use with Claude, Codex, and other agents. Some skills are specific to my own setup (like my Obsidian vault).

## Agent skills format

A skill is a folder of instructions and any files an agent needs to follow them. Skills here use the [Agent Skills format](https://agentskills.io):

```text
skill-name/
├── SKILL.md              # Metadata and instructions
├── references/           # Optional: detailed docs or examples
└── scripts/              # Optional: helper scripts
```

The metadata at the top of `SKILL.md` gives the skill its name and description. The description tells the agent when to load it; the instructions explain how to do the work.

## Plugins

A plugin installs a set of related skills at once. You can still install any of those skills on its own or download its ZIP. If you install a plugin, don't also install its skills separately, or you'll end up with duplicates.

<!-- PLUGINS:START -->

- [Obsidian Tools](plugins/obsidian-tools/) — Operate your Obsidian vault, write note descriptions, and create Templater and Web Clipper templates using your own conventions.

<!-- PLUGINS:END -->

### Claude

On a paid plan, open **Customize → Plugins → Add → Add marketplace** and enter `nweii/agent-stuff`. The plugins appear under **Discover**; add the ones you want. They're saved to your account and also load in Claude Code when you sign in. See [Claude's plugin guide](https://support.claude.com/en/articles/13837440-use-plugins-in-claude).

### ChatGPT and Codex

In the ChatGPT desktop app, open **Plugins** from the sidebar, then **Add → Add a marketplace**, and enter `nweii/agent-stuff`. Install the plugins you want from the list.

In the Codex CLI:

```bash
codex plugin marketplace add nweii/agent-stuff
```

<details>
<summary><strong>ChatGPT workspace admins: import from GitHub</strong></summary>

To keep a workspace's copies in sync with this repo:

1. Open **Admin → Plugins → Add → Import marketplace**.
2. Set **Source** to `https://github.com/nweii/agent-stuff`. Leave **Path** and **Branch, tag, or commit** empty.
3. Import, authorize GitHub access, and make the plugins you want available to workspace members.
4. Members install them from **Plugins**.

ChatGPT checks for updates daily. See [OpenAI's marketplace import guide](https://learn.chatgpt.com/docs/enterprise/plugin-management) for permissions and sync controls.

</details>

## Install individual skills

Copy whatever looks useful.

With Bun or Node.js installed, use the [`skills` CLI](https://github.com/vercel-labs/skills) to choose skills and the coding agents that should load them:

```bash
bunx skills add nweii/agent-stuff

# or
npx skills add nweii/agent-stuff
```

Install a specific skill by name:

```bash
bunx skills add nweii/agent-stuff --skill obsidian-clis
```

By default, skills install in the project where you run the command. Add `-g` to make a skill available across projects.

Update installed skills:

```bash
bunx skills update

# Global installs
bunx skills update -g
```

To refresh one skill, run `skills add` again with its name. Use skills CLI 1.5.24 or later. Older versions can lose track of a skill when I reorganize this repo. Internal skills have one update quirk, explained under [Internal skills](#internal-skills).

### ZIP downloads and manual copies

Every general-purpose skill has a ZIP in [`zips/`](zips/). For Claude, follow [its skill setup guide](https://support.claude.com/en/articles/12512180-use-skills-in-claude) to enable code execution and upload the ZIP. Uploaded copies need manual updates.

You can also copy a skill folder into the skills directory your agent reads. Copy the whole folder so the agent can find any references or scripts its instructions use. Some skills use other apps or services. Installing the skill doesn't install those.

## Internal skills

Skills under the **Internal** heading in the catalog have `metadata.internal: true`. They're personal workflows tied to my own setup (vault paths, tools, naming conventions) and are excluded from the ZIP downloads. "Internal" just means they're written for my setup; the source is still public.

<details>
<summary><strong>Install it as-is</strong> (when the skill's assumptions already match your setup)</summary>

Some don't hardcode anything of mine. They assume a convention (a `related` property, a daily/weekly note hierarchy) or a tool (Granola MCP, `gh`) and otherwise work anywhere. If nothing in the SKILL.md names a folder or template you don't have, just install it:

```bash
bunx skills add nweii/agent-stuff --skill SKILL_NAME
```

Replace `SKILL_NAME` with the name listed in the catalog. Two CLI behaviors matter here:

- `bunx skills add nweii/agent-stuff` skips internal skills. Naming one with `--skill` opts it in.
- After I move a skill to another folder in this repo, `bunx skills update` can falsely report internal skills as deleted, even ones I haven't moved. Use `INSTALL_INTERNAL_SKILLS=1 bunx skills update` (add `-g` for global installs), or decline removal so it doesn't delete a skill that's still here. If the command can't ask for confirmation, it leaves those skills alone.

For a one-off run, or just to read one first, `bunx skills use nweii/agent-stuff -s SKILL_NAME` prints it as a ready-to-paste prompt without installing anything.

</details>

<details>
<summary><strong>Tailor a copy</strong> (when it carries folder conventions you don't share)</summary>

For the ones carrying my folder structure and template names throughout, have your agent read mine and write you your own version instead of installing and then editing:

```
Read skills/[skill-name]/SKILL.md from the github.com/nweii/agent-stuff repo —
use a local checkout if there's one on this machine, otherwise fetch it. It's
one of that repo's internal skills, written for someone else's setup, so some
of the folder paths, tools, and naming conventions in it won't match mine.
List what you'd need to substitute, ask me about anything you can't infer from
my setup, then write the tailored version into my skills directory under
a name of my choosing, with a `metadata.credit` line in its frontmatter noting
what it was adapted from. Leave everything that isn't setup-specific alone.
Don't install the original.
```

Giving your copy its own name keeps a later `add` or `update` from overwriting it.

</details>

## Folders and subagents

Most skill folders are in `skills/`. Skills grouped in a plugin are in `plugins/<id>/skills/`.

The [`agents/`](agents/) folder contains Claude Code subagent examples. Copy them into your own agents directory; the skills CLI does not install them.

## Catalog

<!-- CATALOG:START -->

_Auto-generated by `scripts/update-catalog.py`_

### Skills

- [archive-conversation](skills/archive-conversation/) — Create analytical archival summaries of AI conversations, capturing intellectual journeys, key insights, and technical logs. Use when archiving, saving, or documenting a chat session.
- [audit-transcription](skills/audit-transcription/) — Flag and propose corrections for likely mistranscriptions in auto-transcribed meeting notes or audio transcripts. Use when the user says 'audit this transcript', 'fix the transcription', 'find mistranscriptions', or shares a noisy Granola/Whisper output and asks for cleanup.
- [bb-agent-coordination](skills/bb-agent-coordination/) — Use alongside bb-cli when coordinating work across bb threads: delegation, ownership, environment boundaries, steering, reports, review, reconciliation, or handoff. bb-cli owns commands; this skill owns collaboration.
- [build-lab](skills/build-lab/) — Set up a durable /lab section in a website: a sidebar shell over design experiments, a tested registry, and the host agents-file conventions that make future lab authoring work.
- [commit](skills/commit/) — Create well-formatted commits with conventional commit messages. Use when user asks to commit, wants to commit changes, or needs help with commit messages.
- [drafting-writing](skills/drafting-writing/) — Writing-partner processes that draw out the user's own writing through questioning: guided drafting sessions, fragment mining, shaping raw material into a piece, and phrase tightening. Use for help discovering, developing, and structuring writing (notes, essays, messages, etc).
- [enrich-from-transcript](skills/enrich-from-transcript/) — Enrich an existing meeting/interview note from its transcript, or scaffold one when only a transcript exists. Captures granular narrative, exact phrases, mechanics, casual context, and implicit signals. Run on thin auto-summary notes or transcripts that warrant close reading.
- [extract-flow-scenario](skills/extract-flow-scenario/) — Use when extracting an actual workflow, user journey, or operational scenario from a conversation into a sequence of actors, state changes, and pain points.
- [file-naming](skills/file-naming/) — Analyze file content and propose intelligent renames using context-aware naming conventions. Date-prefixed for transactional/periodic documents, content-first for creative works. Use for organizing files, cleaning up downloads, or standardizing filenames.
- [herdr-agent-coordination](skills/herdr-agent-coordination/) — Use alongside the managed herdr skill whenever recognized agents communicate through Herdr: peer tasks, reports, questions, corrections, return paths, origin checks, or stalled delivery. This skill owns the peer protocol; herdr owns runtime control.
- [obsidian-app-css](skills/obsidian-app-css/) — Use when writing, debugging, auditing, or reorganizing CSS snippets or app themes for Obsidian desktop/mobile, including DOM selectors, CSS variables, platform classes, plugin/theme compatibility, specificity, or cascade conflicts. Excludes hosted Publish, publish.css, and publish.js.
- [obsidian-clis](plugins/obsidian-tools/skills/obsidian-clis/) — Use when operating Obsidian from the terminal: notes, search, properties, links, tasks, Bases, or plugin development. Uses the app CLI, with notesmd-cli as a headless fallback.
- [obsidian-publish-customize](skills/obsidian-publish-customize/) — Use when theming or scripting an Obsidian Publish site through publish.css or publish.js, including client-side workarounds. Excludes ordinary Publish usage, desktop themes, and plugins.
- [obsidian-templater](plugins/obsidian-tools/skills/obsidian-templater/) — Help with templates/snippets for the Obsidian Templater plugin. Use to help generate Obsidian templates from natural language, understand and debug existing tp.* snippets, and adapt vault notes and workflows to Templater when users mention Templater, tp.*, templater syntax.
- [obsidian-web-clipper](plugins/obsidian-tools/skills/obsidian-web-clipper/) — Use when creating, importing, or debugging Obsidian Web Clipper templates: JSON, variables, filters, selectors, interpreter prompts, and URL or schema triggers. Does not handle general scraping.
- [quantify-impact](skills/quantify-impact/) — Surface measurable metrics and outcomes from a description of work via structured conversation. Use when the user says 'help me quantify this', 'what numbers can I attach to X', or is drafting a resume bullet, case study, or impact statement that needs concrete scale.
- [raycast-extensions](skills/raycast-extensions/) — Build Raycast extensions — commands, List/Form/Grid views, hooks like useFetch, AI integration, manifest. Use when the user says 'raycast extension', 'add a raycast command', or is working in a project with @raycast/api and a Raycast manifest.
- [react-useeffect](skills/react-useeffect/) — React useEffect best practices. Use when writing Effects, derived values, or data fetching. Teaches when NOT to use Effects and better alternatives like useMemo or key props.
- [repo-docs](skills/repo-docs/) — Use when writing, revising, or auditing READMEs, repo docs, RFCs, PR descriptions, or commit messages, or preparing docs for public release. Agent-facing files such as AGENTS.md belong to writing-for-agents.
- [semantic-compression](skills/semantic-compression/) — Compress wordy language or loosely expressed thinking into a smaller, sharper form without flattening its meaning. Use when revising an explanation, phrase, sentence, paragraph, concept, label, or coined term whose nuance, implication, or texture must survive the edit.
- [set-note-description](plugins/obsidian-tools/skills/set-note-description/) — Use when writing a note's description property for recall or retrieval. Summarizes a note's own content; parent-period synthesis belongs to periodic-rollup or the environment's specific rollup workflow.
- [software-test-quality](skills/software-test-quality/) — Review software test suites and choose test levels. Use when auditing unit, integration, component, or end-to-end tests; assessing assertions, fixtures, mocks, coverage, or flakiness; or deciding which test level best protects a behavior or risk.
- [spec-shaping](skills/spec-shaping/) — Shape product ideas into actionable specs and sprint plans. Use when interviewing about a product plan, breaking specs into sprints, or turning vague ideas into well-scoped work.
- [suggest-lucide-icons](skills/suggest-lucide-icons/) — Pick Lucide icons for a concept, UI placement, or vault note. Searches the full Lucide catalog for real, verified icon names. Use when the user says 'what icon for X', 'suggest a Lucide icon', 'pick an icon', or needs an icon for note frontmatter, a button, or a section header.
- [teach-me](skills/teach-me/) — Use when the user asks to learn a concept or understand completed work through stepwise tutoring, checks for understanding, or a saved walkthrough or learning record.
- [things-app](skills/things-app/) — Read, capture, schedule, and update tasks and projects in Things 3. Prefer the `things` CLI whenever there's command-line access to Things; otherwise use a connected Things MCP for headless or remote environments (full read + write, any device), the `things:///` URL scheme (any device with Things, write-only), or email-to-Things for unattended capture. Use to add todos, build a project, show Today/Inbox, find tagged tasks, or schedule from desktop, phone, or a serverless routine.
- [tirith-config](skills/tirith-config/) — Operate tirith, the terminal guard against homograph URLs, ANSI injection, and pipe-to-shell. Use when editing ~/.config/tirith/policy.yaml, debugging a blocked command or paste, choosing trust / allowlist / download-and-run / TIRITH=0, or quieting a noisy rule.
- [transcribe-audio](skills/transcribe-audio/) — Transcribe audio or video to text with a locally-run speech-to-text model. Use when the user wants a transcript or captions from a recording, wants to run speech-to-text locally instead of a cloud service, or wants to set up or switch their local transcription model.
- [update-changelog](skills/update-changelog/) — Add or revise a project's Keep-a-Changelog-format changelog, including version bumps and change-type groupings. Use when the user says 'update the changelog', 'log this change', or 'bump the changelog' for a project or plugin.
- [use-tailwind-v4](skills/use-tailwind-v4/) — Tailwind CSS v4 syntax and v3→v4 migration reference. Use when the user mentions 'Tailwind v4', 'upgrade Tailwind', @theme, @utility, or @import 'tailwindcss', or is working in a project whose config indicates v4.
- [validating-startup-ideas](skills/validating-startup-ideas/) — Find and validate startup ideas by mining user complaints, crafting premises, and navigating the idea maze. Use when discovering product opportunities, validating ideas, shaping solutions, researching user pain points, or exploring what to build.
- [visual-keywords](skills/visual-keywords/) — Generate keyword strings for images, screenshots, or visual references — optimized for fuzzy search, not alt text or prose. Use when the user says 'keywords for this image', 'tag this for search', 'visual keywords', or wants searchable labels on an Eagle asset.

### Internal

Personal workflows tied to my own setup (vault paths, tools, naming conventions). Installable, but expect to adapt `SKILL.md` to your own folders and conventions before they're useful.

- [archive-to-brain](skills/archive-to-brain/) — Save an archival summary of an AI conversation to Nathan's Obsidian vault, using the Thinking note template and vault folder conventions to capture intellectual journeys, key insights, and technical logs. Use when archiving a chat session to the vault.
- [clip-skills](skills/clip-skills/) — Save `bunx skills` terminal output (a manifest from `skills add/use <repo> -l`) as a Repos note in the Brain vault under 03-Records/Snippets/Repos/. Use when the user pastes a skills listing and wants it captured. Triggers: '/clip-skills', 'save these skills', 'make a note for this skill repo'.
- [code-to-pantry](skills/code-to-pantry/) — Use when looking up reusable components in Nathan's pantry, bringing one into a project, or saving a code technique to the pantry for reuse.
- [create-topic-note](skills/create-topic-note/) — Create a topic note grouping related notes under a common theme, with automatic backlinking to source notes. Triggers: 'group these under a topic', 'create topic note for [[A]], [[B]], [[C]]'.
- [nweii-skills](skills/nweii-skills/) — Use when creating, editing, migrating, installing, or publishing skills, loading repository skills on demand, or reflecting on a session to improve skills in Nathan's environment.
- [obsidian-granola](skills/obsidian-granola/) — Sync meetings from Granola to Obsidian — pulls notes and transcripts and imports them as formatted meeting/transcript notes. Use when the user says \"sync my last granola meeting\", \"note for my last meeting\", or asks to pull in a Granola transcript.
- [obsidian-log-commits](skills/obsidian-log-commits/) — Fetches today's GitHub commits across personal and org repos, filters noise, and appends a summary as bullets into the ## Log section of today's daily note. Use when asked to log what was worked on today, check today's commits, or update the daily note with dev activity.
- [people-notes](skills/people-notes/) — Use for person-centered work in Nathan's Brain vault: prepare context from a profile and linked records, create a canonical person note, or reconcile an existing one.
- [periodic-rollup](skills/periodic-rollup/) — Use when synthesizing child periodic-note descriptions into a parent week, quarter, or year, or compiling project/topic history. Prefer a vault-specific rollup workflow when the environment provides one.
- [save-napkin-note](skills/save-napkin-note/) — Turn raw capture material into a properly structured Brain vault note (template, frontmatter, folder, links), or integrate a fragment into an existing note after confirmation. Use when filing a quick capture — triggers: 'save this as a note', 'file this', 'napkin note', 'process this dump'.
- [save-term](skills/save-term/) — Use when saving an encountered term or a concept coined in conversation as a Brain Term note, with its source quote or a brief gloss.
- [vault-recipes](skills/vault-recipes/) — Search, read, filter, combine, adapt, and save recipes in the Brain vault collection. Use whenever cooking and the collection are relevant — 'what should I make', 'recipes with miso', 'save this one' all imply it.

### Agents

Claude Code subagents — copy the `*.md` into your own agents directory (not installed by `bunx skills`). See [`agents/`](agents/).

- [vault-reader](agents/vault-reader.md) — Read-only Obsidian vault exploration. Use proactively when searching notes, understanding vault structure, finding connections, or gathering context from a vault.
- [vault-writer](agents/vault-writer.md) — Create and edit notes in an Obsidian vault. Use when the user wants to write, update, or organize notes. Follows vault conventions for metadata, linking, and structure.

<!-- CATALOG:END -->

## License

MIT. See [LICENSE](LICENSE).
