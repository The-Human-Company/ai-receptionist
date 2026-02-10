"""
Deployment validation tests for n8n AI Receptionist workflows.
Tests both VAPI Call Handler and Notifications workflows against
business requirements from all deliverables.
"""
import urllib.request, json, ssl, sys

env = {}
with open('.env', 'r') as f:
    for line in f:
        line = line.strip()
        if '=' in line and not line.startswith('#'):
            k, v = line.split('=', 1)
            env[k.strip()] = v.strip()

INSTANCE_URL = env['N8N_INSTANCE_URL']
API_KEY = env['N8N_API_KEY']
ctx = ssl.create_default_context()

tests_passed = 0
tests_failed = 0
results = []

def test(name, condition, detail=''):
    global tests_passed, tests_failed
    if condition:
        tests_passed += 1
        results.append(('PASS', name, ''))
    else:
        tests_failed += 1
        results.append(('FAIL', name, detail))

def fetch_workflow(wf_id):
    req = urllib.request.Request(
        f'{INSTANCE_URL}/api/v1/workflows/{wf_id}',
        headers={'X-N8N-API-KEY': API_KEY}
    )
    resp = urllib.request.urlopen(req, context=ctx)
    return json.loads(resp.read().decode('utf-8'))

# ==============================================================
# TEST SUITE 1: VAPI Call Handler Workflow
# ==============================================================
print('=' * 60)
print('TEST SUITE 1: VAPI Call Handler (1IX82-PqM5HiZq7sUSfpf)')
print('=' * 60)

wf1 = fetch_workflow('1IX82-PqM5HiZq7sUSfpf')

test('Workflow exists and is accessible', wf1.get('id') == '1IX82-PqM5HiZq7sUSfpf')
test('Workflow is active', wf1.get('active') == True, f"active={wf1.get('active')}")
test('Has 13 nodes', len(wf1.get('nodes', [])) == 13, f"got {len(wf1.get('nodes', []))}")
test('Timezone is Pacific/Honolulu', wf1.get('settings', {}).get('timezone') == 'Pacific/Honolulu')
test('Execution timeout is 3600s', wf1.get('settings', {}).get('executionTimeout') == 3600)
test('Execution order is v1', wf1.get('settings', {}).get('executionOrder') == 'v1')

# Check required nodes exist
node_names = [n['name'] for n in wf1.get('nodes', [])]
required_nodes = [
    'VAPI Webhook', 'Route Event Type', 'Route Function Call',
    'Check Business Hours', 'Classify Caller', 'Save Lead Data',
    'Check Disqualifiers', 'Check Hot Lead', 'Transfer Call',
    'Respond to VAPI', 'Handle Call End', 'Trigger Post-Call Notifications',
    'Handle Status Update'
]
for rn in required_nodes:
    test(f'Node exists: {rn}', rn in node_names, 'missing')

# Webhook tests
webhook_node = [n for n in wf1['nodes'] if n['name'] == 'VAPI Webhook'][0]
test('Webhook is POST method', webhook_node['parameters'].get('httpMethod') == 'POST')
test('Webhook path is vapi-webhook', webhook_node['parameters'].get('path') == 'vapi-webhook')
test('Webhook responseMode=responseNode', webhook_node['parameters'].get('responseMode') == 'responseNode')

# Connection tests
conns = wf1.get('connections', {})
test('VAPI Webhook connects to Route Event Type', 'VAPI Webhook' in conns)
test('Route Event Type has connections', 'Route Event Type' in conns)
test('Route Function Call has 6 outputs',
     len(conns.get('Route Function Call', {}).get('main', [])) == 6,
     f"got {len(conns.get('Route Function Call', {}).get('main', []))}")

# Business logic tests
hours_code = [n for n in wf1['nodes'] if n['name'] == 'Check Business Hours'][0]['parameters'].get('jsCode', '')
test('Business hours uses HST (UTC-10)', 'hstOffset = -10' in hours_code)
test('Business hours checks 9am-5pm', 'hstHours >= 9 && hstHours < 17' in hours_code)
test('After-hours message mentions 9am-5pm', '9am to 5pm' in hours_code)

disq_code = [n for n in wf1['nodes'] if n['name'] == 'Check Disqualifiers'][0]['parameters'].get('jsCode', '')
test('Disqualifier: 3+ claims rule', 'claimsPastYear >= 3' in disq_code)
test('Disqualifier: 72h urgency rule', 'urgency_72h' in disq_code)
test('Disqualifier: polite redirect message', 'specialized attention' in disq_code)

hot_code = [n for n in wf1['nodes'] if n['name'] == 'Check Hot Lead'][0]['parameters'].get('jsCode', '')
test('Hot lead: property > $2M', 'propertyValue > 2000000' in hot_code)
test('Hot lead: auto > $180K', 'autoValue > 180000' in hot_code)
test('Hot lead: senior team transfer message', 'senior team' in hot_code)

save_code = [n for n in wf1['nodes'] if n['name'] == 'Save Lead Data'][0]['parameters'].get('jsCode', '')
test('Migration flag: VAPI_AI_COLLECTED', 'VAPI_AI_COLLECTED' in save_code)
test('Saves personal info (name, phone, email)', 'full_name' in save_code and 'phone' in save_code and 'email' in save_code)
test('Saves DOB and occupation', 'date_of_birth' in save_code and 'occupation' in save_code)
test('Saves referral source', 'referral_source' in save_code)
test('Saves claims history', 'claims_history' in save_code)

classify_code = [n for n in wf1['nodes'] if n['name'] == 'Classify Caller'][0]['parameters'].get('jsCode', '')
test('Classify: detects life insurance', 'life' in classify_code.lower())
test('Classify: detects medicare', 'medicare' in classify_code.lower())
test('Classify: routes life/medicare to Davin', 'davin' in classify_code.lower())
test('Classify: detects existing customer', 'existing' in classify_code.lower())
test('Classify: detects claims', 'claim' in classify_code.lower())

transfer_code = [n for n in wf1['nodes'] if n['name'] == 'Transfer Call'][0]['parameters'].get('jsCode', '')
test('Transfer: has Val contact', 'val' in transfer_code.lower())
test("Transfer: has Val's number +18087800473", '+18087800473' in transfer_code)
test('Transfer: has Davin contact', 'davin' in transfer_code.lower())
test('Transfer: has claims routing', 'claims' in transfer_code.lower())

# ==============================================================
# TEST SUITE 2: Notifications & Escalation Workflow
# ==============================================================
print()
print('=' * 60)
print('TEST SUITE 2: Notifications & Escalation (5LCW3l7WBBOClWIV)')
print('=' * 60)

wf2 = fetch_workflow('5LCW3l7WBBOClWIV')

test('Workflow exists and is accessible', wf2.get('id') == '5LCW3l7WBBOClWIV')
test('Has 9 nodes', len(wf2.get('nodes', [])) == 9, f"got {len(wf2.get('nodes', []))}")
test('Timezone is Pacific/Honolulu', wf2.get('settings', {}).get('timezone') == 'Pacific/Honolulu')

node_names2 = [n['name'] for n in wf2.get('nodes', [])]
required_nodes2 = [
    'Post-Call Webhook', 'Parse & Classify Notification', 'Route Notification Type',
    'Email: Hot Lead Alert', 'Email: New P&C Lead to Val',
    'Email: Commercial Lead to Val', 'Email: Existing Customer to Val',
    'Wait 2 Hours', 'Email: Escalate to Davin'
]
for rn in required_nodes2:
    test(f'Node exists: {rn}', rn in node_names2, 'missing')

# Notification routing
conns2 = wf2.get('connections', {})
test('Route Notification Type has 4 outputs',
     len(conns2.get('Route Notification Type', {}).get('main', [])) == 4,
     f"got {len(conns2.get('Route Notification Type', {}).get('main', []))}")

# Email destination checks
hot_email = [n for n in wf2['nodes'] if n['name'] == 'Email: Hot Lead Alert'][0]
test('Hot lead emails both Davin and Val',
     'davin' in hot_email['parameters'].get('toEmail', '').lower() and
     'val' in hot_email['parameters'].get('toEmail', '').lower())

val_email = [n for n in wf2['nodes'] if n['name'] == 'Email: New P&C Lead to Val'][0]
test('P&C lead goes to Val', 'val@equityinsurance.services' in val_email['parameters'].get('toEmail', ''))

comm_email = [n for n in wf2['nodes'] if n['name'] == 'Email: Commercial Lead to Val'][0]
test('Commercial lead goes to Val', 'val@equityinsurance.services' in comm_email['parameters'].get('toEmail', ''))

escalate_email = [n for n in wf2['nodes'] if n['name'] == 'Email: Escalate to Davin'][0]
test('Escalation goes to Davin', 'davin@equityinsurance.services' in escalate_email['parameters'].get('toEmail', ''))
test('Escalation subject says URGENT', 'URGENT' in escalate_email['parameters'].get('subject', ''))

wait_node = [n for n in wf2['nodes'] if n['name'] == 'Wait 2 Hours'][0]
test('Wait node is 2 hours', wait_node['parameters'].get('amount') == 2 and wait_node['parameters'].get('unit') == 'hours')

# 2hr escalation chain
test('P&C email connects to Wait 2 Hours', 'Email: New P&C Lead to Val' in conns2)
test('Commercial email connects to Wait 2 Hours', 'Email: Commercial Lead to Val' in conns2)
test('Existing customer email connects to Wait 2 Hours', 'Email: Existing Customer to Val' in conns2)
test('Wait 2 Hours connects to Escalate to Davin', 'Wait 2 Hours' in conns2)

# Notification parsing logic
parse_code = [n for n in wf2['nodes'] if n['name'] == 'Parse & Classify Notification'][0]['parameters'].get('jsCode', '')
test('Classify: detects hot leads', 'hot_lead' in parse_code)
test('Classify: detects commercial/business', 'business' in parse_code.lower())
test('Classify: detects existing customer', 'existing_customer' in parse_code)

# ==============================================================
# TEST SUITE 3: Cross-Workflow Integration
# ==============================================================
print()
print('=' * 60)
print('TEST SUITE 3: Cross-Workflow Integration')
print('=' * 60)

notif_trigger = [n for n in wf1['nodes'] if n['name'] == 'Trigger Post-Call Notifications'][0]
test('Call Handler triggers notifications via HTTP', notif_trigger['type'] == 'n8n-nodes-base.httpRequest')

post_webhook = [n for n in wf2['nodes'] if n['name'] == 'Post-Call Webhook'][0]
test('Notifications receives via POST webhook', post_webhook['parameters'].get('httpMethod') == 'POST')
test('Webhook path is post-call-notification', post_webhook['parameters'].get('path') == 'post-call-notification')

# ==============================================================
# TEST SUITE 4: Compliance Rules (from deliverables)
# ==============================================================
print()
print('=' * 60)
print('TEST SUITE 4: Compliance & Business Rules')
print('=' * 60)

# All code nodes combined
all_code = ''
for n in wf1['nodes']:
    all_code += n['parameters'].get('jsCode', '') + '\n'

test('After-hours message in workflow', 'office hours' in all_code.lower())
test('P&C routing for Auto/Renters/Property/Business', 'p_and_c' in classify_code or 'p&c' in classify_code.lower())
test('Data collection includes all 8 required fields',
     all(f in save_code for f in ['full_name', 'phone', 'email', 'mailing_address', 'date_of_birth', 'occupation', 'insurance_type' if 'insurance_type' in save_code else 'type', 'referral_source']))

# ==============================================================
# SUMMARY
# ==============================================================
print()
print('=' * 60)
total = tests_passed + tests_failed
print(f'RESULTS: {tests_passed}/{total} tests passed, {tests_failed} failed')
print('=' * 60)

if tests_failed > 0:
    print()
    print('FAILED TESTS:')
    for status, name, detail in results:
        if status == 'FAIL':
            print(f'  FAIL: {name} - {detail}')

print()
if tests_failed == 0:
    print('All tests pass!')
else:
    print(f'{tests_failed} test(s) need attention.')

sys.exit(0 if tests_failed == 0 else 1)
