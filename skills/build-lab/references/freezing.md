# Freezing decided labs

Read this when adding the lab lifecycle to a host, when freezing, snapshotting, visiting, or thawing a lab, or when a host's labs have started breaking as production changes.

A lab imports live production code. Once it has decided something, every later production change either breaks it or drags a commit into it that only keeps it compiling. Freezing ends that: the lab's code leaves the tree, and a small record keeps what it decided, what it looked like, and where its code still runs.

## Terms

Use these words with the user and in the host's agents file.

- **Live lab**: a lab folder with a page. It runs on today's code and can still be tuned.
- **Frozen lab**: a lab folder holding only its record and captures. Its URL shows the record.
- **Record**: the frozen lab's one data file (`frozen.json`): outcome, dates, captures, and source.
- **Capture**: a screenshot or short clip of the lab running at its decided values, stored beside the record.
- **Outcome**: the one-line decision a lab reached. A lab is frozen because it decided something, so a record always has one.
- **Source**: where the lab's code still lives. For a git host, a commit on the main branch plus the folder path.
- **Snapshot**: a frozen copy of a live lab under a new name (`footer-2026-10`). The lab itself stays live.
- **Visit**: running a frozen lab at its source commit, controls included, without changing the tree.
- **Thaw**: making a frozen lab live again on today's code. Expect drift to repair.

## State comes from files

Never add a status field. Read the state from what the folder holds:

| Files | State |
| --- | --- |
| page, no record | live |
| record, no page | frozen |
| both | a freeze or thaw that stopped partway |
| neither | not a lab (asset folder, stray) |

The loader lists live and frozen folders, and fails the build on "both" with a message naming the command that finishes the operation. It skips the shell's own folders: route groups, dynamic segments, and private folders (`(x)`, `[x]`, `_x` in Next.js).

## The record

```json
{
  "title": "Footer scrim",
  "description": "Tunes the footer's height and the scrim behind it.",
  "date": "2026-08-03",
  "outcome": "64svh, alpha 0.5 → 0.2 on an ease-in-out ending at 85%",
  "frozenOn": "2026-10-28",
  "source": { "kind": "git", "commit": "<40-char sha>", "path": "app/lab/footer" },
  "captures": [{ "file": "capture-124ee4ad.webp", "alt": "…", "variant": "dense" }],
  "ranOn": { "bun": "1.4.4", "node": "22.22.0" }
}
```

- Title, description, and date carry over from the lab's metadata, so the nav renders a frozen lab the same way as a live one.
- Validate the record once, where it is read, with errors naming the file and field. Everything downstream trusts the type.
- `ranOn` records the runtimes a visit should match. Hosts that pin their runtime version can leave it out.

### Why a commit, and which one

The source commit pins every layer at once: the lab's code, the production modules it imported, the packages, and the framework. Nothing gets copied or flattened into the tree, so freezing removes weight instead of adding it.

- Pin to the main-branch commit the working copy is based on (`git merge-base HEAD origin/<main>`). The captures show the lab at that commit, so record and captures agree.
- Require the commit to be on the main branch. A squash merge orphans branch commits, and a branch can be deleted.
- Require everything the lab runs on to equal its state at that commit, with no untracked files: the lab folder, every local module its imports reach (resolved the way the host resolves paths), and the declared version of every package it imports. The captures show the working tree, so a changed production module the lab imports would otherwise put captures of new code beside a pin of old code, and a visit could not reproduce them.
- Don't use tags. Many hosted agent environments can't push them, and the main-branch rule already keeps the commit reachable.
- Shallow clones (CI, cloud sessions) may lack an old commit. Fetch it by hash before a visit or thaw.

### Hosts without git history

If the host has no git, or rewrites main's history, use `"source": { "kind": "copy", "path": "<archive folder>" }`: copy the lab folder, the host's package manifest, and its lockfile into an archive folder outside every build, typecheck, and lint glob (for example a top-level `lab-archive/<slug>/`). This keeps the lab's own code but not the production modules it imported, so a visit may need repair, and the archive adds weight the git path avoids. Tell the user that tradeoff before choosing it. The record and captures carry the decision either way.

## Operations

Build these as one script in the host (`bun run lab <command>`): pure planners that take gathered facts and return a plan or a refusal, and a thin layer that reads git and the filesystem and applies the plan. The script never commits; the user reviews its diff. Every operation is safe to rerun: a finished one plans nothing, and a half-finished one resumes from the record it already wrote.

### Freeze

1. Refuse unless the lab is live, has an outcome, runs on code that matches its pin commit, no code outside it imports from it, and every capture exists in a format the record accepts. Each refusal says what to do.
2. Copy captures into the folder under content-addressed names (`capture-<hash8>.<ext>`), so their URLs can be cached forever.
3. Write the record.
4. Remove packages only this lab imported. Find imports with a parser, never a text search: a package name appears in comments, selectors, and test fixtures that import nothing. TypeScript's `ts.preProcessFile(source, true, true)` reads static, type-only, dynamic, `require`, and re-export imports and ignores strings and comments; read CSS `@import` separately. Keep any package a package-manifest script runs as a command.
5. Delete everything else in the folder. This comes last because a rerun finds the sole-use packages by reading the lab's code.

Take captures with your own browser tool before freezing: the lab at its decided values, controls visible, the shell's sidebar cropped out. Prefer WebP. Record the `?v=` value when the lab has variants.

### Snapshot

Freeze a copy into a new folder (`<slug>-<yyyy-mm>`) with the source pointing at the live lab's folder. Nothing in the live lab changes. Take one when a lab reaches a decision the user may tune past, so the earlier state stays visible.

### Visit

Check out the source commit into a separate worktree outside every build glob (inside the git directory works: `.git/lab-visits/<slug>`), install with the lockfile frozen, and run the dev server on another port at the lab's original path. Remove the worktree when done. Warn when the installed runtime differs from `ranOn`.

### Thaw

Restore the lab's files from the source commit into its folder (from the source path, which differs for a snapshot), re-add packages it imported that are no longer declared, using the specs and dependency sections the commit declared, then delete the record and captures. Production has moved since the commit, so typecheck and open the lab, and repair what broke.

### Reading old values without a visit or thaw

To compare a frozen lab's values with today's parameters, read its files at the source commit (`git show <commit>:<path>/lab.tsx`) and map the old values onto today's production names. Thaw only when the user wants to keep tuning.

## Suggestions

People rarely notice the right moment to freeze or snapshot. A `status` command reads git history and suggests one, with a reason:

- **Snapshot** when a lab's outcome changed in the last 14 days and no snapshot of it has been taken since.
- **Freeze** when a lab has an outcome and every commit to it since then also changed code outside the lab directory. Production is dragging it along.
- **Freeze** when a lab has an outcome and nothing has touched it for 90 days.

Labs without an outcome get no suggestion; they haven't decided anything. Agents run `status` after finishing lab work and mention suggestions to the user. They freeze or snapshot only when asked. In a shallow clone, say that the history is partial.

## Doing it by hand

Without the script, follow the same steps: confirm the outcome and pin, take captures, write the record, remove sole-use packages, delete the code, and commit. To thaw, `git checkout <commit> -- <path>`, re-add packages, delete the record and captures, then repair.
