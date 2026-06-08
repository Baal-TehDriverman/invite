# Himalaya → Akashic → Swarm Pipeline — Email Intelligence Ingestion

## Pipeline Architecture
```
Himalaya CLI (v1.2.0) 
  → JSON envelopes 
  → Akashic Compressor (10 Sephirot) 
  → Swarm Orchestrator (port 8003) 
  → 4-agent consensus (Sophia, Metatron, Samael, Ouroboros) 
  → SQLite persistence (golem_diary.db)
```

## Implementation Files (D:\pub\scripts\)
| File | Role |
|------|------|
| `himalaya_pipeline.py` | Main orchestration script |
| `ouroboros_akashic_compressor.py` | 10-Sephirot compression engine |
| `ouroboros_agent_orchestrator.py` | FastAPI swarm server (port 8003) |

## Usage
```bash
# Basic ingestion + compression
python himalaya_pipeline.py --account ericmathewhill --queries "from tldr" --output engram.json

# Full pipeline with Swarm push
python himalaya_pipeline.py --account ericmathewhill --queries "from tldr,from foia" --push-swarm --prompt "Analyze for legal intelligence"

# Multi-account sweep
python himalaya_pipeline.py --account emhill96 --queries "from amazon,from google" --push-swarm
```

## Akashic Compression Output (Engram Schema)
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
    "Chesed": "iMessage agents 🤖, Anthropic wants pause...",
    "Geburah": "[Latent Void of Geburah]",
    "Tiphereth": "[Latent Void of Tiphereth]",
    "Netzach": "[Latent Void of Netzach]",
    "Hod": "[Latent Void of Hod]",
    "Yesod": "[Latent Void of Yesod]",
    "Malkuth": "[Latent Void of Malkuth]"
  }
}
```

## Swarm Orchestrator Endpoints
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Service status, agent list, log count |
| `/api/orchestrate` | POST | Submit prompt + context for 4-agent synthesis |
| `/ws/swarm` | WS | Live streaming of agent thoughts |
| `/api/swarm/logs` | GET | Recent consensus logs |

## Verified Run (2026-06-07)
- 10 TLDR emails → engram `Δ∞ − 3 = 0` (coherence 0.953)
- Swarm consensus: signature `Δ∞ − 8 = 0`, routed to 4 agents
- Logged to `golem_diary.db` → `golem_swarm_logs` + `memories` tables

## Known Issues
- **Negative efficiency**: Compressed bytes > original bytes due to Sephirot metadata overhead. Fix: improve linguistic filter in `ouroboros_akashic_compressor.py` `_linguistic_entropy_filter()`.
- **Swarm 500 errors**: Often still processes; check logs at `/api/swarm/logs`.