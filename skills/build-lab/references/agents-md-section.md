# Agents-file section template

Merge this into the host project's `AGENTS.md` / `CLAUDE.md` during scaffolding, adapted to the paths, libraries, and shell actually built. Its job is to make future agent sessions understand "lab" the way the user means it — without this, the scaffold is a one-session trick.

Replace bracketed placeholders; drop lines that don't apply.

```markdown
### Labs (`/lab`)

`[app/lab/<slug>/]` holds this site's experiment surfaces: tuning panels wired to production components and design explorations. Retain labs by default so they remain available for retuning and as design history. Record settled decisions in outcome notes; remove labs when the user or this host's lifecycle calls for cleanup.

[State the chosen exposure: public direct-access, protected by the host's existing mechanism, or another deliberate posture.] Apply protection once at `[the lab section boundary]`. The section is `[noindex and omitted from the sitemap and main navigation / intentionally discoverable]`; `noindex` is metadata, not access control.

The lab should feel like a natural extension of this site's design language. Reuse its tokens, components, typography, and interaction patterns when available; diverge when that difference is part of the experiment. The shared shell receives production fit-and-finish even when an experiment remains unfinished. Keep it visually quiet and unframed. Standard lab headers use the shell's title-line height and inset across wide, narrow, expanded, and collapsed states.

Conventions:

- **Folder = lab.** A new folder with a `[page.tsx]` appears in the sidebar automatically; no registration.
- **File split**: `[page.tsx]` (thin server wrapper) + `[lab.tsx]` (client component with the controls).
- **Optional `[meta.ts]`**: default-exports a `[LabMeta]` from `[lib/lab-registry.ts]` with title, description, date, and outcome (a short note on what the lab decided). Absent metadata falls back to the folder slug.
- **Defaults flow from production.** A tuning lab imports defaults from the module it tunes; accepted values travel back through `[the control panel's export mechanism]`, applied by an agent.
- **Harmonize with the destination.** For changes to an existing page, section, or component, use its surrounding content, layout, hierarchy, and interface patterns as the starting point. Depart when that is part of the experiment.
- **The control panel is part of the lab interface.** Use `[the project's control-panel library or native control surface]`. Order controls in the sequence someone tunes the result, group them by concept, keep high-leverage choices visible, and collapse secondary calibration. Use clear labels, useful ranges, and intentional defaults. Its appearance follows the lab by default; a separate appearance is deliberate.
- **Labs stay independent of shell components.** The shell (`[app/lab/layout.tsx]`, `[LabNav.tsx]`, `[entries.ts]`) depends on labs' metadata, never the reverse.

The registry (`[lib/lab-registry.ts]`) is a pure, tested module — keep its test suite green after changes. Parameter snapshots belong in the control panel's presets. Structural or interaction variants use a named `?v=` value, render one direction full-size at a time, and switch instantly; add a visible picker only when rapid comparison helps. Retain unadopted variants by default unless the user or this host's lifecycle calls for cleanup.

Authoring a new lab: create the folder and file split, import production defaults when the lab tunes production, and wire the controls. Prefer a floating panel when the control library supports it and preserving the canvas matters; use an inline panel when persistent side-by-side comparison serves the experiment. Smoke-test unusual wiring such as actions, text fields, manual render loops, and paused states. Animated labs keep play/pause within easy reach, bind Space outside editable controls, and mirror the action in the control panel when its public API supports actions.

When a lab settles a decision, apply the accepted values to the production source, then record the decision as the outcome note in `[meta.ts]`. The lab should then display production's accepted defaults.
```
