# Article template and prompt adaptation

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

For domain-specific templates (recipes, films, books, jobs, etc.), prefer schema-driven extraction (`{{schema:@Type:key}}`) and `schema:@Type` triggers — schema-based templates auto-match across many sites of the same conceptual domain.

## Adapting AI Prompts into Interpreter Variables

To convert an existing AI prompt into a web clipper interpreter variable:

1. Place the prompt text inside `{{"..."}}` for use in `noteContentFormat` or `noteNameFormat`
2. For use inside a JSON property `value`, escape as `{{\\\"...\\\"}}`
3. Add filters after the closing quote: `{{"prompt"|filter1|filter2}}`
4. If the prompt should return structured data, instruct it to return JSON, then chain `map` and `template` filters
5. Keep prompts focused — the AI only sees page content (or whatever `context` provides)
