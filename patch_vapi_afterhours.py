#!/usr/bin/env python3
"""
PATCH the live VAPI after-hours assistant with updated configuration.
Assistant ID: 45bddc18-ab13-40b5-85ca-d5713a54a891
"""

import json
import ssl
import urllib.request

# ── Config ──────────────────────────────────────────────────────────────────
ASSISTANT_ID = "45bddc18-ab13-40b5-85ca-d5713a54a891"
API_KEY = "35c9ce5b-63f5-46a2-91e3-0d5275567738"
API_URL = f"https://api.vapi.ai/assistant/{ASSISTANT_ID}"
HTML_PATH = r"c:\Users\JephMari\Desktop\Portfolio\TheHumanCompany\ai-receptionist\vapi-web-test.html"

# ── Step 1: Extract SYSTEM_PROMPT_AFTERHOURS from vapi-web-test.html ────────
with open(HTML_PATH, "r", encoding="utf-8") as f:
    content = f.read()

start_marker = "const SYSTEM_PROMPT_AFTERHOURS = `"
start_idx = content.find(start_marker)
if start_idx == -1:
    raise RuntimeError("Could not find SYSTEM_PROMPT_AFTERHOURS in vapi-web-test.html")

prompt_start = start_idx + len(start_marker)
end_idx = content.find("`;", prompt_start)
if end_idx == -1:
    raise RuntimeError("Could not find closing backtick-semicolon for SYSTEM_PROMPT_AFTERHOURS")

system_prompt = content[prompt_start:end_idx]
print(f"[OK] Extracted system prompt ({len(system_prompt)} chars)")

# ── Step 2: Build the PATCH payload ─────────────────────────────────────────
payload = {
    "firstMessage": (
        "Aloha, thank you for calling Equity Insurance in Honolulu, Hawaii. "
        "We're currently closed -- our business hours are 9 AM to 5 PM Hawaii time, "
        "Monday through Friday. I'm an AI assistant, but I can take a message and "
        "have someone call you back. May I have your name?"
    ),
    "model": {
        "provider": "anthropic",
        "model": "claude-sonnet-4-6",
        "maxTokens": 500,
        "messages": [
            {
                "role": "system",
                "content": system_prompt,
            }
        ],
    },
    "stopSpeakingPlan": {
        "numWords": 2,
        "voiceSeconds": 0.2,
        "backoffSeconds": 1.2,
        "acknowledgementPhrases": [
            "okay", "got it", "mm-hmm", "uh-huh", "right", "sure", "yep"
        ],
        "interruptionPhrases": [
            "wait", "hold on", "stop", "actually", "excuse me"
        ],
    },
    "startSpeakingPlan": {
        "waitSeconds": 0.6,
        "transcriptionEndpointingPlan": {
            "onPunctuationSeconds": 0.4,
            "onNoPunctuationSeconds": 1.5,
            "onNumberSeconds": 0.8,
        },
        "smartEndpointingPlan": {
            "provider": "livekit",
        },
    },
    "keypadInputPlan": {
        "enabled": True,
        "timeoutSeconds": 3,
        "delimiters": ["#"],
    },
}

payload_json = json.dumps(payload, indent=2)
print(f"\n[PAYLOAD] ({len(payload_json)} bytes):")
print(payload_json)

# ── Step 3: Send the PATCH request ──────────────────────────────────────────
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request(
    API_URL,
    data=payload_json.encode("utf-8"),
    method="PATCH",
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Accept": "application/json",
    },
)

print(f"\n[SENDING] PATCH {API_URL}")

try:
    with urllib.request.urlopen(req, context=ctx) as resp:
        status = resp.status
        body = json.loads(resp.read().decode("utf-8"))

        print(f"\n{'='*60}")
        print(f"[RESPONSE] Status: {status}")
        print(f"{'='*60}")

        # Print key fields from the response
        print(f"\n  Assistant ID   : {body.get('id', 'N/A')}")
        print(f"  Name           : {body.get('name', 'N/A')}")
        first_msg = body.get('firstMessage', 'N/A') or 'N/A'
        print(f"  First Message  : {first_msg[:120]}...")
        print(f"  Created At     : {body.get('createdAt', 'N/A')}")
        print(f"  Updated At     : {body.get('updatedAt', 'N/A')}")

        # Model info
        model = body.get("model", {})
        print(f"\n  Model Provider : {model.get('provider', 'N/A')}")
        print(f"  Model Name     : {model.get('model', 'N/A')}")
        print(f"  Max Tokens     : {model.get('maxTokens', 'N/A')}")

        # System prompt (first 150 chars)
        messages = model.get("messages", [])
        if messages:
            sys_msg = messages[0].get("content", "")
            print(f"  System Prompt  : {sys_msg[:150]}...")

        # Stop speaking plan
        ssp = body.get("stopSpeakingPlan", {})
        print(f"\n  StopSpeaking   : numWords={ssp.get('numWords')}, voiceSeconds={ssp.get('voiceSeconds')}, backoffSeconds={ssp.get('backoffSeconds')}")
        print(f"    ackPhrases   : {ssp.get('acknowledgementPhrases')}")
        print(f"    intPhrases   : {ssp.get('interruptionPhrases')}")

        # Start speaking plan
        stp = body.get("startSpeakingPlan", {})
        tep = stp.get("transcriptionEndpointingPlan", {})
        sep = stp.get("smartEndpointingPlan", {})
        print(f"\n  StartSpeaking  : waitSeconds={stp.get('waitSeconds')}")
        print(f"    transcription: onPunctuationSeconds={tep.get('onPunctuationSeconds')}, onNoPunctuationSeconds={tep.get('onNoPunctuationSeconds')}, onNumberSeconds={tep.get('onNumberSeconds')}")
        print(f"    smartEndpoint: provider={sep.get('provider')}")

        # Keypad input plan
        kip = body.get("keypadInputPlan", {})
        print(f"\n  KeypadInput    : enabled={kip.get('enabled')}, timeoutSeconds={kip.get('timeoutSeconds')}, delimiters={kip.get('delimiters')}")

        print(f"\n{'='*60}")
        print("[DONE] Assistant patched successfully.")

except urllib.error.HTTPError as e:
    error_body = e.read().decode("utf-8")
    print(f"\n[ERROR] HTTP {e.code}: {e.reason}")
    print(f"  Response body: {error_body}")
except Exception as e:
    print(f"\n[ERROR] {type(e).__name__}: {e}")
