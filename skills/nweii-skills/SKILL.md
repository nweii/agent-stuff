---
name: nweii-skills
description: "Use when creating, editing, migrating, installing, or publishing skills in Nathan's environment. Routes source ownership, public/private placement, authoring conventions, install mechanics, and release boundaries."
metadata:
  author: nweii
  version: "2.0.0"
  internal: true
---

# nweii-skills

Treat repository skill folders as source and installed skills as downstream copies. Complete skill work only after every changed artifact has an owner, privacy tier, validation result, and explicit publish state.

## Source ownership

Canonical skills live in two paired repositories:

- `~/Developer/LLMs/agent-stuff/skills/<name>/` for public and internal-but-public skills.
- `~/Developer/LLMs/agent-stuff-private/skills/<name>/` for private skills.

Both repositories generate their catalog and per-skill zip archives through a pre-commit hook. Edit skill source only; do not hand-edit `README.md` catalog entries or `zips/`.

Installed copies under `~/.agents/skills/<name>/` are downstream. Before reconciling apparent installed drift, diff the full installed directory against its canonical directory. Preserve useful local advances in canonical source, then reinstall when authorized. Never maintain the installed copy directly.

When a skill ships a template or configuration for another application, update the source artifact and reconcile its deployed copy in the same authorized change. Record saved, imported, and exercised state separately. An import does not prove the downstream workflow.

## Required branches

Read only the reference needed for the current branch:

- Read [references/authoring.md](references/authoring.md) before creating or substantially editing a skill. It defines frontmatter, writing, versions, attribution, and validation.
- Read [references/privacy-and-migration.md](references/privacy-and-migration.md) before choosing or changing a privacy tier, moving a local skill into a repository, or transferring content between repositories.
- Read [references/installation.md](references/installation.md) before installing, updating, repairing, removing, or diagnosing a skill installation.

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
