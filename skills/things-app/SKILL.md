---
name: things-app
description: "Read, capture, schedule, and update tasks and projects in Things 3 across three modalities: the `things` CLI on a Mac (full read + write), the `things:///` URL scheme on any device including iPhone, and email-to-Things for headless capture. Use to add todos, build a project, show Today/Inbox, find tagged tasks, or schedule from desktop, phone, or a serverless routine."
metadata:
  author: nweii
  version: "1.0.1"
  source: ossianhempel/things3-cli
  credit: "CLI skill adapted from Peter Steinberger (@steipete); wraps ossianhempel/things3-cli and the Things 3 URL scheme by Cultured Code."
---

# Things 3

Drive Things 3 (tasks, projects, areas) through whichever of three modalities fits the environment: the `things` CLI (desktop, full read + write), the `things:///` URL scheme (any device with Things, write-only), or email-to-Things (unattended, Inbox-only capture).

## Pick a modality first

| Modality | Read state? | Schedule & update? | Unattended? | From phone? |
|----------|:-----------:|:------------------:|:-----------:|:-----------:|
| **CLI** (`things` binary) | Yes | Yes | On the Mac only | No |
| **URL scheme** (`things:///`) | No | Yes (`update`/`json` need auth token) | No — someone must open the URL | Yes |
| **Email-to-Things** | No | No (Inbox capture only) | Yes | Yes (send an email) |

The real axis is **attended vs unattended**, not headless. A headless session someone is watching can still use the URL scheme — the agent prints the link, the user opens it. Only a routine with no one to act on its output is limited to email.

Decision rules:

- **On a Mac → use the CLI.** The only modality that can READ Things state (Inbox, Today, search, projects, areas, tags), and it does the full write surface. Default here.
- **No terminal, but the user can act on the output → build a URL.** You construct the `things:///...` link; the user (or an iOS Shortcut) opens it on a device with Things to execute. This holds even when the agent itself is headless — being headless doesn't rule out the URL scheme; only the absence of anyone to open the link does. The mobile and attended-remote write/schedule path.
- **Fully unattended (a remote/NAS routine with no one watching) → email-to-Things.** The only path that needs neither a Mac nor a human. Lands in the Inbox only — no scheduling, no project placement, no updates. Good for dropping raw captures that get triaged later on desktop.

## Credentials

Two values are specific to the user's Things setup:

- **Auth token** — needed only for commands that modify existing data (`update`, `update-project`, `json` with an `update` op); plain `add` / `add-project` / `add-area` don't. Things → Settings → General → Enable Things URLs → **Manage**.
- **Mail-to-Things address** — the capture address for the email modality. Things → Settings → **Mail to Things**.

Resolve each at use time: env var first (`THINGS_AUTH_TOKEN`, `THINGS_EMAIL`), then the inline values below, then ask. Never invent one; never echo either into output, commits, or logs.

In a shell, these belong in the shell profile so an update can't overwrite them; the `things` CLI reads `THINGS_AUTH_TOKEN` on its own:

    export THINGS_AUTH_TOKEN=…
    export THINGS_EMAIL=…@things.email

As a hosted skill (Claude.ai, ChatGPT) there's no shell and nothing overwrites the file — paste the values here instead:

    THINGS_AUTH_TOKEN =
    THINGS_EMAIL      =

---

## 1. CLI (`things` binary) — desktop, full read + write

Default modality on a Mac. Reads the local Things SQLite DB for queries; writes go through the URL scheme under the hood. Reading Things STATE is **only** possible here.

Setup (skip if `which things` returns a path): `brew install ossianhempel/tap/things3-cli`. The DB lives in the Things app sandbox; the terminal may need Full Disk Access to read it. Override the DB path with `THINGSDB` or `--db=PATH` if needed.

### Read (queries the local DB)

- Built-in lists: `things inbox`, `things today`, `things upcoming`, `things anytime`, `things someday`, `things logbook`, `things deadlines`, `things trash`
- Time-scoped: `things logtoday` (completed today), `things createdtoday`, `things completed`, `things canceled`
- Overview: `things all` (Inbox, Today, Upcoming, Anytime, Someday, Logbook, No Area, Areas in one shot)
- Structure: `things projects`, `things areas`, `things tags`
- Search: `things search "query"` — title/notes match; flags `--status=incomplete|completed|canceled|any`, `--project=`, `--area=`, `--tag=`, `--limit=`, `--all` (include completed/canceled/trashed), `--json`
- List todos with filters: `things tasks --project "Travel"`, `things tasks --area "Work"`, `things tasks --tag focus --search "draft"`
- Inspect one item (exact match): `things show "Project Name"`, `things show --id=<ID> --json`
- Most read commands accept `--json` and `--no-header`. Get an item's ID from `--json` output or `things search "x" --json`.

### Write

Preview any write without executing: prepend `--dry-run` (prints the URL, does not open Things). Add `--foreground` to bring Things to the front.

- **Add todo:** `things add "Buy milk" --notes "2% + bananas" --when today --deadline 2026-07-01 --tags "health,phone"`
  - Scheduling via `--when`: `today`, `tomorrow`, `evening` (This Evening), `anytime`, `someday`, a date (`2026-07-01`), or a datetime (`"2026-07-01 18:00"` → adds a reminder).
  - Into a list/heading: `--list "Travel" --heading "Before"` (or `--list-id=<ID>`).
  - Checklist: repeat `--checklist-item "Passport" --checklist-item "Tickets"` (max 100).
  - Multiple at once: `--titles "Milk,Beer,Cheese"` (other flags apply to all).
  - From STDIN (first line = title, rest = notes): `printf 'Title\nNote line\n' | things add -`
- **Update todo (needs auth token):** `things update --id=<ID> "New title" --when today --append-notes "..." --add-tags "urgent"`
  - Notes: `--notes` replaces; `--prepend-notes` / `--append-notes` add. Same pattern for `--checklist-item` (replace) vs `--prepend-checklist-item` / `--append-checklist-item`.
  - Tags: `--tags` replaces; `--add-tags` adds.
  - Move: `--list "Travel" --heading "Before"`. Complete/cancel: `--completed` / `--canceled`.
  - `--duplicate` updates a copy and leaves the original untouched.
- **Areas & projects:** `things add-area "Health"`; `things add-project "New Site" --area "Work" --notes "..." --todo "Task A" --todo "Task B"`
  - `things update-project --id=<ID> --auth-token=$THINGS_AUTH_TOKEN "New Title" --when tomorrow --add-tags Important` (same notes/tags/scheduling flags as `update`, plus `--area` to move, `--todo` to append todos).
  - `things update-area --id=<ID> --add-tags Focus` (AppleScript-based; only updates tags; may prompt for automation permission).

Notes on the CLI write surface: `update`/`update-project`/`update-area` only modify existing items. Repeating todos/projects reject `--when`, `--deadline`, `--completed`, `--canceled`. There is no real "delete" — complete or cancel instead.

---

## 2. URL scheme (`things:///...`) — any device, write-only

Use when building something to open on an **iPhone** (or any device without terminal access). You construct the URL; it executes only when opened on a device that has Things installed. Cannot read state.

Form: `things:///command?param1=value1&param2=value2`. All values are **percent-encoded** (space → `%20`, newline → `%0a`, comma stays literal in tag/list lists). `add` needs no token; `update`, `update-project`, and `json`-with-changes need `auth-token=$THINGS_AUTH_TOKEN`.

Quick examples:

- Capture to Inbox: `things:///add?title=Buy%20milk&notes=Low%20fat`
- Schedule with a tag: `things:///add?title=Call%20doctor&when=next%20monday&tags=Errand` (natural-language dates must be English)
- Into a project with a checklist: `things:///add?title=Trip%20prep&list=Travel&checklist-items=Passport%0aTickets`
- Several todos: `things:///add?titles=Milk%0aBeer%0aCheese&list=Shopping`
- Reschedule an existing todo: `things:///update?id=<ID>&auth-token=$THINGS_AUTH_TOKEN&when=today`
- Show a built-in list: `things:///show?id=today` (ids: `inbox`, `today`, `anytime`, `upcoming`, `someday`, `logbook`, `deadlines`, etc.)

The `json` batch command builds a whole project — headings, todos, notes, checklists — in one URL. For the full per-parameter reference, the `json` schema, date-string formats, and `show`/`search` ids, **read `references/url-scheme.md`** before constructing anything beyond a simple `add`.

When the agent is on the Mac, prefer generating these URLs via `things --dry-run <command> ...`, which prints a correctly-encoded URL you can hand off. Otherwise encode by hand or with a small script.

---

## 3. Email-to-Things — headless capture, Inbox only

The only modality that needs neither a Mac nor any device interaction, so it is the one a remote/NAS routine uses. Send an email to the mail-to-Things address (`$THINGS_EMAIL`):

- **Subject → to-do title. Body → notes.**
- Lands in the **Inbox only.** No scheduling, no tags, no project/area placement, no updates. Triage happens later on desktop.

Use it for unattended capture (a cron job dropping raw items); reach for the CLI or URL scheme whenever scheduling or placement matters.

---

## Gotchas

- **CLI is macOS-only.** It needs the Things app and its local DB present.
- **Reading state (Inbox/Today/search/projects/areas/tags) only works via the CLI** against the local DB. URL scheme and email cannot read anything back.
- **`update` / `update-project` / `json`-with-changes require the auth token.** Plain `add` does not.
- **A `things:///` URL does nothing until opened on a device with Things.** Constructing it is not executing it.
- **Email is Inbox-only** — no scheduling, no placement, no updates.
- **Preview CLI writes with `--dry-run`** before running anything destructive or unfamiliar.
- **Natural-language dates (`next monday`, `in 3 days`) must be in English**, regardless of device language. `yyyy-mm-dd` and `today`/`tomorrow` always work.
- **No true delete** — complete (`--completed`) or cancel (`--canceled`) instead. The CLI's `--when=someday` and `--later` (This Evening) are the scheduling aliases.
- **Renaming/deleting areas and deleting projects aren't in the `things` CLI or URL scheme — but `osascript` (AppleScript) does all of them.** `update-area` exposes tags only, and there's no `delete-area`/`delete-project`, so via those two modalities you can only *create* areas/projects and *reassign* todos (`update --list "..."`). The fourth path is AppleScript against the scriptable Things app — use it on the Mac for exactly these structural edits:
  - Rename an area: `osascript -e 'tell application "Things3" to set name of area "Hobby" to "Side"'`
  - Delete an area: `osascript -e 'tell application "Things3" to delete area "Strata"'`
  - Delete a project (its to-dos go with it): `osascript -e 'tell application "Things3" to delete project "Old Project"'`
  - List/identify first: `osascript -e 'tell application "Things3" to get name of every area'`

  Deletes move items to Things' Trash (recoverable until emptied), not a hard purge. The first `osascript` call may trigger a one-time macOS automation-permission prompt. This is Mac-only and needs no auth token. (The CLI's `update-project --id=<ID> --auth-token=$THINGS_AUTH_TOKEN --canceled` is a softer alternative that sends a project to the Logbook instead of deleting.)
- **Clearing a value via URL:** include the param with an empty value, e.g. `&deadline=` removes a deadline.
