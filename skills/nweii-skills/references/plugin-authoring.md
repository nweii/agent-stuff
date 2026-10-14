# Plugin authoring

Use this reference to create or repackage a plugin for Agent Plugins, Claude Code, and Codex, or to validate and release an existing package. For Nathan’s library, follow the repository’s AGENTS.md and nweii-skills’ source ownership and publish boundaries.

## Create or repackage

1. **Choose membership.** Group skills used together in a coherent workflow. Record every required peer skill, optional companion, tool, and runtime requirement. Bundle required procedures or name their installation dependency; place optional companions beside the branch that uses them. Confirm which target clients can supply each requirement.
2. **Assemble one payload.** Put complete skill folders immediately under `skills/`, with their frontmatter names preserved. Include every packaged reference, script, and asset. Keep package paths inside the plugin root; Nathan’s generators require actual files rather than symlinks.
3. **Generate the adapters.** Maintain shared metadata once and generate each client’s manifest. Use the layout and client rules below. Confirm that generated identities and versions agree and every declared path exists.
4. **Validate the package.** Follow the validation section. Finish packaging only when the complete generated payload and both marketplace entries pass their applicable checks.

```text
my-plugin/
├── plugin.json                  # Portable manifest
├── skills/
│   └── my-skill/
│       ├── SKILL.md
│       └── references/          # Optional supporting files
├── .claude-plugin/plugin.json   # Claude Code adapter
├── .codex-plugin/plugin.json    # Optional Codex fallback
├── mcp.json                     # Optional portable MCP configuration
└── .mcp.json                    # Optional Claude MCP configuration
```

Use the [Agent Plugins specification](https://agent-plugins.org/specification) for root metadata and component discovery. For Claude Code, read [Anthropic’s creation guide](https://code.claude.com/docs/en/plugins/create.md) for scaffolding and local testing, and its [manifest reference](https://code.claude.com/docs/en/plugins-reference) for component fields. Claude’s adapter reads the shared root `skills/` directory.

For Codex, place OpenAI settings in root `plugin.json` under `extensions.com.openai`. That object replaces the entire `.codex-plugin/plugin.json` fallback for client settings; the two are not merged. Keep portable identity at the root. See [OpenAI’s packaging guide](https://developers.openai.com/plugins/build/plugins).

### Nathan’s generator workflow

Start with an existing plugin’s `plugin-source.json` and README. Keep only metadata, assets, and integrations that belong to the target package. Place member folders under `plugins/<id>/skills/`; folder location defines membership. List general-purpose members of a personal bundle in `generalMembers` while preserving their audience.

`plugin-source.json` is a build input, not a standard manifest. Use the repository’s generation, catalog, and archive commands from AGENTS.md. The catalog and ZIP builders read staged files: stage the intended payload before building and inspect the generated result.

For another repository, adapt the build inputs and catalog policy while keeping the package layout. Nathan’s generators assume his library’s structure.

### When adding integrations

Declare remote MCP endpoints once in the generator’s `mcpServers` input. It emits portable `streamable-http` and Claude `http` configurations. Document client-specific omissions through `skipFor`; keep credentials in client-managed authentication. For an existing registered OpenAI connection, use an `apps` mapping and confirm the intended connection supplies the tools.

For local MCP, hooks, agents, or other capabilities beyond the generator’s subset, read the relevant client documentation and extend generation and validation together. Treat each client implementation as a separate runtime check.

## Validate an existing or generated package

Use the repository’s checks for skill frontmatter and references, generated metadata, the portable schema, and both clients’ manifests and catalogs. The project’s Codex contract checks its supported subset; it is not an official published schema. Run generator tests when changing generation behavior.

Inspect the final ZIP itself: root manifests, hidden adapters, and every supporting file must be included without an enclosing package folder. When runtime testing is authorized, use a fresh conversation in each client and verify every intended skill is discoverable, every supporting file reachable, and every required tool usable. Record structural validation and runtime results separately.

## Release when authorized

Follow the repository’s release procedure for version preparation, generated archives, commits, and tags. Marketplace entries are outside the payload; Nathan’s generator emits Claude repository-relative sources and Codex Git subdirectories pinned to release tags.

Verify the published branch, tag, and archive agree. Report publication, installation, and exercised behavior separately; a local tag or valid archive does not establish delivery.
