#!/usr/bin/env python3
"""
Patch both VAPI assistants with updated system prompts and keypadInputPlan.
Reads prompts from vapi-web-test.html, sends PATCH requests to VAPI API.
"""

import json
import re
import ssl
import urllib.request
import os

# --- Config ---
API_KEY = os.environ.get("VAPI_API_KEY", "407f3078-02d3-4951-9ba1-2d414787e4c0")
BASE_URL = "https://api.vapi.ai"
BUSINESS_ID = "bbf67fe2-99dc-427a-a546-37892f58a796"
AFTERHOURS_ID = "8ae61948-d6c5-4586-9f55-b7c1416db25b"

HTML_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vapi-web-test.html")

# Model configs (must match existing provider/model on each assistant)
BUSINESS_MODEL = {"provider": "openai", "model": "gpt-4o"}
AFTERHOURS_MODEL = {"provider": "anthropic", "model": "claude-sonnet-4-6"}


def extract_prompts(html_path):
    """Extract SYSTEM_PROMPT_BUSINESS and SYSTEM_PROMPT_AFTERHOURS from HTML."""
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Match backtick-delimited template literals
    biz_match = re.search(r'const\s+SYSTEM_PROMPT_BUSINESS\s*=\s*`(.*?)`;', content, re.DOTALL)
    ah_match = re.search(r'const\s+SYSTEM_PROMPT_AFTERHOURS\s*=\s*`(.*?)`;', content, re.DOTALL)

    if not biz_match:
        raise ValueError("Could not find SYSTEM_PROMPT_BUSINESS in HTML")
    if not ah_match:
        raise ValueError("Could not find SYSTEM_PROMPT_AFTERHOURS in HTML")

    return biz_match.group(1), ah_match.group(1)


def patch_assistant(assistant_id, name, prompt, model_config):
    """PATCH a VAPI assistant with updated prompt and keypadInputPlan."""
    url = f"{BASE_URL}/assistant/{assistant_id}"

    payload = {
        "model": {
            "provider": model_config["provider"],
            "model": model_config["model"],
            "messages": [{"role": "system", "content": prompt}]
        },
        "keypadInputPlan": {
            "enabled": True,
            "timeoutSeconds": 5,
            "delimiters": ["#"]
        }
    }

    data = json.dumps(payload).encode("utf-8")

    # SSL context with disabled verification
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    req = urllib.request.Request(
        url,
        data=data,
        method="PATCH",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 VAPI-Setup/1.0"
        }
    )

    print(f"\n{'='*60}")
    print(f"PATCHING: {name}")
    print(f"URL: {url}")
    print(f"Provider: {model_config['provider']}, Model: {model_config['model']}")
    print(f"Prompt length: {len(prompt)} chars")
    print(f"{'='*60}")

    try:
        with urllib.request.urlopen(req, context=ctx) as resp:
            status = resp.status
            body = json.loads(resp.read().decode("utf-8"))

            print(f"Status: {status}")

            # Verify keypadInputPlan
            kip = body.get("keypadInputPlan", {})
            print(f"\nkeypadInputPlan in response:")
            print(f"  enabled: {kip.get('enabled')}")
            print(f"  timeoutSeconds: {kip.get('timeoutSeconds')}")
            print(f"  delimiters: {kip.get('delimiters')}")

            if kip.get("timeoutSeconds") == 5:
                print(f"\n[PASS] keypadInputPlan.timeoutSeconds == 5 verified!")
            else:
                print(f"\n[FAIL] keypadInputPlan.timeoutSeconds is {kip.get('timeoutSeconds')}, expected 5")

            # Verify system prompt was set
            messages = body.get("model", {}).get("messages", [])
            if messages and messages[0].get("role") == "system":
                content_len = len(messages[0].get("content", ""))
                print(f"[PASS] System prompt set ({content_len} chars)")
            else:
                print("[WARN] Could not verify system prompt in response")

            # Verify provider
            resp_provider = body.get("model", {}).get("provider")
            print(f"[INFO] Provider: {resp_provider}")

            return True

    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        print(f"HTTP Error {e.code}: {e.reason}")
        print(f"Response body: {error_body}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False


def main():
    print("Reading prompts from vapi-web-test.html...")
    biz_prompt, ah_prompt = extract_prompts(HTML_PATH)
    print(f"  Business prompt: {len(biz_prompt)} chars")
    print(f"  After-hours prompt: {len(ah_prompt)} chars")

    # Patch business hours assistant
    ok1 = patch_assistant(BUSINESS_ID, "Business Hours Assistant", biz_prompt, BUSINESS_MODEL)

    # Patch after-hours assistant
    ok2 = patch_assistant(AFTERHOURS_ID, "After Hours Assistant", ah_prompt, AFTERHOURS_MODEL)

    print(f"\n{'='*60}")
    print("RESULTS:")
    print(f"  Business Hours: {'SUCCESS' if ok1 else 'FAILED'}")
    print(f"  After Hours:    {'SUCCESS' if ok2 else 'FAILED'}")
    print(f"{'='*60}")

    if not (ok1 and ok2):
        exit(1)


if __name__ == "__main__":
    main()
