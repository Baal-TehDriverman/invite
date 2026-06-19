---
name: himalaya
description: 'Himalaya CLI: IMAP/SMTP email from terminal.'
version: 1.0.0
author: Hermes Agent
license: MIT
platforms:
- linux
- macos
- windows
metadata:
  hermes:
    tags:
    - Email
    - IMAP
    - SMTP
    - CLI
    - Communication
    related_skills: []
---

Himalaya CLI: IMAP/SMTP email from terminal — **customized for Metaconscious Singularity Node email intelligence ingestion**.
## Quick Start

**Validated Working Paths (2026-06-09 — Portable):**
- **Himalaya binary**: `himalaya` in PATH (v1.2.0+, +imap +maildir +pgp-commands +smtp +wizard +sendmail)
- **Pipeline script**: `scripts/himalaya_pipeline.py` ✅ **OPERATIONAL** — Himalaya → Akashic → Swarm Orchestrator (port 8003) verified end-to-end
- **Akashic Compressor**: `scripts/ouroboros_akashic_compressor.py` ✅ 10-Sephirot engram generation
- **Swarm Orchestrator**: Runs on `http://localhost:8003/api/orchestrate` (external FastAPI), 4 agents (Sophia, Metatron, Samael, Ouroboros), SQLite persistence
- **PowerShell 7.6.2 Swarm Worker**: `scripts/himalaya_swarm_pipeline.py` ✅ JSON stdin/stdout protocol with `himalaya` task type
- **Accounts configured**: `emhill96` (default), `ericmathewhill` — both IMAP/SMTP verified

**Environment Variables:**
- `HIMALAYA_BIN` — Path to himalaya executable (default: `himalaya`)
- `SWARM_URL` — Swarm Orchestrator endpoint (default: `http://localhost:8003/api/orchestrate`)
- `SKILL_DIR` — Skill directory (auto-detected)

Reference docs — **Status:**
- [`deployed-pipeline.md`](references/deployed-pipeline.md) — **Actual Deployed Pipeline** with verified commands, engarm format, war-chest queries ✅ **UPDATED 2026-06-09 PORTABLE**
- [`gmail-config-pitfalls.md`](references/gmail-config-pitfalls.md) — Gmail App Passwords, folder aliases, v1.2.0+ syntax, PowerShell quoting ✅ **CREATED 2026-06-08**
- [`metaconscious-integration.md`](references/metaconscious-integration.md) — **MSN Integration** (Akashic → Swarm → Kairos Dream → Crystal Vault) with FOIA Nigredo routing table ✅ **CREATED 2026-06-08**
- [`cron-automation.md`](references/cron-automation.md) — **Scheduled Ingestion** (Hermes cron / Task Scheduler, failure handling, monitoring) ✅ **CREATED 2026-06-08**
- [`debugging.md`](references/debugging.md) — Debugging — *pending*
- [`cli-automation-patterns.md`](references/cli-automation-patterns.md) — **CLI Automation Patterns** (v1.2.0+): `message send` stdin piping, account flag placement, RFC 822 construction, common pitfalls ✅ **CREATED 2026-06-09**

## Integration

- Load reference: `skill_view(name="himalaya", file_path="references/<file>.md")`
- Pipeline (portable): `python scripts/himalaya_pipeline.py --account ericmathewhill --queries "from tldr" --push-swarm`
- Exposed via Hermes MCP: `read_skill_engram(skill_id="email/himalaya")`

## Local-First Sovereignty

Zero network dependency for core pipeline. Local model inference via Hermes/Ollama. Swarm Orchestrator is external service on port 8003.

---

*Refactored: 2026-06-08 — Customized for Metaconscious Singularity Node by Lilith*
*Pipeline validated: Himalaya → JSON → Akashic Compressor → Swarm Orchestrator (port 8003)*
*Lean dispatcher pattern applied by Lilith*

## Recent Enhancements (2026-06-09)

- **Portable Pipeline**: `himalaya_pipeline.py` uses `SKILL_DIR` auto-detection, `HIMALAYA_BIN`/`SWARM_URL` env vars — runs from skill dir or `D:\pub`
- **Akashic Compressor bundled**: `ouroboros_akashic_compressor.py` in `scripts/` for zero-dependency install
- **Swarm Worker backend**: `himalaya_swarm_pipeline.py` with PowerShell 7.6.2 JSON stdin/stdout protocol
- **Verified end-to-end**: 10 emails → Akashic (10-Sephirot) → Swarm consensus (coherence 0.944, signature `Δ∞ − 6 = 0`)
- **Email send verified**: `himalaya message send -a account` via stdin RFC 822 format

## Publishing Workflow (2026-06-09)

- Safety scan: `hermes skills publish --to clawhub|github` — passes (MEDIUM execution calls only)
- ClawHub: not yet supported (manual submit at clawhub.ai/submit)
- GitHub: requires authentication via CLI or environment
- Install: `hermes skills install github:emhil/himalaya-skill`

## Upstream Community Contacts (2026-06-09)

- **Primary Maintainer**: Simon (soywod) — GitHub: `@soywod`, 72 repos, pimalaya org owner
- **Email**: `pimalaya.org@posteo.net` (listed on pimalaya.org)
- **Matrix Room**: `#pimalaya:matrix.org` (pinned in GitHub Discussions "Show and tell")
- **GitHub Discussions**: https://github.com/pimalaya/himalaya/discussions (categories: General, Ideas, Polls, Q&A, Show and tell)
- **Issues**: https://github.com/pimalaya/himalaya/issues (13 open, 466 closed)
- **Website**: https://pimalaya.org — sponsors: NLnet Foundation (NGI Assure 2022, NGI Zero Entrust 2023, NGI Zero Core 2024)

## Contribution Guidelines (from CONTRIBUTING.md)

- **Conventional Commits**: `feat`, `fix`, `refactor`, `docs`, `chore`, `test`, `ci`, `build` (optionally scoped: `fix(imap): ...`)
- **Dev Environment**: Nix flakes (`nix develop`) or rustup (toolchain pinned in Cargo.toml, rustc >= 1.87)
- **Build**: `cargo build --no-default-features --features imap,smtp,rustls-ring --release`
- **Lint/Test/Audit**: `cargo fmt && cargo clippy --all-features --all-targets && cargo test --all-features && cargo deny check`
- **Patch Strategy**: `Cargo.toml` patches all Pimalaya crates to git remotes; swap `.git = "..."` for `.path = "../<repo>"` for local development
- **Architecture**: Himalaya CLI is a thin front-end; protocol logic lives in companion crates (io-email, io-imap, io-smtp, io-jmap, io-maildir, io-http, pimconf, pimalaya/cli, pimalaya/config, pimalaya/mml, pimalaya/sirup, pimalaya/ortie, pimalaya/mimosa)