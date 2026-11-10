# Agents-file section template

Merge this into the host project's `AGENTS.md` / `CLAUDE.md` during scaffolding, adapted to the paths, libraries, and shell that were built. Later sessions author labs from this section alone, so it must define "lab" the way the user means it.

Replace bracketed placeholders, and drop lines that don't apply.

```markdown
### Labs (`/lab`)

`[app/lab/<slug>/]` holds this site's labs. A lab is a page where the user decides something about a subject, such as a component, a section, or a motion, by watching it run and changing it. Keep labs by default, for retuning and as design history. Record settled decisions in outcome notes and freeze decided labs. Remove a lab only when the user or this host's lifecycle calls for cleanup. How work divides into labs is the user's call, and one lab can hold one decision or several.

[State the chosen exposure: public direct-access, protected by the host's existing mechanism, or another deliberate posture.] Apply protection once at `[the lab section boundary]`. The section is `[noindex and omitted from the sitemap and main navigation / intentionally discoverable]`. `noindex` only asks crawlers to skip the section, so protect a private lab with access control.

Build the lab section from this site's design language: reuse its tokens, components, typography, and interaction patterns, and diverge when that difference is part of the experiment. Give the shared shell production fit-and-finish even when an experiment is unfinished, at lower emphasis than lab content. Standard lab headers use the shell's title-line height and inset across wide, narrow, expanded, and collapsed states.

Conventions:

- **Folder = lab.** The sidebar lists every folder that has a `[page.tsx]`. A new lab needs only its folder.
- **File split**: `[page.tsx]` (thin server wrapper) + `[lab.tsx]` (client component with the controls).
- **Optional `[meta.ts]`**: default-exports a `[LabMeta]` from `[lib/lab-registry.ts]` with title, description, date, and outcome (a short note on what the lab decided). A lab without metadata takes its title from the folder slug.
- **Defaults come from production.** A lab whose subject is in production imports its defaults from the production module. The user accepts values by copying them from the control panel and handing them to the agent, who applies them to the production source.
- **Harmonize with the destination.** For changes to an existing page, section, or component, use its surrounding content, layout, hierarchy, and interface patterns as the starting point. Depart when that is part of the experiment.
- **A lab differs from the destination.** Deliberate differences, such as forced conditions, fixtures, or an isolated stage, are part of the experiment. Accidental ones come from what the subject reads from its surroundings. For instance, viewport units resolve against the window while the subject sits in a smaller pane, and a subject sized from its container avoids that. Find accidental differences by comparing the subject in the lab and in the destination under the same conditions, such as the same width, before the user decides. Compare when the result could depend on the subject's surroundings. A layout decision usually can, and a color or a duration usually cannot. For a change to an existing page, a lab can render the surrounding section with the variant in place, so the user judges it where it ships. [Accidental differences this host has found, and their fixes.]
- **Code ships by promotion.** The variant production ships is current, and the lab imports it. A proposed variant lives in the lab folder. When the subject has a current, keep it as a variant named `current`, so the user can compare a proposal with what ships. When the user decides to ship a proposed variant, move it into production with history-preserving renames in place of current, point the lab's `current` at the production module, and confirm the destination shows what the lab showed. When a production subject renders only inside its page, propose extracting the part under study into its own production module.
- **Taste has two sources.** Follow `[this project's design docs and tokens]` first. Where they are silent, follow the user's own taste, wherever they keep it. Read both before building. When the user corrects a lab's look, offer to record the rule in whichever source it belongs to.
- **Labs share a canvas.** Render each lab in a layout from `[the canvas module]`: stage (one subject, centered), board (several items on one grid), or full bleed (the lab fills the pane). Write only the lab's content. When no layout fits, add one to the canvas module. A stage lab can give the user a switch to a board that shows its subject under several conditions, such as an interaction state, a theme, a content extreme, or a width. The board reads the same controls. [How this host forces conditions and holds pseudo-classes.]
- **The control panel is part of the lab interface.** Use `[DialKit, or the project's own control-panel library]`. Order controls in the sequence someone tunes the result, group them by concept, keep high-leverage choices visible, and collapse secondary calibration. Use clear labels, useful ranges, and intentional defaults. The panel takes the lab's appearance by default; give it its own only as a deliberate choice.
- **Labs host other work through an adapter.** When a lab holds another skill's or tool's artifact (a state machine, a model, a variant round), that skill owns the artifact and its rules. The lab records four mappings in the artifact's terms: what the page renders, what the controls change, how to state the outcome, and what a capture keeps. [Kinds of work this project allows in the lab, and what each must state.]
- **Dependencies point one way.** The shell (`[app/lab/layout.tsx]`, `[LabNav.tsx]`, `[entries.ts]`, `[app/lab/[slug]/]`) imports only labs' metadata. Labs import `[the canvas module]` and nothing from the shell. Production code imports nothing from a lab.

The registry (`[lib/lab-registry.ts]`) is a pure, tested module, so keep its test suite green after changes. Keep parameter snapshots in the control panel's saved versions. Structural or interaction variants use a named `?v=` value, render one direction full-size at a time, and switch instantly. Add a visible picker only when rapid comparison helps. Retain unadopted variants by default unless the user or this host's lifecycle calls for cleanup.

To author a new lab, create the folder and file split, pick a canvas layout, import production defaults when the subject is in production, and wire the controls. Start the control panel where it covers nothing the user is judging. The user can move it from there. It usually floats over a stage or full bleed lab and docks beside a board. Use the panel's own features, such as saved versions and copy, before building a lab equivalent. Smoke-test unusual wiring such as actions, text fields, manual render loops, and paused states.

When the user settles a decision in a lab, apply the accepted values to the production source and reload the lab to confirm it starts from them. Then record the decision as the outcome note in `[meta.ts]`.

#### Live and frozen labs

A lab imports live production code, so later production changes break a decided lab or alter what it shows. Freezing a decided lab prevents that. A lab's state comes from its files:

- **Live**: the folder has `[page.tsx]`. It runs on today's code.
- **Frozen**: the folder has only `frozen.json` (the record) and `capture-*` files (screenshots or clips of it running). The record holds the outcome and pins the main-branch commit the lab ran at; that commit keeps the lab's code, the production modules it imported, and its packages. `[app/lab/[slug]/]` renders the record at the lab's old URL.
- A folder with both is a freeze or thaw that stopped partway. The build fails and names the command that finishes it.

`[bun run lab]` (`[scripts/lab.ts]`) moves labs between live and frozen. It never commits; review its diff and commit it.

- `status`: labs by state, plus freeze and snapshot suggestions.
- `freeze <slug> --capture <file>`: write the record, keep captures, drop packages only it imported, delete the code.
- `snapshot <slug> --as <slug>-<yyyy-mm>`: freeze a copy under a new name; the lab stays live.
- `visit <slug>` (then `--done`): run a frozen lab at its commit, controls included.
- `thaw <slug>`: make it live again on today's code, then repair drift.

A freeze needs an outcome that states the decided values, no code outside the lab importing it, and a working tree identical to its main-branch commit apart from `[meta.ts]`, so freeze from an up-to-date main. It refuses otherwise and names what differs. Take captures with your browser tool before freezing: the lab at its decided values, controls visible, sidebar cropped out. To read a frozen lab's old values against today's parameters, read its files at the pinned commit and map them; that needs neither a visit nor a thaw.

Run `status` after finishing work on a lab. When it suggests a freeze or snapshot, mention it to the user with its reason. Freeze or snapshot only when asked.
```
