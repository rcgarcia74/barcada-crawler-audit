"""Identify the non-business row(s) with software_product."""
import json
from pathlib import Path

QUEUE_PATH = Path("/Users/administrator/projects/barcada-scraper/eval_data/audits/step2_software_product_queue.jsonl")

with QUEUE_PATH.open() as f:
    for line in f:
        row = json.loads(line)
        if row.get("label") == "non-business":
            print(f"Domain: {row.get('domain')}")
            print(f"Confidence: {row.get('confidence')}")
            print(f"Keywords: {row.get('rationale_keywords')}")
            print(f"Notes: {row.get('notes')}")
            print()
