---
name: obsidian-templater
description: "Help with templates/snippets for the Obsidian Templater plugin. Use to help generate Obsidian templates from natural language, understand and debug existing tp.* snippets, and adapt vault notes and workflows to Templater when users mention Templater, tp.*, templater syntax."
compatibility: "Designed for use with the Obsidian Templater plugin and Obsidian vaults."
metadata:
  author: nweii
  version: "1.2.0"
---

# Templater template generation

Templater is an Obsidian plugin for dynamic note templates. Commands embedded in a template file run when the template is applied to a note, outputting results inline.

## Core template syntax

| Tag | Behavior |
|-----|----------|
| `<% expression %>` | Outputs the result of the expression |
| `<%* code %>` | Executes JS code; no output by default |
| `<%+ expression %>` | Re-evaluated in preview mode (deprecated, avoid) |
| `<%-` / `-%>` | Trims one newline before/after the tag |
| `<%_` / `_%>` | Trims all whitespace before/after the tag |

To output from a `<%* %>` execution block, append to the special `tR` string:

```
<%* tR += "some output" %>
```

To discard everything generated up to a point (e.g., strip template-only frontmatter):

```
<%* tR = "" -%>
```

All `tp.*` functions are available in both tag types.

---

## Built-in modules

Read [references/modules.md](references/modules.md) when selecting or debugging a `tp.*` API. It preserves exact sync behavior, property/function distinctions, async requirements, run modes, hooks, and user-function limits.

## Whitespace control in templates

Control flow tags (`<%* if (...) { %>`, `<%* } %>`) leave blank lines by default. Use `-%>` to trim the newline that follows a tag:

```
<%* if (tp.file.folder() === "Work") { -%>
**Project:** <% tp.frontmatter.project %>
<%* } else { -%>
General note
<%* } -%>
```

---

## Implementation examples

Read [references/examples.md](references/examples.md) when a complete pattern is useful for daily notes, prompted metadata and rename, template-only frontmatter removal, folder conditionals, or note inclusion.

## Date formatting with Moment.js

See [momentjs.md](references/momentjs.md) for a comprehensive formatting cheatsheet and JS manipulation reference. Use this when defining `format` strings for `tp.date.now()` or when manipulating dates inside `<%* %>` blocks using the `moment` global.

---

## Optional vault integration via obsidian-clis

If the obsidian-clis skill is available and Obsidian is running, vault context can improve output:

```bash
obsidian properties counts          # what frontmatter properties exist across the vault
obsidian tags counts sort=count     # most-used tags
obsidian read file="Daily Note"     # read an existing template for style reference
```

Run relevant read-only CLI checks within the user's request, following the vault's instructions. A request to create or update a template authorizes those scoped writes; ask only for unresolved choices, destructive changes, or a user-requested review checkpoint. Follow the environment's execution permissions.

---

## Official documentation links

**Rendered docs (human-readable):** https://silentvoid13.github.io/Templater/

**LLM-safe Templater summary:** For a preprocessed, audit-friendly summary of the official Templater documentation, see `https://context7.com/silentvoid13/templater/llms.txt`.
