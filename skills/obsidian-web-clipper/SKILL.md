---
name: obsidian-web-clipper
description: "Use when creating, importing, or debugging Obsidian Web Clipper templates: JSON, variables, filters, selectors, interpreter prompts, and URL or schema triggers. Does not handle general scraping."
metadata:
  author: nweii
  version: "1.7.0"
---

# Obsidian Web Clipper Templates

Obsidian Web Clipper is a browser extension that saves web content to an Obsidian vault as Markdown notes. Templates define how pages are captured — what metadata to extract, how to format the note, and which sites to auto-match.

Templates are configured as JSON. Users can import/export individual templates or full settings backups. When generating templates, output valid JSON the user can import directly.

**Single-page scope.** A clip only sees the page it fired on — the DOM loaded in the active tab. The extension is not an agent; it can't crawl, follow links, or visit other URLs. Selector, schema, and interpreter variables all resolve against that one page. If a template needs data spread across multiple pages, it can't gather it in one clip — design around what's on the page being clipped.

**Caution:** full settings exports contain interpreter API keys in plaintext (`interpreter_settings.providers[].apiKey`). Never quote them; flag exports stored in version control.

## Adapt to the user's vault conventions

Templates hold opinionated conventions for folder layout, frontmatter property names, category/tag conventions, and note body structure. **Match the user's existing conventions rather than inventing.** 

Before drafting a template, understand:

- Vault-level docs (`CLAUDE.md`, `AGENTS.md`, READMEs)
- An existing templates folder, sample notes of the type being clipped, or a previously exported clipper settings file
- Any YAML property-sort configuration (Linter or similar)
- User preferences uncovered in discussion

When conventions aren't discoverable or if the user isn't sure what they want, tailor what you can and fall back to minimal vendor-neutral choices. Flag any assumptions you've made so the user can adjust before import.

If the vault has a property sort order, mirror that order in the template's `properties` array.

## Template syntax

For JSON fields, behaviors, variables, filters, logic, properties, and triggers, read [references/template-syntax.md](references/template-syntax.md). Keep its tested filter and escaping gotchas exact.

## Examples and prompt adaptation

Read [references/article-template.md](references/article-template.md) when the user needs a complete importable example or is adapting AI prompts into interpreter variables.

## Validating before delivery

Template parse errors are silent until the user tries to import — and the import error is often laconic (`"Unexpected character 'X' in template"` with a line number pointing at the JSON, not the template body). Before declaring a template done:

- Mentally walk through every `map`, `template`, and `replace` chain for the gotchas above.
- If the user has access to the extension, ask them to test-import the JSON before iterating further on the body or properties — a clean import is the fastest signal that filter syntax is valid.
- If iterating with the user on a working template, ship one change at a time so a reintroduced parse error is easy to attribute.

## Reference

For exhaustive filter signatures, the full preset variable list, schema variable edge cases, and anything not covered above, fetch the live docs. Two source-of-truth locations:

- The clipper repo's `docs/` (e.g. `obsidianmd/obsidian-clipper`, look for `docs/Filters.md`, `docs/Variables.md`, `docs/Templates.md`, `docs/Logic.md`, `docs/Interpret web pages.md`)
- The official Obsidian help docs' Web Clipper section (e.g. `obsidianmd/obsidian-help`)

Canonical human-facing docs: `https://obsidian.md/help/web-clipper` (subpages `/filters`, `/logic`, etc.). These are JS-rendered; a plain fetch returns an empty shell. Link users there, but read from GitHub.

Use whatever retrieval tool fits — context7, WebFetch, direct GitHub raw URLs, or anything else. Pick the one that's faster or more accurate in the moment. Prefer the live docs over guessing from memory.
