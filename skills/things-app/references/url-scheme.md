# Things 3 URL scheme — full parameter reference

Exhaustive reference for the `things:///` URL scheme. Load this when constructing anything beyond a simple `add` URL: multi-parameter adds, `update`, `add-project`, the `json` batch command, or `show`/`search` navigation. The auth token is resolved per SKILL.md → Credentials (`$THINGS_AUTH_TOKEN`).

## Conventions

- Form: `things:///command?p1=v1&p2=v2`. Opening the URL on a device with Things executes it.
- **Percent-encode all values.** Space → `%20`, newline → `%0a`. Commas inside tag/filter lists stay literal.
- Max unencoded string length: 4,000 chars for most fields; notes fields allow 10,000.
- **Authorization:** commands that modify existing data (`update`, `update-project`, `json` with an `update` op) require `auth-token=$THINGS_AUTH_TOKEN` (resolved per SKILL.md → Credentials). `add` / `add-project` do not.
- **x-callback-url:** every command supports `x-success`, `x-error`, `x-cancel` callbacks. Many return values to `x-success` (e.g. `x-things-id` = the created item's ID).
- A limit of 250 items per 10-second window applies to `add`.

## Date & time string formats

- **date string:** `today`, `tomorrow`, or `yyyy-mm-dd` (e.g. `2026-07-01`). Things also parses natural-language dates like `in 3 days` or `next tuesday` — **English only**, regardless of device language.
- **time string:** `9:30PM` or `21:30` (local time zone).
- **date time string:** date `@` time, e.g. `2026-07-01@14:00`. Adds a reminder at that time.
- **ISO8601 date time string:** e.g. `2026-07-01T14:30:00Z` (used by `creation-date` / `completion-date`).
- For `when`: a datetime adds a reminder; the time component is ignored if `anytime` or `someday` is used.

## add

Create a to-do. With neither `when` nor `list`/`list-id`, it goes to the Inbox.

| Param | Type | Notes |
|-------|------|-------|
| `title` | string | The to-do title. Ignored if `titles` is set. |
| `titles` | string, `%0a`-separated | Create multiple to-dos; other params apply to all. Beats `title`/`show-quick-entry`. |
| `notes` | string | Notes field (max 10,000). |
| `when` | string | `today`, `tomorrow`, `evening`, `anytime`, `someday`, a date string, or a date time string (reminder). |
| `deadline` | date string | Deadline. |
| `tags` | comma-separated | Tag titles. A tag that doesn't exist is skipped (not created). |
| `checklist-items` | string, `%0a`-separated | Up to 100 checklist rows. |
| `list` / `list-id` | string | Target project or area by title / ID (`list-id` wins). |
| `heading` / `heading-id` | string | Heading within the target project (`heading-id` wins). Ignored if no project or heading missing. |
| `completed` / `canceled` | boolean | `canceled` beats `completed`. |
| `show-quick-entry` | boolean | Show the quick-entry dialog populated with this data instead of adding. Ignored if `titles` set. |
| `reveal` | boolean | Navigate to the new to-do. |
| `use-clipboard` | string | `replace-title` / `replace-notes` / `replace-checklist-items`. Beats `title`/`notes`/`checklist-items`. |
| `creation-date` / `completion-date` | ISO8601 | Backdate in the DB; future dates ignored; completion needs completed/canceled. |

Returns `x-things-id` (comma-separated IDs of created to-dos) on `x-success`.

## add-project

Create a project. All params optional.

| Param | Type | Notes |
|-------|------|-------|
| `title` | string | Project title. |
| `notes` | string | Max 10,000. |
| `when` | string | Same values as `add`. |
| `deadline` | date string | |
| `tags` | comma-separated | Existing tags only. |
| `area` / `area-id` | string | Target area by title / ID (`area-id` wins). |
| `to-dos` | string, `%0a`-separated | Titles of to-dos to create inside the project. |
| `completed` / `canceled` | boolean | Cascades to all child to-dos. |
| `reveal` | boolean | Navigate into the new project. |
| `creation-date` / `completion-date` | ISO8601 | Also applied to `to-dos` if present. |

Returns `x-things-id` (the project ID).

## update (requires auth-token)

Update an existing to-do. `id` and `auth-token` required; everything else optional. **Including a param with an empty value clears it** — e.g. `&deadline=` removes the deadline.

Beyond the `add` fields, `update` adds: `prepend-notes`, `append-notes`; `add-tags` (vs `tags` which replaces); `prepend-checklist-items`, `append-checklist-items` (vs `checklist-items` which replaces); `duplicate` (boolean — update a copy, leave original). `when`, `deadline`, `completed`, `canceled`, `creation-date`/`completion-date` **cannot be set on repeating to-dos.** Returns `x-things-id`.

## update-project (requires auth-token)

Same shape as `update` for projects. `id` + `auth-token` required; empty value clears. Supports `prepend-notes`/`append-notes`, `add-tags`, `area`/`area-id` to move, `duplicate`. Setting `completed`/`canceled=true` is ignored unless all child to-dos are completed/canceled and all headings archived. No repeating-project edits to `when`/`deadline`/status. Returns `x-things-id`.

## show

Navigate to an item or built-in list. Either `id` or `query` required; `filter` optional.

- `id` — an item's ID, or a built-in list: `inbox`, `today`, `anytime`, `upcoming`, `someday`, `logbook`, `tomorrow`, `deadlines`, `repeating`, `all-projects`, `logged-projects`. Beats `query`.
- `query` — name of an area/project/tag/built-in list (first quick-find match). A task cannot be shown via `query`; use `id` or `search`.
- `filter` — comma-separated tag titles to filter the shown list.

Example: `things:///show?query=vacation&filter=errand`.

## search

`things:///search?query=vacation` opens the search screen with the query run. `query` optional (omit to just open search).

## version

`things:///version` returns `x-things-scheme-version` and `x-things-client-version` to `x-success`.

## json (batch — build whole projects)

`things:///json?data=<URL-encoded JSON array>&auth-token=<TOKEN if any update op>&reveal=<bool>`. The most powerful command: create projects with headings, to-dos, notes, and checklists in one shot, or batch updates.

`data` is a JSON array of operation objects. Each object:

- `type` — `to-do`, `project`, `heading`, or `checklist-item`. Required.
- `operation` — `create` (default) or `update`. Only `to-do` and `project` are updatable.
- `id` — required for `update`.
- `attributes` — dict of properties (all optional individually; the key itself is required).

**to-do attributes:** `title`, `notes`, `when`, `deadline`, `tags` (array), `checklist-items` (array of `checklist-item` objects), `list`/`list-id`, `heading`/`heading-id`, `completed`, `canceled`, `creation-date`, `completion-date`. Update-only: `prepend-notes`, `append-notes`, `add-tags`, `prepend-checklist-items`, `append-checklist-items`.

**project attributes:** `title`, `notes`, `when`, `deadline`, `tags` (array), `area`/`area-id`, `completed`, `canceled`, `creation-date`, `completion-date`. Create-only: `items` (array of `to-do` or `heading` objects). Update-only: `prepend-notes`, `append-notes`, `add-tags`. (`list`/`heading` on a to-do are ignored when it sits inside a project's `items`.)

**heading attributes:** `title`, `archived`. **checklist-item attributes:** `title`, `completed`, `canceled`.

Workflow: write the JSON, strip whitespace, URL-encode, append as `data=`. Returns `x-things-ids` (array of top-level item IDs; IDs of to-dos nested in projects are not returned).

Unencoded example (a project with headings, nested to-dos, and a checklist):

```json
[
  {
    "type": "project",
    "attributes": {
      "title": "Vacation in Rome",
      "notes": "Some time in August.",
      "area": "Family",
      "items": [
        { "type": "to-do", "attributes": { "title": "Add dates to calendar" } },
        { "type": "heading", "attributes": { "title": "Sights" } },
        { "type": "to-do", "attributes": { "title": "The Colosseum", "notes": "12 EUR" } },
        { "type": "heading", "attributes": { "title": "Planning" } },
        { "type": "to-do", "attributes": { "title": "Book flights", "when": "today" } },
        {
          "type": "to-do",
          "attributes": {
            "title": "Research",
            "checklist-items": [
              { "type": "checklist-item", "attributes": { "title": "Hotels", "completed": true } },
              { "type": "checklist-item", "attributes": { "title": "Transport from airport" } }
            ]
          }
        }
      ]
    }
  }
]
```

Minimal encoded form: `things:///json?data=%5B%7B%22type%22%3A%22to-do%22%2C%22attributes%22%3A%7B%22title%22%3A%22Buy%20milk%22%7D%7D%5D`

(`add-json` is deprecated; use `json`.)
