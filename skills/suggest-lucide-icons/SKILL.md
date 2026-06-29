---
name: suggest-lucide-icons
description: "Pick Lucide icons for a concept, UI placement, or vault note. Searches the full Lucide catalog for real, verified icon names. Use when the user says 'what icon for X', 'suggest a Lucide icon', 'pick an icon', or needs an icon for note frontmatter, a button, or a section header."
model: sonnet, inherit
metadata:
  author: nweii
  version: "1.4.0"
---

# Suggest Lucide Icons

Suggest the most relevant icons from the [Lucide open source icon pack](https://lucide.dev) to symbolize a concept or fit specific UI placements. Reason about symbolic associations broadly — across culture, science, and design — rather than only literal matches.

## Input

Provide one or both:

- **Concept**: The idea, action, or meaning to represent
- **Screenshot**: UI context showing where icons are needed

## The catalog script

`scripts/lucide.py` (Python 3, no dependencies) fetches the entire Lucide set once from `unpkg.com/lucide-static@latest/tags.json`, caches it ~24h, and searches and validates locally — so you never fetch icons one at a time:

- `search "<terms>"` — real icons matching a concept by name and semantic tag, ranked. Every result is an icon that exists, listed with its tags so you can see why it fits.
- `validate <name>...` — confirm specific names (e.g. a compound you built by hand). Misses come back with near-match suggestions, and the exit code is nonzero if any name is missing.

If Python 3 isn't available, fetch that URL directly (it's `{name: [tags]}`), or check one icon at `https://unpkg.com/lucide-static@latest/icons/<name>.svg` (200 exists, 404 doesn't; follow the 302 redirect).

## Naming conventions

Icon names follow strict rules — apply these when reading results or building compound candidates to validate:

- **kebab-case**: `arrow-up` not `Arrow Up`
- **International English**: `color` not `colour`
- **Group variants**: `<group>-<variant>` — e.g. `badge-plus` is based on `badge`
- **Multiple elements, different sizes**: list largest first — `circle-person` if circle is bigger
- **Element with modifier**: `[element]-[modifier]` — `circle-dashed` not `dashed-circle`; combined: `circle-dashed-heart-broken`

## Process

1. **Brainstorm associations** — key ideas, visual metaphors, and screenshot context clues. Turn them into a handful of search terms.

2. **Search the catalog** — pull candidates from the script's results rather than guessing names:

   ```bash
   python3 scripts/lucide.py search "calendar schedule date"
   ```

   The tags show why each fits. If you build a compound name from the naming conventions, confirm it before suggesting:

   ```bash
   python3 scripts/lucide.py validate circle-dashed-heart-broken
   ```

3. **Present 3 confirmed candidates** — icon name, and why it fits (symbolic meaning, visual clarity, context appropriateness).

4. **Recommend best choice** — single strongest option, with rationale.

## Guidelines

- Only suggest icons confirmed by `search` (results are real) or `validate` (for hand-built names) — never a made-up name.
- If fewer than 3 candidates survive, search more terms before giving up.
- If no good matches exist after thorough searching, say so.
- For screenshots, tailor to the specific design context.
- Provide a distinct recommendation for each icon needed.
- Ready for multiple feedback rounds to refine suggestions.

## Output Format

**Brainstorm**: [Key associations and metaphors]

**Candidate Icons**:

1. **icon-name** — Explanation of fit
2. **icon-name** — Explanation of fit
3. **icon-name** — Explanation of fit

**Recommendation**: **icon-name** — Why this is the strongest choice for [context]
