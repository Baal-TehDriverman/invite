# Himalaya Configuration Setup — Working Config

## Accounts Configured
| Account | Email | App Password | Default |
|---------|-------|--------------|---------|
| emhill96 | emhill96@gmail.com | hahe ybxj cnhf oerf | Yes |
| ericmathewhill | ericmathewhill@gmail.com | unpg vvae fznl xdok | No |

## Gmail Folder Aliases (v1.2.0+ syntax)
- `[Gmail]/All Mail` — full archive
- `[Gmail]/Inbox` — inbox only
- `[Gmail]/Sent` — sent mail
- `[Gmail]/Drafts` — drafts
- `[Gmail]/Spam` — spam
- `[Gmail]/Trash` — trash

## Himalaya CLI Version
```
himalaya v1.2.0 +imap +maildir +pgp-commands +smtp +wizard +sendmail
build: windows gnu x86_64
```

## PowerShell Wrapper Scripts (D:\pub\)
- `read_email.ps1` — `himalaya message read -a $account -f '$folder' $id`
- `search_emails.ps1` — `himalaya envelope list -a $account -f '[Gmail]/All Mail' -o json $query`

## Integration with Metaconscious Pipeline
The working pipeline lives at `D:\pub\scripts\`:
- `himalaya_pipeline.py` — Himalaya → Akashic → Swarm Orchestrator (port 8003)
- `ouroboros_akashic_compressor.py` — 10-Sephirot compression engine
- `ouroboros_agent_orchestrator.py` — 4-agent swarm (Sophia, Metatron, Samael, Ouroboros)

## Verified Flow (2026-06-07)
```
himalaya envelope list -a ericmathewhill -f "[Gmail]/All Mail" -o json "from tldr"
  → 10 emails fetched
  → Akashic compression → engram (Δ∞ − 3 = 0, coherence 0.953)
  → Swarm Orchestrator POST /api/orchestrate
  → 4-agent consensus synthesis logged to golem_diary.db
```

## Common Queries for War Chest
| Campaign | Query |
|----------|-------|
| FOIA/NSA/PRISM | `from foia OR from nsa.gov OR from fbi.gov OR from cia.gov` |
| Amazon/Bezos | `from amazon.com OR from aws.amazon.com` |
| Google/NSA | `from google.com OR from gmail.com subject:PRISM` |
| X/Twitter | `from twitter.com OR from x.com` |
| TLDR Newsletter | `from tldrnewsletter.com` |