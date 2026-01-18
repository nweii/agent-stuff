---
title: spec-interview
description: Interview the user about a product plan idea until a detailed spec is produced.
argument-hint: [plan]
model: opus
# based on https://x.com/trq212/status/2005315275026260309
---

Read this plan file $1 and interview me in detail about literally anything: technical implementation, UI & UX, concerns, tradeoffs, etc. Make sure questions are not obvious.

## Interview Principles

1. **Narrow before expanding**: Push to narrow the problem until it can be described in one clear sentence. Vague scope ("build a calendar") leads to endless shaping. Precise scope ("show empty time slots between existing events") enables real solutions.

2. **Surface complexity early**: Ask "what could make this harder than it sounds?" and "where are the hidden dependencies?" The goal is to reveal time bombs before they're in the middle of a build, not after.

3. **Distinguish understanding from justification**: Watch for the anti-pattern where someone has already decided what to build and is looking for data to justify it. Ask why this problem matters *before* discussing solutions.

4. **Probe the adjacent user**: If this is user-facing, ask who the *next* user is — the one just outside the current target. What would need to be different for them?

## Process

Be very in-depth. Continue interviewing until you're confident the problem is well-framed and the key risks are surfaced. Then write the spec to the file.

A good spec should be **shapeable** — someone should be able to read it and describe the solution in ≤9 major components. If they can't, the problem isn't narrow enough yet.