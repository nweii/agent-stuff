---
name: build-lab
description: "Set up a durable /lab section in a website: a sidebar shell over design experiments, a tested registry, and the host agents-file conventions that make future lab authoring work."
disable-model-invocation: true
metadata:
  author: nweii
  version: "0.1.0"
  credit: "Pattern developed on nathancheng.work (live demo at nathancheng.work/lab). Variant-divergence discipline adapted from Emil Kowalski's prototyping approach."
---

# Lab

A **lab** is a durable experiment surface inside a website the user runs: a page where a design idea gets built against real production components, tuned with live controls, and then *kept* — as an instrument to revisit and as design history. The `/lab` section is the wing of the site that holds them, with a sidebar to move between labs.

Labs are the opposite of throwaway prototypes. Never delete a lab — keep every lab, and record what a settled exploration decided in its metadata (the outcome note).

This skill is for **setup**: it installs the shell and teaches the host repo the vocabulary. Day-to-day lab authoring is then driven by the section it writes into the project's agents file — after setup, "make me a lab for X" needs no skill at all. If the project has no `app`-style routing or the user wants a standalone playground, the host can be a bare app whose only content is `/lab`.

## The conventions

Canonical statement of the pattern. The agents-file template restates these for the host repo so it stands alone — an edit to either must be mirrored in the other.

- **Folder = lab.** A new folder with a page inside the lab directory appears in the sidebar automatically. No registration step, ever.
- **File split**: a thin server/route wrapper (`page`) plus a client component holding the experiment and its controls (`lab`).
- **Optional metadata**: a lab may carry a small `meta` module — title, description, date, outcome (a short note on what the lab decided, written once when accepted values go back to production; its absence just means the lab hasn't decided anything). Absent metadata falls back to the folder slug. Metadata is never required — there is deliberately no status field to keep fresh.
- **Defaults flow from production.** A tuning lab imports its starting values from the production module it tunes, so the lab can never drift from what ships. Accepted values travel back by copying the control panel's output and applying it to the production source — so whatever control-panel library is chosen must export its current values in copyable form.
- **The dependency points one way.** The shell reads labs' metadata; labs stay independent of shell components, so swapping shells touches zero labs.
- **Labs own their canvas.** The shell stays background-free edge to edge; an opaque shell layer silently covers labs that paint fixed or negative-z backdrops.
- **Direct-access section**: `noindex` metadata, absent from the sitemap and the main site's navigation — reachable by URL. Access control, when wanted, lives in infrastructure in front of the path (Cloudflare Access or equivalent).
- **Variants** inside a lab use a `?v=<name>` search param, each named for the axis it diverges on (layout, density, personality, motion). Variants that don't get adopted stay; the outcome note names the one that did.

## Shell design defaults

The shell is chrome, not a contestant — labs are the show. These are defaults, stated so the shell comes out consistent without a design brief; where the host's design language disagrees, the host wins.

- **Native but quieter.** Build the shell from the host's existing design tokens, one register down from content: muted text at rest, small type, no ornament. It should feel like the site *and* recede behind whatever a lab renders.
- **Separate by tone, not lines.** The sidebar/content boundary is a tonal step between surface colors with at most a hairline.
- **Sit on the content's rhythm.** The shell's wordmark, toggle controls, and a content pane's heading share one title line, so chrome reads as part of the page rather than floating over it.
- **Elevation reads lighter (dark UIs).** A surface resting on another — active-item fill, a raised pill — is lighter than its parent. Component-library dark defaults often invert this.
- **Dim stroke icons with solid colors.** Semi-transparent strokes brighten where an icon's paths overlap; pick the solid gray that matches the intended level.
- **Motion is quiet and intentional.** The sidebar slides on an eased curve, list reorders animate items to their new slots, and everything degrades to cross-fades under reduced motion. Switching labs itself stays instant — it's the highest-frequency action.

## Setup

For a Next.js App Router host, read [references/nextjs-scaffold.md](references/nextjs-scaffold.md) before writing code — it holds the concrete module shapes and gotchas. For another router or a bare app, skip that reference and build from the conventions above using the host's native route, module, and styling patterns.

1. **Recon the host.** Done when you can name the router, styling system, design tokens, any installed component library, any control-panel library, and every existing experiment route scattered elsewhere (debug routes, internal pages).
2. **Migrate strays.** Move existing experiment pages into the lab directory with history-preserving renames (`git mv`), normalizing each to the file split, and remove dev-only route gates — the section's posture is decided at the layout, not per lab. Old URLs may 404; they were unlinked. Done when every route from the recon has a migrated destination or a recorded reason to stay put.
3. **Build the registry seam.** One pure function: folder slugs plus optional metadata in, nav model out. Filesystem access and metadata imports live in a thin loader beside the layout. Done when the registry has passing tests (this is the only unit-tested code in the shell) and the loader lists exactly the page-bearing folders.
4. **Build the shell**: a layout that renders the sidebar from the registry and sets `noindex`. For the sidebar and the control panel, use what the host already has; where the host has neither, ask the user to choose (sidebar: a component library's sidebar — e.g. shadcn's — or a plain ~60-line rail; control panel: dialkit or their preference), then build with the choice. Host-specific extras (a link to an internal dashboard, "back to main site") go in the sidebar footer, marked as host extensions outside the general pattern.
5. **Update the host's agents file.** Merge the section in [references/agents-md-section.md](references/agents-md-section.md) into the project's `AGENTS.md` / `CLAUDE.md`. Done when the merged section contains no bracketed placeholders and its paths, libraries, and loop descriptions match what was actually built — this is what makes "make me a lab for X" work in later sessions.
6. **Verify.** Done when: registry and loader tests pass; the production build passes; the `/lab` index and every lab route load in a browser with a clean console; every lab route renders `noindex` in its head; and the section appears in no sitemap or main-site navigation.

Completion criterion: every experiment route the recon found is migrated or accounted for, every sidebar entry resolves to a rendering lab, the agents-file section is placeholder-free and accurate, and every check in step 6 passes.
