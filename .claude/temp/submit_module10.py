#!/usr/bin/env python3
"""
Submit Module 10 lectures to VectorShift pipeline and collect task IDs.
"""

import json
import urllib.request
import time
import os
from datetime import datetime

# Configuration
API_KEY = "sk_fkyJyb86LyHQR9IaomQq52xCdL7a31uyYbuHDxuqoTVqdf6n"
PIPELINE_ID = "6961308d6fdec16163ee0e2f"
MODULE_ID = "module-10"

# Load lecture metadata
LECTURES_FILE = r"c:\Users\JephMari\Desktop\NextGenMed\GitHubEnterprise\ngm-website-official\.claude\temp\module10_lectures.json"
OUTPUT_FILE = r"c:\Users\JephMari\Desktop\NextGenMed\GitHubEnterprise\ngm-website-official\.claude\temp\module10_task_ids.json"

def extract_html_from_json_file(filepath):
    """Extract HTML content from the JSON-wrapped export file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    # The file is a JSON array with one element containing 'text' field
    if isinstance(data, list) and len(data) > 0:
        return data[0].get('text', '')
    return ''

def submit_to_vectorshift(html_content, lecture_title, module_name):
    """Submit a lecture to VectorShift pipeline and return task_id."""
    url = f"https://api.vectorshift.ai/v1/pipeline/{PIPELINE_ID}/run"

    payload = {
        "inputs": {
            "html_content": html_content,
            "lecture_title": lecture_title,
            "module_name": module_name
        },
        "background": True
    }

    data = json.dumps(payload).encode('utf-8')

    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result.get('task_id'), None
    except Exception as e:
        return None, str(e)

def main():
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Loading lectures from {LECTURES_FILE}")

    with open(LECTURES_FILE, 'r', encoding='utf-8') as f:
        lectures = json.load(f)

    print(f"[{datetime.now().strftime('%H:%M:%S')}] Found {len(lectures)} lectures to process")

    results = {
        "module_id": MODULE_ID,
        "started_at": datetime.now().isoformat(),
        "tasks": []
    }

    for i, lecture in enumerate(lectures):
        lecture_num = lecture['lecture_number']
        lecture_title = lecture['lecture_title']
        html_file = lecture['html_file']

        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Processing lecture {lecture_num}: {lecture_title}")
        print(f"  Reading HTML from: {html_file}")

        try:
            html_content = extract_html_from_json_file(html_file)
            print(f"  HTML content size: {len(html_content)} characters")

            if len(html_content) < 100:
                print(f"  WARNING: HTML content seems too short, skipping")
                results["tasks"].append({
                    "lecture_number": lecture_num,
                    "lecture_title": lecture_title,
                    "status": "error",
                    "error": "HTML content too short"
                })
                continue

            print(f"  Submitting to VectorShift...")
            task_id, error = submit_to_vectorshift(html_content, lecture_title, MODULE_ID)

            if task_id:
                print(f"  SUCCESS! Task ID: {task_id}")
                results["tasks"].append({
                    "lecture_number": lecture_num,
                    "lecture_title": lecture_title,
                    "task_id": task_id,
                    "status": "submitted",
                    "submitted_at": datetime.now().isoformat()
                })
            else:
                print(f"  FAILED: {error}")
                results["tasks"].append({
                    "lecture_number": lecture_num,
                    "lecture_title": lecture_title,
                    "status": "error",
                    "error": error
                })

            # Small delay between submissions to avoid rate limiting
            if i < len(lectures) - 1:
                time.sleep(2)

        except Exception as e:
            print(f"  ERROR: {e}")
            results["tasks"].append({
                "lecture_number": lecture_num,
                "lecture_title": lecture_title,
                "status": "error",
                "error": str(e)
            })

    results["completed_at"] = datetime.now().isoformat()

    # Save results
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)

    print(f"\n{'='*60}")
    print(f"SUMMARY")
    print(f"{'='*60}")

    successful = [t for t in results["tasks"] if t.get("task_id")]
    failed = [t for t in results["tasks"] if not t.get("task_id")]

    print(f"Total lectures: {len(lectures)}")
    print(f"Successfully submitted: {len(successful)}")
    print(f"Failed: {len(failed)}")
    print(f"\nResults saved to: {OUTPUT_FILE}")

    if successful:
        print(f"\nSuccessful Task IDs:")
        for t in successful:
            print(f"  Lecture {t['lecture_number']}: {t['task_id']}")

if __name__ == "__main__":
    main()
