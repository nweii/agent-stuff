# Commit

Create well-formatted commits with conventional commit messages and emojis. Follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification. This command helps automate formatting, checks, and clarity.

## Usage

- `/commit` - Standard commit with pre-commit checks
- `/commit --no-verify` - Skip pre-commit checks

## Features

- Runs pre-commit checks by default (lint, build, generate docs)
- Automatically stages files if none are staged
- Uses conventional commit format with descriptive emojis
- Suggests splitting commits for different concerns

## Commit Message Structure

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

## Commit Types

Required prefix (noun) followed by a colon and space.

| Type       | Description                                           | SemVer Correlation |
| ---------- | ----------------------------------------------------- | ------------------ |
| `feat`     | New features                                          | MINOR              |
| `fix`      | Bug fixes                                             | PATCH              |
| `docs`     | Documentation changes                                 | -                  |
| `style`    | Formatting, missing semicolons, etc. (no code change) | -                  |
| `refactor` | Code restructuring without changing functionality     | -                  |
| `perf`     | Performance improvements                              | -                  |
| `test`     | Adding or correcting tests                            | -                  |
| `build`    | Build system or external dependencies                 | -                  |
| `ci`       | CI configuration and scripts                          | -                  |
| `chore`    | Tooling, configuration, maintenance                   | -                  |
| `revert`   | Reverting a previous commit                           | -                  |

_Additional types used in this workflow:_

- `wip`: Work in progress
- `remove`: Removing code or files
- `hotfix`: Critical fixes
- `security`: Security improvements

## Required Elements

1. **Type**: One of the types listed above.
2. **Description**: Short summary immediately after the type/scope prefix. Use imperative mood ("Add feature" not "Added feature").

## Optional Elements

### Scope

- Provide additional contextual information in parentheses
- Example: `feat(parser): add ability to parse arrays`

### Body

- Optional longer explanation after the description
- MUST begin one blank line after the description

### Breaking Changes

Indicate breaking changes (MAJOR release) in one of two ways:

1. **Using `!` in the type/scope prefix:** `feat!: drop support for Node 14`
2. **Using BREAKING CHANGE footer:**

   ```
   feat: allow config to extend other configs

   BREAKING CHANGE: `extends` key now used for extending config files
   ```

### Footers

- metadata following git trailer format
- Format: `token:<space>value` or `token<space>#value`
- Example: `Closes: #123`

## Process

1. Check for staged changes (`git status`)
2. If no staged changes, review and stage appropriate files
3. Run pre-commit checks (unless --no-verify)
4. Analyze changes to determine commit type
5. Generate descriptive commit message
6. Include scope if applicable
7. Add body for complex changes explaining why
8. Execute commit

## Examples

### Simple fix

```
fix: correct spelling of CHANGELOG
```

### Feature with scope

```
feat(lang): add Polish language support
```

### Feature with breaking change

```
feat!: drop support for Node 14

BREAKING CHANGE: use JavaScript features not available in Node 14
```

## Best Practices

- Keep commits atomic and focused
- Explain why, not just what
- Reference issues/PRs when relevant
- Split unrelated changes into separate commits
