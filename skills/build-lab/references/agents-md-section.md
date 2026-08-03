# Agents-file section template

Merge this into the host project's `AGENTS.md` / `CLAUDE.md` during scaffolding, adapted to the paths, libraries, and shell actually built. Its job is to make future agent sessions understand "lab" the way the user means it — without this, the scaffold is a one-session trick.

Replace bracketed placeholders; drop lines that don't apply.

```markdown
### Labs (`/lab`)

`[app/lab/<slug>/]` holds this site's experiment surfaces: tuning panels wired
to production components, and design explorations. Labs are **durable
instruments, never deleted** — they are revisited to re-tune values and kept as
design history; settled explorations get annotated, not cleaned up. The section
is public but unlinked and `noindex`ed; any gating belongs in infrastructure in
front of the path, never in app code.

Conventions:

- **Folder = lab.** A new folder with a `[page.tsx]` appears in the sidebar
  automatically; no registration.
- **File split**: `[page.tsx]` (thin server wrapper) + `[lab.tsx]` (client
  component with the controls).
- **Optional `[meta.ts]`**: default-exports a `[LabMeta]` (`[lib/lab-registry.ts]`)
  — title, description, date, status (`tuning`/`settled`/`superseded`), outcome
  (what it settled on). Absent meta falls back to the folder slug.
- **Defaults flow from production**: a tuning lab imports its defaults from the
  module it tunes; accepted values travel back via [the control panel's
  copy-to-clipboard], applied by an agent.
- **Labs never import shell components.** The shell (`[app/lab/layout.tsx]`,
  `[LabNav.tsx]`, `[entries.ts]`) depends on labs' metadata, never the reverse.

The registry (`[lib/lab-registry.ts]`) is a pure, tested module — keep the test
suite green after changes. Variant exploration inside a lab uses a `?v=` search
param with named variants that diverge on a stated axis (layout, density,
personality, motion) — real names, never "Option A/B/C"; losing variants stay.

Authoring a new lab: create the folder and file split (it appears in the
sidebar with no registration), wire controls with [the project's control-panel
library — e.g. dialkit] importing defaults from the production module under test, and verify
the controls change what's on screen. When a lab settles a decision, apply the
accepted values back to the production source, then mark its `[meta.ts]`
(status, outcome) — the lab now shows production's new defaults, closing the
loop.
```
