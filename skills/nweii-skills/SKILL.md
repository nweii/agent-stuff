---
name: nweii-skills
description: "Reference for Nathan's agent skills setup: the nweii/agent-stuff and nweii/agent-stuff-private repos, install/symlink mechanics, frontmatter and writing conventions, skill content craft, privacy tiers, and migrating local skills into a repo. Use when creating, editing, migrating, or installing skills in Nathan's environment."
metadata:
  author: nweii
  version: "1.13.0"
  internal: true
---

# nweii-skills

Reference context for Nathan's skills ecosystem. Read this before creating, editing, or migrating any skill in his environment.

## The repos

Skills live in two paired repos:

- **[nweii/agent-stuff](https://github.com/nweii/agent-stuff)** — public + internal-but-public skills. Cloned at `~/Developer/LLMs/agent-stuff/`.
- **`nweii/agent-stuff-private`** — truly private skills (sensitive materials, personal workflows, confidential content). Pushed to a private GitHub remote.

Both repos share a core layout, with some folders specific to one:

```
<repo>/
├── skills/          # Skill folders
├── agents/          # Subagent definitions (public: inspiration set; private: backups)
├── zips/            # Auto-built per-skill zips for drag-into-Claude.ai (generated)
├── scripts/         # update-catalog.py + build-zips.py (run by the pre-commit hook)
└── templates/       # SKILL_TEMPLATE.md, RULE_TEMPLATE.md (agent-stuff only)
```

Both repos have a `.githooks/pre-commit` that, when a skill changes, regenerates the `README.md` catalog (`update-catalog.py`) and rebuilds the `zips/` mirror (`build-zips.py`) into the same commit.

### The `zips/` mirror

Each skill is also packaged as a `<name>.zip` (one top-level folder named after the skill, containing its files) for non-CLI user convenience. Key properties:

- **Built locally by the pre-commit hook**, not a GitHub Action — the zip lands in the same commit as the skill edit, and reverts with it.
- **Deterministic** — `build-zips.py` uses fixed timestamps, sorted entries, and **git-tracked files only** (so `.DS_Store` and other junk never get in). An unchanged skill produces a byte-identical zip, so editing one skill diffs exactly one zip; no churn.
- **Self-healing** — the hook wipes and fully rebuilds `zips/` each run, so a deleted, renamed, or newly-internal skill drops its stale zip automatically.
- **Per-repo scope** — `build-zips.py` carries a `ZIP_INCLUDE_INTERNAL` constant: `False` in `agent-stuff` (general-purpose skills only — don't encourage dropping internal ones in unmodified), `True` in `agent-stuff-private` (every skill is personal, so zip all).

The `agent-stuff` README catalog also splits skills into a general list and an `### Internal` section (the script's existing `is_internal` flag). The private README stays a flat list.

### The `agents/` folders

Subagent definitions (`*.md`), **not** installed by `bunx skills` — copy them into `~/.agents/agents/` by hand. In `agent-stuff` this is a small curated inspiration set (`vault-reader`, `vault-writer`) with a framing README; in `agent-stuff-private` it's version-controlled backups of Nathan's personal subagents.

## Use the repos as a source of truth over local installs

**All edits to a skill happen in the repo working copy** (`~/Developer/LLMs/agent-stuff/skills/<name>/` or `~/Developer/LLMs/agent-stuff-private/skills/<name>/`). The installed skill under `~/.agents/skills/<name>/` is a **downstream copy** placed there by `bunx skills add` and overwritten on the next install — it isn't version-controlled and never reaches GitHub. If you find yourself reaching for `~/.agents/skills/<name>/SKILL.md`, stop: edit the matching repo folder instead, then reinstall to sync the change down.

## Installing and updating skills

Always install via `bunx skills add`, from the GitHub slug for every repo, public or private:

- **Public (`agent-stuff`)** → `nweii/agent-stuff`. Updates via `bunx skills update`.
- **Private (`agent-stuff-private`)** → `nweii/agent-stuff-private`. Cloning a private repo relies on an authenticated `gh` (it falls back to `gh repo clone`, then SSH); make sure `gh auth status` is logged in.
- **Third-party** → their GitHub slug.

Don't install private skills from the local clone path or an SSH URL — the slug works for private repos through `gh` and keeps the recorded source portable across machines.

To try a skill without installing it, `bunx skills use <owner/repo> -s <name>` generates a usage prompt.

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

`--skill` takes the **frontmatter `name:`**, not the repo folder name. When the two differ, pass the frontmatter name. Bunx will silently install nothing if you pass the folder name in this case.

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

Skill content gets read by a human as often as by an agent, so write it to be read. Sort the substance first (the instructions, gotchas, and structure), then make a separate succinctness pass over the finished draft: cut filler, merge split sentences, tighten wording. Drop words that don't earn their place, but don't compress the prose into something illegibly terse. If a trim makes a sentence harder to read, it went too far. Compactness should serve readability.

**Keep procedure skills operational.** When a skill exists to *do* something (write a note, scaffold a file, drive a tool) write the body as the steps to follow, in order, with the decision-points and gotchas inline. Lead with what to do, not with background or rationale the agent doesn't need. Defer anything it already knows or can read elsewhere (the vault's `AGENTS.md`, a sibling skill) rather than restating it. However, reference skills that exist to *explain* (a system, a set of conventions) may carry more exposition.

## Skill content craft

When available, lean on the /writing-great-skills skill (user-invoked — type its name) for any new skill or non-trivial edit.

Essentials:

- **Skills give agents more predictable behavior** A skill exists to pull determinism out of a stochastic agent. The aim isn't to produce identical output, but to run the same process each time — or reliably understand important context.
- **Lead with a completion criterion the agent can check.** End a step (or a rule) on a condition that distinguishes done from not-done, and make it exhaustive where it matters ("every modified file accounted for", not "produce a change list"). Vague criteria invite the agent to stop early.
- **Reach for leading words** — a compact concept the model already holds from pretraining (*tight loop*, *tracer bullet*, *red*, *fog of war*) anchors a whole region of behaviour in one token by recruiting priors the agent already has. Prefer one strong word to a restated triad ("fast, deterministic, low-overhead" → *tight*). It sharpens both execution (same behaviour each time the word appears) and invocation (shared language across prompts/docs makes the agent fire the skill more reliably).
- **Diagnose with the failure-mode names.** When a skill misbehaves, name what's wrong: *premature completion* (ending a step before it's done — fix the completion criterion first, split the sequence only if that fails), *duplication* (same meaning in two places — costs tokens and inflates its apparent importance), *sediment* (stale layers that pile up because adding feels safe), *sprawl* (too long even when every line is live — cure with progressive disclosure and splitting), *no-op* (a line the agent already obeys by default — pays load to say nothing).
- **Single source of truth.** Keep each meaning in one authoritative place so changing behaviour is a one-place edit. On the pruning pass, run the no-op test sentence by sentence and delete whole sentences that fail rather than trimming words.

Cross-cutting habits for what goes in the body:

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

**Write the description for routing, not summary.** Its job is to make the model pick this skill at the right moment and skip it otherwise, so spend the words on concrete triggers — what the user says or does, the file types or contexts involved — over a thorough account of what the skill contains. Scrutinize whether any detail earns its place. Detailed elaborations belong in the skill body. Treat ~200–300 characters as a ceiling rather than a target: shorter is always welcome and often sharper, but don't drop a trigger or a distinction that routing needs just to hit a lower count. (1024 is the hard limit.)

Phrase skill descriptions imperatively and from the user's side — "Use when…" over "This skill does…", describing user intent rather than the skill's mechanics. Be a little pushy: name the contexts where it applies, including ones where the user won't say the domain outright ("even if they don't mention 'CSV'"). Agents skip skills for tasks they can already handle in a step or two, so a description earns its trigger on specialized or multi-step work. For systematic tuning (eval queries, train/validation split, trigger-rate loop) see the optimizing-descriptions reference under [Skill content craft](#skill-content-craft).

`metadata.internal: true` marks personal workflows that are pushed to GitHub but not intended for general use. Use it on any skill that's specifically tuned to Nathan's setup, regardless of which repo it lives in.

**Versioning.** Keep a skill (or agent) at `0.y.z` while it's still in development or dogfooding — not yet in real use. That's what the pre-1.0 range is for in semver: anything can still change. Promote to `1.0.0` once it's mature and stable; after that, bump the minor for new capability and the patch for fixes. This applies to agent files too, which borrow the same `metadata` block for tracking even though their runtime ignores it.

**Attribution** uses two fields, by provenance shape:

- `metadata.source` — a single pointer (GitHub slug or URL) when the skill directly derives from or documents one specific upstream artifact.
- `metadata.credit` — prose, for provenance that doesn't reduce to a pointer: adapted from multiple skills, inspired by someone's approach, or authored by a person rather than a repo ("Prompt by Suzanne at Anthropic, shared in a tweet thread by Thariq").

They can coexist (source for the artifact, credit for the story). When someone else wrote the content wholesale and it's only being packaged here, put them in `author` and elaborate in `credit`.

## Privacy tiers

Three tiers, two repos:

| Tier | Repo | Visibility | Use for |
|------|------|------------|---------|
| Public | `agent-stuff` | Public on GitHub, no `internal` flag | Skills genuinely useful to others |
| Internal-but-public | `agent-stuff` | Public on GitHub, `metadata.internal: true` | Personal workflows that aren't sensitive but aren't general-purpose either |
| Private | `agent-stuff-private` | Private GitHub remote, `metadata.internal: true` | Career materials, project-specific assistants, anything that shouldn't leave Nathan's environment |

The previous `skills/private/` (gitignored subfolder of agent-stuff) tier is retired — that pattern was fragile (one stray `git add -A` and content leaks) and made cross-machine sync impossible. All formerly-private skills now live in `agent-stuff-private`.

### Writing register per tier

The tier decides who the reader is, so it also decides how specific the prose should be. Match the register to the tier:

- **Public (no `internal` flag)** — write vendor-neutral and user-neutral. The reader is a stranger with their own vault, stack, and conventions. State conventions as general practice, tell the skill to adapt to *the user's* existing setup rather than assuming Nathan's, and give escape hatches ("skip if the target vault stores these as plain strings"). No references to Nathan, his vault paths, his folder names, or his specific tooling.

- **Internal-but-public (`internal: true` in `agent-stuff`)** — Nathan-specific is fine, but write it so a stranger reading it on GitHub can still follow the reasoning and adapt it as an example. This tier is for personal workflows that aren't sensitive and that others might reasonably want to copy or configure for themselves. Name Nathan's conventions concretely, but explain *why* enough that the pattern transfers; don't assume the reader shares his setup silently.

- **Private (`agent-stuff-private`)** — write straight to Nathan's environment with no translation. Hard-code paths, folder names, tool wiring, personal conventions. Nothing here is read by a stranger, so spend zero words generalizing.

The deciding question when a skill is Nathan-specific: is this something others might want to configure for themselves or use as an example (→ internal-but-public), or is it too tied to his private conventions/quirks to want to reveal (→ private)? When a skill mixes a general capability with Nathan-specific conventions, prefer keeping the general capability vendor-neutral in the public skill and pushing the personal layer into a separate private or internal skill, rather than baking his quirks into the reusable one.

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
