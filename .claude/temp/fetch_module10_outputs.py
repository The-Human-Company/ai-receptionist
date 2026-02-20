#!/usr/bin/env python3
"""
Fetch VectorShift pipeline outputs for Module 10 lectures and save as JSON files.
"""

import json
import urllib.request
import time
import os
import re
from datetime import datetime

# Configuration
API_KEY = "sk_fkyJyb86LyHQR9IaomQq52xCdL7a31uyYbuHDxuqoTVqdf6n"
PIPELINE_ID = "6961308d6fdec16163ee0e2f"
MODULE_ID = "module-10"
OUTPUT_DIR = r"c:\Users\JephMari\Desktop\NextGenMed\GitHubEnterprise\ngm-website-official\content\ngm-lectures\module-10"

# Task IDs from the pipeline runs
TASK_IDS = [
    {"lecture_number": 151, "title": "Introduction to AI in Healthcare & Longevity Applications", "task_id": "696ac3ab89cf947718ce9246"},
    {"lecture_number": 152, "title": "Large Language Models: GPT, Claude & Medical Reasoning", "task_id": "696ac3af89cf947718ce9247"},
    {"lecture_number": 153, "title": "AI-Powered Biomarker Discovery & Pattern Recognition", "task_id": "696ac3b589cf947718ce9248"},
    {"lecture_number": 154, "title": "Machine Learning for Aging Clock Development", "task_id": "696ac3b989cf947718ce9249"},
    {"lecture_number": 155, "title": "LLMs for Patient Communication & Education", "task_id": "696ac3bd89cf947718ce924a"},
    {"lecture_number": 156, "title": "AI-Assisted Clinical Decision Support Systems", "task_id": "696ac3c189cf947718ce924b"},
    {"lecture_number": 157, "title": "Natural Language Processing for Medical Literature Synthesis", "task_id": "696ac3c589cf947718ce924c"},
    {"lecture_number": 158, "title": "Predictive Modeling for Healthspan Optimization", "task_id": "696ac3c989cf947718ce924d"},
    {"lecture_number": 159, "title": "AI Ethics in Longevity Medicine & Bias Mitigation", "task_id": "696ac3cf89cf947718ce924e"},
    {"lecture_number": 160, "title": "Automated Report Generation & Clinical Documentation", "task_id": "696ac3d389cf947718ce924f"},
    {"lecture_number": 161, "title": "AI-Driven Drug Discovery & Repurposing", "task_id": "696ac3d889cf947718ce9250"},
    {"lecture_number": 162, "title": "Voice AI & Conversational Health Interfaces", "task_id": "696ac3dc89cf947718ce9251"},
    {"lecture_number": 163, "title": "LLM Integration with EMRs & Practice Management", "task_id": "696ac3e089cf947718ce9252"},
    {"lecture_number": 164, "title": "Data Privacy & HIPAA Compliance with AI Tools", "task_id": "696ac3e489cf947718ce9253"},
    {"lecture_number": 165, "title": "Future of AI: AGI Implications for Longevity Medicine", "task_id": "696ac3e889cf947718ce9254"},
]

def extract_json(raw_output):
    """Extract JSON from VectorShift output (may be wrapped in markdown fences)"""
    if not raw_output:
        return None

    content = raw_output.strip()

    # Remove markdown code fences if present
    if content.startswith('```json'):
        content = content[7:]
    elif content.startswith('```'):
        content = content[3:]
    if content.endswith('```'):
        content = content[:-3]

    content = content.strip()

    # Find JSON object
    match = re.search(r'\{[\s\S]*\}', content)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError as e:
            print(f"    JSON parse error: {e}")
            return None
    return None

def fetch_task_status(task_id):
    """Fetch the status and result of a VectorShift task."""
    url = f"https://api.vectorshift.ai/v1/pipeline/{PIPELINE_ID}/run/status/{task_id}"

    req = urllib.request.Request(
        url,
        headers={"Authorization": f"Bearer {API_KEY}"}
    )

    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        return {"error": str(e)}

def main():
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Fetching VectorShift outputs for Module 10")
    print(f"Output directory: {OUTPUT_DIR}")

    # Create output directory if it doesn't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    results = {
        "completed": [],
        "in_progress": [],
        "failed": []
    }

    for task in TASK_IDS:
        lecture_num = task["lecture_number"]
        title = task["title"]
        task_id = task["task_id"]

        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Lecture {lecture_num}: {title}")
        print(f"  Task ID: {task_id}")

        # Fetch status
        response = fetch_task_status(task_id)

        if "error" in response:
            print(f"  ERROR: {response['error']}")
            results["failed"].append({"lecture": lecture_num, "error": response["error"]})
            continue

        status = response.get("status", "unknown")
        print(f"  Status: {status}")

        if status == "completed":
            result = response.get("result", {})
            lecture_json_raw = result.get("lecture_json", "")

            if lecture_json_raw:
                lecture_data = extract_json(lecture_json_raw)

                if lecture_data:
                    # Save to file
                    output_file = os.path.join(OUTPUT_DIR, f"lecture-{lecture_num}.json")
                    with open(output_file, 'w', encoding='utf-8') as f:
                        json.dump(lecture_data, f, indent=2, ensure_ascii=False)

                    print(f"  [OK] Saved: lecture-{lecture_num}.json")
                    results["completed"].append({
                        "lecture": lecture_num,
                        "title": lecture_data.get("title", title),
                        "file": output_file
                    })
                else:
                    print(f"  [FAIL] Could not extract JSON from lecture_json output")
                    results["failed"].append({"lecture": lecture_num, "error": "JSON extraction failed"})
            else:
                print(f"  [FAIL] No lecture_json in result")
                results["failed"].append({"lecture": lecture_num, "error": "No lecture_json output"})

        elif status == "in_progress":
            print(f"  [WAIT] Still processing...")
            results["in_progress"].append({"lecture": lecture_num, "task_id": task_id})

        else:
            print(f"  [FAIL] Unknown status: {status}")
            results["failed"].append({"lecture": lecture_num, "error": f"Status: {status}"})

    # Summary
    print(f"\n{'='*60}")
    print(f"SUMMARY")
    print(f"{'='*60}")
    print(f"Completed: {len(results['completed'])}")
    print(f"In Progress: {len(results['in_progress'])}")
    print(f"Failed: {len(results['failed'])}")

    if results["completed"]:
        print(f"\nCompleted lectures saved to {OUTPUT_DIR}:")
        for item in results["completed"]:
            print(f"  - lecture-{item['lecture']}.json: {item['title']}")

    if results["in_progress"]:
        print(f"\nStill processing (run script again later):")
        for item in results["in_progress"]:
            print(f"  - Lecture {item['lecture']}: {item['task_id']}")

    if results["failed"]:
        print(f"\nFailed:")
        for item in results["failed"]:
            print(f"  - Lecture {item['lecture']}: {item['error']}")

    # Save summary
    summary_file = os.path.join(OUTPUT_DIR, "_fetch_summary.json")
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    print(f"\nSummary saved to: {summary_file}")

if __name__ == "__main__":
    main()
