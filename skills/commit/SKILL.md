---
name: commit
description: "Create well-formatted commits with conventional commit messages. Use when user asks to commit, wants to commit changes, or needs help with commit messages."
metadata:
  author: nweii
  version: "1.1.0"
---

# Commit

Create well-formatted git commits following [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/).

## Format

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Formatting, missing semi-colons, etc. (no code change)
- `refactor`: Code change that neither fixes a bug nor adds a feature
- `perf`: Performance improvement
- `test`: Adding missing tests
- `chore`: Maintenance tasks (build process, dependencies, etc.)

### Guidelines

- **Subject line**: Imperative mood ("add", not "added"); aim for ≤50 characters.
- **Body**: Wrap at 72; explain *what* and *why*, not *how*.
- **Scope**: Optional, indicates section of codebase (e.g., `feat(auth):`).
- **Breaking changes**: Add `!` after type/scope (e.g., `feat!:`) and explain in footer.

## Process

1. Review staged changes (`git diff --staged`) and outstanding `git status`.
2. Stage files explicitly when there's any chance `git add -A` would sweep in secrets or unrelated work.
3. Pick the type and scope that fit.
4. Write a concise subject; add a body when the change isn't self-explanatory.

## Examples

```
feat(auth): add OAuth2 login support

Implements Google and GitHub OAuth providers.
Closes #123
```

```
fix: resolve race condition in data fetcher

The previous implementation could return stale data
when multiple requests were in flight.
```

```
chore: update dependencies to latest versions
```
