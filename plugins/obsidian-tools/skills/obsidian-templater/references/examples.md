# Templater implementation examples

### Daily note

```
---
date: <% tp.date.now() %>
---

<< [[<% tp.date.yesterday() %>]] | [[<% tp.date.tomorrow() %>]] >>

# <% tp.file.title %>

<%* tR += await tp.web.daily_quote() %>

<% tp.file.cursor() %>
```

### Prompted metadata + file rename

```
<%*
const title = await tp.system.prompt("Note title", tp.file.title)
const status = await tp.system.suggester(["Draft", "In progress", "Done"], ["draft", "in-progress", "done"])
await tp.file.rename(title)
-%>
---
title: <% title %>
status: <% status %>
created: <% tp.file.creation_date() %>
---

# <% title %>

<% tp.file.cursor() %>
```

### Strip template-file frontmatter from output

```
---
type: template
description: This is a person template.
---

<%* tR = "" -%>
---
type: person
created: <% tp.file.creation_date() %>
---

# <% tp.file.cursor() %>
```

### Conditional content by folder

```
<%* if (tp.file.folder() === "Work") { -%>
**Project:** <% tp.frontmatter.project ?? "unassigned" %>
<%* } else { -%>
**Topic:**
<%* } -%>
```

For subfolder matching: `tp.file.folder(true).startsWith("Work/")` — `folder(true)` returns the full vault-relative path.

### Include another note

```
<% await tp.file.include("[[Shared Header]]") %>
```

---
