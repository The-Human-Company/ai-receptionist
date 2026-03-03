#!/usr/bin/env python3
"""AI Receptionist - Comprehensive Scenario Test Suite"""
import json, subprocess, os, sys, time
from datetime import datetime

TEMP = os.environ.get('TEMP', '/tmp')
N8N_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI4ZjkzZWVhYS1lZWQ5LTRlMDYtOWMxOC1mNmFjYThmZjA3YjMiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzcwOTI5NzMzLCJleHAiOjE3NzM1MDQwMDB9.ii-Qih5OEXeIaXwIeTfk4rUwoaegEk0-zppAnHfHShg"
BASE_API = "https://solarexpresss.app.n8n.cloud/api/v1"
WH = "https://solarexpresss.app.n8n.cloud/webhook/"

PASS = 0
FAIL = 0
RESULTS = []

def run_test(test_id, desc, url, payload_dict, expect):
    global PASS, FAIL
    pfile = os.path.join(TEMP, 'test_payload_tmp.json')
    with open(pfile, 'w', encoding='utf-8') as f:
        json.dump(payload_dict, f)

    result = subprocess.run(
        ["curl", "-s", "--ssl-no-revoke", "--max-time", "20",
         "-X", "POST", url,
         "-H", "Content-Type: application/json",
         "-d", "@" + pfile],
        capture_output=True, text=True, encoding='utf-8'
    )
    body = result.stdout.strip()
    passed = expect.lower() in body.lower()
    if passed:
        print(f"{test_id}  PASS  {desc}")
        PASS += 1
        RESULTS.append((test_id, "PASS", desc))
    else:
        print(f"{test_id}  FAIL  {desc}")
        print(f"  Expected: {expect}")
        print(f"  Got: {body[:200]}")
        FAIL += 1
        RESULTS.append((test_id, "FAIL", desc))

def tc(tid, name, args):
    return {"message":{"type":"tool-calls","toolCallList":[
        {"id":tid,"type":"function","function":{"name":name,"arguments":args}}
    ]}}

def fetch_workflow(wf_id):
    result = subprocess.run(
        ["curl", "-s", "--ssl-no-revoke", "-X", "GET",
         f"{BASE_API}/workflows/{wf_id}",
         "-H", f"X-N8N-API-KEY: {N8N_KEY}"],
        capture_output=True, text=True, encoding='utf-8'
    )
    return json.loads(result.stdout)

print("================================================================")
print("  AI RECEPTIONIST - COMPREHENSIVE SCENARIO TEST SUITE")
print(f"  Date: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}")
print("================================================================")
print()

# ─── SCENARIO 1: New Customer P&C Quote Flow ───
print("=== SCENARIO 1: New Customer P&C Quote Flow ===")
print("Caller: Sarah Tanaka | Phone: 808-555-2001 | Home Insurance")
print()

run_test("S1-T1", "WF-01 Call Router -> assistant config", WH+"vapi-call-started",
    {"message":{"type":"function-call","functionCall":{"name":"check_business_hours","parameters":{}}}},
    "assistant")

run_test("S1-T2", "save_field(caller_name=Sarah Tanaka)", WH+"vapi-save-field",
    tc("s1t2","save_field",{"field_name":"caller_name","field_value":"Sarah Tanaka","call_id":"scenario-1-newcust"}),
    "saved successfully")

run_test("S1-T3", "save_field(caller_phone=808-555-2001)", WH+"vapi-save-field",
    tc("s1t3","save_field",{"field_name":"caller_phone","field_value":"808-555-2001","call_id":"scenario-1-newcust"}),
    "saved successfully")

run_test("S1-T4", "save_field(caller_email)", WH+"vapi-save-field",
    tc("s1t4","save_field",{"field_name":"caller_email","field_value":"sarah.tanaka@example.com","call_id":"scenario-1-newcust"}),
    "saved successfully")

run_test("S1-T5", "save_field(caller_address)", WH+"vapi-save-field",
    tc("s1t5","save_field",{"field_name":"caller_address","field_value":"1234 Ala Moana Blvd, Honolulu HI 96815","call_id":"scenario-1-newcust"}),
    "saved successfully")

run_test("S1-T6", "save_field(caller_dob=1985-03-15)", WH+"vapi-save-field",
    tc("s1t6","save_field",{"field_name":"caller_dob","field_value":"1985-03-15","call_id":"scenario-1-newcust"}),
    "saved successfully")

run_test("S1-T7", "save_field(caller_occupation=Teacher)", WH+"vapi-save-field",
    tc("s1t7","save_field",{"field_name":"caller_occupation","field_value":"Teacher","call_id":"scenario-1-newcust"}),
    "saved successfully")

run_test("S1-T8", "save_field(policy_type=home)", WH+"vapi-save-field",
    tc("s1t8","save_field",{"field_name":"policy_type","field_value":"home","call_id":"scenario-1-newcust"}),
    "saved successfully")

run_test("S1-T9", "check_disqualifier(1 claim) -> Not disqualified", WH+"vapi-check-disqualifier",
    tc("s1t9","check_disqualifier",{"claims_count_worst_year":1,"urgency_hours":96,"call_id":"scenario-1-newcust"}),
    "Not disqualified")

run_test("S1-T10", "check_hotlead($800K home) -> Not hot lead", WH+"vapi-check-hotlead",
    tc("s1t10","check_hot_lead",{"policy_type":"property","estimated_value":800000,"call_id":"scenario-1-newcust"}),
    "Not a hot lead")

print()

# ─── SCENARIO 2: Hot Lead ───
print("=== SCENARIO 2: Hot Lead - $3.5M Property ===")
print("Caller: James Nakamura | Kahala | Triggers immediate transfer")
print()

run_test("S2-T1", "save_field(caller_name=James Nakamura)", WH+"vapi-save-field",
    tc("s2t1","save_field",{"field_name":"caller_name","field_value":"James Nakamura","call_id":"scenario-2-hotlead"}),
    "saved successfully")

run_test("S2-T2", "check_disqualifier(0 claims) -> Pass", WH+"vapi-check-disqualifier",
    tc("s2t2","check_disqualifier",{"claims_count_worst_year":0,"urgency_hours":168,"call_id":"scenario-2-hotlead"}),
    "Not disqualified")

run_test("S2-T3", "check_hotlead($3.5M property) -> HOT LEAD!", WH+"vapi-check-hotlead",
    tc("s2t3","check_hot_lead",{"policy_type":"property","estimated_value":3500000,"call_id":"scenario-2-hotlead"}),
    "HOT LEAD")

run_test("S2-T4", "check_hotlead($200K auto) -> HOT LEAD!", WH+"vapi-check-hotlead",
    tc("s2t4","check_hot_lead",{"policy_type":"auto","estimated_value":200000,"call_id":"scenario-2-hotlead-auto"}),
    "HOT LEAD")

print()

# ─── SCENARIO 3: Disqualified Caller ───
print("=== SCENARIO 3: Disqualified Caller ===")
print("Mike Johnson | 5 claims | Also tests 48hr urgency")
print()

run_test("S3-T1", "save_field(caller_name=Mike Johnson)", WH+"vapi-save-field",
    tc("s3t1","save_field",{"field_name":"caller_name","field_value":"Mike Johnson","call_id":"scenario-3-disq"}),
    "saved successfully")

run_test("S3-T2", "check_disqualifier(5 claims) -> DISQUALIFIED", WH+"vapi-check-disqualifier",
    tc("s3t2","check_disqualifier",{"claims_count_worst_year":5,"urgency_hours":168,"call_id":"scenario-3-disq"}),
    "DISQUALIFIED")

run_test("S3-T3", "check_disqualifier(48hr urgency) -> DISQUALIFIED", WH+"vapi-check-disqualifier",
    tc("s3t3","check_disqualifier",{"claims_count_worst_year":0,"urgency_hours":48,"call_id":"scenario-3-urgent"}),
    "DISQUALIFIED")

run_test("S3-T4", "check_disqualifier(72hr boundary) -> DISQUALIFIED", WH+"vapi-check-disqualifier",
    tc("s3t4","check_disqualifier",{"claims_count_worst_year":0,"urgency_hours":72,"call_id":"scenario-3-boundary"}),
    "DISQUALIFIED")

run_test("S3-T5", "check_disqualifier(3 claims boundary) -> DISQUALIFIED", WH+"vapi-check-disqualifier",
    tc("s3t5","check_disqualifier",{"claims_count_worst_year":3,"urgency_hours":168,"call_id":"scenario-3-boundary2"}),
    "DISQUALIFIED")

print()

# ─── SCENARIO 4: Existing Customer ───
print("=== SCENARIO 4: Existing Customer ===")
print("Lisa Wong | Address update | Creates ticket + notifies")
print()

run_test("S4-T1", "WF-04 route_existing_customer -> Ticket + Notify", WH+"vapi-existing-customer",
    tc("s4t1","route_existing_customer",{"call_id":"scenario-4-existing","caller_name":"Lisa Wong","caller_phone":"808-555-4001","policy_type":"home","request_summary":"Needs to update mailing address on home policy"}),
    "results")

print()

# ─── SCENARIO 5: Claims Call ───
print("=== SCENARIO 5: Claims Call ===")
print("David Kim | Auto accident | Priority notification")
print()

run_test("S5-T1", "WF-05 route_claim -> Priority notification", WH+"vapi-claim",
    tc("s5t1","route_claim",{"call_id":"scenario-5-claim","caller_name":"David Kim","caller_phone":"808-555-5001","policy_number":"POL-HI-2024-001","claim_type":"Auto","claim_description":"Rear-ended on H1 freeway near Aloha Stadium exit"}),
    "results")

print()

# ─── SCENARIO 6: Post-Call Processing ───
print("=== SCENARIO 6: Post-Call Processing ===")
print("End-of-call report -> transcript + summary email")
print()

run_test("S6-T1", "WF-06 end-of-call (Scenario 1) -> Complete", WH+"vapi-call-ended",
    {"message":{"type":"end-of-call-report","call":{"id":"scenario-1-newcust","status":"ended"},
     "durationSeconds":245,"endedReason":"customer-ended-call",
     "artifact":{"transcript":"AI: Aloha! User: I need home insurance. AI: Name? User: Sarah Tanaka.","recordingUrl":""}}},
    "ok")

time.sleep(5)  # Wait for WF-06 to finish processing before sending next webhook

run_test("S6-T2", "WF-06 end-of-call (Scenario 5 claim) -> Complete", WH+"vapi-call-ended",
    {"message":{"type":"end-of-call-report","call":{"id":"scenario-5-claim","status":"ended"},
     "durationSeconds":120,"endedReason":"customer-ended-call",
     "artifact":{"transcript":"AI: Aloha! User: I was in an accident. AI: Collecting details...","recordingUrl":""}}},
    "ok")

print()

# ─── SCENARIO 7: After Hours Config ───
print("=== SCENARIO 7: After Hours Config Validation ===")
print()

pfile = os.path.join(TEMP, 'test_payload_tmp.json')
with open(pfile, 'w') as f:
    json.dump({"message":{"type":"function-call","functionCall":{"name":"check_business_hours","parameters":{}}}}, f)

result = subprocess.run(
    ["curl", "-s", "--ssl-no-revoke", "--max-time", "15",
     "-X", "POST", WH+"vapi-call-started",
     "-H", "Content-Type: application/json", "-d", "@" + pfile],
    capture_output=True, text=True, encoding='utf-8'
)
try:
    d = json.loads(result.stdout.strip())
    a = d.get('assistant', {})
    tools = a.get('tools', [])
    tool_names = [t.get('function',{}).get('name','') for t in tools]
    voice = a.get('voice',{}).get('voiceId','')
    txcr = a.get('transcriber',{}).get('model','')

    checks = []
    if 'save_field' in tool_names: checks.append('save_field')
    if 'route_claim' in tool_names: checks.append('route_claim')
    if voice == 'sarah': checks.append('voice=sarah')
    if txcr == 'scribe_v2_realtime': checks.append('transcriber')

    if len(checks) == 4:
        print(f"S7-T1  PASS  After Hours Config: {', '.join(checks)}")
        PASS += 1
        RESULTS.append(("S7-T1", "PASS", "After Hours Config"))
    else:
        missing = [x for x in ['save_field','route_claim','voice=sarah','transcriber'] if x not in checks]
        print(f"S7-T1  FAIL  Missing: {', '.join(missing)}")
        FAIL += 1
        RESULTS.append(("S7-T1", "FAIL", "After Hours Config"))
except Exception as e:
    print(f"S7-T1  FAIL  Error: {e}")
    FAIL += 1
    RESULTS.append(("S7-T1", "FAIL", "After Hours Config"))

print()

# ─── SCENARIO 8: Gmail Recipients ───
print("=== SCENARIO 8: Gmail Recipients Validation ===")
print()

wf_ids = ["BEOQVaIituRIqug9","AxGXJxHIDQJILOtQ","BNsx9bdXMBKfJjCe","ZAoSyxR2U2lH2a7b","nKwYydxwd8n58ExN","aTOUUPC13xwUH6PI"]
wf_names = ["WF-02","WF-03","WF-04","WF-05","WF-06","WF-07"]
all_gmail_ok = True

for wf_id, wf_name in zip(wf_ids, wf_names):
    wf = fetch_workflow(wf_id)
    for node in wf.get('nodes', []):
        if node['type'] == 'n8n-nodes-base.gmail':
            to = node.get('parameters',{}).get('sendTo','')
            ok = to == 'jephdaligdig98@gmail.com'
            status = "OK" if ok else "WRONG: " + to
            print(f"  {wf_name} [{node['name']}]: {to} {status}")
            if not ok:
                all_gmail_ok = False

if all_gmail_ok:
    print("S8-T1  PASS  All Gmail recipients = jephdaligdig98@gmail.com")
    PASS += 1
    RESULTS.append(("S8-T1", "PASS", "Gmail Recipients"))
else:
    print("S8-T1  FAIL  Some Gmail recipients are wrong")
    FAIL += 1
    RESULTS.append(("S8-T1", "FAIL", "Gmail Recipients"))

print()

# ─── SCENARIO 9: All Workflows Active ───
print("=== SCENARIO 9: All Workflows Active ===")
print()

all_wfs = [
    ("mghU5hDPImnGTMKe","WF-01"),("BEOQVaIituRIqug9","WF-02"),("AxGXJxHIDQJILOtQ","WF-03"),
    ("BNsx9bdXMBKfJjCe","WF-04"),("ZAoSyxR2U2lH2a7b","WF-05"),("nKwYydxwd8n58ExN","WF-06"),
    ("aTOUUPC13xwUH6PI","WF-07")
]
all_active = True
for wf_id, wf_name in all_wfs:
    wf = fetch_workflow(wf_id)
    status = "ACTIVE" if wf['active'] else "INACTIVE"
    print(f"  {wf_name}: {status}")
    if not wf['active']:
        all_active = False

if all_active:
    print("S9-T1  PASS  All 7 workflows ACTIVE")
    PASS += 1
    RESULTS.append(("S9-T1", "PASS", "All Workflows Active"))
else:
    print("S9-T1  FAIL  Some workflows inactive")
    FAIL += 1
    RESULTS.append(("S9-T1", "FAIL", "All Workflows Active"))

TOTAL = PASS + FAIL
print()
print("================================================================")
print(f"  FINAL RESULTS: {PASS} PASS / {FAIL} FAIL / {TOTAL} total")
print("================================================================")

if FAIL == 0:
    print("  ALL TESTS PASS!")
else:
    print(f"  {FAIL} test(s) FAILED - needs investigation")
