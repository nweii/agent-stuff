---
name: nweii-skills
description: "Reference for Nathan's agent skills setup: the nweii/agent-stuff and nweii/agent-stuff-private repos, install/symlink mechanics, frontmatter and writing conventions, skill content craft, privacy tiers, and migrating local skills into a repo. Use when creating, editing, migrating, or installing skills in Nathan's environment."
metadata:
  author: nweii
  version: "1.11.0"
  internal: true
---

# nweii-skills

Reference context for Nathan's skills ecosystem. Read this before creating, editing, or migrating any skill in his environment.

## The repos

Skills live in two paired repos:

- **[nweii/agent-stuff](https://github.com/nweii/agent-stuff)** — public + internal-but-public skills. Cloned at `~/Developer/LLMs/agent-stuff/`.
- **`nweii/agent-stuff-private`** — truly private skills (career materials, personal workflows, confidential content). Cloned at `~/Developer/LLMs/agent-stuff-private/`. Pushed to a private GitHub remote; never made public.

Both repos use the same layout:

```
<repo>/
├── skills/          # Skill folders
├── commands/        # Slash commands (agent-stuff only)
├── templates/       # SKILL_TEMPLATE.md, RULE_TEMPLATE.md (agent-stuff only)
└── reference/       # Platform docs (agent-stuff only)
```

`agent-stuff` has a git hook that auto-updates `README.md` with a skills catalog on every commit. `agent-stuff-private` does not (kept simple).

## Source of truth: the repos, not the install dir

**All edits to a skill happen in the repo working copy** (`~/Developer/LLMs/agent-stuff/skills/<name>/` or `~/Developer/LLMs/agent-stuff-private/skills/<name>/`). The installed skill under `~/.agents/skills/<name>/` is a **downstream copy** placed there by `bunx skills add` and overwritten on the next install — it isn't version-controlled and never reaches GitHub, so edits there are silently ephemeral. If you find yourself reaching for `~/.agents/skills/<name>/SKILL.md`, stop: edit the matching repo folder instead, then reinstall to sync the change down.

## Installing and updating skills

Always install via `bunx skills add`, from the GitHub slug — same form for every repo, public or private:

- **Public (`agent-stuff`)** → `nweii/agent-stuff`. Updates via `bunx skills update`.
- **Private (`agent-stuff-private`)** → `nweii/agent-stuff-private`. Cloning a private repo relies on an authenticated `gh` (it falls back to `gh repo clone`, then SSH); make sure `gh auth status` is logged in.
- **Third-party** → their GitHub slug.

Don't install private skills from the local clone path or an SSH URL — the slug works for private repos through `gh` and keeps the recorded source portable across machines.

To try a skill without installing it, `bunx skills use <owner/repo> --skill <name>` generates a usage prompt.

### Architecture: how the install is laid out

`bunx skills add` keeps **one real copy** of each skill in the canonical dir `~/.agents/skills/<name>/`, then **symlinks each agent's skills dir to it**. So Claude Code sees `~/.claude/skills/<name>` as a symlink pointing to `../../.agents/skills/<name>`.

- The real files live once, in `~/.agents/skills/`. The agent dirs hold symlinks, not duplicate copies.
- Trashing the symlink at `~/.claude/skills/<name>` leaves the canonical copy intact; trashing `~/.agents/skills/<name>` removes the real skill.
- A `~/.claude/skills/<name>` that is a real directory instead of a symlink is **copy-mode drift** — see the install command below for why it happens and how to avoid it.

**On Nathan's MacBook, `~/.claude/skills` is itself a directory-level symlink to `~/.agents/skills`** (`readlink ~/.claude/skills` to confirm on any machine). Under this layout per-skill symlinks never appear: every `~/.claude/skills/<name>` is the canonical copy seen through the parent link, so it lists as a real directory. That is NOT copy-mode drift — do not "repair" it. Trashing `~/.claude/skills/<name>` here deletes the real skill, and creating a per-skill symlink inside it produces a self-referencing loop. Check the parent with `readlink` before diagnosing anything about per-skill symlinks.

### Install commands

The default install mode is symlink, but **bunx only uses it when two or more agent directories are targeted.** Installing to a single agent (`-a claude-code` alone) silently falls back to copy mode — it writes a real folder into `~/.claude/skills/` and skips the canonical `~/.agents/skills/` entirely. To get the symlink layout, add a second agent whose skills dir *is* the canonical `~/.agents/skills`, so the real copy lands there and Claude Code gets a symlink. `zed` works for this and creates no stray agent dir (its global skills dir is `~/.agents/skills`); `cline`, `dexto`, `loaf`, `warp`, and `kimi-code-cli` work the same way.

```bash
# Public agent-stuff
bunx skills add nweii/agent-stuff --skill <name> -a claude-code zed -g -y

# Private agent-stuff-private (clones via authenticated gh)
bunx skills add nweii/agent-stuff-private --skill <name> -a claude-code zed -g -y

# Third-party
bunx skills add vercel-labs/agent-skills --skill <name> -a claude-code zed -g -y
```

Scoping with `-a` matters either way: without it, `bunx skills add` spreads the skill into every agent directory it knows about, for tools that aren't used.

### Updating an installed skill

`bunx skills update <name> -g` works for public, non-`internal` skills (and third-party skills). It does **not** work for:

- **Private-repo skills** — `update` checks the GitHub tree over an unauthenticated API call and can't see a private repo, so it reports "Failed to fetch tree."
- **`internal: true` skills** (even in the public repo) — `update`'s internal handoff filters them out and reports "Failed to update."

For both, refresh by re-running `bunx skills add` (which installs internal skills fine, since naming a skill with `--skill` opts it in):

```bash
bunx skills add nweii/agent-stuff-private --skill <name> -a claude-code zed -g -y
```

### Repairing a copied (non-symlink) install

First check `readlink ~/.claude/skills` — if the skills dir is itself a symlink to `~/.agents/skills` (as on Nathan's MacBook), real directories inside it are the canonical copies and there is nothing to repair. Otherwise: if `~/.claude/skills/<name>` is a real directory rather than a symlink into `~/.agents/skills/`, it was installed in copy mode. Reinstall it with the two-agent command above — that rebuilds the canonical copy and the symlink, and refreshes the skill from upstream in the same step (so a drifted local copy is reconciled to source, not preserved).

`--skill` takes the **frontmatter `name:`**, not the repo folder name. When the two differ (e.g. repo folder `lennys-podcast-transcripts-slim` with frontmatter `name: lennys-podcast-transcripts`), pass the frontmatter name. Bunx will silently install nothing if you pass the folder name in this case.

### Cleaning up multi-agent spread

If a previous install spread to multiple agents, pass agents space-separated to a single `-a` flag (the comma-separated form does not parse):

```bash
bunx skills remove --skill <name> -a augment codebuddy cursor -g -y
```

## Pushing changes

Commit freely in either repo working copy — that's local-only. Pushing is where the gate is:

- **`agent-stuff` (public)** — **always get explicit user confirmation before `git push`.** Public commits are world-readable on GitHub and feed the auto-generated catalog. Don't push opportunistically.
- **`agent-stuff-private`** — push as needed, no extra gate.

## Writing conventions

Skill content gets read by a human as often as by an agent, so write it to be read. Sort the substance first — the actual instructions, gotchas, and structure — then make a separate succinctness pass over the finished draft: cut filler, merge split sentences, tighten wording. Aim for succinctness, not raw brevity. The point is to drop words that don't earn their place, not to compress the prose into something terse or cryptic. If a trim makes a sentence harder to read or forces a re-parse, it went too far — keep the words that carry the meaning.

**Keep procedure skills operational.** When a skill exists to *do* something — write a note, scaffold a file, drive a tool — write the body as the steps to follow, in order, with the decision-points and gotchas inline. Lead with what to do, not with background or rationale the agent doesn't need in order to act. Defer anything it already knows or can read elsewhere (the vault's `AGENTS.md`, a sibling skill) rather than restating it. Reference skills that exist to *explain* — a system, a set of conventions — can carry more exposition; a procedure skill padded with it is just harder to execute against.

## Skill content craft

Cross-cutting habits for what goes in the body, condensed from the agentskills.io guides (linked below for the fuller treatment):

- **Add what the agent lacks, omit what it knows.** Spend tokens on project conventions, domain procedures, non-obvious edge cases, and which exact tool/API to use — not on explaining what a PDF or an HTTP request is. The test per line: would the agent get this wrong without it? If no, cut it.
- **Provide defaults, not menus.** When several tools or approaches work, pick one and mention alternatives briefly as an escape hatch, rather than listing equals the agent has to choose between.
- **Match specificity to fragility.** Be prescriptive — exact commands, "don't add flags" — where a step is fragile or order-dependent; give freedom (and say *why*) where variation is fine and judgment helps.
- **Progressive disclosure.** Keep `SKILL.md` to the core path (the spec targets <500 lines / ~5k tokens); move deep reference into `references/` and tell the agent *when* to load each file ("read `references/x.md` if the API returns non-200"), not a generic "see references/."
- **Gotchas sections** earn their keep — environment-specific facts that defy reasonable assumptions (soft-deletes, an ID that's named three things across services). When a correction has to be made during real use, fold it back here.

### Bundled scripts

If a skill ships scripts (`scripts/`), design them for a non-interactive agent:

- **No interactive prompts** — take input via flags, env, or stdin; a TTY prompt hangs the run. Fail with a usage hint instead.
- **`--help` is the interface** the agent reads, so keep it short and current. Write errors that say what was expected and what to try.
- **Structured output** — data to stdout (JSON/CSV), diagnostics to stderr, so output stays parseable and composable.
- **Safe under retry** — idempotent where possible, `--dry-run` for destructive ops, meaningful exit codes, bounded output (paginate or require `--output` for large results).
- **Self-contained deps** — declare inline (PEP 723 + `uv run`, or Bun's runtime auto-install) so there's no separate install step.

Reach for a script only when a one-off command grows too complex to get right inline, or when traces show the agent reinventing the same logic each run.

### References

Fuller treatment, fetch on demand:

- [Best practices](https://agentskills.io/skill-creation/best-practices.md) — scoping, control calibration, the gotchas/template/checklist/validation patterns.
- [Optimizing descriptions](https://agentskills.io/skill-creation/optimizing-descriptions.md) — trigger evals, train/validation split, the optimization loop.
- [Using scripts](https://agentskills.io/skill-creation/using-scripts.md) — one-off commands, self-contained scripts, agentic script design.

## Frontmatter conventions

```yaml
---
name: skill-name           # lowercase-with-hyphens, max 64 chars
description: "..."         # Always quoted. Max ~1024 chars. Describe what it does AND when to use it.
metadata:
  author: nweii
  version: "1.0.0"         # semver, always quoted; bump on meaningful change
  internal: true           # only include when true
  source: owner/repo       # optional: single canonical upstream pointer
  credit: "..."            # optional: prose attribution
---
```

**Description quoting is required** — always wrap in double quotes. YAML chokes on unquoted descriptions that contain `: ` (colon-space), em dashes, or other special characters. This is a silent failure: the skill file appears valid but bunx can't parse the name and won't find the skill.

**Write the description for routing, not summary.** Its job is to make the model pick this skill at the right moment and skip it otherwise, so spend the words on concrete triggers — what the user says or does, the file types or contexts involved — over a thorough account of what the skill contains. Detail belongs in the body; the description is the matcher. Treat ~200–300 characters as a ceiling rather than a target: shorter is always welcome and often sharper, but don't drop a trigger or a distinction that routing needs just to hit a lower count. (1024 is the hard limit.)

Phrase it imperatively and from the user's side — "Use when…" over "This skill does…", describing what the user is trying to do rather than the skill's mechanics. Be a little pushy: name the contexts where it applies, including ones where the user won't say the domain outright ("even if they don't mention 'CSV'"). One nuance — agents skip skills for tasks they can already handle in a step or two, so a description earns its trigger on specialized or multi-step work, not trivial one-liners. For systematic tuning (eval queries, train/validation split, trigger-rate loop) see the optimizing-descriptions reference under [Skill content craft](#skill-content-craft), or let `skill-creator` automate it.

`metadata.internal: true` marks personal workflows that are pushed to GitHub but not intended for general use. Use it on any skill that's specifically tuned to Nathan's setup, regardless of which repo it lives in.

**Versioning.** Keep a skill (or agent) at `0.y.z` while it's still in development or dogfooding — not yet in real use. That's what the pre-1.0 range is for in semver: anything can still change. Promote to `1.0.0` once it's actually adopted and stable; after that, bump the minor for new capability and the patch for fixes. This applies to agent files too, which borrow the same `metadata` block for tracking even though their runtime ignores it.

**Attribution** uses two fields, by provenance shape:

- `metadata.source` — a single pointer (GitHub slug or URL) when the skill directly derives from or documents one specific upstream artifact.
- `metadata.credit` — prose, for provenance that doesn't reduce to a pointer: adapted from multiple skills, inspired by someone's approach, or authored by a person rather than a repo ("Prompt by Suzanne at Anthropic, shared in a tweet thread by Thariq").

They can coexist (source for the artifact, credit for the story). When someone else wrote the content wholesale and it's only being packaged here, put them in `author` and elaborate in `credit`.

## Privacy tiers

Three tiers, two repos:

| Tier | Repo | Visibility | Use for |
|---|---|---|---|
| Public | `agent-stuff` | Public on GitHub, no `internal` flag | Skills genuinely useful to others |
| Internal-but-public | `agent-stuff` | Public on GitHub, `metadata.internal: true` | Personal workflows that aren't sensitive but aren't general-purpose either |
| Private | `agent-stuff-private` | Private GitHub remote, `metadata.internal: true` | Career materials, project-specific assistants, anything that shouldn't leave Nathan's environment |

The previous `skills/private/` (gitignored subfolder of agent-stuff) tier is retired — that pattern was fragile (one stray `git add -A` and content leaks) and made cross-machine sync impossible. All formerly-private skills now live in `agent-stuff-private`.

## Migrating a locally-developed skill into a repo

When a skill has been developed directly in `~/.agents/skills/` and needs to move into a repo:

1. Decide the tier (public, internal-but-public, or private) and pick the matching repo
2. Copy the skill folder to `<repo>/skills/<name>/`
3. **Fix the description** — wrap it in double quotes if it isn't already
4. Commit and push (private repo: ensure the remote is private)
5. Trash the local install: `trash ~/.agents/skills/<name>`
6. Reinstall via bunx from the appropriate slug:
   ```bash
   # Public
   bunx skills add nweii/agent-stuff --skill <name> -a claude-code zed -g -y
   # Private
   bunx skills add nweii/agent-stuff-private --skill <name> -a claude-code zed -g -y
   ```

   Future edits happen in the repo, then re-run `bunx skills add` (private or `internal`) or `bunx skills update` (public, non-`internal`) to sync the install.

**The install dir is downstream, not source** — if you suspect the install drifted before migrating, diff it against the repo and reconcile to the repo before reinstalling.
