---
name: build-lab
description: "Set up a /lab section in a website: a sidebar-navigated home for durable design experiments (tuning panels, prototypes), plus the agents-file conventions that make future lab authoring work. Use when the user wants a lab endpoint, experiment shell, or prototyping wing in a web project."
disable-model-invocation: true
metadata:
  author: nweii
  version: "0.1.0"
  credit: "Pattern developed on nathancheng.work (live demo at nathancheng.work/lab). Variant-divergence discipline adapted from Emil Kowalski's prototyping approach."
---

# Lab

A **lab** is a durable experiment surface inside a website the user runs: a page where a design idea gets built against real production components, tuned with live controls, and then *kept* — as an instrument to revisit and as design history. The `/lab` section is the wing of the site that holds them, with a sidebar to move between labs.

Labs are the opposite of throwaway prototypes. Never delete a lab; a settled exploration gets annotated (status, outcome), not cleaned up. This posture is the load-bearing decision — everything else follows from it.

This skill is for **setup**: it installs the shell and teaches the host repo the vocabulary. Day-to-day lab authoring is then driven by the section it writes into the project's agents file — after setup, "make me a lab for X" needs no skill at all. If the project has no `app`-style routing or the user wants a standalone playground, the host can be a bare app whose only content is `/lab` — the pattern is unchanged.

## The conventions (both branches rest on these)

- **Folder = lab.** A new folder with a page inside the lab directory appears in the sidebar automatically. No registration step, ever.
- **File split**: a thin server/route wrapper (`page`) plus a client component holding the experiment and its controls (`lab`).
- **Optional metadata**: a lab may carry a small `meta` module — title, description, date, status (`tuning` / `settled` / `superseded`), outcome (what it settled on). Absent metadata falls back to the folder slug. Metadata is never required.
- **Defaults flow from production.** A tuning lab imports its starting values from the production module it tunes, so the lab can never drift from what ships. Accepted values travel back by copying the control panel's output and applying it to the production source. For the control panel itself, use whatever the host already has; if it has nothing, suggest dialkit — the user's preference wins. Whatever the library, the capability that matters is exporting the panel's current values in a copyable form, so the apply-back loop works.
- **Labs never import shell components.** The shell reads labs' metadata; the dependency never points the other way. Swapping shells must touch zero labs.
- **The shell asserts no background.** Labs own their canvas edge to edge; an opaque shell layer will silently cover labs that paint fixed or negative-z backdrops.
- **Public, unlinked, unindexed** by default: no links from the main site, `noindex` metadata, absent from any sitemap. Access control, when wanted, is infrastructure in front of the path (Cloudflare Access or equivalent) — never auth code in the app.
- **Variants** inside a lab use a `?v=<name>` search param. Variants diverge on a nameable axis (layout, density, personality, motion) and get real names, never "Option A/B/C". Losing variants stay, marked in metadata.

## Setup

Read [references/nextjs-scaffold.md](references/nextjs-scaffold.md) before writing code — it holds the concrete module shapes and the gotchas that cost real debugging time. For a non-Next host, translate its shapes; the conventions above are framework-neutral.

1. **Recon the host.** Identify the router, styling system, design tokens, whether a component library (e.g. shadcn) is already installed, and whether any experiment pages already exist scattered elsewhere (debug routes, internal pages).
2. **Migrate strays.** Move existing experiment pages into the lab directory with history-preserving renames (`git mv`), normalizing each to the file split. Old URLs may 404; they were unlinked. Remove any dev-only route gates — the section's posture is public-unlinked-unindexed, decided at the layout, not per lab.
3. **Build the registry seam.** One pure, tested function: folder slugs plus optional metadata in, ordered nav model out. Filesystem access and metadata imports live in a thin loader beside the layout. This is the only unit-tested code in the shell.
4. **Build the shell**: a layout that renders the sidebar from the registry and sets `noindex`. For the sidebar, use the host's existing component library if present; with none, suggest shadcn's sidebar or offer a plain rail (~60 lines) for hosts that don't want the dependency — the user's preference wins. Host-specific extras (a link to an internal dashboard, "back to main site") go in the sidebar footer, marked as host extensions outside the general pattern.
5. **Update the host's agents file.** Merge the section in [references/agents-md-section.md](references/agents-md-section.md) into the project's `AGENTS.md` / `CLAUDE.md`, adapted to what was actually built. This is what makes "make me a lab for X" work in later sessions — don't skip it.
6. **Verify**: registry tests green, production build green, every migrated lab loads in a browser with a clean console, and the lab index responds with `noindex` in its rendered head.

Completion criterion: every experiment page the recon found is reachable from the sidebar, the agents-file section exists, and the verification list above passes.
