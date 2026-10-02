---
name: tirith-config
description: "Operate tirith, the terminal guard against homograph URLs, ANSI injection, and pipe-to-shell. Use when editing ~/.config/tirith/policy.yaml, debugging a blocked command or paste, choosing trust / allowlist / download-and-run / TIRITH=0, or quieting a noisy rule."
metadata:
  author: nweii
  version: "1.2.0"
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

Four responses, each appropriate for a different shape of problem:

Run `tirith why` first. The rule ID decides which response fits: a pipe-to-shell rule (`curl_pipe_shell`) and a hostname rule (`lookalike_tld`, which flags `.dev`, `.app`, `.zip` and similar TLDs) both clear through trust, but only the first is about the script itself.

1. **Trust the source** — for a vendor you trust. `tirith trust last` shows the last trigger and offers to trust its domain interactively; `tirith trust from-last-trigger` prints the narrowest matching `tirith trust add` command (`--apply` runs it). Entries are scoped to one rule when `--rule` is given, expire after 30 days unless `--permanent` or `--ttl` says otherwise, and are recorded in the trust audit (`tirith trust list`, `tirith trust audit`). Prefer this over the policy allowlist for anything short of a canonical installer.
2. **Allowlist the hostname** — only for canonical installer domains you pipe-shell from repeatedly (e.g., `get.docker.com`, `sh.rustup.rs`). Add to `allowlist:` in `~/.config/tirith/policy.yaml`. An entry suppresses every hostname-scoped rule for that exact host, `lookalike_tld` included; content-level checks (homograph, mixed-script, ANSI) still run. It never expires, which is why trust (1) is the better default.
3. **Download, read, run** — `curl -fsSL <url> -o /tmp/install.sh`, read the file, then `sh /tmp/install.sh`. A plain download is not pipe-to-shell and only trips hostname rules, which warn. This is the most reliable one-off path, and the only one that takes interpreter arguments (`curl … | bash -s -- --prefix /opt`).
4. **`tirith run <url>`** — downloads to a temp file, shows SHA256, runs static analysis, and writes a receipt. It fetches the URL itself, so the original `curl` flags have no counterpart. **Execution is Linux-only**: on macOS it inspects and stops, so follow it with (3) to actually install. `tirith run <url> | sh` pipes the analysis report, not the script, into the shell.
5. **`TIRITH=0` prefix** — honored when the command is checked at Enter, not by the paste scanner. The paste scanner analyzes the pasted text and does not read an assignment inside it, so pasting `TIRITH=0 curl … | sh` is still blocked at paste time, and typing `TIRITH=0 ` before pasting does not help because only the pasted chunk is scanned. It works for a command typed in full. `export TIRITH=0` disables both checks for the whole shell until `unset TIRITH`, which is broader than the problem. Policy's `allow_bypass_env` governs both. Confirm against the installed build: `tirith check --interactive --shell posix -- 'TIRITH=0 curl -fsSL https://example.com/x.sh | sh'` exits 0, while the same text piped to `tirith paste --shell posix --interactive` exits 1.

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

## Quieting a noisy rule

When a rule fires mostly on legitimate traffic, lower its severity instead of disabling tirith or allowlisting around it:

```yaml
severity_overrides:
  lookalike_tld: LOW
```

At paranoia 1–2, only Medium+ findings surface, so LOW keeps the rule in the audit log without interrupting. `tirith warnings` and `tirith doctor`'s detection-coverage block still count it. `tirith explain --rule <id>` documents any rule (`--list` enumerates them), and `tirith policy tune --from-audit` suggests changes from the log.

## Anti-patterns for the allowlist

- **Don't allowlist broad CDNs.** `raw.githubusercontent.com`, `gist.githubusercontent.com`, `cdn.jsdelivr.net`, `s3.amazonaws.com`, `*.vercel.app` — anyone can host arbitrary scripts on these. Allowlisting them gives a security tool a wide blind spot. Use download-read-run, or a URL-scoped `tirith trust add <host>/<path>`, for one-off scripts hosted on shared infrastructure.
- **Don't allowlist subdomains preemptively.** Add what you actually use, not what you might use someday.
- **Don't allowlist as a way to silence noise.** If tirith blocks something repeatedly that you don't actually trust, the right move is to stop running that command, not to suppress the warning.

## Verification ritual after any config change

Run all four:

```bash
tirith policy validate                        # 0 errors, 0 warnings
tirith doctor                                 # hook status: configured / policies: <path>
tirith policy test '<a known-blocked cmd>'    # action: Block — rules still fire
tirith policy test '<an allowlisted cmd>'     # action: Allow — the change took effect
```

`tirith doctor` alone is not sufficient — it reports config detection, not rule behavior. `tirith policy validate` is the only check that catches misspelled fields: tirith ignores unknown keys with a warning, so `allow_bypass:` (the real key is `allow_bypass_env`) or `version:` (the real key is `schema_version`) silently do nothing. `tirith policy effective` prints the fully resolved policy with defaults filled in.

To test a candidate policy without touching the live file, point `TIRITH_POLICY_ROOT` at a directory holding `.tirith/policy.yaml` and run `tirith policy test` with it set.

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

For client work that needs stricter rules than the global config, drop a `.tirith/policy.yaml` at the project root. Tirith walks up from the current directory and uses the first match. A repo-scoped policy is **tightening-only**: weakening fields such as `allowlist` are ignored with a notice, so a cloned repo cannot loosen your protection. Loosen at user scope (global policy or `tirith trust add --scope user`). `tirith policy effective` shows which fields were neutralized.

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
