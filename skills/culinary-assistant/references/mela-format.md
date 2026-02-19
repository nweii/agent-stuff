# Mela recipe format

Reference for Mela's `.melarecipe` file format. See [official docs](https://mela.recipes/fileformat/index.html).

## File types

- **`.melarecipe`** — Single recipe, JSON file
- **`.melarecipes`** — Multiple recipes, ZIP containing `.melarecipe` files

## JSON fields

| Field | Type | Notes |
|-------|------|-------|
| `id` | String | Required. URL without schema (e.g., `example.com/recipe/123`) or UUID |
| `title` | String | Recipe name |
| `text` | String | Short description. Markdown: links only |
| `images` | [String] | Base64-encoded images (use `[]` for imports) |
| `categories` | [String] | **No commas allowed** in category names |
| `yield` | String | Servings or yield |
| `prepTime` | String | Human-readable (e.g., "15 minutes") |
| `cookTime` | String | Human-readable |
| `totalTime` | String | Doesn't have to equal prep + cook |
| `ingredients` | String | Items separated by `\n`. Markdown: links, `#` for group titles |
| `instructions` | String | Steps separated by `\n`. Markdown: `#`, `*`, `**`, links |
| `notes` | String | Tips, variations. Markdown: `#`, `*`, `**`, links |
| `nutrition` | String | Nutrition info. Markdown: `#`, `*`, `**`, links |
| `link` | String | Source (URL or any text) |

### Ignored on import

These fields exist in exports but are ignored when importing:

| Field | Type | Notes |
|-------|------|-------|
| `favorite` | Boolean | |
| `wantToCook` | Boolean | |
| `date` | Double | Seconds since 2001-01-01 00:00:00 UTC |

## Formatting guidelines

### Ingredients

```
# For the dough
2 cups flour
1 tsp salt
# For the filling
1 lb ground beef
1 onion, diced
```

### Instructions

Do not number steps—Mela adds numbers automatically.

```
# Prep
Dice the onion and mince the garlic.
# Cook
Heat oil in a large skillet over medium-high heat.
Add the onion and cook until softened, about 5 minutes.
```

### Step organization

- Combine related actions into coherent steps
- Use `#` headers for distinct phases (components, major transitions, parallel processes)
- Keep steps focused—neither too granular nor too dense

Good: "Add the wontons to the simmering broth and cook until they float, about 3-4 minutes"

Not: "Add the wontons" + "Cook until they float"

## Common issues

- **Commas in categories**: Will break. Use separate array items instead
- **Double newlines**: Never use `\n\n`—use `#` headers for visual separation
- **Empty `id`**: Import will fail. Always generate a UUID if no source URL
