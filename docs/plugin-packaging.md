# Package and release plugins

Use this workflow for plugin metadata, generated catalogs, upload archives, and release tags. Plugin format and membership decisions are described in the plugin-authoring reference; this guide owns this repository’s build and validation procedure.

## Prepare the payload

Edit `plugins/<id>/plugin-source.json` and place complete member folders under `plugins/<id>/skills/`. Folder placement defines membership. Preserve skill names and approved public install paths. For personal bundles, declare general-purpose members in `generalMembers` while preserving their audience.

Generate metadata with `python3 scripts/generate-plugins.py`. This produces root `plugin.json`, the Claude manifest, and both marketplaces from one input. OpenAI settings live in the root manifest’s `extensions.com.openai` object.

Stage the intended source files before building catalogs or archives: those builders read the Git index, including supporting files and hidden manifests. The pre-commit hook regenerates metadata and README sections, stages the generated documentation, builds archives, and checks their exact contents against staged source. Run `python3 scripts/test-plugins.py` when changing these scripts or the hook.

## Check the generated package

From the repository root, after staging and building:

```bash
uv run scripts/validate-plugins.py --archives
claude plugin validate --strict plugins/<id>
claude plugin validate --strict .claude-plugin/marketplace.json
python3 scripts/release-plugin.py <id> --check
```

The consolidated validator checks generated metadata, the published Agent Plugins schema, the project’s OpenAI extension and marketplace contracts, and final ZIPs. Archive checks reject missing, extra, duplicate, stale, or changed entries, including hidden files. Plugin archives put the payload at the archive root. The same archive check runs after every hook build and before release tagging; routine commits need no separate manual ZIP inspection.

Validate changed skill frontmatter and references with the repository’s skill checks. Structural checks do not exercise client authentication or tool behavior. When changing membership, discovery, or integrations, test the affected workflows in fresh client conversations and record the runtime result separately.

## Cut an authorized release

1. Prepare the version with `python3 scripts/release-plugin.py <id> --version <version>`.
2. Commit the intended payload and generated archive. The hook writes `zips/plugins/<id>-<version>.zip`, retaining the current version of each plugin.
3. Run `python3 scripts/release-plugin.py <id> --tag` from a clean checkout. It checks both manifests, marketplace versions and sources, and the plugin archive before creating `<id>/v<version>`.
4. Push only within the repository’s publishing authorization. Verify the remote branch and release tag identify the intended commit.

Claude marketplace entries use repository-relative plugin paths; Codex entries use Git subdirectories pinned to release tags. A local tag is unavailable to remote installs until pushed.

ChatGPT account-level archive installations do not follow repository updates. Upload the released ZIP through Plugins → Personal → Upload plugin archive when an account installation or update is authorized. Report publication, installation, and exercised behavior separately.
