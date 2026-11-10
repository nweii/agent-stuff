---
name: build-lab
description: "Set up a durable /lab section of design experiments in a website, or add shared canvases or freezing to an existing one."
disable-model-invocation: true
metadata:
  author: nweii
  version: "0.5.0"
  credit: "Lab-building patterns draw on DialKit by Josh Puckett, Emil Kowalski's prototype workflow, and shadcn/ui's sidebar building blocks."
---

# Lab

A **lab** is a page inside a website the user runs where a design idea is built against the production components and tuned with live controls. The user keeps labs to revisit them and as design history. The `/lab` section holds the labs, with a sidebar to move between them.

The user tunes and decides in a lab. The agent builds it, sets starting points the user can change while using it, and applies what the user decides.

[GLOSSARY.md](GLOSSARY.md) defines the terms used here. Use each term as it is defined there.

Everything in this skill is a working default. Reshape its structure, tools, appearance, exposure, and lifecycle around the user's needs and the host codebase. Keep labs by default: record settled decisions in outcome metadata and freeze decided labs. Remove a lab only when the user or the host's lifecycle calls for it.

This skill is for **setup**: it installs the shell and writes the lab conventions into the project's agents file. Later sessions author labs from that section alone. If the project has no `app`-style routing or the user wants a standalone playground, the host can be a bare app whose only content is `/lab`; its labs hold their own starting values. If the host already has a lab section, start at step 5 to add canvases or step 6 to add freezing.

## The conventions

This list is the canonical statement of the pattern. The agents-file template restates it for the host repo, so mirror every edit to one in the other.

- **Folder = lab.** The sidebar lists every folder in the lab directory that has a page. The loader reads the directory, so a new lab needs only its folder.
- **File split**: a thin server/route wrapper (`page`) plus a client component holding the experiment and its controls (`lab`).
- **Optional metadata**: a lab may carry a small `meta` module with a title, description, date, and outcome. The outcome is a short note on what the user decided in the lab, stating the accepted values, written once when they go back to production. A lab without metadata takes its title from the folder slug.
- **Defaults come from production.** A lab whose subject is in production imports its starting values from the production module, so the lab starts from what ships. The user accepts values by copying them from the control panel and handing them to the agent. The agent applies them to the production source and reloads the lab to confirm it starts from them.
- **Labs host other work through an adapter.** A lab can hold whatever another skill or tool produces, such as a state machine, a model, a variant round or a prototype. That skill owns the artifact and its rules, and the lab maps four things onto it: what the page renders, what the controls change, how to state the outcome, and what a capture keeps. Read [references/hosting.md](references/hosting.md) when a lab holds anything other than a tuning panel.
- **Harmonize with the destination.** For changes to an existing page, section, or component, use its surrounding content, layout, hierarchy, and interface patterns as the starting point. Depart when that is part of the experiment.
- **A lab differs from the destination.** Deliberate differences, such as forced conditions, fixtures, or an isolated stage, are part of the experiment. Accidental ones come from what the subject reads from its surroundings, such as viewport units that resolve against the window while the subject sits in a smaller pane. Find them by comparing the subject in the lab and in the destination, before the user decides. Compare when the result could depend on the subject's surroundings. A layout decision usually can, and a color or a duration usually cannot.
- **Code ships by promotion.** Current lives in production and the lab imports it. A proposed variant lives in the lab folder. When the subject has a current, keep it as a variant, so the user can compare a proposal with what ships. When the user decides to ship a proposed variant, move it into production in place of current and import it back into the lab. Read [references/promotion.md](references/promotion.md) before promoting a variant, or when a subject renders differently in the lab and the destination.
- **Taste has two sources.** Follow the host's design system and docs first. Where they are silent, follow the user's own taste, wherever they keep it. Read both before building. When the user corrects a lab's look, offer to record the rule in whichever source it belongs to.
- **Labs share a canvas.** Render each lab in one of the host's canvas layouts (stage, board, or full bleed) and write only the lab's content. A stage lab can give the user a switch to a board that shows its subject under several conditions, such as interaction states, themes, content extremes, and widths. Read [references/canvases.md](references/canvases.md) before building the canvas, adding a layout, or adding a conditions board.
- **The control surface is an interface.** DialKit is the default control panel. Order controls in the sequence someone tunes the result, group them by concept, keep high-leverage choices visible, and collapse secondary calibration. Use clear labels, useful ranges, and intentional defaults, and place the panel where the subject stays visible. The panel takes the lab's appearance by default; give it its own only as a deliberate experiment choice. The user can drag a floating panel while using a lab. Read [references/dialkit.md](references/dialkit.md) before wiring a lab's controls.
- **Files define a lab's state.** A folder with a page is a live lab. A folder holding only a record and captures is a frozen one. Read the state from the folder each time, and store it nowhere else.
- **Decided labs freeze.** A lab imports live production code, so later production changes break a decided lab or alter what it shows. Freezing removes its code and keeps a record of the outcome, captures of it running, and the main-branch commit where it still runs, served at the lab's old URL. Suggest a freeze or snapshot when the lab's history warrants one, and act only when asked. Read [references/freezing.md](references/freezing.md) before adding the lifecycle or freezing, snapshotting, visiting, or thawing a lab.
- **Dependencies point one way.** The shell imports only labs' metadata. Labs import the canvas and nothing from the shell, so a replacement shell requires no lab edits. Production code imports nothing from a lab.
- **Labs own the backdrop.** Keep every shell layer transparent across the content pane. An opaque shell layer covers a lab that paints a fixed or negative-z backdrop.
- **Exposure follows the host.** Public labs default to direct access, `noindex`, and omission from the sitemap and main navigation. Protected labs reuse the host's route protection or deployment infrastructure at the `/lab` boundary. `noindex` only asks crawlers to skip the section, so protect a private lab with access control. Read [references/access-control.md](references/access-control.md) when protection is selected or already exists.
- **Variants** inside a lab use a `?v=<name>` search param, each named for the axis it diverges on (layout, density, personality, motion). Retain unadopted variants by default for later comparison, and name the accepted one in the outcome note. Follow the user's or host's cleanup preference when it differs. Read [references/variant-comparison.md](references/variant-comparison.md) when one lab needs rapid comparison between structural or interaction directions. Keep parameter snapshots in the control panel.

## Shell design defaults

The shell makes labs easy to find and use, and draws less attention than their contents. Adapt these defaults to the user's needs, the host's design language, and the purpose of each lab.

- **Extend the site's design language.** When the host has an established visual system, reuse its tokens, components, typography, and interaction patterns. Diverge when that difference is part of the experiment.
- **Finish the shared chrome.** Give the shell production fit-and-finish even when an experiment is unfinished. Omit status badges, introductory eyebrows, and portfolio-style explanation unless the host uses them.
- **Quieter than content.** Build the shell from the host's design tokens at lower emphasis than content: muted text at rest, small type, no ornament.
- **Separate by tone.** Mark the sidebar/content boundary with a step between surface colors, plus a hairline at most.
- **One title line.** Define one title-line height and inset for the shell wordmark, collapsed trigger, and standard lab headers, and preserve it across wide, narrow, expanded, and collapsed states.
- **Raised surfaces are lighter (dark UIs).** Make a surface that rests on another, such as an active-item fill, lighter than its parent. Component-library dark defaults often invert this.
- **Dim stroke icons with solid colors.** Semi-transparent strokes brighten where an icon's paths overlap, so pick the solid gray that matches the intended level.
- **Complete every interaction state.** Give navigation, triggers, tabs, and buttons intentional rest, hover, focus-visible, pressed, and selected states with legible contrast in every supported appearance.
- **Restrained motion.** Slide the sidebar on an eased curve, animate reordered list items to their new slots, and fall back to cross-fades under reduced motion. Switch labs instantly, because it is the most frequent action.

## Setup

For a Next.js App Router host, read [references/nextjs-scaffold.md](references/nextjs-scaffold.md) before writing code. It holds the concrete module shapes and gotchas. For another router or a bare app, skip that reference and build from the conventions above using the host's native route, module, and styling patterns.

1. **Recon the host.** Done when you can name the router, styling system, design tokens, any installed component and control-panel libraries, the site's existing route-protection pattern, the intended public or protected exposure, and every experiment route scattered elsewhere (debug routes, internal pages).
2. **Migrate strays.** Show the user the experiment routes the recon found and which ones would move. Move the ones the user approves into the lab directory with history-preserving renames (`git mv`), normalize each to the file split, and consolidate route gates at the section boundary according to the chosen exposure. Tell the user that the old URLs stop resolving. Done when every route from the recon has a migrated destination or a recorded reason to stay put.
3. **Build the registry seam.** Write one pure function that takes folder slugs plus optional metadata and returns the nav model. Put filesystem access and metadata imports in a thin loader beside the layout. Done when the registry has passing tests and the loader lists exactly the live and frozen lab folders.
4. **Build the shell.** Render the sidebar from the registry, set the chosen exposure once at the section boundary, and add `noindex` unless the user wants the lab discoverable. Reuse the host's navigation, component, and control systems. If a needed system is absent, choose an implementation suited to the stack with the user. When the host has no control panel, propose DialKit and install it once the user agrees. Read [references/dialkit.md](references/dialkit.md) and the installed DialKit version's documentation before wiring grouping, placement, appearance, actions, persistence, and export behavior. On a host with another control-panel library, read that library's documentation. Put host-specific extras (an internal dashboard or main-site link) in the sidebar footer, marked as host extensions outside the general pattern.
5. **Build the canvas.** Follow [references/canvases.md](references/canvases.md). Done when its verification passes.
6. **Add the lifecycle.** Follow [references/freezing.md](references/freezing.md): a record page at the lab URL, a quieter frozen group in the sidebar, and a script for freeze, snapshot, visit, thaw, and status. The record page is shared chrome, so it follows the shell design defaults: the standard title line, plain labels instead of eyebrows, and the host's tokens. Done when the planners have passing tests and one lab has been frozen, visited, and thawed in a scratch worktree, or the user has deferred the lifecycle. Use the copy-source fallback only for a host without git history, after telling the user its tradeoff.
7. **Update the host's agents file.** Merge the section in [references/agents-md-section.md](references/agents-md-section.md) into the project's `AGENTS.md` / `CLAUDE.md`. Later sessions author labs from this section. Done when the merged section contains no bracketed placeholders and its paths, libraries, and loop descriptions match what was built.
8. **Verify.** Done when: registry, loader, and lifecycle tests pass; the production build passes; the `/lab` index, every live lab, and every frozen lab's record page load in a browser with a clean console; metadata and discovery match the chosen exposure; protected sections block an unauthenticated request at the index and a nested lab; and the shared chrome passes one wide and one narrow viewport with the sidebar expanded, collapsed, and mobile. In those states, inspect title alignment, unexplained gaps or overlap, and every shell control's hover, focus-visible, pressed, and selected states in each supported appearance.

Completion criterion: every experiment route the recon found is migrated or accounted for, every sidebar entry resolves to a rendering lab, the agents-file section is placeholder-free and accurate, and every check in step 8 passes.
