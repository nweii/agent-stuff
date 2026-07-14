---
name: codex-dispatch
description: "Use when the user wants Codex to handle a task from Claude Code: investigating a bug, attempting a fix, taking a second or cheaper pass, drafting, or refactoring. Also when routing to the codex-rescue subagent, or deciding whether Codex should edit files or only report back."
compatibility: "Designed for Claude Code. Requires the Codex CLI, authenticated with a ChatGPT subscription or an OpenAI API key, plus OpenAI's Codex plugin installed from the openai-codex marketplace. Dispatches that run shell network commands also need network_access enabled in Codex's own config; web search needs nothing extra."
metadata:
  author: nweii
  version: "0.2.1"
  source: openai/codex-plugin-cc
---

# Codex dispatch

A dispatch is one complete, self-contained prompt sent to Codex. Give it the deliverable, target files or directories, constraints, and required checks. Codex works from that prompt alone: the conversation, the reasoning behind the request, and the skills loaded in this session all stay on this side, and Codex starts with the repository, whatever its own configuration supplies, and the prompt. Put substantial prompts in a file and pass `--prompt-file`.

Use the companion as the contract. The companion speaks Codex `app-server` JSON-RPC over a socket through a persistent broker, which provides resumable threads, background jobs, and structured review output. `codex exec` bypasses that broker, loses those, and has no remaining advantage.

## Send a dispatch

The plugin's `codex:*` surfaces are designed entry points the main thread reaches on its own: the `codex-rescue` subagent, and the `review`, `adversarial-review`, and `setup` companion subcommands the commands wrap. Prefer one when the task carries little session context and ergonomics beat a hand-tuned brief: `setup` for readiness, `review` or `adversarial-review` for a structured pass, the subagent for a quick throw-over. Author the `task` prompt yourself when the brief benefits from folding in the session's skills, conventions, and decisions.

The main thread writes the prompt, chooses the scope, submits the dispatch, pulls its result, and verifies the outcome. The `codex:codex-rescue` subagent is a pipe by design: its instructions confine it to forwarding one `task` call and returning stdout verbatim, and bar it from inspecting the repository, polling status, or fetching results. Treat that as its contract rather than a guarantee, and keep inspection, polling, result retrieval, and follow-up work in the main thread.

Take stock of what this session is running on before writing the brief: skills in play, conventions from instruction files, decisions already made, constraints the user set. Fold whatever shapes the work into the prompt. Knowledge carries well — voice rules, domain facts, the standard the result has to meet. Procedure tied to this harness, such as tool names, MCP servers, or subagents, reads as noise on the other side, so state the outcome it was meant to produce instead.

To hand over a skill, resolve its absolute path here and tell Codex to read it before starting, naming the entry file and any sibling reference files it needs. Reads outside the workspace succeed, so the path holds regardless of `--cwd`. Pass the path rather than the name, so Codex has a file to open. Then ask the result for something only that skill would produce, since a dispatch that missed it still returns finished-looking work.

Standing conventions belong in `AGENTS.md`, which Codex loads on its own.

Glob the installed companion version instead of naming one:

```sh
node ~/.claude/plugins/cache/openai-codex/codex/*/scripts/codex-companion.mjs task [flags] [prompt]
```

An empty glob means the plugin is absent. `/codex:setup` reports whether Codex is installed and authenticated.

Run short, bounded work in the foreground. Send anything long or open-ended to `--background`, which returns a job id and leaves the session free to keep working; `status` then reports live progress, `result <task-id>` pulls the finished output, and `cancel <task-id>` stops it. A dispatch is complete once its terminal result is retrieved and the main thread has verified the requested work.

Make the first prompt specific enough to name the thread. The companion derives the thread name from that prompt, so begin with a concrete verb and object.

Wait for a terminal result before sending a correction; `--resume-last` then appends it to the visible thread. A resume aimed at a job that is still running is refused outright (`Task <id> is still running`) before Codex is invoked, so a mid-run correction never reaches the work.

## Choose the scope before adding `--write`

1. For code inside the session's repository, pass `--write`. Default cwd resolution already targets that repository.
2. When the session spans more than one directory, name the target explicitly with `--cwd <absolute path>`. The workspace otherwise resolves from the directory the command itself runs in, which may not be the repository the request concerns; paired with `--write`, a dispatch that lands in the wrong tree still reports success.
3. For prose or notes in a non-code repository (a documentation repo, a notes vault), dispatch read-only and take the prose back as text. Let the main thread apply it after the user reads it.

`--write` selects the `workspace-write` sandbox; without it the companion uses `read-only`. The rescue pipe is instructed to add `--write` unless asked otherwise, so a read-only dispatch must say so explicitly.

`--cwd <dir>` relocates a job but cannot narrow it. The workspace root resolves to the git root of that directory, or to the directory itself when it is not a git repository, so there is no way to scope a dispatch below a repository root.

Naming a subdirectory therefore does more than fail to confine the job: it runs from the repository root instead. Every relative path in the prompt resolves from that root rather than from the directory named, so `./out.txt` lands at the top of the repository and `../out.txt` lands beside it, outside. Codex reports these writes as successful because they are, merely not where the prompt implied. Give absolute paths whenever placement matters.

Because the companion catches a failed git lookup, a non-git directory needs no `--skip-git-repo-check`; that flag and raw-CLI flag-ordering workarounds do not apply to companion commands.

The sandbox permits reads outside the workspace and rejects writes outside it (`patch rejected: writing outside of the project`). Temp directories stay writable regardless, which makes a scratch directory a poor place to test confinement.

Shell network access is a separate setting, off unless Codex's own config enables it. Without it, DNS does not resolve, so `curl`, `git push`, and deployments fail inside a dispatch. Turn it on in `~/.codex/config.toml`:

```toml
[sandbox_workspace_write]
network_access = true
```

The companion passes no network setting either way, so this is Codex's configuration rather than anything the plugin controls. A broker is started per working directory and caches config when it launches, so a config change reaches only workspaces whose broker starts afterward.

Web search is a different channel and needs none of the above. Codex reaches the web through its own `web.run` tool, which works under the default sandbox with shell network off, so research dispatches need no configuration.

## Verify the surface instead of trusting a list

Codex and its plugin move faster than any list written here. Three checks answer the questions that rot, each cheap enough to run before depending on the answer.

Flags the installed companion accepts:

```sh
grep -oE "options\.[a-zA-Z]+" ~/.claude/plugins/cache/openai-codex/codex/*/scripts/codex-companion.mjs | sort -u
```

Model slugs, default efforts, and the effort levels each model supports:

```sh
cat ~/.codex/models_cache.json
```

The cache refreshes itself and is authoritative. Read it rather than assuming an effort level exists, since the companion's own documented range and a given model's supported range can disagree.

Leave `--model` and `--effort` unset by default; both inherit the user's Codex configuration. Set them when the user asks for a particular model or a heavier pass.

The companion's path, via the glob above rather than a pinned version directory.

Two flags are worth naming because their behavior is not evident from the name: `--prompt-file <path>` reads the prompt from a file, and `--write` carries the sandbox consequences described above. For everything else, run the grep.

These instructions were verified against codex plugin 1.0.0 and codex-cli 0.144.1. The three checks are what keep them current; the version pin only says when they were last confirmed.

## Keep the audit trail

`task` produces a named, resumable thread visible in the Codex app at `codex://threads/<id>`, and `--resume-last` continues it. Every delegation therefore leaves an inspectable record outside Claude Code.

The companion prints `Thread ready (<id>)` as the thread opens, ahead of the work. Give the user `codex://threads/<id>` at that point, so a backgrounded dispatch can be watched in the Codex app while it runs. The app is an optional viewer: where it is absent (a headless box), the thread still opens and resumes, so inspect it with `status` and `result` in place of the GUI. `review` and `adversarial-review` are ephemeral by design and leave no visible thread, so a missing thread after a review is not a failure. Raw `codex exec` leaves no app-server thread at all.
