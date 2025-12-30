# Command Template

Commands are user-invoked shortcuts for executing specific prompts quickly (e.g., `/optimize`, `/test`).

## Structure

For Cursor, commands are typically defined in `.cursor/commands/` directory.

```yaml
---
name: command-name
description: What this command does when invoked
# trigger: /commandname  # Optional: slash command shortcut
---

Your prompt template goes here.

Use {SELECTION} to reference selected code.
Use {FILE} to reference current file.
Use {CONTEXT} for additional context.

## Example prompt:

Analyze the selected code for:
- Performance bottlenecks
- Security issues  
- Best practice violations

Provide specific recommendations with code examples.
```

## Command vs Skill

| Feature | Command | Skill |
|---------|---------|-------|
| **Invocation** | User types `/command` | Claude decides automatically |
| **Use Case** | Quick shortcuts | Autonomous expertise |
| **Flexibility** | Fixed prompt | Adaptive application |
| **Visibility** | Explicit | Invisible until needed |

## Best Practices

1. **Make commands specific**: Each command should do one thing well
2. **Use clear triggers**: Choose memorable slash command names
3. **Include context variables**: Use {SELECTION}, {FILE} where relevant
4. **Provide examples**: Show expected input/output
5. **Keep prompts concise**: Commands should be quick to execute

## Template Variables

Common variables you can use in command prompts:

- `{SELECTION}` - Currently selected text
- `{FILE}` - Current file path
- `{FILENAME}` - Current file name
- `{LANGUAGE}` - Current file's programming language
- `{CONTEXT}` - Additional context from opened files
- `{CLIPBOARD}` - Clipboard contents

## Example Commands

### Code Review
```
Perform a thorough code review of {SELECTION}:
- Check for bugs and edge cases
- Suggest performance improvements
- Identify security concerns
- Recommend better patterns
```

### Generate Tests
```
Generate comprehensive unit tests for {SELECTION} in {LANGUAGE}:
- Cover happy path and edge cases
- Use appropriate test framework
- Include setup/teardown if needed
- Add descriptive test names
```

### Explain Code
```
Explain the following code in detail:

{SELECTION}

Include:
1. High-level purpose
2. Step-by-step walkthrough
3. Key algorithms or patterns used
4. Potential issues or improvements
```
