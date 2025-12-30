---
description: "Brief description of what this rule provides or enforces"
alwaysApply: false  # true = apply to every session; false = agent decides based on description
# globs: ["**/*.ts", "**/*.tsx"]  # Optional: apply to specific file patterns
---

# Rule Name

Rules provide persistent instructions that shape agent behavior across sessions.

## Purpose

Describe what this rule accomplishes and why it's useful.

## Instructions

### Code Style

- Specific style guideline 1
- Specific style guideline 2
- Example: "Always use `const` for immutable variables"

### Architecture Patterns

- Pattern or convention to follow
- Example: "Follow the repository pattern for data access"
- Example: "Keep business logic in service layers"

### Best Practices

- Important practice to maintain
- Example: "Write descriptive commit messages in present tense"
- Example: "Include error handling in all async functions"

## Examples

### Good Example ✅

```typescript
// Follows the rule
const result = await fetchData();
if (!result) {
  throw new Error('Failed to fetch data');
}
```

### Bad Example ❌

```typescript
// Violates the rule
let result = await fetchData();  // Should use const
// Missing error handling
```

## When This Rule Applies

Explain the scope or context where this rule should be followed:
- File types (e.g., "All TypeScript files")
- Directories (e.g., "Files in /src/services/")
- Scenarios (e.g., "When implementing API endpoints")

## Rule Types

### Always Apply
Set `alwaysApply: true` for rules that should be included in every chat session.
Good for: Global preferences, fundamental code style

### Apply Intelligently (Agent-Decided)
Set `alwaysApply: false` and write a clear `description`.
Good for: Domain-specific knowledge, project conventions

### Apply to Specific Files
Use `globs` to target file patterns.
Good for: Language-specific rules, directory conventions

```yaml
globs: ["**/*.test.ts", "**/*.spec.ts"]
```

### Apply Manually
Rules can be @-mentioned in chat: `@my-rule`
Good for: Optional guidelines, experimental rules

## References

Link to related documentation or resources:
- [Internal style guide](https://example.com/style)
- [Architecture docs](https://example.com/architecture)

## Notes

Additional context, caveats, or considerations for using this rule.
