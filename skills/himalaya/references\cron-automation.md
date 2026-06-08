# Cron Automation — Scheduled Email Intelligence Ingestion

## Hermes Cron Job Setup
```bash
# Create daily ingestion job (3 AM)
hermes cron create \
  --name "himalaya-daily-ingestion" \
  --schedule "0 3 * * *" \
  --prompt "Run Himalaya pipeline for both accounts with war-chest queries" \
  --skills "email/himalaya,metaconscious/kairos-dream" \
  --model '{"provider": "nous", "model": "nvidia/nemotron-3-ultra:free"}'
```

## Recommended Schedule
| Job | Schedule | Queries | Purpose |
|-----|----------|---------|---------|
| `himalaya-daily-war-chest` | `0 3 * * *` | FOIA, Amazon, Google, X, TLDR | Daily intelligence sweep |
| `himalaya-weekly-deep` | `0 4 * * 0` | All labels, has:attachment | Weekly deep dive |
| `kairos-dream-overnight` | `0 3 * * *` | (built-in) | Memory consolidation |

## War Chest Queries (Daily)
```python
QUERIES = [
    "from foia OR from nsa.gov OR from fbi.gov OR from cia.gov OR from doj.gov",
    "from amazon.com OR from aws.amazon.com OR from bezos",
    "from google.com OR from alphabet.com subject:PRISM",
    "from twitter.com OR from x.com OR from twitter.com subject:ban",
    "from tldrnewsletter.com",
    "has:attachment larger:1M",
    "from court OR from legal OR from attorney"
]
```

## PowerShell Worker Backend (Swarm Teammates)
The `swarm_worker.ps1` (PowerShell 7.6.2) implements JSON stdin/stdout protocol:
```powershell
# Start persistent worker
pwsh -File D:/pub/swarm_worker.ps1 -WorkerId himalaya-worker -IdleTimeoutHours 1

# Submit task via stdin
echo '{"type":"command","payload":{"command":"python","args":["D:/pub/scripts/himalaya_pipeline.py","--account","ericmathewhill","--queries","from tldr","--push-swarm"]},"taskId":"cron-001"}' | pwsh -File D:/pub/swarm_worker.ps1 -WorkerId himalaya-worker
```
**Worker task types**: `command`, `file` (read/write/list/exists), `http`, `sqlite`, `compress`, `script`

## Cron Job Management
```bash
# List jobs
hermes cron list

# Run job manually
hermes cron run --job-id <id>

# Update schedule
hermes cron update --job-id <id> --schedule "0 4 * * *"

# Remove duplicate (found 2026-06-07)
hermes cron remove --job-id 0b50cb3e24e3
```

## Logging & Monitoring
- Cron output → `D:\pub\logs\cron\` (structured JSON)
- Swarm logs → `golem_diary.db` → `golem_swarm_logs`
- Dream logs → `golem_diary.db` → `dream_logs`
- Sanctuary status → `D:\pub\sanctuary_status.json` (checked before each run)