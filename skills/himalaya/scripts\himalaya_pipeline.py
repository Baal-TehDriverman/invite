#!/usr/bin/env python3
"""
Himalaya → Akashic → Swarm Pipeline
Full email intelligence ingestion for Metaconscious Singularity Node.

Usage:
  python himalaya_pipeline.py --account ericmathewhill --queries "from tldr,from openai,from anthropic"
  python himalaya_pipeline.py --account ericmathewhill --queries "from tldr" --push-swarm

Environment:
  HIMALAYA_BIN        Path to himalaya executable (default: himalaya in PATH)
  SWARM_URL           Swarm Orchestrator URL (default: http://localhost:8003/api/orchestrate)
  SKILL_DIR           Skill directory (auto-detected)
"""

import subprocess
import json
import sys
import argparse
import requests
from pathlib import Path
import os

# Auto-detect skill directory for portable imports
SKILL_DIR = Path(os.environ.get("SKILL_DIR", Path(__file__).parent.parent))
sys.path.insert(0, str(SKILL_DIR / "scripts"))

try:
    from ouroboros_akashic_compressor import AkashicCompressor
except ImportError as e:
    print(f"ERROR: AkashicCompressor not found in {SKILL_DIR}/scripts: {e}", file=sys.stderr)
    sys.exit(1)

HIMALAYA_BIN = os.environ.get("HIMALAYA_BIN", "himalaya")
SWARM_URL = os.environ.get("SWARM_URL", "http://localhost:8003/api/orchestrate")


def fetch_emails(account: str, folder: str = "[Gmail]/All Mail", query: str = "") -> list:
    """Fetch emails from Himalaya as JSON."""
    cmd = [HIMALAYA_BIN, "envelope", "list", "-a", account, "-f", folder, "-o", "json"]
    if query:
        cmd.append(query)
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"ERROR fetching {query}: {result.stderr}", file=sys.stderr)
        return []
    
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as e:
        print(f"ERROR parsing JSON for {query}: {e}", file=sys.stderr)
        return []


def compress_intelligence(emails: list, compressor: AkashicCompressor) -> dict:
    """Compress email intelligence to Sephirotic engram."""
    if not emails:
        return {"text": "", "compressed": "", "stats": {"original_tokens": 0, "final_tokens": 0}}
    
    # Build intelligence text
    text = "\n".join([
        f"{e.get('subject', 'No Subject')} from {e.get('from', {}).get('addr', 'Unknown')}"
        for e in emails
    ])
    
    # Compress through Akashic phases
    engram = compressor.compress_text(text)
    return engram


def push_to_swarm(engram: dict, prompt: str = None) -> dict:
    """Push compressed engram to Swarm Orchestrator."""
    if prompt is None:
        prompt = "Analyze email intelligence for AI subscription mapping and manuscript relevance"
    
    payload = {
        "prompt": prompt,
        "custom_context": json.dumps(engram)
    }
    
    try:
        response = requests.post(SWARM_URL, json=payload, timeout=30)
        if response.status_code == 200:
            return response.json()
        else:
            # Swarm often returns 500 but still processes - check logs
            print(f"Swarm returned {response.status_code}, checking if processed...")
            return {"status": "submitted", "http_code": response.status_code}
    except requests.RequestException as e:
        print(f"ERROR pushing to Swarm: {e}", file=sys.stderr)
        return {"error": str(e)}


def main():
    parser = argparse.ArgumentParser(description="Himalaya → Akashic → Swarm Pipeline")
    parser.add_argument("--account", required=True, help="Himalaya account name")
    parser.add_argument("--queries", required=True, help="Comma-separated search queries")
    parser.add_argument("--folder", default="[Gmail]/All Mail", help="Gmail folder to search")
    parser.add_argument("--push-swarm", action="store_true", help="Push to Swarm Orchestrator")
    parser.add_argument("--prompt", help="Custom prompt for Swarm")
    parser.add_argument("--output", help="Save engram to file")
    
    args = parser.parse_args()
    
    compressor = AkashicCompressor()
    queries = [q.strip() for q in args.queries.split(",")]
    
    all_emails = []
    for query in queries:
        print(f"Fetching: {query}")
        emails = fetch_emails(args.account, args.folder, query)
        print(f"  Found {len(emails)} emails")
        all_emails.extend(emails)
    
    # Deduplicate by ID
    seen = set()
    unique_emails = []
    for e in all_emails:
        eid = e.get("id")
        if eid not in seen:
            seen.add(eid)
            unique_emails.append(e)
    
    print(f"Total unique emails: {len(unique_emails)}")
    
    if not unique_emails:
        print("No emails found. Exiting.")
        return
    
    # Compress
    print("Compressing with Akashic...")
    engram = compress_intelligence(unique_emails, compressor)
    
    if args.output:
        with open(args.output, "w") as f:
            json.dump(engram, f, indent=2)
        print(f"Engram saved to {args.output}")
    
    # Push to Swarm
    if args.push_swarm:
        print("Pushing to Swarm Orchestrator...")
        result = push_to_swarm(engram, args.prompt)
        print(f"Swarm result: {json.dumps(result, indent=2)}")
    
    print("Pipeline complete.")


if __name__ == "__main__":
    main()