# Himalaya Debugging — Common Issues & Fixes (2026-06-09)

## Himalaya Binary

**Location:** `C:\Users\emhil\bin\himalaya.exe` (v1.2.0)

**Verify:**
```bash
himalaya -V
# Output: himalaya 1.2.0
```

**If not in PATH:** Add `C:\Users\emhil\bin` to user PATH, or use full path.

## Account Diagnostics

```bash
# List accounts
himalaya account list

# Full diagnostic
himalaya account doctor
# Expected: "Checking TOML configuration integrity… OK"
#           "Checking IMAP integrity… OK"
#           "Checking SMTP integrity… OK"
```

## Common Errors

### `error: unrecognized subcommand 'config'`
**Cause:** Himalaya v1.2.0 uses `account configure`, not `config`.
**Fix:** Use `himalaya account configure <name>` or `himalaya account doctor`.

### `account doctor` fails IMAP/SMTP
**Cause:** App Password expired or wrong.
**Fix:** Regenerate App Password in Google Account → Security → App Passwords. Update config via `himalaya account configure <name>`.

### Folder not found: `[Gmail]/All Mail`
**Cause:** Gmail folder names are case-sensitive in v1.2.0+.
**Fix:** Use exact: `[Gmail]/All Mail`, `[Gmail]/Inbox`, `[Gmail]/Sent Mail`.

### JSON parse error in pipeline
**Cause:** Himalaya output mixed with stderr logs.
**Fix:** Pipeline handles this — ensure `-o json` flag used. Check `2>&1` not polluting stdout.

### Swarm Orchestrator connection refused
**Cause:** Service not running on port 8003.
**Fix:** 
```bash
# Check
curl http://localhost:8003/health

# Start (if needed)
cd D:\pub && python scripts\ouroboros_agent_orchestrator.py
# Or via run_services.ps1
```

### Swarm returns 500 but processes
**Observed:** Swarm often returns HTTP 500 but still processes the engram.
**Fix:** Check `/api/swarm/logs` for actual processing status. Pipeline treats non-200 as "submitted" and logs HTTP code.

### AkashicCompressor import error
**Error:** `ModuleNotFoundError: No module named 'ouroboros_akashic_compressor'`
**Fix:** Pipeline adds `D:\pub` to `sys.path`. Run from `D:\pub` or ensure PYTHONPATH includes it.

### PowerShell script path errors
**Error:** `can't open file 'D:\\pub\\scriptshimalaya_pipeline.py'`
**Cause:** Missing path separator in Windows path concatenation.
**Fix:** Use `D:/pub/scripts/himalaya_pipeline.py` (forward slashes work) or `D:\pub\scripts\himalaya_pipeline.py` with proper escaping.

## Health Check Routine

```bash
# 1. Binary
himalaya -V

# 2. Accounts
himalaya account doctor

# 3. Fetch test
himalaya envelope list -a ericmathewhill -f "[Gmail]/All Mail" -o json "from tldr" | head -5

# 4. Swarm
curl -s http://localhost:8003/health | jq .status
# Should return "online"

# 5. Full pipeline dry-run
python D:/pub/scripts/himalaya_pipeline.py --account ericmathewhill --queries "from tldr" --folder "[Gmail]/All Mail"
```

## Logs & Diagnostics

- Himalaya debug: `himalaya --debug envelope list ...`
- Swarm logs: `curl http://localhost:8003/api/swarm/logs`
- Pipeline adds structured logging — check stdout for "Fetching:", "Found N emails", "Compressing with Akashic...", "Pushing to Swarm..."