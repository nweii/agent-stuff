---
name: obsidian-publish-customize
description: "Customize an Obsidian Publish site through the publish.css and publish.js root hooks — theming with Publish CSS variables, and scripting the rendered page (injecting frontmatter blocks, nav, widgets). Use when editing publish.css/publish.js files, theming a Publish site, or working around Publish's undocumented client-side behavior. NOT for Publish usage, Obsidian desktop-app theming, or plugin development."
compatibility: "Assumes an Obsidian Publish subscription and an active Publish website to customize. A custom domain is required for javascript-driven customizations."
metadata:
  author: nweii
  version: "1.0.0"
  last: 2026-06-14
---

# Obsidian Publish customization

Obsidian Publish hosts a vault as a website. Two root files are the only hooks for changing it beyond the built-in site options: `publish.css` (custom styles) and `publish.js` (custom scripts). Both are supported insertion points, but almost everything past basic theming is undocumented — you script against Publish's rendered DOM and private globals, which can change without notice.

- Both files live at the **vault root** (`/publish.css`, `/publish.js`). Hidden from the file explorer by default; publish them from the **Publish changes** dialog.
- `publish.js` **only runs on a custom domain.** On the default `publish.obsidian.md/<site-id>` URL it's inert. `publish.css` works everywhere.

**Scope.** Theming via Publish CSS variables, and scripting the rendered page via publish.js. Out of scope, kept separate as three documentation domains:

- Normal Publish operation — publishing notes, custom-domain setup, the Publish CLIs.
- Obsidian *desktop-app* theming — themes and CSS snippets inside the app.
- Plugin development — the developer API for community plugins.

CSS variables overlap between app and Publish (see Theming), but the app's theming workflow and the plugin API are separate references — don't conflate them.

## Pushing and iterating

Publishing the root files needs an active Publish subscription and one of two CLIs, depending on the environment:

- **Desktop app available:** the Obsidian app CLI publishes a file directly — `obsidian publish:add path=publish.css` (or `path=publish.js`); needs the desktop app running. Its `publish:list`/`status`/`site` commands may return no output, so there's no reliable confirmation a push landed — verify in the browser.
- **Headless / CI (no desktop app):** the `obsidian-headless` CLI (`ob` via `bun` or `npm install -g obsidian-headless`) publishes from the command line. After `ob login` and `ob publish-setup --site <slug>`, run `ob publish` — by default it includes only `publish: true` notes, so add `--all` to include the root static assets, and `--dry-run` to preview. `ob publish-site-options` sets the site toggles non-interactively.

Then, regardless of which CLI pushed:

- Publish CDN-caches assets; **hard-refresh** after every push.
- **Test publish.js in the browser console before committing it.** Iteration is live-site-only and undocumented, so prototype in DevTools first. An agent usually can't reach the authenticated site directly, so the loop is: hand the user a self-contained snippet to paste into the web inspector — an IIFE that `console.log`s what it finds and fails closed so it can't break the page — have them report back, iterate, then commit the finished script. Confirm across a few page types (a clipping, a note with backlinks, a note with no metadata).
- `curl` against the live website may return a challenge page (HTTP 403). Probe site endpoints and JSON from the browser console with a same-origin `fetch`, not the shell.

## Scripting publish.js

Two methods. Prefer the post-processor where it fits; reach for the observer when you must react to navigation or place content relative to late-rendering DOM.

### 1. The post-processor API

Publish exposes a `publish` global with `registerMarkdownPostProcessor((el, ctx) => {...})`, mirroring the plugin API. It fires per rendered section; `ctx.frontmatter` is the note's parsed frontmatter as an object (no YAML parsing needed), and `ctx.containerEl` is the render container.

This `publish` global is **undocumented** and not in the official help, so treat it as empirical: you can confirm it still exists with `typeof publish` / `console.log(publish)` in the console.

```js
publish.registerMarkdownPostProcessor((el, ctx) => {
  const fm = el.querySelector("pre.frontmatter");
  if (!fm || !ctx.frontmatter) return;
  // ctx.frontmatter.author, ctx.frontmatter.related, ctx.frontmatter.url, ...
});
```

`window.siteInfo` carries `{ uid, host, customurl, ... }`. The published-file index — needed to resolve a note title to its URL — is fetched same-origin from `https://${siteInfo.host}/cache/${siteInfo.uid}`. (`/cache.json` 404s.)

**Caveat:** the post-processor can run on a render pass whose container is later discarded. Anything injected into the section's own DOM rides along, but `ctx.containerEl` is unreliable for finding elements rendered later (e.g. the backlinks footer) — for those, use the observer.

### 2. MutationObserver over the live DOM

Publish re-renders the content pane on navigation without a full reload, so a load-time script misses later pages. Run an init on each mutation via a `MutationObserver` on `document.body`, gated by an idempotency marker (a class on processed elements) so it doesn't double-bind:

```js
const SEEN = "mb-done";
new MutationObserver(() => {
  document.querySelectorAll(`.target:not(.${SEEN})`).forEach((el) => {
    el.classList.add(SEEN);
    // bind or inject
  });
}).observe(document.body, { childList: true, subtree: true });
```

Use this to react to navigation, or to insert relative to elements that appear after the post-processor runs. To place a block just above the backlinks, watch for `.markdown-preview-sizer > .mod-footer` and `insertBefore` it (with an append fallback for notes that have no backlinks footer).

Both methods build on one primitive: Publish emits each note's frontmatter as a hidden `pre.frontmatter.language-yaml` element. The post-processor hands it to you parsed as `ctx.frontmatter`; without the post-processor, read and parse the element's text.

## DOM gotchas

- **Don't give injected links the `internal-link` class.** Publish's SPA resolver hijacks `.internal-link` for both click handling (rejecting hrefs it doesn't recognize with a "does not exist" page) and hover previews (a misleading "does not exist" popover). Give injected links a private class and your own `href`; add a `stopPropagation` on click as a guard.
- **Use the site's custom domain for every link, never `publish.obsidian.md`.** Read it from `window.siteInfo.customurl` and build absolute URLs as `https://${siteInfo.customurl}/<path>`. This applies to links injected by publish.js *and* to any URL handed to the user (e.g. a page to test) — a `publish.obsidian.md/<site-id>/...` link points at the wrong origin, where internal navigation and link previews break.
- **URL encoding:** Publish encodes path spaces as `+`, not `%20`, and its router rejects `%20`. Build each path segment as `encodeURIComponent(segment).replace(/%20/g, "+")`.
- **`<button>` inherits a themed background** from Publish's base CSS that's hard to beat on specificity. For text-style controls (a toggle, a "show more"), use a `<span role="button" tabindex="0">` with click + Enter/Space handlers — nothing to override.
- **Unpublished wikilinks:** Publish styles links to unpublished notes as disabled with a padlock via `.internal-link.is-unresolved`. Injected links can reuse that class to inherit the treatment, or be dropped/rendered as plain text if a field may point at private notes.

## Theming with publish.css

CSS variables are **deliberately shared between the desktop app and Publish** so themes carry over — but the two sets only partly overlap, and not every variable is exercised on both. They fall into two groups:

- **Publish-specific** — defined on `.published-container`. They cover Publish chrome: site header / logo / name, the nav tree, left and right sidebars, component titles (backlinks / graph / outline headings), graph height, page width and padding, page and site titles, footer. Set these on `.published-container` (mostly layout, mode-independent).
- **App-foundation** — colors, typography, spacing, and content-element variables Publish inherits from the app. Set mode-dependent colors on `.theme-light` / `.theme-dark`, and font families/sizes on `body`. Many carry over; not all are used on Publish.

```css
@import url("...");          /* fonts — @import must be the very first rule */
.published-container { --page-width: 800px; --footer-display: none; }
.theme-light { --background-primary: #fff; --h1-color: #111; }
.theme-dark  { --background-primary: #100f0f; --h1-color: #eee; }
body { --font-text-theme: "..."; }
```

- The canonical variable catalog is the developer docs — read it there rather than duplicating: `docs.obsidian.md/Reference/CSS variables/Publish/`. The inherited app foundation is the sibling Foundations / Components / Editor sections (app docs, not Publish-specific).
- **Responsive breakpoints** Publish uses: `1000px` (right sidebar hides) and `750px` (both sidebars hide, nav becomes a hamburger).
- **Style Settings does not work on Publish** — community themes built around it lose their controls. `--footer-display: none` on `.published-container` removes the "Powered by Obsidian Publish" footer.
- Keep publish.css small; it loads on every visit. Avoid base64-embedded fonts/images (weight + flash of unstyled content).

## Official vs. hack

Knowing the line prevents "fixing" something that is a deliberate limit:

- **Official:** the two static assets; all site-option toggles (theme, navigation, search, graph, table of contents, backlinks, hover preview, readable line length, stacked pages); Cloudflare or proxy custom domains; permalinks and full-path `alias` redirects; the meta properties `publish` / `permalink` / `description` / `image`; CSS-variable theming; publish.js for analytics and a consent banner.
- **Hack territory (not officially supported):** rendering a visible frontmatter/properties block on the page, comments, per-note passwords, anything needing a plugin render codeblock (Dataview and similar), embedded search results, Style Settings.

## A worked combination

These pieces compose in a single root `publish.js`. A representative setup: an icon injector keyed off a frontmatter property, a theme-color meta-tag setter for the mobile toolbar, and a frontmatter **metadata block** that renders selected properties (date, author, url, prev/next, related, freshness) under the page title — the last exercising the post-processor API, the cache endpoint for wikilink resolution, the private-link-class workaround, `+`-encoded custom-domain URLs, and a span-based collapse/expand control. Style the injected output from `publish.css` using the variables above.

## Reference

For the full CSS-variable catalog, site-option details, custom-domain setup, the headless CLI, and anything not covered above, fetch the live docs.

- **Official Publish help** (user-facing) — repo `obsidianmd/obsidian-help`, under `en/Obsidian Publish/`: `Customize your site.md` (the static-asset hooks), `Manage sites.md` (the site-options table), `Custom domains.md`, `Headless Publish.md`, `Publish limitations.md`.
- **Developer docs** (CSS-variable reference) — repo `obsidianmd/obsidian-developer-docs`, under `en/Reference/CSS variables/Publish/` for the Publish-specific variables, and the sibling `Foundations/` / `Components/` / `Editor/` for the inherited app foundation.
- **Community recipes** — the Obsidian forum's "Obsidian Publish resources" thread (`forum.obsidian.md/t/74582`): a catalog of DOM-scripting techniques, all undocumented and tied to Publish's current markup — treat as fragile.

Canonical human-facing docs live at `help.obsidian.md` (Publish help) and `docs.obsidian.md` (developer reference, including the CSS variables). Both are JS-rendered — a plain fetch returns an empty shell, so link users there but read from GitHub.

Use whatever retrieval tool fits — context7, WebFetch, GitHub raw URLs — whichever is faster or more accurate. Prefer live docs over memory.
