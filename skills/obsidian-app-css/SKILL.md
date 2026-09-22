---
name: obsidian-app-css
description: "Use when writing, debugging, auditing, or reorganizing CSS snippets or app themes for Obsidian desktop/mobile, including DOM selectors, CSS variables, platform classes, plugin/theme compatibility, specificity, or cascade conflicts. Excludes hosted Publish, publish.css, and publish.js."
metadata:
  author: nweii
  version: "0.1.0"
  source: nweii/agent-stuff
  credit: "Informed by Obsidian's developer documentation and David V. Kimball's obsidian-dev-skills."
---

# Obsidian app CSS

Treat the running app and its current styles as the source of truth. Obsidian's internal DOM is useful but not a stable public interface; prefer supported variables and high-level selectors, and verify any deeper selector against the installed app version.

## Keep the surface straight

This skill owns CSS loaded inside the Obsidian app:

- CSS snippets in `.obsidian/snippets/`
- App themes and their `theme.css`
- Core-view, editor, mobile, and community-plugin presentation

Hosted Obsidian Publish is a different DOM and runtime. Route `publish.css`, `publish.js`, and Publish-site customization to `obsidian-publish-customize`.

## Inspect before changing

1. Read the vault or theme repository instructions.
2. Read the relevant snippets and the current `.obsidian/appearance.json`. Treat the enabled basenames as configuration, but inspect the live app when exact cascade order matters.
3. Read the selected theme's `theme.css` and any targeted plugin stylesheet. A variable such as `--bg1` or class such as `tabs-modern` may belong to one theme rather than Obsidian.
4. For an undocumented selector or disputed computed value, inspect the live element in Electron DevTools. Use the installed `app.css` as a secondary source when DevTools is unavailable.

Inspection is complete when every selector and variable being changed has a known owner: Obsidian, the selected theme, a plugin, CodeMirror, or the snippet itself.

For the practical hierarchy and selector stability ladder, read [DOM and selectors](references/dom-and-selectors.md).

## Put each rule with its owner

Organize snippets by the surface that must change together, not by vague intent such as “tweaks” or “polish.” Useful ownership seams include:

- `Core - Typography`
- `Core - Markdown`
- `Core - Workspace`
- `Core - Components`
- `Core - Interaction`
- `Mobile - …`
- `Plugin - <name>`
- `Palette - <name>`
- `Theme - <name> - <concern>`

Keep a rule with the narrowest owner that explains it. A generic visual goal can cross several owners; that is a reason to split it, not a reason to create a grab-bag file. Combine rules when they always need the same activation scope and test matrix.

When reorganizing a collection of local overrides, read [Snippet boundaries](references/snippet-boundaries.md) before deciding which rules share a file.

Installed themes do not share a dependable class naming the selected theme. Treat `Theme -` snippets as explicit companions that may need manual activation. A theme's settings classes are valid gates only when that theme actually owns them; do not infer the selected theme from platform classes such as `.mod-macos`.

## Choose the most stable seam

Use this order:

1. Documented Obsidian CSS variable
2. High-level body/platform/state class or view attribute
3. Stable core, theme, or plugin class
4. Short descendant selector
5. Deep DOM path, positional selector, or CodeMirror implementation class

Move down only when the level above cannot express the behavior. Comment the dependency when a rule relies on private theme variables, positional structure, `:has()`, `nth-*`, or CodeMirror internals.

Prefer selectors such as:

```css
body:not(.is-mobile) { }
body.is-phone { }
.workspace-leaf-content[data-type="markdown"] { }
.workspace-leaf-content[data-mode="source"] { }
```

Use `!important` only when the existing cascade cannot be crossed with a variable or a comparably scoped selector. Put the reason beside it.

## Audit the cascade

Before consolidating or splitting files, inventory:

- variables declared by more than one enabled snippet;
- selectors aimed at the same element or state;
- generic `.theme-light` and `.theme-dark` rules that replace the selected theme;
- private theme variables used outside their theme gate;
- plugin selectors mixed into core snippets;
- mobile rules embedded in otherwise desktop-only files;
- stale enabled basenames and renamed files.

Do not assume alphabetical display proves stylesheet injection order. Inspect `<head>` or computed styles when order determines the result.

## Verify the result

After editing:

1. Parse the changed CSS with the project's linter when available; otherwise at least check balanced blocks and comments.
2. Confirm every enabled basename resolves to one root-level `.css` file.
3. Confirm renamed, split, or consolidated rules have exactly one live owner.
4. Exercise the affected surface in the live app. For shared snippets, check every installed theme they claim to support; for color rules, check light and dark; for responsive rules, check desktop plus the relevant phone/tablet class.
5. Report static inspection separately from live visual verification.

Verification is complete when each changed rule has one owner, every configured snippet resolves, and every claimed environment has either been exercised or named as unverified.

## Sources

- [Obsidian CSS variables](https://docs.obsidian.md/Reference/CSS+variables/CSS+variables)
- [Obsidian app themes](https://docs.obsidian.md/Themes/App+themes/App+themes)
- [Obsidian sample theme](https://github.com/obsidianmd/obsidian-sample-theme)
- [Obsidian developer skills](https://github.com/davidvkimball/obsidian-dev-skills)
