# Token-Efficient MCP Examples

## Sanity MCP Examples

**Note:** Sanity requires authentication first: `bunx mcporter auth "Sanity Developer"`

### Example 1: Query documents, extract only IDs and titles

**Problem:** Querying all posts returns full content, images, metadata—thousands of tokens.

**Solution:**

```bash
bunx mcporter call 'Sanity Developer.query_documents(
  resource: {projectId: "your-project", dataset: "production"},
  query: "*[_type == \"post\"]",
  limit: 20
)' | jq '[.[] | {id: ._id, title: .title, slug: .slug.current}]'
```

This returns a compact array like:

```json
[
  { "id": "abc123", "title": "My Post", "slug": "my-post" },
  { "id": "def456", "title": "Another Post", "slug": "another-post" }
]
```

### Example 2: Search with filters, extract summaries

```bash
bunx mcporter call 'Sanity Developer.query_documents(
  resource: {projectId: "your-project", dataset: "production"},
  query: "*[_type == \"project\" && !(_id in path(\"drafts.**\"))]"
)' | jq '[.[] | {
    id: ._id,
    title: .title,
    summary: .description[:100],
    status: .status
  }]'
```

### Example 3: Get specific document fields

```bash
bunx mcporter call 'Sanity Developer.query_documents(
  resource: {projectId: "your-project", dataset: "production"},
  query: "*[_id == \"project-ember\"][0]"
)' | jq '{title: .title, role: .role, tech: .technologies}'
```

## Brain Vault MCP Examples

### Example 1: Semantic search, metadata only

**Problem:** Vault search returns full file contents—can be 50k+ tokens for a few notes.

**Solution:**

```bash
bunx mcporter call 'Brain.vault(action: "search", query: "portfolio case studies", pageSize: 5)' \
  | jq '.result.results[0:3] | [.[] | {
    path: .path,
    score: .score
  }]'
```

Returns just compact results:

```json
[
  {
    "path": "03-Records/Project X.md",
    "score": 1.5
  }
]
```

### Example 2: Graph traversal, neighbor titles only

```bash
bunx mcporter call 'Brain.graph(action: "neighbors", sourcePath: "04-Entities/Ember.md", maxDepth: 1)' \
  | jq '.result.nodes[0:5] | [.[] | {title: .title, path: .path}]'
```

Returns just node titles and paths:

```json
[
  { "title": "Ember", "path": "04-Entities/Ember.md" },
  { "title": "Venture for America", "path": "04-Entities/Venture for America.md" }
]
```

### Example 3: List files in folder, extract just paths

```bash
bunx mcporter call 'Brain.vault(action: "list", directory: "03-Records/Working notes")' \
  | jq '.result[0:10]'
```

Returns a simple array of file paths:

```json
["03-Records/Working notes/File1.md", "03-Records/Working notes/File2.md"]
```
