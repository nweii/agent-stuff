---
name: vault-recipes
description: "Search, read, filter, combine, adapt, and save recipes in the Brain vault collection. Use whenever cooking and the collection are relevant — 'what should I make', 'recipes with miso', 'save this one' all imply it."
metadata:
  author: nweii
  version: "1.0.0"
  internal: true
---

# Vault recipes

Recipes live in this vault as one note per dish. This skill covers finding, reading, filtering, adapting, combining, and saving them, plus the cooking judgment that reworking them calls for.

## Where the recipes live

A settled set of locations — don't relocate or restructure them:

- `03-Records/Clippings/Recipes/` — the recipe notes (one `.md` per recipe)
- `98-Spaces/Recipes.md` — the hub note (embeds the base; the place to browse)
- `98-Spaces/Engines/Recipes.base` — the query engine (seven views, below)
- `99-Admin/Templates/Recipe Template.md` — the skeleton for new recipes

Recipe notes carry both `[[Clippings]]` and `[[Recipes]]` categories — filed as clippings, but specific enough to live in their own subfolder.

## Pick your access tier

Use the first tier available and stop there:

1. **Obsidian CLI** (`obsidian …`) — when the desktop app is running and the CLI is on PATH. Richest surface: wikilink resolution, link-safe edits, and direct `.base` queries the MCP can't do. Run `obsidian help` for the full command set. Don't reach for the MCP when the CLI is available.
2. **notesmd-cli + file tools** — headless/local without the app.
3. **Brain MCP** (`vault_*` tools) — MCP-only environments like Claude.ai.

The operations below give both the CLI and the MCP form. Translate to notesmd-cli or plain file reads when that's the tier you're on.

## Operations

| Intent | Obsidian CLI (local) | Brain MCP (remote) |
|---|---|---|
| List the collection | `obsidian base:query file=Recipes.base view=Gallery format=json`, or `ls` the folder | `vault_read(mode="list", path="03-Records/Clippings/Recipes")` |
| Full-text search (ingredient, keyword) | `obsidian search query="miso" path="03-Records/Clippings/Recipes"` | `vault_search_content(query="miso", folder="03-Records/Clippings/Recipes")` |
| Find by title fragment | `obsidian read file="Gochujang Buttered Noodles"` (resolves by title) | `vault_search_title(title="gochujang")` → `vault_read` |
| Read a recipe | `obsidian read file="…"` | `vault_read(path="…")` |
| Peek without full read | `obsidian property:read name=description file="…"` | `vault_read_section(heading="Ingredients", path="…")` |
| Filter by cuisine / rating / untried | `obsidian base:query file=Recipes.base view=Untried format=json` | frontmatter regex (see views below) |
| Save a new recipe | `obsidian create name="Title" template="Recipe Template"` | `vault_create(path="03-Records/Clippings/Recipes/Title.md", content=…)` |
| Adapt an existing recipe | `obsidian append/prepend`, or edit the file | `vault_edit_section`, or `vault_update` with `base_version` |

These calls are illustrative; the live tools and their schemas may change, so defer to them.

### Searching by ingredient, precisely

Full-text search matches anywhere in the file, so a hit on "shrimp" might sit in a review or a note rather than the ingredient list. When the question is "which recipes *use* X", confirm the match falls under `## Ingredients` before counting it — read the section, or check the snippet.

### The seven base views

`Recipes.base` already encodes the common filters. Query them directly with the CLI (`obsidian base:query file=Recipes.base view=<View> format=json`); on MCP, approximate with a frontmatter regex over the folder.

| View | What it shows | MCP approximation |
|---|---|---|
| Gallery | everything, newest first, by cover image | list the folder |
| Favorites | `rating > 3` | `vault_search_content(query="^rating: [45]", folder=…)` |
| Untried | `rating` is empty | `vault_search_content(query="^rating: *$", folder=…)` |
| Recently added | last 30 | sort the list by `created` |
| By cuisine | grouped by `cuisine` | `vault_search_content(query="^cuisine:.*Korean", folder=…)` |
| By source | grouped by `publisher` | regex on `^publisher:` |
| Author | recipes whose `author` links a given person | `vault_search_content(query="author:.*Eric Kim", folder=…)` |

Empty `rating` means not yet tried/rated — the signal for "what should I cook next."

## The recipe note shape

New and edited recipes follow this skeleton (keep the field order — it matches the vault's lint order):

```markdown
---
aliases:
categories:
  - "[[Clippings]]"
  - "[[Recipes]]"
icon: LiCookingPot
cover:
description:
url:
author:
publisher:
cuisine:
yield:
prep-time:
cook-time:
rating:
related:
tags:
  - recipes
created:
---

_One tight sentence describing the dish, in italics._

## Ingredients

- 

## Steps

1. 

## Top reviews

Author Name:
> Review body
```

Field notes:

- **cover** — image URL; drives the Gallery and Favorites card images. Blank when there's none.
- **description** — the first sentence of the intro, kept tight; mirror it as the italic line that opens the body.
- **author** — a wikilinked YAML list (`- "[[Eric Kim]]"`). **publisher** — a wikilinked string (`"[[NYT Cooking]]"`). Both link to person/entity notes, which is what powers the Author view.
- **cuisine / yield / prep-time / cook-time** — times in compact form (`5m`, `25m`, `1h 30m`).
- **rating** — 1–5; a favorite is 5. Leave blank to mean untried.
- **tags** — always `recipes`, plus kebab-case descriptors (`pasta`, `pressure-cooker`, `tofu`).

Sections beyond Ingredients and Steps are optional and appear only with content: `## Top reviews` (blockquotes, from clipped recipes), `## Notes` (personal tweaks), `## Nutrition`.

Personal and family recipes use the same skeleton with most fields blank. Don't invent metadata to fill gaps; an empty field is correct when the value is unknown.

## Naming and variants

Filenames are content-first (the dish name, no date prefix). Iterations get a parenthetical suffix rather than overwriting the original:

- `(modified)` / `(enhanced)` — reader comments or hand tweaks already folded into the directions
- `(Instant Pot)`, `(Oven Version)` — cooking-method variant
- `(NYT)` — disambiguates a same-named recipe by source
- `(#79)` — disambiguates two distinct recipes that share a title

When producing a tweaked version, keep the base title and add a suffix — make a new note, don't clobber the source.

## Adapting and combining recipes

Read the recipe(s) in full before changing anything. Note the components, the method, and what gives the dish its character; that's what to preserve.

**Integrating reader comments** (the `(modified)` workflow): weigh suggestions on culinary merit, not popularity. When they conflict, prioritize technique corrections over safety over clarity over flavor over personal preference. Patterns matter — several people reporting the same problem is signal. Be skeptical of changes that alter the dish's character. Fold in the well-reasoned ones; skip vague praise. Mirror the original's layout and voice in the result.

**Step organization**: combine related actions into one coherent step; use headers for distinct phases (separate components, major transitions, parallel work); keep steps neither too granular nor too dense.

- Good: "Add the wontons to the simmering broth and cook until they float, about 3–4 minutes."
- Not: "Add the wontons." then "Cook until they float."

**Combining two recipes**: identify the load-bearing element of each and resolve conflicts in proportion and method by judgment, not by averaging. Offer to save the result as a new note with a variant-style title; don't overwrite either source.

**Scaling**: scale ingredients proportionally, but adjust seasoning, leavening, and cook times by judgment rather than linearly.

## Common workflows

- **Ideas from the collection** — sample or list the folder, surface what recurs (cuisines, proteins, methods), then propose along or against the grain. Cite the notes drawn from.
- **Cook with these pantry items** — search each ingredient inside the folder, intersect the results, and rank candidates by how many of the items each recipe already uses. Surface the closest matches and what they'd still need.
- **Recipes with X** — search `X` in the folder; confirm ingredient-list hits (above).
- **Combine A and B** — see Adapting and combining.
- **What haven't I tried** — Untried view (CLI) or empty-`rating` regex (MCP).

## Saving a recipe from a URL

`vault_clip_url` fetches the page, renders it through the Recipe template in the Web Clipper settings (which auto-matches pages exposing `@Recipe` schema), and returns a note shaped as italic description → Ingredients → Steps → top reviews. Write it into the recipes folder with `vault_create`. For pages with no recipe schema, extract the ingredients and steps directly and fill the skeleton above.

## Guardrails

- **Don't overwrite tuned directions.** A `(modified)` or `(enhanced)` recipe has hand-edited steps — never replace them with a stock version.
- **Respect stated dietary constraints.** When the cook names an allergy or restriction, flag any recipe or suggestion that violates it and offer a substitution.
- **Food safety holds.** Keep safe temperatures, avoid cross-contamination, and note storage limits when relevant.
- **Cultural respect.** Represent dishes and their traditions accurately rather than flattening them.
- **Acknowledge uncertainty.** If unsure about a substitution or technique, say so rather than guess.
- **Concurrency.** On MCP edits to an existing note, pass `base_version` from your last read.
- **Don't publish.** These notes aren't public; never set `publish: true`.
- **Inspect before editing.** Read the note before proposing changes.
