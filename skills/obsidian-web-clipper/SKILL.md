---
name: obsidian-web-clipper
description: "Author and debug Obsidian Web Clipper extension templates: template JSON, variables, filters, schema.org/CSS selector syntax, AI interpreter prompts, URL/schema triggers. Use when generating, importing, or fixing a clipper template, or matching a template to a target site. Not for general scraping or other Obsidian features."
metadata:
  author: nweii
  version: "1.3.0"
---

# Obsidian Web Clipper Templates

Obsidian Web Clipper is a browser extension that saves web content to an Obsidian vault as Markdown notes. Templates define how pages are captured — what metadata to extract, how to format the note, and which sites to auto-match.

Templates are configured as JSON. Users can import/export individual templates or full settings backups. When generating templates, output valid JSON the user can import directly.

## Adapt to the user's vault conventions

Templates are deeply opinionated about folder layout, frontmatter property names, category/tag conventions, and note body structure. **Match the user's existing conventions rather than inventing.** Before drafting a template, look for:

- `CLAUDE.md`, `AGENTS.md`, or a `README.md` at the vault root — vault-level conventions
- An existing templates folder (commonly `99-Admin/Templates/`, `_templates/`, or similar) — frontmatter shape and naming for similar note types
- An existing exported web clipper settings file — other templates the user has authored
- Any YAML sort order configuration (Linter plugin, frontmatter sort plugin) — property order
- A few sample notes of the type being clipped — tone, body structure, italicization conventions

When conventions aren't discoverable, default to vendor-neutral, minimal choices (a single `Clippings/` folder, generic property names like `url`, `author`, `tags`, `created`) and explicitly flag the assumptions you made so the user can adjust before import.

If the user mentions plugins like Linter or has a property sort order note, mirror that order in the template's `properties` array — the extension preserves array order in the output frontmatter.

## Template JSON Schema

```json
{
  "schemaVersion": "0.1.0",
  "name": "Template Name",
  "behavior": "create",
  "noteNameFormat": "{{title}} - {{site}}",
  "noteContentFormat": "{{content}}",
  "vault": "VaultName",
  "path": "folder/subfolder",
  "context": "",
  "properties": [],
  "triggers": []
}
```

| Field               | Type   | Description                                                 |
| ------------------- | ------ | ----------------------------------------------------------- |
| `schemaVersion`     | string | Always `"0.1.0"`                                            |
| `name`              | string | Display name shown in the extension                         |
| `behavior`          | string | How the note is created (see below)                         |
| `noteNameFormat`    | string | Filename for the note, supports variables                   |
| `noteContentFormat` | string | Note body content, supports variables                       |
| `vault`             | string | Target vault name (optional — omit to use default)          |
| `path`              | string | Folder path within the vault (optional)                     |
| `context`           | string | Limits what page content the interpreter AI sees (optional) |
| `properties`        | array  | Frontmatter properties (optional)                           |
| `triggers`          | array  | Auto-match rules for URLs/schemas (optional)                |

When exporting a single template, the JSON is the template object directly (no wrapper). When part of a full settings export, templates are stored as `template_[id]` keys.

### Behaviors

| Value              | Description                         |
| ------------------ | ----------------------------------- |
| `create`           | Create a new note                   |
| `append-daily`     | Append to today's daily note        |
| `prepend-daily`    | Prepend to today's daily note       |
| `append-specific`  | Append to a specific existing note  |
| `prepend-specific` | Prepend to a specific existing note |

## Variables

All variables use `{{variableName}}` syntax. Filters chain with pipes: `{{variable|filter1|filter2:"arg"}}`.

### Preset Variables

| Variable          | Description                                                                           |
| ----------------- | ------------------------------------------------------------------------------------- |
| `{{title}}`       | Page title                                                                            |
| `{{author}}`      | Page author                                                                           |
| `{{content}}`     | Article content in Markdown (returns highlights if any, else article, else selection) |
| `{{contentHtml}}` | Article content in HTML                                                               |
| `{{fullHtml}}`    | Full unprocessed page HTML                                                            |
| `{{url}}`         | Current URL                                                                           |
| `{{domain}}`      | Domain name                                                                           |
| `{{site}}`        | Site name / publisher                                                                 |
| `{{date}}`        | Current date                                                                          |
| `{{time}}`        | Current date and time                                                                 |
| `{{published}}`   | Published date                                                                        |
| `{{description}}` | Page description / excerpt                                                            |
| `{{image}}`       | Social share image URL                                                                |
| `{{favicon}}`     | Favicon URL                                                                           |
| `{{highlights}}`  | Array of highlights (each has `.text` and timestamp)                                  |
| `{{words}}`       | Word count                                                                            |

### Schema Variables (Schema.org JSON-LD)

Extract structured data from pages that include Schema.org markup.

| Pattern                   | Example                       |
| ------------------------- | ----------------------------- |
| `{{schema:key}}`          | `{{schema:name}}`             |
| `{{schema:@Type:key}}`    | `{{schema:@Movie:name}}`      |
| `{{schema:parent.child}}` | `{{schema:author.name}}`      |
| `{{schema:key[0].prop}}`  | `{{schema:director[0].name}}` |
| `{{schema:key[*].prop}}`  | `{{schema:actors[*].name}}`   |

Common schema types: `@Article`, `@NewsArticle`, `@BlogPosting`, `@Movie`, `@Product`, `@Recipe`, `@Person`, `@Organization`, `@SocialMediaPosting`, `@JobPosting`, `@Event`

### Selector Variables (CSS)

| Pattern                          | Example                                             |
| -------------------------------- | --------------------------------------------------- |
| `{{selector:css}}`               | `{{selector:h1}}` — text content                    |
| `{{selector:css?attr}}`          | `{{selector:img.hero?src}}` — attribute value       |
| `{{selectorHtml:css}}`           | `{{selectorHtml:article}}` — raw HTML               |
| `{{selectorHtml:css\|markdown}}` | `{{selectorHtml:body\|markdown}}` — HTML → Markdown |

### Interpreter Variables (AI Prompts)

When the interpreter is enabled (requires an LLM provider configured in settings), natural language prompts generate content:

```
{{"a summary of the page"}}
{{"3 tags describing this content"}}
{{"a summary"|blockquote}}
{{"return JSON array with fields: author, text"|map:item => item.text|join:"\n"}}
```

The `context` field controls what page content the AI receives. Use `{{selectorHtml:#main}}` to limit input to a specific element, or provide structured context like:

```
<page>\nTitle: {{title}}\nAuthor: {{author}}\n{{content}}\n</page>
```

## Filters

Chain filters with `|`. Common filters with examples:

| Filter       | Usage                         | Example                                                   |
| ------------ | ----------------------------- | --------------------------------------------------------- |
| `date`       | `date:"YYYY-MM-DD"`           | `{{date\|date:"YYYY-MM-DD"}}` → `2024-01-15`              |
| `split`      | `split:"delimiter"`           | `{{url\|split:"?"\|slice:0,1}}` — strip query params      |
| `slice`      | `slice:start,end`             | `slice:0,3` — first 3 items; `slice:-1` — last item       |
| `join`       | `join:"sep"`                  | `join:", "` — combine array with separator                |
| `map`        | `map:item => expr`            | `map:item => item.text` — extract property from each      |
| `template`   | `template:"${var}"`           | `template:"- ${name}: ${value}\n"` — format objects       |
| `wikilink`   | (no args)                     | Wraps in `[[...]]` — works on arrays too                  |
| `blockquote` | (no args)                     | Prefixes each line with `> `                              |
| `markdown`   | (no args)                     | Converts HTML to Markdown                                 |
| `safe_name`  | `safe_name` or `safe_name:os` | Filename-safe text                                        |
| `replace`    | `replace:"old":"new"`         | Also supports regex: `replace:"/pattern/g":"replacement"` |
| `link`       | `link:"text"`                 | Converts URL to `[text](url)`                             |
| `image`      | `image:"alt"`                 | Converts URL to `![alt](url)`                             |
| `list`       | `list` or `list:numbered`     | Formats array as Markdown list                            |
| `callout`    | (no args)                     | Formats as Obsidian callout                               |

**All available filters:** blockquote, calc, callout, camel, capitalize, date, date_modify, duration, first, footnote, fragment_link, html_to_json, image, join, kebab, last, length, link, list, lower, map, markdown, merge, nth, number_format, object, pascal, remove_attr, remove_html, remove_tags, replace, replace_tags, reverse, round, safe_name, slice, snake, split, strip_attr, strip_md, strip_tags, table, template, title, trim, uncamel, unescape, unique, upper, wikilink

For full filter documentation, query context7 with library ID `/obsidianmd/obsidian-clipper` (the clipper repo's `docs/Filters.md`) or `/obsidianmd/obsidian-help` (the official Obsidian help docs, which include a Web Clipper section). Either works; query both if one doesn't surface the answer.

### Filter gotchas (verified via testing)

These trip up template authors most often:

- **String concatenation with `+` doesn't work inside `map` callbacks.** The expression parser treats `+` as an unexpected character and fails the template import with `"Unexpected character '+' in template"`. Use template literals instead:

  ```
  ✗ |map:item => "- " + item               (parse error on import)
  ✓ |map:item => "- ${item}"               (template literal — correct)
  ```

- **Built-in filters cannot be chained inside `map`.** Flatten or transform inside `map`, then apply filters to the result outside:

  ```
  ✗ |map:item => item.text|trim            (filter not allowed inside map)
  ✓ |map:item => item.text|join:"\n"|trim  (filter chain outside map)
  ```

- **For arrays of objects with multi-line per-item output, use `map` to flatten to flat keys, then `template`.** Nested key access in `template` literals is not documented and unreliable; flattening first is the safe pattern:

  ```
  |map:item => ({name: item.author.name, body: item.reviewBody})
  |template:"${name}:\n> ${body}\n\n"
  ```

- **`duration` outputs `HH:mm:ss`, not compact human format.** For something like `45m` or `1h 30m`, skip the filter and chain `replace` on the raw ISO 8601 string:

  ```
  {{schema:@Recipe:prepTime|replace:"PT":""|replace:"H":"h "|replace:"M":"m"|trim}}
  → "PT1H30M" becomes "1h 30m"
  → "PT45M"   becomes "45m"
  ```

- **`|list` works on string arrays directly** — no need to map a `"- " + item` prefix yourself. Use `|list` for bullets, `|list:numbered` for numbered, `|list:task` for checkboxes.

### Common Filter Chains

```
{{url|split:"?"|slice:0,1}}                              — strip query params
{{schema:actors[*].name|wikilink|slice:0,4|join}}         — first 4 actors as wikilinks
{{highlights|map:item => item.text|join:"\n\n"|blockquote}} — highlights as blockquote
{{date|date:"YYYY-MM-DD-ddd"}}                            — formatted date with day name
{{"return JSON..."|map:item => item.title|join:"\n"}}     — AI → structured → formatted
```

## Properties

Properties become Obsidian frontmatter fields. **Order matters:** the extension writes properties to frontmatter in the order they appear in the array. If the target vault uses a YAML sort plugin (Linter, etc.), match the template's property order to the user's sort order so freshly clipped notes don't reshuffle on lint.

Each property in the array:

```json
{
  "name": "property_name",
  "value": "{{variable|filter}}",
  "type": "text"
}
```

| Type        | Description                                      |
| ----------- | ------------------------------------------------ |
| `text`      | Single string value                              |
| `multitext` | Array (comma-separated values become list items) |
| `date`      | Date value (ISO format or use `date` filter)     |
| `number`    | Numeric value                                    |
| `checkbox`  | Boolean — expects `"true"` or `"false"`          |

### JSON Escaping for Interpreter Prompts in Properties

Interpreter prompts inside JSON property `value` strings require escaped quotes. The inner `"` that delimit the prompt must be escaped as `\\\"` in the JSON:

```json
{
  "name": "description",
  "value": "{{\\\"Summarize in 1-2 sentences\\\"}}",
  "type": "text"
}
```

This is the trickiest part of template authoring. The escaping layers:

1. Outer `"` → JSON string delimiter
2. `\\\"` → produces literal `\"` in the parsed string
3. Template engine sees `{{"Summarize in 1-2 sentences"}}` and sends to interpreter

Static values and preset variables don't need this escaping — only interpreter prompts inside JSON strings.

Filters on interpreter prompts in properties also need escaping:

```json
"value": "{{\\\"author's full name\\\"|wikilink}}"
```

## Triggers

Auto-select this template when the URL or page schema matches.

| Type        | Format           | Example                                         |
| ----------- | ---------------- | ----------------------------------------------- |
| URL prefix  | Plain URL string | `"https://letterboxd.com/film/"`                |
| Regex       | Enclosed in `/`  | `"/^https?:\\/\\/docs\\.google\\.com\\/forms/"` |
| Schema type | `schema:@Type`   | `"schema:@NewsArticle"`                         |

Multiple triggers in the array act as OR — any match selects the template.

## Example: Full-Text Article Template

A vendor-neutral article clipper. Captures the full article body and a small set of metadata; mixes preset variables with optional AI-interpreter prompts. Treat the folder, tag, and prompt choices as illustrative — substitute the user's own conventions before delivering.

```json
{
  "schemaVersion": "0.1.0",
  "name": "Article",
  "behavior": "create",
  "noteNameFormat": "{{title}} - {{site}}",
  "noteContentFormat": "{{content}}",
  "path": "Clippings",
  "properties": [
    {
      "name": "title",
      "value": "{{title}}",
      "type": "text"
    },
    {
      "name": "url",
      "value": "{{url|split:\\\"?\\\"|slice:0,1}}",
      "type": "text"
    },
    {
      "name": "author",
      "value": "{{author}}",
      "type": "text"
    },
    {
      "name": "site",
      "value": "{{site}}",
      "type": "text"
    },
    {
      "name": "published",
      "value": "{{published}}",
      "type": "date"
    },
    {
      "name": "description",
      "value": "{{description}}",
      "type": "text"
    },
    {
      "name": "tags",
      "value": "{{\\\"2-3 comma-separated topical tags, lowercase, max two words each\\\"}}",
      "type": "multitext"
    },
    {
      "name": "created",
      "value": "{{date}}",
      "type": "date"
    }
  ],
  "triggers": []
}
```

Key patterns in this example:

- `noteContentFormat: "{{content}}"` captures the full article body in Markdown.
- `noteNameFormat` combines page title with site name; swap to whatever filename shape the user prefers.
- URL stripped of query/tracking params: `{{url|split:\\\"?\\\"|slice:0,1}}`.
- `description` uses the page's own description (`{{description}}`); replace with an interpreter prompt only if the user wants AI-generated summaries.
- `tags` uses an AI-interpreter prompt for topical tags. Drop or replace with a static value if the user doesn't have the interpreter enabled.
- Dates use preset variables directly.

For domain-specific templates (recipes, films, books, jobs, etc.), prefer schema-driven extraction (`{{schema:@Type:key}}`) and `schema:@Type` triggers — schema-based templates auto-match across many sites of the same domain.

## Adapting AI Prompts into Interpreter Variables

To convert an existing AI prompt into a web clipper interpreter variable:

1. Place the prompt text inside `{{"..."}}` for use in `noteContentFormat` or `noteNameFormat`
2. For use inside a JSON property `value`, escape as `{{\\\"...\\\"}}`
3. Add filters after the closing quote: `{{"prompt"|filter1|filter2}}`
4. If the prompt should return structured data, instruct it to return JSON, then chain `map` and `template` filters
5. Keep prompts focused — the AI only sees page content (or whatever `context` provides)

## Validating before delivery

Template parse errors are silent until the user tries to import — and the import error is often laconic (`"Unexpected character 'X' in template"` with a line number pointing at the JSON, not the template body). Before declaring a template done:

- Mentally walk through every `map`, `template`, and `replace` chain for the gotchas above.
- If the user has access to the extension, ask them to test-import the JSON before iterating further on the body or properties — a clean import is the fastest signal that filter syntax is valid.
- If iterating with the user on a working template, ship one change at a time so a reintroduced parse error is easy to attribute.

## Deeper Reference

For complete filter documentation, advanced patterns, or edge cases, use context7. Two complementary libraries:

- `/obsidianmd/obsidian-clipper` — the clipper repo's `docs/Filters.md`, with full per-filter API reference
- `/obsidianmd/obsidian-help` — the official Obsidian help docs, which include a Web Clipper section with examples and gotchas

Key doc pages worth retrieving when stuck:

- Templates — template configuration and structure
- Variables — all variable types and syntax
- Filters — complete filter reference with parameters
- Interpreter — AI prompt system details
