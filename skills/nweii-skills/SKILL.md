---
name: nweii-skills
description: "Use when creating, editing, auditing, migrating, installing, or publishing skills, loading repository skills on demand, or reflecting on a session to improve skills in Nathan's environment."
argument-hint: "[reflect | skill task]"
metadata:
  author: nweii
  version: "2.5.0"
  internal: true
  credit: "Reflection mode adapted from Lauren Tan (poteto)'s pstack reflect: https://github.com/cursor/plugins/blob/e5a8186d7b43be8d6ac4452440fbead5f1a51c70/pstack/skills/reflect/SKILL.md. MIT notice: LICENSE.pstack."
---

# nweii-skills

Treat repository skill folders as source and installed skills as downstream copies. Complete skill work only after every changed artifact has an owner, privacy tier, validation result, and explicit publish state.

## Reflect on a session

When Nathan supplies `reflect` as an argument or explicitly asks to review a session for skill improvements, follow [references/reflect.md](references/reflect.md). This mode reviews session evidence through judgment, tooling, and divergent lenses, then returns proposed edits, rejected findings, and a local backlog. Run it only on request. Present concrete edits for approval unless Nathan already authorized applying them; an ordinary skill task does not start reflection.

## Audit a skill collection

When Nathan asks to assess overlap, redundancy, or consolidation, follow [references/audit.md](references/audit.md). Inventory the requested installed collection or source library, compare contested procedures, and return evidenced dispositions and scoped commands. Audit proposals remain unapplied until authorized.

## Use a skill on demand

When Nathan names a skill to use, load and follow it for the current task. Keep frequently discovered skills installed; use repository skills on demand for occasional tasks Nathan invokes by name. A request to use a skill authorizes loading it, not installing it.

Read [references/installation.md](references/installation.md) for repository discovery and `bunx skills use`. Read the returned instructions and resolve relative references from the downloaded supporting-files directory, then carry out the task in this conversation. Leave off `--agent` to keep execution here.

## Source ownership

The paired repositories have distinct roles:

- `~/Developer/LLMs/agent-stuff-private/` holds the complete canonical library of Nathan's own skills and retained adaptations.
- `~/Developer/LLMs/agent-stuff/` holds a curated, approved set of public exports. Its existing skill and plugin paths remain valid for public users.

Author and edit private source first, including skills suitable for general audiences. Repository visibility controls access; `metadata.internal: true` marks a personal audience, not private storage. A general skill in the private library keeps its general metadata.

In each repository, a standalone skill lives in `skills/<name>/` and a plugin member in `plugins/<id>/skills/<name>/`. Each name is unique within a repository. Folder placement defines plugin membership, which is a separate decision from source ownership or public export approval. Read the repository's `AGENTS.md` before changing packaging or releases.

The canonical repository's `scripts/public-exports.json` maps each approved export name to its fixed path in the public repository. Preserve those paths when reorganizing private source. Exporting a skill requires Nathan's explicit approval and a privacy review of the complete folder, including references, scripts, examples, assets, and attribution. Approval to edit private source alone does not authorize an export.

Approved pairs follow one of two contracts:

- **Mirror** (default): the complete folders agree, with only `metadata.credit` allowed to differ. Maintain the approved public copy from safe private-source changes within the authorized export scope. If a private change introduces material unsuitable for that export, hold the public change and resolve the boundary rather than copying it incidentally.
- **Variant** (listed in `scripts/public-variants.txt`): the public procedure is generalized and the private copy personalized. Carry shared procedure changes across by hand while preserving the public audience. `things-app` is a deliberate variant.

`scripts/check-mirrors.py` enforces that public skills have private canonical counterparts, export membership and paths match the approved map, and mirrored folders agree. A new export, removed export, or public path change needs explicit approval before updating the map.

For third-party skills, use the upstream source or supported upstream plugin by default. Retain or bundle a copy only for a documented exception, with its source revision, license, attribution, and adaptation boundary. A retained copy does not transfer upstream authorship to Nathan.

Both repositories generate their catalog and per-skill zip archives through a pre-commit hook. Edit skill source only; do not hand-edit `README.md` catalog entries or `zips/`.

Installed copies under `~/.agents/skills/<name>/` are downstream. Before reconciling apparent installed drift, diff the full installed directory against its canonical directory. Preserve useful local advances in canonical source, then reinstall when authorized. Never maintain the installed copy directly.

When a skill ships a template or configuration for another application, update the source artifact and reconcile its deployed copy in the same authorized change. Record saved, imported, and exercised state separately. An import does not prove the downstream workflow.

## Required branches

Read only the reference needed for the current branch:

- Read [references/authoring.md](references/authoring.md) before creating or substantially editing a skill. It defines frontmatter, writing, versions, attribution, and validation.
- Read [references/privacy-and-migration.md](references/privacy-and-migration.md) before choosing or changing a privacy tier, moving a local skill into a repository, or transferring content between repositories.
- Read [references/installation.md](references/installation.md) before discovering or using a repository skill on demand, or installing, updating, repairing, removing, or diagnosing a skill installation.

## Publish boundaries

Local commits are allowed in either repository.

- `agent-stuff` is public. Get Nathan's explicit confirmation immediately before pushing.
- `agent-stuff-private` is private. Push completed work as needed unless the task sets a narrower boundary.

A commit, push, installation, and exercised downstream workflow are distinct states. Report only the states verified from their owning artifact.

## Completion check

Before finishing skill work, verify:

- every edit starts in the private canonical library and respects its audience and export boundary;
- approved public exports retain their mapped paths and pass the mirror or deliberate-variant checks;
- frontmatter and relative references validate;
- new or changed scripts have an observable check;
- generated catalogs or archives were changed only through their repository workflow;
- installation and publishing occurred only when authorized;
- useful installed drift is either reconciled or explicitly held with its reason.
