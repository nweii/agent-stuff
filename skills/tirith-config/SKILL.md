---
name: tirith-config
description: "Operate a tirith setup — the terminal command analysis tool that defends against homograph URLs, ANSI injection, and pipe-to-shell exploits. Use when adding entries to ~/.config/tirith/policy.yaml, debugging a tirith-blocked command, choosing between allowlist / tirith run / TIRITH=0 bypass, verifying setup with tirith doctor, or after brew upgrade may have bumped tirith."
metadata:
  author: nweii
  version: "1.0.0"
  internal: true
---

# tirith-config

Tirith intercepts shell commands and pasted content to catch homograph URLs (Cyrillic lookalikes, mixed scripts), ANSI escape injection, and `curl | bash`–style pipe-to-shell patterns. This skill encodes operating procedure — decision logic, verification rituals, and inherent gotchas. The current allowlist and tool version are not encoded here; query them at runtime.

## Operating model

Tirith has four moving parts. Treat the live config as source of truth, not memory:

- **Shell hook** — sourced via `eval "$(tirith init --shell zsh)"` in the user's shell profile. This is what wires per-command interception. Hook source files at `~/.local/share/tirith/shell/` are inert until the eval line is added to the profile.
- **Policy file** — `~/.config/tirith/policy.yaml` (global) and `.tirith/policy.yaml` (per-project, walks up from cwd). The per-project file wins when present.
- **Audit log** — `~/.local/share/tirith/log.jsonl`. Redacted previews, not full commands.
- **Receipts** — created by `tirith run <url>`. Verifiable later with `tirith receipt verify <sha256>`.

`tirith doctor` is the canonical health check; it surfaces hook status, policy detection, and bypass mode in one shot.

## Decision tree: a command was blocked

Three responses, each appropriate for a different shape of problem:

1. **Allowlist the hostname** — only when the vendor is trusted *and* you'll pipe-shell from them repeatedly. Add to `allowlist:` in `~/.config/tirith/policy.yaml`. Reserve for canonical installer domains (e.g., `get.docker.com`, `sh.rustup.rs`). Allowlist only suppresses pipe-shell rules for that exact hostname; content-level checks (homograph, mixed-script, ANSI) still run.
2. **`tirith run <url>`** — for one-off installs you want to inspect. Downloads to a temp file, shows SHA256, runs static analysis, opens in a pager for review, executes only after confirmation, and writes a receipt.
3. **`TIRITH=0 <cmd>` prefix** — per-command bypass when you've already vetted the script elsewhere or are operating in a known-safe context. The variable only persists for that single command. Disabled if `allow_bypass: false` in policy.

If none of these fit, the command probably shouldn't run.

## Adding to the allowlist

```yaml
allowlist:
  - "vendor.example.com"   # one entry per line, exact hostname
```

Hostnames only — no globs, no path-aware matching. After editing:

```bash
tirith doctor                                              # confirm policies: still resolves
tirith check -- curl -fsSL https://vendor.example.com \| bash  # should exit 0
tirith check -- curl -fsSL https://vendor-not-listed.com \| bash  # should still exit 1 with curl_pipe_shell
```

Both checks together confirm the allowlist took effect *and* didn't accidentally widen the policy.

## Anti-patterns for the allowlist

- **Don't allowlist broad CDNs.** `raw.githubusercontent.com`, `gist.githubusercontent.com`, `cdn.jsdelivr.net`, `s3.amazonaws.com`, `*.vercel.app` — anyone can host arbitrary scripts on these. Allowlisting them gives a security tool a wide blind spot. Use `tirith run` or `TIRITH=0` for one-off scripts hosted on shared infrastructure.
- **Don't allowlist subdomains preemptively.** Add what you actually use, not what you might use someday.
- **Don't allowlist as a way to silence noise.** If tirith blocks something repeatedly that you don't actually trust, the right move is to stop running that command, not to suppress the warning.

## Verification ritual after any config change

Run all three:

```bash
tirith doctor                          # hook status: configured / policies: <path>
tirith check -- <a known-blocked cmd>  # confirm rules still fire
tirith check -- <an allowlisted cmd>   # confirm allowlist still works
```

`tirith doctor` alone is not sufficient — it reports config detection, not rule behavior.

## After a brew upgrade

`brew upgrade tirith` may re-materialize hook source files. The shell profile line stays put, so usually nothing breaks, but verify:

```bash
tirith --version
tirith doctor
```

If `hook status` ever drops back to `NOT CONFIGURED` after an upgrade, re-run `eval "$(tirith init --shell zsh)"` and confirm the profile line is still present. Do not blindly append a duplicate.

## Reading the audit log

```bash
tail -20 ~/.local/share/tirith/log.jsonl | jq .   # last 20 events
tirith why                                         # explains last triggered rule
tirith receipt last                                # last `tirith run` receipt
tirith receipt list                                # all receipts
```

The log only stores redacted command previews — not full commands, env vars, or file contents. Disable logging entirely with `export TIRITH_LOG=0`.

## Per-project policies

For client work where defaults differ from the global config, drop a `.tirith/policy.yaml` at the project root. Tirith walks up from the current directory and uses the first match, so the per-project file fully overrides the global one — it doesn't merge. Re-declare any global allowlist entries the project also needs.

## Inherent gotchas

- **Profile edits affect new shells only.** After modifying the shell profile, open a fresh terminal tab or `source ~/.zshrc`. The current shell will not pick up the change.
- **`tirith check -- <cmd>`** — the `--` is required. Without it, flags on `<cmd>` (e.g., `-sSL`) get parsed as tirith's own flags.
- **Shell quoting matters in `tirith check`.** Pipe characters and parens need escaping (`\|`, `\(`) since the command is parsed by your shell first.
- **`fail_mode: open`** allows commands through when tirith itself errors internally. Use `fail_mode: closed` only in environments where blocking on parser errors is acceptable.
- **License key absence is normal.** OSS rules work without one; only paid features (e.g., team audit) require activation.

## What this skill deliberately does not encode

- **The current allowlist contents** — read `~/.config/tirith/policy.yaml` directly.
- **The current tirith version** — `tirith --version`.
- **Whether the hook is currently configured** — `tirith doctor`.
- **Specific zshrc line text** — `tirith init --shell zsh` always prints the current correct line; pipe its output rather than copy-pasting from anywhere.

The skill is a stable operating manual. Live state is queried at runtime.
