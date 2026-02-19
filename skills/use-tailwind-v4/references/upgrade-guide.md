# Tailwind CSS v3 to v4 Upgrade Guide

Source: https://tailwindcss.com/docs/upgrade-guide

## Using the Upgrade Tool

```bash
npx @tailwindcss/upgrade
```

- Requires Node.js 20+
- Run in a new branch, review diff and test in browser
- Automates: dependency updates, config migration to CSS, template changes

Review all [breaking changes](#changes-from-v3) for anything the tool may miss.

---

## Manual Upgrade Steps

### PostCSS Configuration

Replace `tailwindcss` with `@tailwindcss/postcss`. Remove `postcss-import` and `autoprefixer` (now handled automatically):

```js
// postcss.config.mjs
export default {
  plugins: {
    "@tailwindcss/postcss": {},
  },
};
```

### Vite Configuration

Use the dedicated Vite plugin for better performance:

```ts
// vite.config.ts
import { defineConfig } from "vite";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  plugins: [tailwindcss()],
});
```

### Tailwind CLI

Use `@tailwindcss/cli` instead of `tailwindcss`:

```bash
# Before
npx tailwindcss -i input.css -o output.css

# After
npx @tailwindcss/cli -i input.css -o output.css
```

---

## Changes from v3

### Removed @tailwind Directives

```css
/* Before */
@tailwind base;
@tailwind components;
@tailwind utilities;

/* After */
@import "tailwindcss";
```

### Removed Deprecated Utilities

| Deprecated | Replacement |
|------------|-------------|
| `bg-opacity-*` | `bg-black/50` |
| `text-opacity-*` | `text-black/50` |
| `border-opacity-*` | `border-black/50` |
| `divide-opacity-*` | `divide-black/50` |
| `ring-opacity-*` | `ring-black/50` |
| `placeholder-opacity-*` | `placeholder-black/50` |
| `flex-shrink-*` | `shrink-*` |
| `flex-grow-*` | `grow-*` |
| `overflow-ellipsis` | `text-ellipsis` |
| `decoration-slice` | `box-decoration-slice` |
| `decoration-clone` | `box-decoration-clone` |

### Renamed Utilities

| v3 | v4 |
|----|-----|
| `shadow-sm` | `shadow-xs` |
| `shadow` | `shadow-sm` |
| `drop-shadow-sm` | `drop-shadow-xs` |
| `drop-shadow` | `drop-shadow-sm` |
| `blur-sm` | `blur-xs` |
| `blur` | `blur-sm` |
| `backdrop-blur-sm` | `backdrop-blur-xs` |
| `backdrop-blur` | `backdrop-blur-sm` |
| `rounded-sm` | `rounded-xs` |
| `rounded` | `rounded-sm` |
| `outline-none` | `outline-hidden` |
| `ring` | `ring-3` |

### Space-between Selector Change

```css
/* Before */
.space-y-4 > :not([hidden]) ~ :not([hidden]) {
  margin-top: 1rem;
}

/* Now */
.space-y-4 > :not(:last-child) {
  margin-bottom: 1rem;
}
```

If this causes issues, migrate to flex/grid with `gap`:

```html
<div class="flex flex-col gap-4 p-4">
```

### Gradient Variants

In v4, gradient values are preserved across variants. Use `via-none` to unset a three-stop gradient:

```html
<div class="bg-linear-to-r from-red-500 via-orange-400 to-yellow-400 dark:via-none dark:from-blue-500 dark:to-teal-400">
```

### Container Configuration

Configure via `@utility` instead of JS config:

```css
@utility container {
  margin-inline: auto;
  padding-inline: 2rem;
}
```

### Default Border Color

Changed from `gray-200` to `currentColor`. Explicitly specify colors:

```html
<div class="border border-gray-200 px-2 py-3">
```

Or restore v3 behavior:

```css
@layer base {
  *, ::after, ::before, ::backdrop, ::file-selector-button {
    border-color: var(--color-gray-200, currentColor);
  }
}
```

### Default Ring Width and Color

Changed from 3px/`blue-500` to 1px/`currentColor`. Update:

```html
<button class="focus:ring-3 focus:ring-blue-500">
```

Or restore v3 behavior:

```css
@theme {
  --default-ring-width: 3px;
  --default-ring-color: var(--color-blue-500);
}
```

### Preflight Changes

**Placeholder color**: Now uses current text color at 50% opacity instead of `gray-400`.

**Buttons**: Now use `cursor: default`. To restore pointer:

```css
@layer base {
  button:not(:disabled), [role="button"]:not(:disabled) {
    cursor: pointer;
  }
}
```

**Dialog margins**: Now reset. To restore centering:

```css
@layer base {
  dialog { margin: auto; }
}
```

### Prefix Syntax

Prefixes now look like variants at the beginning:

```html
<div class="tw:flex tw:bg-red-500 tw:hover:bg-red-600">
```

Theme variables configured without prefix; generated CSS includes prefix:

```css
@import "tailwindcss" prefix(tw);

@theme {
  --font-display: "Satoshi", "sans-serif"; /* No prefix */
}

/* Generated: --tw-font-display */
```

### Custom Utilities

Replace `@layer utilities/components` with `@utility`:

```css
/* Before */
@layer utilities {
  .tab-4 { tab-size: 4; }
}

/* After */
@utility tab-4 {
  tab-size: 4;
}
```

### Variant Stacking Order

Changed from right-to-left to left-to-right. Reverse order-sensitive variants:

```html
<!-- Before -->
<ul class="first:*:pt-0 last:*:pb-0">

<!-- After -->
<ul class="*:first:pt-0 *:last:pb-0">
```

### Variables in Arbitrary Values

Use parentheses instead of square brackets:

```html
<!-- Before -->
<div class="bg-[--brand-color]"></div>

<!-- After -->
<div class="bg-(--brand-color)"></div>
```

### Hover Styles on Mobile

Now only applies when device supports hover:

```css
@media (hover: hover) {
  .hover\:underline:hover { text-decoration: underline; }
}
```

To restore old behavior:

```css
@custom-variant hover (&:hover);
```

### Transitioning outline-color

`transition` and `transition-color` now include `outline-color`. Set outline color unconditionally:

```html
<button class="outline-cyan-500 transition hover:outline-2">
```

### theme() Function

Prefer CSS variables:

```css
/* Before */
background-color: theme(colors.red.500);

/* After */
background-color: var(--color-red-500);
```

For media queries, use CSS variable name:

```css
@media (width >= theme(--breakpoint-xl)) { }
```

### JavaScript Config

Still supported but not auto-detected. Load explicitly:

```css
@config "../../tailwind.config.js";
```

Not supported: `corePlugins`, `safelist`, `separator` options.

### Theme Values in JavaScript

Use CSS variables directly instead of `resolveConfig`:

```jsx
<motion.div animate={{ backgroundColor: "var(--color-blue-500)" }} />
```

Get computed values:

```js
let styles = getComputedStyle(document.documentElement);
let shadow = styles.getPropertyValue("--shadow-xl");
```

### @apply with Vue/Svelte/CSS Modules

Use `@reference` to access theme in separate stylesheets:

```vue
<style>
  @reference "../../app.css";
  h1 { @apply text-2xl font-bold text-red-500; }
</style>
```

Or use CSS variables directly:

```vue
<style>
  h1 { color: var(--text-red-500); }
</style>
```
