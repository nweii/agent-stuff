# Dispatch to Codex

Use OpenAI's Codex companion for automated execution. It speaks Codex `app-server` JSON-RPC through a persistent broker, so tasks are resumable, backgroundable, and visible in the Codex app. Raw `codex exec` does not provide that thread contract.

## Check setup

The companion lives at:

```sh
~/.claude/plugins/cache/openai-codex/codex/*/scripts/codex-companion.mjs
```

If the glob is empty, ask before installing the plugin:

```sh
claude plugin marketplace add openai/codex-plugin-cc
claude plugin install codex@openai-codex
```

Run `/codex:setup` in Claude Code after installation. It checks the Codex CLI and authentication, offers to install a missing CLI, and preserves the instruction to run `!codex login` when authentication is missing.

The Codex desktop app is optional for execution. It is required only to open the recovery URI visually.

## Start and control the task

Glob the installed version rather than pinning its directory:

```sh
node ~/.claude/plugins/cache/openai-codex/codex/*/scripts/codex-companion.mjs task [flags] [prompt]
```

Use `--prompt-file <path>` for a substantial brief. Begin the prompt with a concrete verb and object because the companion derives the thread name from it.

Run bounded work in the foreground. Add `--background` for long or open-ended work; use `status`, `result <task-id>`, and `cancel <task-id>` to manage it. Wait for a terminal result before using `--resume-last` for a correction.

The companion prints `Thread ready (<id>)` before the work completes. Surface the raw URI immediately and repeat it with the terminal result:

```text
Codex task: codex://threads/<id>
```

`review` and `adversarial-review` are ephemeral and produce no visible thread. Use `task` when recovery and continued conversation matter.

## Set scope and permissions

- For code inside the current repository, add `--write`.
- When the session spans directories, pass `--cwd <absolute-path>`. It relocates the task but cannot narrow access below the resolved Git root.
- For prose or notes outside a code repository, default to read-only and bring the proposed text back for the originating agent to apply.
- Use absolute paths when placement matters. Relative paths resolve from the repository root, even when `--cwd` names a subdirectory.

`--write` selects Codex's `workspace-write` sandbox. Shell network access remains off unless the user's Codex configuration enables it:

```toml
[sandbox_workspace_write]
network_access = true
```

Web search uses Codex's web tool and does not require shell network access. A broker caches configuration per working directory, so config changes reach brokers started afterward.

## Verify current surfaces

The companion and Codex model catalog change independently. Check rather than preserving a large flag or model list:

```sh
grep -oE "options\.[a-zA-Z]+" ~/.claude/plugins/cache/openai-codex/codex/*/scripts/codex-companion.mjs | sort -u
cat ~/.codex/models_cache.json
```

Leave `--model` and `--effort` unset unless the user requests them. These instructions were verified against Codex plugin 1.0.0 and codex-cli 0.144.1.
