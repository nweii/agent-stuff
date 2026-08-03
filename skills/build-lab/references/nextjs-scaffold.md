# Next.js scaffold shapes and gotchas

Concrete shapes for an App Router host. Adapt names to the project; keep the seams.

## Module layout

```
app/lab/
├── layout.tsx        # shell: sidebar + noindex; server component
├── page.tsx          # /lab index (a quiet landing — the sidebar carries the list)
├── entries.ts        # fs loader: lab dirs + optional meta modules → LabEntry[]
├── LabNav.tsx        # client nav: active-state highlight (usePathname), optional sorting
├── InsetTrigger.tsx  # client: floating open-sidebar button, shown when collapsed
└── <slug>/
    ├── page.tsx      # thin route wrapper
    ├── lab.tsx       # "use client" experiment + controls
    └── meta.ts       # optional; default-exports LabMeta

lib/lab-registry.ts       # pure nav-model builder — the tested seam
lib/lab-registry.test.ts
```

## The registry (pure, tested)

This module is framework-neutral — use it verbatim:

```ts
export type LabStatus = "tuning" | "settled" | "superseded";

export type LabMeta = {
  title?: string;
  description?: string;
  /** ISO date (YYYY-MM-DD): when the lab started, or was last meaningfully revisited. */
  date?: string;
  status?: LabStatus;
  /** What the exploration settled on — a variant name or a short phrase. */
  outcome?: string;
};

export type LabEntry = { slug: string; meta?: LabMeta; modified?: string };

export type LabNavItem = LabMeta & {
  slug: string;
  href: string;
  title: string;
  modified?: string;
};

/** Sentence-cases a folder slug: "color-picker" → "Color picker". */
export function titleFromSlug(slug: string): string {
  const words = slug.replace(/-/g, " ").trim();
  return words.charAt(0).toUpperCase() + words.slice(1);
}

/**
 * Builds the sidebar nav model. Metadata is optional throughout — a bare
 * folder yields a nav item titled from its slug. Input order is preserved:
 * ordering is the nav's concern (it sorts client-side by user preference).
 */
export function buildLabRegistry(entries: LabEntry[]): LabNavItem[] {
  return entries.map(({ slug, meta, modified }) => ({
    ...meta,
    slug,
    href: `/lab/${slug}`,
    title: meta?.title || titleFromSlug(slug),
    ...(modified ? { modified } : {}),
  }));
}
```

Keep exactly **one** sort implementation. The registry preserves input order; whatever renders the nav owns ordering (a client sort by mtime/name, a user preference). A registry that also sorts is dead code the moment the nav re-sorts — this was a real review finding, not a hypothetical.

Test exactly this module's external behavior: slug fallback, input-order preservation, metadata passthrough, no `undefined` keys. Also give the loader a small contract test against the real lab folder (every entry's folder has a page, every `modified` parses). Nothing else in the shell needs tests.

## The loader

```ts
const LAB_DIR = path.join(process.cwd(), "app", "lab");

export async function loadLabEntries(): Promise<LabEntry[]> {
  const dirs = fs.readdirSync(LAB_DIR, { withFileTypes: true })
    .filter((e) => e.isDirectory()).map((e) => e.name);
  return Promise.all(dirs.map(async (slug) => {
    if (!fs.existsSync(path.join(LAB_DIR, slug, "meta.ts"))) return { slug };
    const meta = (await import(`./${slug}/meta.ts`)).default as LabMeta;
    return { slug, meta };
  }));
}
```

Only folders bearing a `page.tsx` become entries — a stray asset folder must not appear as a dead nav link. The template-literal dynamic import works under Turbopack/webpack (it builds a context of matching modules) **but only if at least one `meta.ts` exists** — scaffold one annotated lab so the context is never empty. Optionally stat each lab dir's newest file mtime into `modified` for a "recently modified" sort; guard the empty-folder case (`Math.max()` of no files is `-Infinity`, which throws when stamped into a Date), and know the sort is meaningful locally only — deploy checkouts flatten mtimes.

## The layout

```tsx
export const metadata: Metadata = { title: "Lab", robots: { index: false, follow: false } };
// SidebarProvider > Sidebar (header wordmark + nav + footer) > SidebarInset > children
```

No sitemap entry, no links from the main site. If a host link must appear only in some builds (a dev-only dashboard), gate it with a build-time constant (`process.env.NODE_ENV`), not a per-request check — request-time APIs in the layout would force every lab route dynamic.

## Gotchas (each cost real debugging time)

- **The shell must not paint over labs.** Content-pane wrappers often ship an opaque background (shadcn's `SidebarInset` has `bg-background`). A lab that renders a `fixed` backdrop at negative z-index gets covered: positioned ancestors paint after root-level negative-z elements. Make the inset `bg-transparent`; the page body's background is the canvas.
- **The sidebar needs its own background behind its border.** If only an inner element carries the fill, the 1px border column is transparent to the body behind it and reads as a dark seam. Put the background on the bordered container.
- **The mobile sidebar is a different element.** Sheet/drawer implementations portal to `body`, so classes on the desktop container and scoped CSS under a wrapper never reach it. Style it via its own attribute (e.g. `[data-slot="sidebar"][data-mobile="true"]`).
- **shadcn styles differ by registry style.** Base-UI-based styles (e.g. base-maia) use a `render` prop where Radix styles use `asChild`; check the installed component before wiring links into buttons.
- **Default motion may be off-brand.** shadcn's sidebar slides with `ease-linear` on inner divs its props never reach; override with scoped CSS (`.lab-shell [data-slot="sidebar-gap"], .lab-shell [data-slot="sidebar-container"] { transition-timing-function: …; }`).
- **Trigger placement**: inside the sidebar header when expanded; a floating twin in the content pane fades in when collapsed. Make the twin `sticky` (not `fixed`, which overlaps the open sidebar), sit it on the content's title line, give it a page-colored translucent backing so it survives content scrolling under it, and right-align it on small screens where content titles start flush left.
- **Dimming stroke icons**: use solid colors, not alpha tokens — semi-transparent strokes brighten where an icon's paths overlap.
- **Elevation reads lighter.** In dark UIs, a surface on top of another (active-tab fill, raised pill) should be lighter than its parent; several shadcn dark defaults invert this.
- **Framework CSS variables may not re-resolve in theme subtrees.** Aliases declared at `:root` (`--accent`, `--sidebar-*`) capture values at declaration scope; forcing a theme on a subtree requires re-declaring the alias set inside it. Simplest escape: keep the whole lab wing single-theme.
