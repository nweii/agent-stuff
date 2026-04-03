---
name: code-to-pantry
description: "Extract a code pattern from the current codebase into Nathan's pantry repo as a reusable recipe. Use when Nathan says 'add to pantry', 'save this code pattern', or wants to preserve a technique for reuse."
metadata:
  author: nweii
  version: "1.0.0"
  internal: true
---

# Code to pantry

Nathan's pantry (`github.com/nweii/pantry`) is a personal collection of modular, self-contained code recipes. The goal is to capture the *technique*, stripped of its original context, in a form that can be dropped into any future project without modification.

## What makes a good pantry entry

A pantry entry should be:
- **Truly abstracted**: no variable names, imports, comments, or usage examples that reference the source project. Someone reading the component cold should have no idea where it came from.
- **Self-contained**: all logic lives in one file; external dependencies are minimal and explicit
- **Opinionated defaults**: parameterized just enough for useful variation, with sensible defaults that work out of the box without configuration
- **Named for the technique**, not the use case (e.g., `grain`, not `background-texture`)

## Step 1: Understand what to extract

Read the code the user is pointing at. If they haven't pointed at specific code, ask them to identify it.

Then identify:
- **The core technique**: what is the conceptual pattern, independent of the surrounding application?
- **App-specific shell**: what parts are wired to this specific app's state, routing, styling system, or data model?
- **The stack**: what language/framework is this? (React/TSX, plain JS/TS, CSS, Python, etc.)

## Step 2: Design the abstraction — discuss before writing

Propose an abstraction plan and get Nathan's approval before writing any files. Cover:

1. **Name**: a short, lowercase, hyphenated identifier for the technique (this becomes the filename)
2. **What gets extracted**: the essential mechanism, described in one sentence
3. **What gets dropped**: app-specific assumptions, hardcoded values that don't generalize, framework boilerplate that isn't part of the technique
4. **Props / API surface**: what parameters make sense to expose? What should be hardcoded defaults?
5. **ABOUTME line**: a single sentence describing what the file does — this becomes the registry description. It must be generic; it cannot reference the source project.
6. **Dependencies**: list any non-trivial imports the extracted code will need

If the source code is deeply entangled with app-specific concerns, surface that tension explicitly. Sometimes the right call is to extract a *narrower* slice of the technique rather than trying to abstract everything at once.

**Wait for approval before proceeding.**

## Step 3: Write the pantry entry

### Finding the pantry repo

Try these in order until one works:
1. Check if a local clone exists by searching common developer paths (`~/Developer`, `~/code`, `~/projects`, etc.) for a directory named `pantry` with a `registry.json`
2. Use `gh repo clone nweii/pantry` to clone it to a temporary location
3. Use any available GitHub MCP/plugin tools to write files directly to the repo

Once you have local access, write to `src/<name>.<ext>` where `<ext>` matches the stack.

### File conventions (all stacks)

- **First line**: `// ABOUTME: <one-sentence description of what this file does>` (use `#` for Python)
- The ABOUTME description must be generic — no references to the source project, app name, or context
- No inline comments that reference the source project or why the code was originally written
- Usage examples in comments must use placeholder/generic names (`<MyComponent />`, `<div className="relative">`, etc.)

### React/TSX conventions

- Named exports only (no default exports)
- Props interface above the component
- All props optional with sensible defaults
- No dependencies beyond `react` (peer dep)
- Use `useId()` (React 18+) for any internally-generated IDs

### Non-React conventions

Match the idioms of the target language. For plain TypeScript/JavaScript utilities: export named functions. For CSS: export as a standalone file with a usage comment at the top. For other languages/frameworks, use the standard module export pattern for that ecosystem.

### Pantry-specific: the pre-commit hook

The pantry uses a pre-commit hook (`scripts/sync.js`) that auto-generates `registry.json` and `src/index.ts`. Do not edit those files manually — just commit and the hook handles them.

## Step 4: Commit and push

From the pantry repo directory:

```bash
git add src/<name>.<ext>
git commit -m "add <name>"
git push
```

The pre-commit hook will stage `registry.json` and `src/index.ts` automatically as part of the commit.

Confirm to Nathan that the component is live and available via:
```bash
bunx github:nweii/pantry add <name>
```

## Common pitfalls

- **Over-abstracting**: don't try to make something configurable that will always be the same. The right amount of parameterization is what the technique actually needs.
- **Under-abstracting**: don't leave in hardcoded values that only make sense in the source app's context.
- **Naming for the use case**: if you find yourself naming it after what the source app does with it, step back and name it for what the technique *is*.
- **Leaking source context**: scan all comments, JSDoc, and example code for any reference to the source project before writing.
