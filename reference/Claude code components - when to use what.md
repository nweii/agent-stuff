---
aliases:
  - "Guide to Claude Code's Extension System"
  - Claude plugin system overview
categories: ["[[Clippings]]", "[[Guides]]"]
icon:
publish: false
description: Reference on Claude feature selection (Commands, Plugins, Agents, Skills) with decision criteria for each. Use when building AI tooling, architecting workflows, or deciding whether to use user-invoked shortcuts versus autonomous AI workers versus capability enhancements.
url: https://code.claude.com/docs/en/plugins
author: ["[[Anthropic]]"]
related:
  - "[[Agent Skills - Claude Code Docs]]"
  - "[[AI Prompts]]"
tags: [clippings, ai, ai-tools, ai/agents, prompt-engineering, claude, claude-code, dev, workflows, processes, docs, best-practices, reference]
created: 2025-12-05T00:00
modified: 2025-12-05T20:56
---
Based on the documentation, here's when to use each:

**Use a Command when:**
- You want to **execute specific prompts quickly** with slash commands
- You need **reusable prompt templates** for frequent tasks
- You want team members to easily invoke common workflows
- Example: `/optimize` to analyze code performance

**Use a Plugin when:**
- You want to **package and distribute** multiple components together (commands, agents, skills, hooks, MCP servers)
- You need to **share functionality across teams/projects**

**Use an Agent when:**
- You need to **delegate entire tasks** to a separate AI worker with its own context
- The task requires **independent reasoning** across multiple steps

**Use a Skill when:**
- You want to **enhance Claude's capabilities** with specific knowledge/procedures
- Claude should **autonomously decide** when to apply this expertise

**Key difference**: Commands are user-invoked shortcuts. Agents are AI workers. Skills are autonomous capabilities. Plugins bundle everything together.

