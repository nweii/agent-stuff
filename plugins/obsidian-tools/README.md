# Obsidian Tools

Operate your Obsidian vault, write note descriptions, and create Templater and Web Clipper templates using your own conventions. The vault's instructions and existing examples supply its folder layout, metadata, and writing preferences.

Skills in `skills/` are the canonical payload. Obsidian CLIs uses the app CLI with a headless fallback; the other tools write note descriptions and help author Templater and Web Clipper templates. Install the relevant Obsidian application, community plugin, or browser extension before using its tool. This package includes no remote vault connection or account credentials.

## Individual installation

Use one delivery route per skill in an environment to avoid loading a standalone and plugin copy together. Individual ZIP downloads remain in the repository's `zips/` folder.

Install a named skill through the repository's local Claude catalog (tested with skills CLI 1.7.0):

```bash
bunx skills add nweii/agent-stuff --skill obsidian-clis
```

Existing standalone locks can follow moves within this repository with skills CLI 1.5.24 or later (tested with 1.7.0). Internal skills elsewhere in the repository can receive false deletion warnings during an update. Include them in discovery with `INSTALL_INTERNAL_SKILLS=1`, or decline removal. Noninteractive updates skip deletion.

## Metadata and release

Edit `plugin-source.json` for the plugin's promise and presentation. The generator writes root `plugin.json`, `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`, and both marketplace catalogs. Membership is the folder; there is no separate list. Version `0.1.0` is the first release candidate.

The Claude catalog uses `./plugins/obsidian-tools`, which supports named and unscoped skills CLI discovery. Claude plugin payloads follow the marketplace checkout (normally the repository's default branch). Git-hosted installed plugins stay on their version until it changes; new installers can receive unreleased edits under the current version. This version gate does not apply to plugins loaded in place from a local marketplace directory.

The Codex catalog pins `git-subdir` + `ref` to `obsidian-tools--v0.1.0`. That tag must exist remotely before Codex can fetch the release. Watch pending [skills PR 1334, remote marketplace sources](https://github.com/vercel-labs/skills/pull/1334): support for that source type could remove the discovery reason for the split (open/unmerged when checked October 4, 2026).

From the repository root:

```bash
python3 scripts/generate-plugins.py
python3 scripts/test-plugins.py
uv run scripts/validate-plugins.py
claude plugin validate --strict plugins/obsidian-tools
claude plugin validate --strict .claude-plugin/marketplace.json
python3 scripts/release-plugin.py obsidian-tools --check
```

To cut a release, prepare the version with `--version MAJOR.MINOR.PATCH`, review and commit metadata, then run `--tag` from a clean checkout. The release script requires all three manifests and both catalog versions to match, plus the Claude local source and Codex release ref, before calling plain `git tag`. It performs no push. Ordinary skill edits do not bump the plugin version; Codex release payloads remain fixed at their tags, while Claude follows the version behavior above.

Agent Plugins validation uses its [published 1.0.0 schema](https://agent-plugins.org/schemas/1.0.0/plugin.schema.json). Codex validation uses project-owned contract schemas derived from the [official packaging reference](https://developers.openai.com/plugins/build/plugins) and its pinned parser sources; these are not published OpenAI schemas. Schema and manifest validation do not establish account import, runtime behavior, or update propagation.
