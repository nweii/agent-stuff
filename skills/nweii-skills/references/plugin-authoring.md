# Plugin authoring

Use this reference when choosing members or building a plugin for Agent Plugins, Claude Code, and Codex. Follow the target repository’s AGENTS.md for source ownership, packaging checks, and release procedure.

## Choose the payload

Bundle skills used together in a coherent workflow. Identify required peer skills, optional companions, tools, and runtime requirements. Include required procedures or name their installation dependency; place optional companions beside the branch that uses them. Confirm which target clients can supply each requirement.

Keep complete skill folders immediately under `skills/`, preserving frontmatter names. Packaged references, scripts, and assets must resolve inside the plugin root. Use actual files for Nathan’s generators.

```text
my-plugin/
├── plugin.json                  # Portable manifest, including OpenAI settings
├── skills/
│   └── my-skill/
│       ├── SKILL.md
│       └── references/          # Optional supporting files
├── .claude-plugin/plugin.json   # Claude Code adapter
├── mcp.json                     # Optional portable MCP configuration
└── .mcp.json                    # Optional Claude MCP configuration
```

## Adapt to each client

Use the [Agent Plugins specification](https://agent-plugins.org/specification) for root metadata and component discovery. For Claude Code, read [Anthropic’s creation guide](https://code.claude.com/docs/en/plugins/create.md) for scaffolding and local testing, and its [manifest reference](https://code.claude.com/docs/en/plugins-reference) for component fields. Claude’s adapter reads the shared root `skills/` directory.

For Codex, keep portable identity at the root and put OpenAI settings in `extensions.com.openai`. This supplies presentation and registered-app mappings within the portable manifest. See [OpenAI’s packaging guide](https://developers.openai.com/plugins/build/plugins).

Maintain shared metadata once and generate the client adapters. In Nathan’s repositories, `plugin-source.json` is the build input; AGENTS.md points to the packaging workflow. For another repository, adapt the build inputs and catalogs to its conventions.

## Add integrations when needed

Portable MCP uses root `mcp.json`; Claude uses `.mcp.json`. Nathan’s generator accepts remote endpoints once and emits portable `streamable-http` and Claude `http` configurations. Document client omissions through `skipFor` and keep credentials in client-managed authentication.

For an existing registered OpenAI connection, use an `apps` mapping and confirm it supplies the intended tools. For local MCP, hooks, agents, or other capabilities beyond the generator’s subset, read the relevant client documentation and extend generation and validation together. Test the affected workflow on each target client.
