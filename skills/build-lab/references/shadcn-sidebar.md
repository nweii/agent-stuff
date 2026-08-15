# shadcn sidebar adapter

Read this only when the lab shell uses shadcn's Sidebar. Inspect the installed components first because registry styles and underlying primitives differ.

- `SidebarInset` commonly carries an opaque background. Make the lab content pane transparent so full-canvas and negative-z backdrops remain visible.
- Put the sidebar fill on the bordered sidebar container, not only an inner element, so the border column cannot expose the page background as a seam.
- The mobile sidebar renders through a portaled sheet or drawer. Style its mobile element directly; scoped desktop selectors do not cross the portal.
- Link composition differs across registry styles. Some builds use Radix `asChild`; Base UI variants may use `render`. Follow the installed component's API.
- Sidebar transitions can live on internal gap and container elements. Apply the host's intended easing to the elements that actually move, and preserve reduced-motion behavior.
- Keep the expanded trigger in the sidebar header. Its collapsed counterpart belongs on the content title line, stays sticky rather than fixed, and moves to the title line's opposite edge when narrow content starts flush left.

Done when the desktop and mobile sidebars share the intended appearance, the collapsed trigger never overlaps the open sidebar or page title, the content canvas remains visible edge to edge, and navigation links use the installed composition API without console warnings.
