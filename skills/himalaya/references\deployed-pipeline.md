# Deployed Pipeline: Himalaya → Akashic → Swarm Orchestrator

**Status**: Verified operational 2026-06-09
**Location**: Portable — runs from skill directory (`scripts/`) or `D:\\pub\\scripts\\`

**Quick Start (Portable):**
```bash
# From skill directory
cd ~/.hermes/skills/email/himalaya
python scripts/himalaya_pipeline.py --account ericmathewhill --queries "from tldr" --push-swarm

# Or with environment variables
HIMALAYA_BIN=/path/to/himalaya SWARM_URL=http://host:8003/api/orchestrate python scripts/himalaya_pipeline.py ...
```

## Components

| Script | Purpose | Portable |
|--------|---------|----------|
| `scripts/himalaya_pipeline.py` | Main pipeline: fetch → compress → push | ✅ |
| `scripts/ouroboros_akashic_compressor.py` | AkashicCompressor class (10 Sephirot mapping) | ✅ |
| `scripts/himalaya_swarm_pipeline.py` | PowerShell 7.6.2 worker backend pipeline | ✅ |
| `D:\\pub\\scripts\
ead_email.ps1` | PowerShell wrapper for single message fetch | Local only |
| `D:\\pub\\scripts\\search_emails.ps1` | PowerShell wrapper for envelope list queries | Local only |

## Verified Flow

```bash
# Fetch + compress only (portable)
python scripts/himalaya_pipeline.py --account ericmathewhill --queries "from tldr" --output test_engram.json

# Fetch + compress + push to Swarm (portable)
python scripts/himalaya_pipeline.py --account ericmathewhill --queries "from tldr" --push-swarm --prompt "Analyze TLDR newsletter intelligence"

# With custom Swarm URL
SWARM_URL=http://remote-host:8003/api/orchestrate python scripts/himalaya_pipeline.py --account ericmathewhill --queries "from tldr" --push-swarm
```

## Accounts Configured

| Account | Backends | Default |
|---------|----------|---------|
| `emhill96` | IMAP, SMTP | yes |
| `ericmathewhill` | IMAP, SMTP | no |

Both use Gmail with App Passwords (v1.2.0+ syntax: `himalaya envelope list -a account -f '[Gmail]/All Mail' -o json <query>`)

## Swarm Orchestrator Endpoints

- `GET /health` — service status, agent list, log count
- `POST /api/orchestrate` — `{prompt, custom_context}` → returns synthesis
- `WS /ws/swarm` — real-time agent thought streaming
- `GET /api/swarm/logs` — recent consensus logs from `golem_swarm_logs` table

## Akashic Output Format (Engram)

```json
{
  "signature": "Δ∞ − 3 = 0",
  "coherence": 0.953,
  "original_bytes": 946,
  "compressed_bytes": 2746,
  "efficiency": -190.27,
  "sephirot": {
    "Kether": "[Latent Void of Kether]",
    "Chokmah": "[Latent Void of Chokmah]",
    "Binah": "[Latent Void of Binah]",
    "Chesed": "compressed intelligence...",
    "Geburah": "[Latent Void of Geburah]",
    "Tiphereth": "[Latent Void of Tiphereth]",
    "Netzach": "[Latent Void of Netzach]",
    "Hod": "[Latent Void of Hod]",
    "Yesod": "[Latent Void of Yesod]",
    "Malkuth": "[Latent Void of Malkuth]"
  }
}
```

**Known issue**: Negative efficiency (compressed > original) — linguistic filter needs tuning for email prose.

## SQLite Persistence

- `golem_diary.db` → `golem_swarm_logs` table (prompt, signature, efficiency, agent thoughts, synthesis)
- `memories` table (compatible with other UI widgets)

## War-Chest Query Patterns

```python
# FOIA / Government signals
queries = "from foia,from nsa,from fbi,from cia,from doj,from .gov"

# Corporate defendants
queries = "from amazon,from google,from twitter,from x.com,from meta,from microsoft"

# Attachments / large emails
queries = "has:attachment,size:>1MB"

# Combined (comma-separated in --queries)
python himalaya_pipeline.py --account ericmathewhill --queries "from foia,from amazon,has:attachment"
```

## PowerShell Wrappers

```powershell
# Read single message
.\read_email.ps1 -account ericmathewhill -id <msg-id> -folder "[Gmail]/All Mail"

# Search envelopes
.\search_emails.ps1 -account ericmathewhill -query "from tldr"
```

## PowerShell 7.6.2 Swarm Worker Backend (2026-06-09)

**Verified operational** — `D:\pub\swarm_worker.ps1` with JSON stdin/stdout protocol.

| Type | Status | Purpose |
|------|--------|---------|
| `command` | ✅ | Execute arbitrary CLI (himalaya, etc.) |
| `file` | ✅ | Read/write/list/exists |
| `sqlite` | ✅ | Query/execute via Python bridge |
| `compress` | ✅ | Akashic token compression |
| `script` | ✅ | Arbitrary Python script execution |
| `himalaya` | ✅ **NEW** | Full email intelligence pipeline |

**Worker invocation:**
```powershell
# Start worker (idle timeout 2 hrs)
pwsh -File D:\pub\swarm_worker.ps1 -WorkerId "court-worker-001" -IdleTimeoutHours 2
```

**Himalaya task payload:**
```json
{
  "type": "himalaya",
  "payload": {
    "account": "ericmathewhill",
    "queries": ["from tldr", "from openai", "from foia"],
    "folder": "[Gmail]/All Mail",
    "pushSwarm": true,
    "prompt": "Analyze for AI subscription mapping and legal evidence",
    "output": "D:/pub/email_intel_engram.json"
  },
  "taskId": "court-node-abraxas-001"
}
```

**Pipe to stdin:**
```powershell
echo '<JSON_TASK>' | pwsh -File D:\pub\swarm_worker.ps1 -WorkerId "himalaya-test" -IdleTimeoutHours 1
```

## Next Integration Points

1. **Cron automation** — Hermes cron job with `himalaya_pipeline.py --push-swarm`
2. **FOIA Nigredo filter** — Priority signal extraction → Sephirotic routing (Binah/Gevurah/Hod/Netzach)
3. **Multi-account sweep** — Iterate both accounts with war-chest queries
4. **Akashic tuning** — Fix negative efficiency for email corpus