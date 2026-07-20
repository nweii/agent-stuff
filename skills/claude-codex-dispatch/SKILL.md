---
name: claude-codex-dispatch
description: "Use when handing work between Claude Code and Codex: dispatching a task, choosing terminal or desktop ownership, recovering or continuing dispatched work, and retrieving its result."
compatibility: "Designed for Claude Code and Codex surfaces with local shell access. Claude-to-Codex dispatch uses OpenAI's Codex plugin for Claude Code. Codex-to-Claude dispatch uses the Claude Code CLI; native background sessions require Claude Code 2.1.139 or later."
metadata:
  author: nweii
  version: "0.3.0"
---

# Claude-Codex dispatch

A dispatch hands one self-contained task to the other provider. It owns the task it creates through completion or an explicit transfer to a desktop surface; it does not provide general access to unrelated sessions.

## Dispatch the task

1. Identify the target provider. When Claude is sending to Codex, read [`references/dispatch-to-codex.md`](references/dispatch-to-codex.md). When Codex is sending to Claude, read [`references/dispatch-to-claude.md`](references/dispatch-to-claude.md). Do not load the other provider branch.
2. Write a self-contained brief with the deliverable, target files or directories, relevant session decisions, constraints, permission scope, and required checks. Resolve any skill the target must use to its absolute `SKILL.md` path. Standing repository conventions stay in `AGENTS.md`, which both providers load themselves.
3. Start the dispatch through the target branch's native execution surface. Prefer automated, provider-owned execution; use a prefilled terminal or desktop link only when the user asks to review and send the prompt manually.
4. Surface the target's raw recovery handle as soon as it exists. The handoff is incomplete until the user has received it.
5. Keep ownership in the originating session: monitor the task, retrieve its terminal result, and verify the requested outcome. Wait for a terminal state before sending a correction. If the user transfers a Claude CLI session with `/desktop`, report that Claude Desktop owns all further steering and results, then stop monitoring it from Codex.

A dispatch is complete when its terminal result has been retrieved and verified, or when ownership has been explicitly transferred to Claude Desktop and the user has been told where the task continues. Keep recovery handles in the conversation; create no parallel task registry.
