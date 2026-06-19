#!/usr/bin/env python3
"""
Himalaya → Akashic → Swarm Pipeline (PowerShell 7.6.2 Backend)
Full email intelligence ingestion using the external swarm worker backend.
"""

import subprocess
import json
import sys
import argparse
import requests
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

PWSH_PATH = r"C:\Program Files\WindowsApps\Microsoft.PowerShell_7.6.2.0_x64__8wekyb3d8bbwe\pwsh.exe"
WORKER_SCRIPT = r"D:\pub\swarm_worker.ps1"
SWARM_ORCHESTRATOR = "http://localhost:8003/api/orchestrate"

class SwarmWorkerPool:
    """Manages a pool of PowerShell swarm workers for parallel task execution."""
    
    def __init__(self, worker_count=3):
        self.worker_count = worker_count
        self.workers = []
        self.start_workers()
    
    def start_workers(self):
        for i in range(self.worker_count):
            worker_id = f"worker-{i+1}"
            proc = subprocess.Popen(
                [PWSH_PATH, "-File", WORKER_SCRIPT, "-WorkerId", worker_id],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding='utf-8',
                bufsize=1
            )
            self.workers.append({
                'id': worker_id,
                'proc': proc,
                'lock': threading.Lock(),
                'busy': False
            })
            time.sleep(0.2)
    
    def get_available_worker(self):
        for w in self.workers:
            if not w['busy']:
                w['busy'] = True
                return w
        return None
    
    def release_worker(self, worker):
        worker['busy'] = False
    
    def execute_task(self, worker, task_type, payload, timeout=60):
        with worker['lock']:
            import time as time_module
            request = {
                "taskId": f"{worker['id']}-{task_type}-{int(time_module.time()*1000)}",
                "type": task_type,
                "payload": payload
            }
            request_json = json.dumps(request)
            worker['proc'].stdin.write(request_json + "\n")
            worker['proc'].stdin.flush()
            
            start = time_module.time()
            while time_module.time() - start < timeout:
                line = worker['proc'].stdout.readline()
                if line and "__RESULT__" in line:
                    result_json = line.split("__RESULT__")[1].strip()
                    return json.loads(result_json)
                elif line and "ERROR" in line.upper():
                    return {"error": line.strip(), "success": False}
            return {"error": "Timeout", "success": False}
    
    def shutdown_all(self):
        for w in self.workers:
            try:
                w['proc'].stdin.write("__SHUTDOWN__\n")
                w['proc'].stdin.flush()
                w['proc'].wait(timeout=5)
            except:
                w['proc'].kill()

def fetch_emails(account: str, folder: str, query: str) -> list:
    """Fetch emails from Himalaya as JSON."""
    cmd = ["himalaya", "envelope", "list", "-a", account, "-f", folder, "-o", "json"]
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

def compress_with_worker(worker_pool, text: str) -> dict:
    """Compress text using Akashic compressor via worker pool."""
    worker = worker_pool.get_available_worker()
    if not worker:
        return {"error": "No available workers", "success": False}
    
    try:
        result = worker_pool.execute_task(worker, "compress", {"text": text})
        return result
    finally:
        worker_pool.release_worker(worker)

def push_to_swarm(engram: dict, prompt: str | None = None) -> dict:
    """Push compressed engram to Swarm Orchestrator (port 8003)."""
    if prompt is None:
        prompt = "Analyze email intelligence for AI subscription mapping and manuscript relevance"
    
    payload = {
        "prompt": prompt,
        "custom_context": json.dumps(engram)
    }
    
    try:
        response = requests.post(SWARM_ORCHESTRATOR, json=payload, timeout=30)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Swarm returned {response.status_code}, checking if processed...")
            return {"status": "submitted", "http_code": response.status_code}
    except requests.RequestException as e:
        print(f"ERROR pushing to Swarm: {e}", file=sys.stderr)
        return {"error": str(e)}

def process_query_batch(worker_pool, account: str, folder: str, queries: list, push_swarm: bool, swarm_prompt: str) -> dict:
    """Process a batch of queries through the full pipeline."""
    
    all_emails = []
    for query in queries:
        print(f"Fetching: {query}")
        emails = fetch_emails(account, folder, query)
        print(f"  Found {len(emails)} emails")
        all_emails.extend(emails)
    
    seen = set()
    unique_emails = []
    for e in all_emails:
        eid = e.get("id")
        if eid not in seen:
            seen.add(eid)
            unique_emails.append(e)
    
    print(f"Total unique emails: {len(unique_emails)}")
    
    if not unique_emails:
        return {"status": "no_emails_found", "count": 0}
    
    text = "\n".join([
        f"{e.get('subject', 'No Subject')} from {e.get('from', {}).get('addr', 'Unknown')}"
        for e in unique_emails
    ])
    
    print("Compressing with Akashic (via swarm worker)...")
    compress_result = compress_with_worker(worker_pool, text)
    
    if not compress_result.get("success"):
        return {"status": "compression_failed", "error": compress_result.get("error")}
    
    engram_content = compress_result.get("content", "")
    
    if push_swarm and engram_content:
        print("Pushing to Swarm Orchestrator...")
        swarm_result = push_to_swarm({"compressed": engram_content}, swarm_prompt)
        return {
            "status": "complete",
            "email_count": len(unique_emails),
            "compressed": engram_content,
            "swarm_result": swarm_result
        }
    
    return {
        "status": "complete",
        "email_count": len(unique_emails),
        "compressed": engram_content
    }

def main():
    parser = argparse.ArgumentParser(description="Himalaya → Akashic → Swarm Pipeline (PowerShell Backend)")
    parser.add_argument("--account", required=True, help="Himalaya account name")
    parser.add_argument("--queries", required=True, help="Comma-separated search queries")
    parser.add_argument("--folder", default="[Gmail]/All Mail", help="Gmail folder to search")
    parser.add_argument("--push-swarm", action="store_true", help="Push to Swarm Orchestrator")
    parser.add_argument("--prompt", help="Custom prompt for Swarm")
    parser.add_argument("--output", help="Save result to file")
    parser.add_argument("--workers", type=int, default=3, help="Number of worker processes")
    
    args = parser.parse_args()
    
    queries = [q.strip() for q in args.queries.split(",")]
    
    print(f"Starting worker pool ({args.workers} workers)...")
    worker_pool = SwarmWorkerPool(args.workers)
    
    try:
        result = process_query_batch(
            worker_pool, args.account, args.folder, queries, 
            args.push_swarm, args.prompt
        )
        
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2)
            print(f"Result saved to {args.output}")
        
        print(json.dumps(result, indent=2))
        
    finally:
        worker_pool.shutdown_all()

if __name__ == "__main__":
    main()