---
name: build-lab
description: "Set up a durable /lab section in a website: a sidebar shell over design experiments, a tested registry, and the host agents-file conventions that make future lab authoring work."
disable-model-invocation: true
metadata:
  author: nweii
  version: "0.2.0"
  credit: "Lab-building patterns draw on DialKit by Josh Puckett, Emil Kowalski's prototype workflow, and shadcn/ui's sidebar building blocks."
---

# Lab

A **lab** is a durable experiment surface inside a website the user runs: a page where a design idea gets built against real production components, tuned with live controls, and retained as an instrument to revisit and as design history. The `/lab` section is the wing of the site that holds them, with a sidebar to move between labs.

Everything in this skill is a working default. Freely reshape its structure, tools, appearance, exposure, and lifecycle around the user's needs and the host codebase. Labs are optimized for retention, so keep them by default and record settled decisions in outcome metadata; remove them when the user or host lifecycle calls for it.

This skill is for **setup**: it installs the shell and teaches the host repo the vocabulary. Day-to-day lab authoring is then driven by the section it writes into the project's agents file — after setup, "make me a lab for X" needs no skill at all. If the project has no `app`-style routing or the user wants a standalone playground, the host can be a bare app whose only content is `/lab`.

## The conventions

Canonical statement of the pattern. The agents-file template restates these for the host repo so it stands alone — an edit to either must be mirrored in the other.

- **Folder = lab.** A new folder with a page inside the lab directory appears in the sidebar automatically. No registration step, ever.
- **File split**: a thin server/route wrapper (`page`) plus a client component holding the experiment and its controls (`lab`).
- **Optional metadata**: a lab may carry a small `meta` module — title, description, date, outcome (a short note on what the lab decided, written once when accepted values go back to production; its absence just means the lab hasn't decided anything). Absent metadata falls back to the folder slug. Metadata is never required — there is deliberately no status field to keep fresh.
- **Defaults flow from production.** A tuning lab imports its starting values from the production module it tunes, so the lab can never drift from what ships. Accepted values travel back by copying the control panel's output and applying it to the production source — so whatever control-panel library is chosen must export its current values in copyable form.
- **Harmonize with the destination.** For changes to an existing page, section, or component, use its surrounding content, layout, hierarchy, and interface patterns as the starting point. Depart when that is part of the experiment.
- **The control surface is an interface.** Order controls in the sequence someone tunes the result, group them by concept, keep high-leverage choices visible, and collapse secondary calibration. Use clear labels, useful ranges, intentional defaults, and a placement that preserves the experiment's canvas. Its appearance follows the lab by default; an independent appearance is a deliberate experiment choice.
- **The dependency points one way.** The shell reads labs' metadata; labs stay independent of shell components, so swapping shells touches zero labs.
- **Labs own their canvas.** The shell stays background-free edge to edge; an opaque shell layer silently covers labs that paint fixed or negative-z backdrops.
- **Exposure follows the host.** Public labs default to direct access, `noindex`, and omission from the sitemap and main navigation. Protected labs reuse the host's route protection or deployment infrastructure at the `/lab` boundary; `noindex` is metadata, not access control. Read [references/access-control.md](references/access-control.md) when protection is selected or already exists.
- **Variants** inside a lab use a `?v=<name>` search param, each named for the axis it diverges on (layout, density, personality, motion). Retain unadopted variants by default for later comparison; the outcome note names the one that was accepted. Follow the user's or host's cleanup preference when it differs. Read [references/variant-comparison.md](references/variant-comparison.md) when one lab needs rapid comparison between structural or interaction directions; parameter snapshots stay in the control panel.

## Shell design defaults

The shared shell should make labs easy to find and use without competing visually with their contents. The defaults below provide a coherent starting point; adapt them to the user's needs, the host's design language, and the purpose of each lab.

- **Extend the site's design language.** When the host has an established visual system, reuse its tokens, components, typography, and interaction patterns so the lab feels native to the site. Diverge when that difference is part of the experiment.
- **Finish the shared chrome.** The shell receives production fit-and-finish even when an experiment remains unfinished. Keep it unframed: omit status badges, introductory eyebrows, and portfolio-style explanation unless the host uses them.
- **Native but quieter.** Build the shell from the host's existing design tokens, one register down from content: muted text at rest, small type, no ornament. It should feel like the site *and* recede behind whatever a lab renders.
- **Separate by tone, not lines.** The sidebar/content boundary is a tonal step between surface colors with at most a hairline.
- **Sit on the content's rhythm.** Define one title-line height and inset for the shell wordmark, collapsed trigger, and standard lab headers, and preserve it across wide, narrow, expanded, and collapsed states.
- **Elevation reads lighter (dark UIs).** A surface resting on another — active-item fill, a raised pill — is lighter than its parent. Component-library dark defaults often invert this.
- **Dim stroke icons with solid colors.** Semi-transparent strokes brighten where an icon's paths overlap; pick the solid gray that matches the intended level.
- **Complete every interaction state.** Navigation, triggers, tabs, and buttons have intentional rest, hover, focus-visible, pressed, and selected states with legible contrast in every supported appearance.
- **Motion is quiet and intentional.** The sidebar slides on an eased curve, list reorders animate items to their new slots, and everything degrades to cross-fades under reduced motion. Switching labs itself stays instant — it's the highest-frequency action.

## Setup

For a Next.js App Router host, read [references/nextjs-scaffold.md](references/nextjs-scaffold.md) before writing code — it holds the concrete module shapes and gotchas. For another router or a bare app, skip that reference and build from the conventions above using the host's native route, module, and styling patterns.

1. **Recon the host.** Done when you can name the router, styling system, design tokens, any installed component and control-panel libraries, the site's existing route-protection pattern, the intended public or protected exposure, and every experiment route scattered elsewhere (debug routes, internal pages).
2. **Migrate strays.** Move existing experiment pages into the lab directory with history-preserving renames (`git mv`), normalize each to the file split, and consolidate route gates at the section boundary according to the chosen exposure. Old URLs may 404; they were unlinked. Done when every route from the recon has a migrated destination or a recorded reason to stay put.
3. **Build the registry seam.** One pure function: folder slugs plus optional metadata in, nav model out. Filesystem access and metadata imports live in a thin loader beside the layout. Done when the registry has passing tests (this is the only unit-tested code in the shell) and the loader lists exactly the page-bearing folders.
4. **Build the shell.** Render the sidebar from the registry, set the chosen exposure once at the section boundary, and add `noindex` unless the user wants the lab discoverable. Reuse the host's navigation, component, and control systems. If a needed system is absent, choose an implementation suited to the stack with the user. Read an installed control-panel library's documentation before wiring its grouping, placement, appearance, actions, persistence, and export behavior. Host-specific extras (an internal dashboard or main-site link) go in the sidebar footer, marked as host extensions outside the general pattern.
5. **Update the host's agents file.** Merge the section in [references/agents-md-section.md](references/agents-md-section.md) into the project's `AGENTS.md` / `CLAUDE.md`. Done when the merged section contains no bracketed placeholders and its paths, libraries, and loop descriptions match what was actually built — this is what makes "make me a lab for X" work in later sessions.
6. **Verify.** Done when: registry and loader tests pass; the production build passes; the `/lab` index and every lab route load in a browser with a clean console; metadata and discovery match the chosen exposure; protected sections block an unauthenticated request at the index and a nested lab; and the shared chrome passes one wide and one narrow viewport with the sidebar expanded, collapsed, and mobile. In those states, inspect title alignment, unexplained gaps or overlap, and every shell control's hover, focus-visible, pressed, and selected states in each supported appearance.

Completion criterion: every experiment route the recon found is migrated or accounted for, every sidebar entry resolves to a rendering lab, the agents-file section is placeholder-free and accurate, and every check in step 6 passes.
