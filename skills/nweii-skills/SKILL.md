---
name: nweii-skills
description: "Use when creating, editing, migrating, installing, or publishing skills, loading repository skills on demand, or reflecting on a session to improve skills in Nathan's environment."
argument-hint: "[reflect | skill task]"
metadata:
  author: nweii
  version: "2.3.0"
  internal: true
  credit: "Reflection mode adapted from Lauren Tan (poteto)'s pstack reflect: https://github.com/cursor/plugins/blob/e5a8186d7b43be8d6ac4452440fbead5f1a51c70/pstack/skills/reflect/SKILL.md. MIT notice: LICENSE.pstack."
---

# nweii-skills

Treat repository skill folders as source and installed skills as downstream copies. Complete skill work only after every changed artifact has an owner, privacy tier, validation result, and explicit publish state.

## Reflect on a session

When Nathan supplies `reflect` as an argument or explicitly asks to review a session for skill improvements, follow [references/reflect.md](references/reflect.md). This mode reviews session evidence through judgment, tooling, and divergent lenses, then returns proposed edits, rejected findings, and a local backlog. Run it only on request. Present concrete edits for approval unless Nathan already authorized applying them; an ordinary skill task does not start reflection.

## Use a skill on demand

When Nathan names a skill to use, load and follow it for the current task. Keep frequently discovered skills installed; use repository skills on demand for occasional tasks Nathan invokes by name. A request to use a skill authorizes loading it, not installing it.

Read [references/installation.md](references/installation.md) for repository discovery and `bunx skills use`. Read the returned instructions and resolve relative references from the downloaded supporting-files directory, then carry out the task in this conversation. Leave off `--agent` to keep execution here.

## Source ownership

Canonical skills live in two paired repositories:

- `~/Developer/LLMs/agent-stuff/` for public and internal-but-public skills.
- `~/Developer/LLMs/agent-stuff-private/` for private skills.

In each, a standalone skill lives in `skills/<name>/` and a plugin member in `plugins/<id>/skills/<name>/`; the folder is the plugin membership. Each repository's `AGENTS.md` covers plugin packaging and releases.

A skill name in both repositories marks one of two deliberate relationships. The private repository's `scripts/public-variants.txt` says which:

- **Mirror** (the default): the private copy is canonical, and the public copy is published for reference. Edit the private copy, then copy the change to the public one in the same session; they match except for the private copy's `metadata.credit` line. The private repository's pre-commit hook warns when a mirrored pair differs.
- **Variant** (listed): the public copy is generalized for others, and the private copy is personalized and the one in use. Carry shared procedure changes across by hand, and keep personal details private.

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

- every edit is in the canonical repository and within the selected privacy tier;
- frontmatter and relative references validate;
- new or changed scripts have an observable check;
- generated catalogs or archives were changed only through their repository workflow;
- installation and publishing occurred only when authorized;
- useful installed drift is either reconciled or explicitly held with its reason.
