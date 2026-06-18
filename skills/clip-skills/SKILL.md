---
name: clip-skills
description: "Save `bunx skills` terminal output (a manifest from `skills add/use <repo> -l`) as a Repos note in the Brain vault under 03-Records/Snippets/Repos/. Use when the user pastes a skills listing and wants it captured. Triggers: '/clip-skills', 'save these skills', 'make a note for this skill repo'."
metadata:
  author: nweii
  version: "1.0.0"
  internal: true
---

# Clip skills

Turn a `bunx skills` manifest (run in the terminal, not the browser) into one note in `03-Records/Snippets/Repos/`. This is the CLI-entry twin of the Obsidian Web Clipper **"Agent skills"** template, which handles the same note when clipping a GitHub/skills.sh page in the browser. Match that template's shape so notes from either path look identical.

## Defer first

Vault layout, metadata semantics, and tool-choice rules live in the vault's `AGENTS.md` / `CLAUDE.md`. Read those if unsure about a field or which write tool to use. This skill only adds the procedure for this one note type.

## Input

The user has run one of these and pasted the output:

```shell
bunx skills add <owner/repo or URL> -l   # lists a collection's skills
bunx skills use <owner/repo> --skill <name>
```

Derive `<owner/repo>` (or the bare URL slug, e.g. `https://docs.stripe.com`) from what they ran. If the listing is missing or partial, ask them to re-run with `-l`.

## Note shape

**Path:** `03-Records/Snippets/Repos/`

**Filename:**
- Collection of skills → `<1-3 word descriptor> skills - <repo owner>` (e.g. `Payments skills - stripe`, `Design engineering skills - Emil Kowalski`)
- Single skill → `<1-4 word descriptor of what it does> skill - <repo owner>`

No quotes in the filename.

**Frontmatter:**

```yaml
aliases:        # 1-2 retrieval-friendly alt titles, sentence case
categories:     # [[Snippets]] and [[Web]] always; add [[Clippings]] ONLY if the source is a clipped web page (e.g. a docs site), not a bare GitHub repo
icon: "LiSparkles"
description:    # what this offers in 1-2 plain sentences — collection focus/breadth, or the single skill's own description lightly compressed
url:           # the source page/repo URL, query string stripped
author:        # repo owner or credited person as a [[wikilink]]; prefer full name over handle
last:          # today's date
tags:          # clippings/skills, plus 1-2 broad lowercase topical tags (hyphens, no spaces)
```

**Body** — two sections:

```markdown
## Use

<codeblocks, see below>

## Skills

<flat bullet list, see below>
```

### `## Use` codeblocks

Use ` ```shell ` fences, one command per block, each preceded by its label line.

Collection (three blocks):
- `Browse the collection:` → `bunx skills add <owner/repo> -l`
- `Try one without installing:` → `bunx skills use <owner/repo> --skill <name>`
- `Install one:` → `bunx skills add <owner/repo> --skill <name> -a claude-code zed -g -y`

Single skill (two blocks):
- `Try without installing:` → `bunx skills use <owner/repo> --skill <name>`
- `Install:` → `bunx skills add <owner/repo> --skill <name> -a claude-code zed -g -y`

Leave `<name>` as a literal placeholder for a collection; for a single skill use its actual skill name.

### `## Skills` bullets

One bullet per skill: `**skill-name**: <one rich sentence>`. Compress the manifest's full description to a single sentence that keeps the substance — don't paste the whole multi-sentence blurb, don't truncate to a fragment. Include every skill the listing names, in listing order.

When the `-l` output reports files for a skill, add one nested bullet under it:

```markdown
- **skill-name**: one-line purpose.
    - Files: `SKILL.md`, `references/a.md`, `b.md`, ...
```

Omit the Files line for skills that reported none. Keep the source's own groupings as plain subheadings only if it has them.

## Write

Use the vault's preferred write path (Obsidian CLI when available, else the environment's equivalent — see CLAUDE.md). Don't leave raw Templater `<% %>` fields. After writing, give the note title and its `obsidian://open?vault=Brain&file=...` URI.
