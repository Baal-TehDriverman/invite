# Gmail Config Pitfalls — v1.2.0+ Syntax & Gotchas

## Folder Syntax (Critical)
**Wrong**: `INBOX`, `[Gmail]/Inbox` (without quotes in PowerShell)  
**Correct**: `'[Gmail]/All Mail'` — single quotes required in PowerShell, square brackets literal

## App Passwords
- 16-char format: `xxxx yyyy zzzz wwww` (spaces ignored by Himalaya)
- Must enable 2FA on Google account first
- One App Password per account per device/app

## v1.2.0+ Changes
- `envelope list` replaces `message list` for metadata-only fetches
- `-o json` flag for machine-readable output
- `-f` folder flag required (no default)
- Account `-a` flag required (no default in scripts)

## PowerShell Escaping
```powershell
# Correct - single quotes around folder with brackets
himalaya envelope list -a ericmathewhill -f '[Gmail]/All Mail' -o json "from tldr"

# WRONG - double quotes eat the brackets
himalaya envelope list -a ericmathewhill -f "[Gmail]/All Mail" -o json "from tldr"
```

## Common Errors
| Error | Cause | Fix |
|-------|-------|-----|
| `folder not found` | Wrong folder syntax | Use `'[Gmail]/All Mail'` |
| `authentication failed` | Wrong app password | Regenerate in Google Account > Security > App Passwords |
| `account not found` | Account name mismatch | Run `himalaya account list` to verify exact name |
| `json decode error` | Output not JSON | Add `-o json` flag |

## Rate Limits
- Gmail IMAP: ~300 req/min per account
- Himalaya batches naturally; no client-side throttling needed
- For bulk: add `sleep 1` between queries in scripts