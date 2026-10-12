# Privacy and migration

Use this reference before choosing an audience, importing installed work, exporting a skill, or changing repository placement.

## Audience and access

Every skill starts in `agent-stuff-private`, the complete canonical library. `agent-stuff` contains only approved public exports. These are separate decisions:

| Audience | Marker | Public export requirement |
|---|---|---|
| General | Omit `internal` | Useful to strangers, with no personal dependencies or confidential material |
| Personal | `metadata.internal: true` | An explicitly approved, non-sensitive example that explains enough context for a public reader |

Private storage supports both audiences. Confidential, personal, project-specific, and restricted material stays outside public exports. Neither an `internal` flag nor a folder named `private` creates access control in a public repository.

Keep general procedure and personal conventions separable when they serve different readers. Prefer conditional references or a focused personal layer over making every reader load Nathan's environment.

## Import or reconcile source

1. Diff the complete installed folder against its canonical counterpart and identify useful drift.
2. Add or reconcile the complete skill folder in the private library. Preserve the audience, original author, source revision, license, references, and scripts.
3. Quote the description and set a meaningful version. Follow [authoring.md](authoring.md).
4. Check `scripts/public-exports.json` for an approved public counterpart and its fixed path. Reorganizing private source does not relocate the export.
5. Within the authorized export scope, carry safe changes into that public copy. Mirrors agree except for `metadata.credit`; deliberate variants listed in `scripts/public-variants.txt` preserve their separate audiences.
6. Validate canonical source, relative references, and export contracts. Commit and publish only within the current authorization boundary.
7. When installation is authorized, follow [installation.md](installation.md). Refresh Nathan's own skills from the private source; existing public installations remain valid until deliberately refreshed.

## Export approval and review

Before adding an export or changing its public path, prepare the complete proposed public folder and obtain Nathan's explicit export approval. Review every supporting file for private names, paths, account details, confidential examples, credentials, licensing limits, and personal assumptions the public audience cannot understand. A generalized export must stand alone.

An approved export is recorded by name and fixed public path in `scripts/public-exports.json`. `scripts/check-mirrors.py` enforces the complete private superset, approved membership and paths, and mirror agreement. Keep the export map within the approved scope; validation does not grant export authority.

For a retained third-party skill, prefer upstream installation. A vendored exception needs documented provenance and redistribution permission before public export or plugin bundling. Preserve the upstream source and any local adaptation boundary.

Credentials and install tokens belong in neither repository. Completion means retained drift is in canonical source, approved exports pass their contracts, and installation and publication states are reported separately.
