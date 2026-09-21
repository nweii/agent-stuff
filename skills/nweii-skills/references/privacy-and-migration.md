# Privacy and migration

Use this reference before selecting a privacy tier, moving a local skill into a repository, or transferring content between repositories.

## Privacy tiers

| Tier | Repository | Marker | Content |
|---|---|---|---|
| Public | `agent-stuff` | no `internal` flag | Vendor-neutral skills useful to strangers |
| Internal-but-public | `agent-stuff` | `metadata.internal: true` | Nathan-specific, non-sensitive workflows that remain understandable as public examples |
| Private | `agent-stuff-private` | `metadata.internal: true` | Personal, confidential, career, project-specific, or restricted material |

The retired `agent-stuff/skills/private/` pattern is not a privacy boundary.

Public prose must not contain Nathan's paths, private names, or personal tooling assumptions. Internal-but-public prose may name Nathan's conventions but must explain enough for a public reader to adapt them. Private skills may address Nathan's environment directly.

When a skill mixes a reusable capability with personal conventions, keep the general capability public and place the personal layer in a separate internal or private skill.

## Migrating installed work

1. Diff the whole local skill against any canonical copy and identify the useful changes.
2. Choose the privacy tier and canonical repository.
3. Add or reconcile the complete skill folder under `skills/<name>/`.
4. Correct and quote the description, preserve attribution, and set a meaningful version.
5. Validate the skill and relative references.
6. Commit and publish only under the repository's current authorization boundary.
7. When installation is authorized, use the commands in [installation.md](installation.md) to replace the downstream copy.

Credentials and install tokens never belong in either repository. Migration is complete when canonical source contains every retained change and downstream installation state is reported separately.
