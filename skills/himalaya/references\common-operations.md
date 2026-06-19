# Common Operations — Himalaya + Pipeline

## Quick Commands

```bash
# List accounts
himalaya account list

# Search envelopes (metadata only, fast)
himalaya envelope list -a ericmathewhill -f '[Gmail]/All Mail' -o json "from tldr"
himalaya envelope list -a emhill96 -f '[Gmail]/All Mail' -o json "from amazon has:attachment"

# Read full message
himalaya message read -a ericmathewhill -f '[Gmail]/All Mail' <message-id>

# Account status
himalaya account status -a ericmathewhill
```

## Pipeline Operations

```bash
# Fetch + compress only (save engram)
python D:/pub/scripts/himalaya_pipeline.py --account ericmathewhill --queries "from tldr" --output D:/pub/engram_tldr.json

# Fetch + compress + push to Swarm
python D:/pub/scripts/himalaya_pipeline.py --account ericmathewhill --queries "from tldr" --push-swarm --prompt "Analyze for AI agent landscape"

# Multi-query (comma-separated)
python D:/pub/scripts/himalaya_pipeline.py --account ericmathewhill --queries "from foia,from nsa,from amazon,has:attachment" --push-swarm

# Both accounts
for acc in emhill96 ericmathewhill; do
  python D:/pub/scripts/himalaya_pipeline.py --account $acc --queries "from foia,from amazon" --push-swarm
done
```

## Swarm Orchestrator

```bash
# Health check
curl -s http://localhost:8003/health | jq

# Orchestrate manually
curl -s -X POST http://localhost:8003/api/orchestrate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Test prompt", "custom_context": "{\"test\": \"data\"}"}' | jq

# View recent logs
curl -s http://localhost:8003/api/swarm/logs | jq '.[0]'
```

## PowerShell Wrappers

```powershell
# Search
.\search_emails.ps1 -account ericmathewhill -query "from tldr"

# Read message
.\read_email.ps1 -account ericmathewhill -id <msg-id> -folder "[Gmail]/All Mail"
```

## Akashic Compressor Standalone

```bash
# Compress text file
python D:/pub/scripts/ouroboros_akashic_compressor.py D:/pub/some_text.txt

# Compress Python file (code mode)
python D:/pub/scripts/ouroboros_akashic_compressor.py D:/pub/scripts/himalaya_pipeline.py

# Self-test
python D:/pub/scripts/ouroboros_akashic_compressor.py
```

## Database Queries

```bash
# Swarm logs
sqlite3 D:/pub/golem_diary.db "SELECT id, timestamp, signature, efficiency FROM golem_swarm_logs ORDER BY id DESC LIMIT 10;"

# Memories
sqlite3 D:/pub/golem_diary.db "SELECT timestamp, content FROM memories WHERE type='Swarm Consensus' ORDER BY timestamp DESC LIMIT 5;"
```

## Known Issues

| Issue | Workaround |
|-------|------------|
| Negative efficiency (compressed > original) | Email prose has high filler; tune `_linguistic_entropy_filter` in AkashicCompressor |
| Swarm returns 500 but processes | Check logs: `curl localhost:8003/api/swarm/logs` — often succeeds despite HTTP 500 |
| PowerShell bracket parsing | Wrap folder in single quotes: `-f '[Gmail]/All Mail'` |
| SQLite locked (concurrent runs) | Pipeline uses timeout=30; serialize cron runs |
| Himalaya auth failure | Re-run `himalaya account add` with fresh App Password |