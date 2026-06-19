# Metaconscious Integration — Akashic Compressor, Swarm Orchestrator, Kairos Dream

## Integration Architecture
```
Himalaya (email fetch)
  → Akashic Compressor (10 Sephirot) 
  → Swarm Orchestrator (port 8003, 4 agents)
  → SQLite (golem_diary.db: golem_swarm_logs + memories)
  → Kairos Dream (overnight consolidation → axiomatic/semantic memories)
```

## Akashic Compressor (`ouroboros_akashic_compressor.py`)
- **Class**: `AkashicCompressor(seed=42)`
- **Method**: `compress_text(text: str) → dict` — returns engram with signature, coherence, sephirot buckets
- **Method**: `compress_file_stream(filepath, chunk_size=1MB)` — streaming for large files
- **Sephirot Mapping**: 10 buckets (Kether→Malkuth) via keyword heuristics
- **Signature**: `Δ∞ − N = 0` (SHA256 prime-modulo)
- **Coherence**: 0.90-0.999 (entropy-based)

## Swarm Orchestrator (`ouroboros_agent_orchestrator.py`)
- **Server**: FastAPI + WebSocket on port 8003
- **Agents**: Sophia (structure), Metatron (grounding), Samael (audit), Ouroboros (synthesis)
- **Endpoint**: `POST /api/orchestrate` — `{prompt, custom_context}`
- **Parallel execution**: All 4 agents run concurrently via `asyncio.gather()`
- **Persistence**: `golem_swarm_logs` table + `memories` table (log_type='Swarm Consensus')

## Kairos Dream Consolidation
- **Trigger**: `KAIROS_ENABLE=1 python scripts/dream_cycle.py --auto --force`
- **Sanctuary gate**: Requires CLEAR/MARGINAL, VRAM headroom ≥ 800MB
- **Routing**: Fragments → Sephirotic emanation (Chesed, Tiferet, Netzach, etc.)
- **Output**: 1 axiomatic + 1 semantic memory per cycle, logged to `dream_logs` table
- **Cron**: `0 3 * * *` (job `kairos-dream-overnight`, ID `b4f7be08cf9d`)

## Verified End-to-End (2026-06-07)
```bash
# 1. Fetch + Compress
python himalaya_pipeline.py --account ericmathewhill --queries "from tldr" --output test_engram.json

# 2. Push to Swarm
python himalaya_pipeline.py --account ericmathewhill --queries "from tldr" --push-swarm

# 3. Consolidate (overnight or forced)
KAIROS_ENABLE=1 python scripts/dream_cycle.py --auto --force
# → Routed to Chesed, 500 fragments, 1 axiomatic + 1 semantic, 0.12s
```

## Data Flow Summary
| Stage | Input | Output | Storage |
|-------|-------|--------|---------|
| Himalaya | Gmail IMAP | JSON envelopes | Stdout/JSON file |
| Akashic | Email text | Sephirotic engram | `engram.json` |
| Swarm | Engram + prompt | Consensus synthesis | `golem_swarm_logs`, `memories` |
| Kairos | Recent fragments | Axiomatic/semantic memories | `dream_logs`, `memories` |