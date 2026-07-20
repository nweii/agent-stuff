# Dispatch to Claude

Use Claude Code's native background sessions for automated execution. They persist under Claude's supervisor without another plugin and remain manageable from the CLI.

## Check setup

Run:

```sh
command -v claude
claude --version
claude auth status
claude doctor
```

Native background sessions require Claude Code 2.1.139 or later. If the CLI is missing, ask before running Anthropic's native installer on macOS, Linux, or WSL:

```sh
curl -fsSL https://claude.ai/install.sh | bash
```

Use `claude auth login` when authentication is missing. Preserve the user's project settings and permission policy; add `--permission-mode`, `--allowedTools`, or `--disallowedTools` only when the task needs an explicit boundary. Bypass mode requires its disclaimer to have been accepted interactively.

## Start and control the task

Start a durable background session from the target working directory:

```sh
claude --bg --name "<task-name>" "<prompt>"
```

The command returns a short task ID and management commands. Surface the recovery command immediately:

```text
Claude task: claude attach <id>
```

Use the native supervisor for status and results:

```sh
claude agents --json --all --cwd <absolute-path>
claude logs <id>
claude attach <id>
claude stop <id>
```

Use the full `sessionId` from `claude agents --json --all` when a programmatic follow-up needs `claude -p --resume <session-id> --output-format json "<prompt>"`. Wait for the background task to reach a terminal state before sending that follow-up.

For short blocking work, `claude -p "<prompt>" --output-format json` returns the result and session ID. Print-mode sessions stay resumable by ID but do not appear in the interactive session picker.

## Choose the Claude surface

The automated target is a Claude CLI session. It can continue in Claude Desktop through a one-way ownership transfer:

1. Run `claude attach <id>`.
2. Enter `/desktop` in the attached interactive session.
3. Continue steering and reviewing the task in Claude Desktop.

`/desktop` saves the session, opens it in Claude Desktop, and exits the CLI. After transfer, Claude Desktop owns the live session; stop CLI polling and tell the user where the task continues. The transfer requires macOS or Windows and subscription authentication. It is unavailable with API-key authentication and third-party providers.

When the user asks to review a new prompt in Claude Desktop before sending it, provide a raw, URL-encoded link instead of starting a background task:

```text
claude://code/new?q=<encoded-prompt>&folder=<encoded-absolute-path>
```

The link prefills a new Desktop composer, asks the user to confirm the folder, and does not send the prompt. It cannot open an existing Claude CLI task. `claude-cli://open?...` provides the same manual pattern for a new terminal session.

Claude CLI and Desktop keep separate histories except for the explicit `/desktop` transfer. Treat that transfer as terminal from the originating Codex session rather than as synchronization.
