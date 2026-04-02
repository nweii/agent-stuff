---
name: obsidian-log-commits
description: "Fetches today's GitHub commits across personal and org repos, filters noise, and appends a summary as bullets into the ## Log section of today's daily note. Use when asked to log what was worked on today, check today's commits, or update the daily note with dev activity."
argument-hint: "[date YYYY-MM-DD — defaults to today]"
compatibility: Requires gh CLI or GitHub MCP. Designed for the Brain Obsidian vault.
metadata:
  author: nweii
  version: "1.0.0"
  internal: true
---

Fetches GitHub commits for the target date, filters to meaningful work, and inserts bullets into the `## Log` section of the corresponding daily note.

## 1. Determine target date

- If `$ARGUMENTS` provides a date (`YYYY-MM-DD`), use it.
- Otherwise default to today.
- Identify the corresponding daily note path: `01-Days/YYYY-MM-DD-ShortDayName.md` (e.g. `01-Days/2026-04-02-Thu.md`).

## 2. Discover repos to check

Use the GitHub CLI or API to discover repos dynamically rather than relying on a hardcoded list:

1. List personal repos: `gh repo list <username> --limit 50`
2. List orgs: `gh api /user/orgs` → for each org, list repos: `gh repo list <org> --limit 50`

Check all discovered repos for commits on the target date. Run in parallel where possible.

## 3. Filter commits

Keep only commits that represent real intentional work. Discard:

- Automated or scheduled commits — messages matching patterns like `vault backup:`, `daily config backup`, `chore: daily`, `Merge pull request` (unless the PR merge message itself is meaningful)
- Dependency bumps with no context (e.g. bare `chore(deps): bump X`)

Group remaining commits by repo.

## 4. Synthesize log bullets

For each repo with meaningful commits, write one bullet summarizing the day's work in that repo. Do not list every commit message verbatim — synthesize into a brief, readable description.

Format: `- [wikilinks if applicable] — [description]`

**Wikilinks:** If you can identify a project note in the vault that corresponds to this repo (from CLAUDE.md context, STATUS.md, or note titles), include it as a wikilink. If the repo maps to multiple project notes, include both. If you can't identify a match, omit wikilinks and just describe the work.

Example:

```
- [[Project Alpha]] / [[Work notes]] — routing architecture refactor, component extraction, form modularization
- [[My side project]] — added new skill
```

## 5. Insert into the daily note

Read the daily note. Locate the `## Log - [DayName]` section. Insert the bullets at the **end of that section**, immediately before the next `##` heading (or before EOF if no subsequent heading exists). Do not append to the end of the file.

If the `## Log` section already has content, add the new bullets after existing content in that section.

If the daily note does not exist, create it using the daily note template before inserting.

## 6. Confirm

Report which repos were checked, which had meaningful commits, and what was appended.

## Important

- **Synthesize, don't transcribe.** One bullet per repo, not one bullet per commit.
- **Wikilinks from context only.** Don't guess project note names — only link notes you can verify exist.
- **Section placement is critical.** Bullets go inside `## Log`, not at EOF.
- **Skip noise silently.** Don't mention filtered-out commits in the confirmation unless nothing meaningful was found.
