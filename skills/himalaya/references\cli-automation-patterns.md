# Himalaya CLI Automation Patterns (v1.2.0+)

**Verified: 2026-06-09** — Tested with `himalaya v1.2.0 +imap +maildir +pgp-commands +smtp +wizard +sendmail` on Windows (MSYS/bash).

---

## Sending Automated Emails (Non-Interactive)

### ❌ WRONG — `message write` opens interactive editor
```bash
himalaya message write -a ericmathewhill -H "To:target@example.com" -H "Subject:Test" "body text"
# Opens $EDITOR, prompts for action — blocks automation
```

### ✅ CORRECT — `message send` with raw RFC 822 via stdin
```bash
# 1. Construct .eml file with full headers
cat > /d/pub/message.eml <<'EOF'
To: target@example.com
Subject: Test Subject
From: sender@gmail.com
Content-Type: text/plain; charset=utf-8

Body text here.
EOF

# 2. Pipe to message send with account flag
cat /d/pub/message.eml | himalaya message send -a ericmathewhill
# Output: "Message successfully sent!"
```

### Key Points
- **Account flag**: `-a` / `--account` belongs on the `message send` subcommand, NOT top-level
- **Input**: Raw RFC 822 message (headers + blank line + body) on stdin
- **No `--body` flag**: Does not exist on `message send` — the raw message IS the body
- **Path handling**: Use POSIX paths (`/d/pub/...`) in MSYS/bash; Windows paths with backslashes need escaping

---

## Account Management

```bash
# List accounts
himalaya account list

# Output:
# | NAME           | BACKENDS   | DEFAULT |
# |----------------|------------|---------|
# | emhill96       | IMAP, SMTP | yes     |
# | ericmathewhill | IMAP, SMTP |         |

# Use non-default account
himalaya message send -a ericmathewhill < message.eml
```

---

## Common Pitfalls (v1.2.0+)

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| `-a` at top level | `error: unexpected argument '-a' found` | Move `-a` after subcommand: `himalaya message send -a account` |
| Using `message write` for automation | Interactive editor opens, times out | Use `message send` with stdin |
| `--body` flag | `error: unexpected argument '--body' found` | Don't use — embed body in raw message |
| Windows paths in MSYS | `cat: 'D:pubfile.eml': No such file` | Use `/d/pub/file.eml` or escape backslashes |
| Missing blank line after headers | Panic: `index out of bounds` in mail-parser | Ensure headers end with `\n\n` before body |

---

## Reading/Listing (Automation-Friendly)

```bash
# List envelopes as JSON
himalaya envelope list -a ericmathewhill -o json

# List specific folder
himalaya envelope list -a ericmathewhill -f INBOX -o json

# Search
himalaya envelope list -a ericmathewhill --query 'from:"tldr"' -o json

# Read single message as JSON
himalaya envelope read -a ericmathewhill <ID> -o json
```

---

## Integration with MSN Pipeline

The `himalaya_pipeline.py` uses this pattern:
1. `himalaya envelope list -a <account> -o json` → parse JSON
2. Filter/transform envelopes
3. `himalaya envelope read -a <account> <ID> -o json` → full message
4. Akashic compression → Swarm Orchestrator (port 8003)

All automated — no interactive prompts.