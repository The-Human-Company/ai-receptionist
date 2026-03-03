#!/usr/bin/env python3
import json, re, ssl, urllib.request, os

ASSISTANT_ID = "af31b79d-92e1-4888-905d-c15d01fd7751"
VAPI_API_KEY = "35c9ce5b-63f5-46a2-91e3-0d5275567738"
N8N_BASE = "https://solarexpresss.app.n8n.cloud/webhook"
VAPI_URL = "https://api.vapi.ai/assistant/" + ASSISTANT_ID
HTML_PATH = os.path.join("C:" + os.sep, "Users", "JephMari", "Desktop",
                         "Portfolio", "TheHumanCompany", "ai-receptionist",
                         "vapi-web-test.html")

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

print("=" * 60)
print("STEP 1: Reading SYSTEM_PROMPT_BUSINESS from vapi-web-test.html")
print("=" * 60)

with open(HTML_PATH, "r", encoding="utf-8") as f:
    html_content = f.read()

backtick = chr(96)
pattern = r"const SYSTEM_PROMPT_BUSINESS\s*=\s*" + backtick + r"(.*?)" + backtick + r";"
match = re.search(pattern, html_content, re.DOTALL)
if not match:
    raise RuntimeError("Could not find SYSTEM_PROMPT_BUSINESS")

system_prompt = match.group(1)
print("  Extracted prompt length: {} chars".format(len(system_prompt)))

if "EMAIL FORM LINK" in system_prompt:
    print("  [OK] Prompt contains EMAIL FORM LINK")
elif "SMS FORM LINK" in system_prompt:
    print("  [UPDATE] Replacing SMS with EMAIL in prompt")
    system_prompt = system_prompt.replace("SMS FORM LINK", "EMAIL FORM LINK")
    system_prompt = system_prompt.replace("send you a text with a link", "send you an email with a link")
else:
    print("  [WARN] No FORM LINK section found in prompt")

print()
print("=" * 60)
print("STEP 2: Building tools array (6 function tools + transferCall)")
print("=" * 60)

tools = [
    {
        "type": "function",
        "function": {
            "name": "save_field",
            "description": "Save a collected data field from the caller to the system. Call this after collecting each piece of information.",
            "parameters": {
                "type": "object",
                "properties": {
                    "call_id": {"type": "string", "description": "The unique call identifier"},
                    "field_name": {
                        "type": "string",
                        "enum": [
                            "caller_name","caller_phone","caller_email","caller_address","caller_dob",
                            "caller_occupation","policy_type","referral_source","claims_count","claims_details",
                            "urgency_timeline","current_coverage","shopping_reason",
                            "auto_vehicle_info","auto_vin","auto_lien_type","auto_lienholder",
                            "auto_violations","auto_household_drivers","auto_title_names",
                            "renter_address","renter_possessions_value","renter_mgmt_company","renter_addl_insured",
                            "property_address","property_first_buyer","property_value","property_coverage_needs","property_policy_age",
                            "biz_name","biz_ein","biz_start_date","biz_revenue","biz_industry","biz_contact",
                            "cross_sell_interest","cross_sell_types"
                        ]
                    },
                    "field_value": {"type": "string", "description": "The value collected from the caller"}
                },
                "required": ["call_id", "field_name", "field_value"]
            }
        },
        "server": {"url": N8N_BASE + "/vapi-save-field"}
    },
    {
        "type": "function",
        "function": {
            "name": "check_disqualifier",
            "description": "Check if the caller is disqualified based on claims history or coverage urgency. Call after collecting claims count and urgency timeline.",
            "parameters": {
                "type": "object",
                "properties": {
                    "call_id": {"type": "string", "description": "The unique call identifier"},
                    "claims_count_worst_year": {"type": "integer", "description": "The highest number of claims in any single year"},
                    "urgency_hours": {"type": "integer", "description": "How many hours until coverage is needed"}
                },
                "required": ["call_id", "claims_count_worst_year", "urgency_hours"]
            }
        },
        "server": {"url": N8N_BASE + "/vapi-check-disqualifier"}
    },
    {
        "type": "function",
        "function": {
            "name": "check_hot_lead",
            "description": "Check if the caller qualifies as a high-value hot lead for immediate agent transfer. Call after collecting property value or auto value.",
            "parameters": {
                "type": "object",
                "properties": {
                    "call_id": {"type": "string", "description": "The unique call identifier"},
                    "policy_type": {"type": "string", "description": "The type of insurance policy"},
                    "estimated_value": {"type": "number", "description": "The estimated property or auto value in dollars"}
                },
                "required": ["call_id", "policy_type", "estimated_value"]
            }
        },
        "server": {"url": N8N_BASE + "/vapi-check-hotlead"}
    },
    {
        "type": "function",
        "function": {
            "name": "route_existing_customer",
            "description": "Route an existing customer request. Creates a support ticket and notifies the team.",
            "parameters": {
                "type": "object",
                "properties": {
                    "call_id": {"type": "string", "description": "The unique call identifier"},
                    "caller_name": {"type": "string", "description": "The existing customer name"},
                    "caller_phone": {"type": "string", "description": "The customer phone number"},
                    "policy_type": {"type": "string", "description": "The type of policy they have or are asking about"},
                    "request_description": {"type": "string", "description": "What the customer is asking for specifically"}
                },
                "required": ["call_id", "caller_name", "caller_phone", "request_description"]
            }
        },
        "server": {"url": N8N_BASE + "/vapi-existing-customer"}
    },
    {
        "type": "function",
        "function": {
            "name": "route_claim",
            "description": "Route a claim call. Attempts to transfer to claims agent during business hours and sends priority notification.",
            "parameters": {
                "type": "object",
                "properties": {
                    "call_id": {"type": "string", "description": "The unique call identifier"},
                    "caller_name": {"type": "string", "description": "The caller name"},
                    "caller_phone": {"type": "string", "description": "The caller phone number"},
                    "policy_number": {"type": "string", "description": "The policy number if available"},
                    "claim_type": {"type": "string", "description": "The type of claim (auto, property, etc.)"},
                    "claim_description": {"type": "string", "description": "Description of the claim"}
                },
                "required": ["call_id", "caller_name", "caller_phone", "claim_type", "claim_description"]
            }
        },
        "server": {"url": N8N_BASE + "/vapi-claim"}
    },
    {
        "type": "function",
        "function": {
            "name": "send_form_link",
            "description": "Email the caller a link to the insurance quote form after collecting their basic info (name, phone, email, insurance type). Call this once during the conversation.",
            "parameters": {
                "type": "object",
                "properties": {
                    "call_id": {"type": "string", "description": "The unique call identifier"},
                    "caller_name": {"type": "string", "description": "The caller's name"},
                    "caller_email": {"type": "string", "description": "The caller's email address to send the form link to"}
                },
                "required": ["call_id", "caller_name", "caller_email"]
            }
        },
        "server": {"url": N8N_BASE + "/vapi-send-form"}
    },
    {
        "type": "transferCall",
        "destinations": [
            {
                "type": "number",
                "number": "+18087800473",
                "message": "I'm going to connect you with our agent now. Just one moment."
            }
        ]
    }
]

print("  Built {} tools:".format(len(tools)))
for i, t in enumerate(tools, 1):
    if t["type"] == "function":
        print("    {}. {} -> {}".format(i, t["function"]["name"], t["server"]["url"]))
    else:
        print("    {}. {} -> {}".format(i, t["type"], t["destinations"][0]["number"]))

print()
print("=" * 60)
print("STEP 3: Sending PATCH request to VAPI API")
print("=" * 60)

payload = {
    "model": {
        "provider": "openai",
        "model": "gpt-4o",
        "messages": [
            {"role": "system", "content": system_prompt}
        ],
        "tools": tools,
        "temperature": 0.7
    }
}

data = json.dumps(payload).encode("utf-8")
print("  Payload size: {} bytes".format(len(data)))
print("  Target: PATCH {}".format(VAPI_URL))

req = urllib.request.Request(
    VAPI_URL,
    data=data,
    headers={
        "Authorization": "Bearer " + VAPI_API_KEY,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Python/3.13",
    },
    method="PATCH",
)

try:
    with urllib.request.urlopen(req, context=ctx) as resp:
        status = resp.status
        body = json.loads(resp.read().decode("utf-8"))
        print("  Response status: {}".format(status))
        print()
        print("=" * 60)
        print("STEP 4: Verification")
        print("=" * 60)
        print("  Assistant ID: {}".format(body.get("id")))
        print("  Assistant Name: {}".format(body.get("name", "N/A")))

        model_data = body.get("model", {})
        print("  Model: {}".format(model_data.get("model", "N/A")))
        print("  Provider: {}".format(model_data.get("provider", "N/A")))

        model_tools = model_data.get("tools", [])
        print("  Tools count: {}".format(len(model_tools)))
        for i, t in enumerate(model_tools, 1):
            if t.get("type") == "function":
                fn = t.get("function", {})
                params = list(fn.get("parameters", {}).get("properties", {}).keys())
                print("    {}. {} (params: {})".format(i, fn.get("name"), params))
                if fn.get("name") == "send_form_link":
                    print("       Description: {}".format(fn.get("description")))
                    print("       [OK] Uses caller_email: {}".format("caller_email" in params))
                    print("       [OK] No caller_phone: {}".format("caller_phone" not in params))
                if fn.get("name") == "save_field":
                    enums = fn.get("parameters", {}).get("properties", {}).get("field_name", {}).get("enum", [])
                    print("       field_name enums: {} items".format(len(enums)))
            elif t.get("type") == "transferCall":
                dests = t.get("destinations", [])
                num = dests[0].get("number") if dests else "N/A"
                print("    {}. transferCall -> {}".format(i, num))

        messages = model_data.get("messages", [])
        if messages:
            prompt_content = messages[0].get("content", "")
            has_email = "EMAIL FORM LINK" in prompt_content
            has_sms = "SMS FORM LINK" in prompt_content
            print("  System prompt length: {} chars".format(len(prompt_content)))
            print("  Contains EMAIL FORM LINK: {}".format(has_email))
            print("  Contains SMS FORM LINK: {}".format(has_sms))

        print()
        print("=" * 60)
        print("PATCH COMPLETE - Assistant updated successfully!")
        print("=" * 60)

except urllib.error.HTTPError as e:
    error_body = e.read().decode("utf-8")
    print("  ERROR: HTTP {}".format(e.code))
    print("  Response: {}".format(error_body))
    raise
