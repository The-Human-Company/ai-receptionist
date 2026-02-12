"""
Deployment validation tests for n8n AI Receptionist workflows.
Tests all 7 workflows (WF-01 through WF-07) plus legacy workflows
against business requirements from the build document.
"""
import urllib.request, json, ssl, sys, os

# Load env
env = {}
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
with open(env_path, 'r') as f:
    for line in f:
        line = line.strip()
        if '=' in line and not line.startswith('#'):
            k, v = line.split('=', 1)
            env[k.strip()] = v.strip()

INSTANCE_URL = env['N8N_INSTANCE_URL'].rstrip('/')
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

def get_node(wf, name):
    for n in wf.get('nodes', []):
        if n['name'] == name:
            return n
    return None

def get_node_by_type(wf, ntype):
    return [n for n in wf.get('nodes', []) if n['type'] == ntype]

# Load deployments
deploy_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.n8n-deployments.json')
with open(deploy_path, 'r') as f:
    deployments = json.load(f)['deployments']

WF_IDS = {
    'WF-01': deployments['wf01-inbound-call-router']['workflowId'],
    'WF-02': deployments['wf02-new-customer-intake']['workflowId'],
    'WF-03': deployments['wf03-hot-lead-transfer']['workflowId'],
    'WF-04': deployments['wf04-existing-customer']['workflowId'],
    'WF-05': deployments['wf05-claims-router']['workflowId'],
    'WF-06': deployments['wf06-post-call-processor']['workflowId'],
    'WF-07': deployments['wf07-escalation-monitor']['workflowId'],
}

# ==============================================================
# TEST SUITE 1: All 7 Workflows Exist and Are Accessible
# ==============================================================
print('=' * 60)
print('TEST SUITE 1: Workflow Existence & Structure')
print('=' * 60)

workflows = {}
for wf_name, wf_id in WF_IDS.items():
    try:
        wf = fetch_workflow(wf_id)
        workflows[wf_name] = wf
        test(f'{wf_name} exists on n8n (ID: {wf_id})', wf.get('id') == wf_id)
    except Exception as e:
        test(f'{wf_name} exists on n8n (ID: {wf_id})', False, str(e))

# Node counts
expected_nodes = {
    'WF-01': 6, 'WF-02': 17, 'WF-03': 7, 'WF-04': 5,
    'WF-05': 7, 'WF-06': 15, 'WF-07': 5
}
for wf_name, expected in expected_nodes.items():
    if wf_name in workflows:
        actual = len(workflows[wf_name].get('nodes', []))
        test(f'{wf_name} has {expected} nodes', actual == expected, f'got {actual}')

# Settings checks
for wf_name, wf in workflows.items():
    settings = wf.get('settings', {})
    test(f'{wf_name} timezone=Pacific/Honolulu', settings.get('timezone') == 'Pacific/Honolulu')
    test(f'{wf_name} executionOrder=v1', settings.get('executionOrder') == 'v1')

# ==============================================================
# TEST SUITE 2: WF-01 Inbound Call Router
# ==============================================================
print()
print('=' * 60)
print('TEST SUITE 2: WF-01 Inbound Call Router')
print('=' * 60)

if 'WF-01' in workflows:
    wf1 = workflows['WF-01']
    nodes1 = {n['name']: n for n in wf1['nodes']}

    # Webhook
    wh = get_node(wf1, 'Webhook Trigger')
    test('WF-01 webhook path=/vapi-call-started', wh and wh['parameters'].get('path') == 'vapi-call-started')
    test('WF-01 webhook method=POST', wh and wh['parameters'].get('httpMethod') == 'POST')
    test('WF-01 webhook responseMode=responseNode', wh and wh['parameters'].get('responseMode') == 'responseNode')

    # Extract Call Data
    extract = get_node(wf1, 'Extract Call Data')
    test('WF-01 extracts call_id', extract is not None)

    # Business Hours
    hours = get_node(wf1, 'Check Business Hours')
    test('WF-01 has Check Business Hours node', hours is not None)
    if hours:
        code = hours['parameters'].get('jsCode', '')
        test('WF-01 business hours uses UTC-10 offset', 'utcHours - 10' in code or 'hstHours' in code)
        test('WF-01 checks weekday (Mon-Fri)', 'hstDay >= 1 && hstDay <= 5' in code)
        test('WF-01 checks 9am-5pm range', 'hstHours >= 9 && hstHours < 17' in code)
        test('WF-01 handles day wrap-around', 'hstHours < 0' in code)

    # IF Business Hours
    if_biz = get_node(wf1, 'IF Business Hours')
    test('WF-01 has IF Business Hours branch', if_biz is not None)

    # Business Hours Response
    biz_resp = get_node(wf1, 'Return Business Hours Config')
    test('WF-01 has Business Hours response', biz_resp is not None)
    if biz_resp:
        body = biz_resp['parameters'].get('responseBody', '')
        test('WF-01 biz-hours: firstMessage mentions Equity Insurance', 'Equity Insurance' in body)
        test('WF-01 biz-hours: disclaims Tulsa Oklahoma', 'Tulsa, Oklahoma' in body)
        test('WF-01 biz-hours: asks new/existing/claim', 'new customer' in body.lower())
        test('WF-01 biz-hours: has system prompt', 'system' in body)
        test('WF-01 biz-hours: system prompt has RULES', 'IMPORTANT RULES' in body)
        test('WF-01 biz-hours: no coverage advice rule', 'NEVER give coverage guarantees' in body)
        test('WF-01 biz-hours: no PMI/FHA rule', 'Private Mortgage Insurance' in body)
        test('WF-01 biz-hours: no pet/travel insurance', 'Pet Insurance' in body)
        test('WF-01 biz-hours: quotes 24-72 hours', '24 to 72 hours' in body)
        test('WF-01 biz-hours: $150 min premium', '$150' in body)
        test('WF-01 biz-hours: Davin redirect for P&C', 'Davin is currently assisting' in body)
        test('WF-01 biz-hours: life/medicare transfer', 'Life Insurance or Medicare' in body)
        test('WF-01 biz-hours: pound key for human', 'pound' in body.lower())
        test('WF-01 biz-hours: has save_field tool', 'save_field' in body)
        test('WF-01 biz-hours: has check_disqualifier tool', 'check_disqualifier' in body)
        test('WF-01 biz-hours: has check_hot_lead tool', 'check_hot_lead' in body)
        test('WF-01 biz-hours: voice provider=elevenlabs', 'elevenlabs' in body)
        test('WF-01 biz-hours: model=gpt-4o', 'gpt-4o' in body)
        test('WF-01 biz-hours: temperature=0.3', '0.3' in body)
        test('WF-01 biz-hours: data collection order specified', 'DATA COLLECTION FOR NEW P&C CUSTOMERS' in body)
        test('WF-01 biz-hours: has route_existing_customer tool', 'route_existing_customer' in body)
        test('WF-01 biz-hours: has route_claim tool', 'route_claim' in body)
        test('WF-01 biz-hours: route_existing_customer hits WF-04 webhook', 'vapi-existing-customer' in body)
        test('WF-01 biz-hours: route_claim hits WF-05 webhook', 'vapi-claim' in body)
        test('WF-01 biz-hours: existing customer flow in prompt', 'route_existing_customer' in body)
        test('WF-01 biz-hours: claim flow in prompt', 'route_claim' in body)
        test('WF-01 biz-hours: policy-specific auto questions', 'VIN' in body)
        test('WF-01 biz-hours: policy-specific renters questions', 'possessions' in body)
        test('WF-01 biz-hours: policy-specific property questions', 'first-time home buyer' in body)
        test('WF-01 biz-hours: policy-specific business questions', 'annual revenue' in body)
        test('WF-01 biz-hours: cross-sell instruction', 'cross-sell' in body.lower())
        test('WF-01 biz-hours: referral source wording', 'thank the person who might have referred you' in body)
        test('WF-01 biz-hours: Progressive carrier mention', 'Progressive' in body)

    # After-Hours Response
    ah_resp = get_node(wf1, 'Return After-Hours Config')
    test('WF-01 has After-Hours response', ah_resp is not None)
    if ah_resp:
        ah_body = ah_resp['parameters'].get('responseBody', '')
        test('WF-01 after-hours: mentions office hours', '9 AM to 5 PM' in ah_body)
        test('WF-01 after-hours: mentions extension dial', 'extension' in ah_body.lower())
        test('WF-01 after-hours: restricted tool set', 'caller_name' in ah_body)
        test('WF-01 after-hours: brief interaction instruction', 'brief' in ah_body.lower() or 'AFTER HOURS' in ah_body)

    # Connections
    conns1 = wf1.get('connections', {})
    test('WF-01 Webhook->Extract', 'Webhook Trigger' in conns1)
    test('WF-01 Extract->CheckHours', 'Extract Call Data' in conns1)
    test('WF-01 CheckHours->IF', 'Check Business Hours' in conns1)
    test('WF-01 IF branches to 2 responses', len(conns1.get('IF Business Hours', {}).get('main', [])) == 2)

# ==============================================================
# TEST SUITE 3: WF-02 New Customer P&C Intake
# ==============================================================
print()
print('=' * 60)
print('TEST SUITE 3: WF-02 New Customer P&C Intake')
print('=' * 60)

if 'WF-02' in workflows:
    wf2 = workflows['WF-02']

    # Three webhook entry points
    webhooks = get_node_by_type(wf2, 'n8n-nodes-base.webhook')
    test('WF-02 has 3 webhook triggers', len(webhooks) == 3, f'got {len(webhooks)}')

    webhook_paths = [w['parameters'].get('path', '') for w in webhooks]
    test('WF-02 has /vapi-save-field webhook', 'vapi-save-field' in webhook_paths)
    test('WF-02 has /vapi-check-disqualifier webhook', 'vapi-check-disqualifier' in webhook_paths)
    test('WF-02 has /vapi-check-hotlead webhook', 'vapi-check-hotlead' in webhook_paths)

    # Branch A: Save Field
    validate = get_node(wf2, 'Validate Field')
    test('WF-02 has Validate Field node', validate is not None)
    if validate:
        vcode = validate['parameters'].get('jsCode', '')
        test('WF-02 validates phone format', 'caller_phone' in vcode)
        test('WF-02 validates email format', 'caller_email' in vcode)
        test('WF-02 validates DOB', 'caller_dob' in vcode)

    if_valid = get_node(wf2, 'IF Valid')
    test('WF-02 has IF Valid branch', if_valid is not None)

    save_sheet = get_node(wf2, 'Save to Google Sheet')
    test('WF-02 saves to Google Sheets', save_sheet is not None)
    if save_sheet:
        test('WF-02 sheet uses GOOGLE_SHEET_LEADS_ID env', 'GOOGLE_SHEET_LEADS_ID' in json.dumps(save_sheet['parameters']))
        test('WF-02 sets migration_flag=VAPI_AI_COLLECTED', 'VAPI_AI_COLLECTED' in json.dumps(save_sheet['parameters']))

    ret_success = get_node(wf2, 'Return Success')
    test('WF-02 has Return Success response', ret_success is not None)
    ret_error = get_node(wf2, 'Return Validation Error')
    test('WF-02 has Return Validation Error response', ret_error is not None)

    # Branch B: Disqualifier
    disq = get_node(wf2, 'Evaluate Disqualifier Rules')
    test('WF-02 has Evaluate Disqualifier node', disq is not None)
    if disq:
        dcode = disq['parameters'].get('jsCode', '')
        test('WF-02 disqualifier: claims threshold=3', 'claimsThreshold = 3' in dcode or 'claims_count_worst_year >= 3' in dcode)
        test('WF-02 disqualifier: urgency threshold=72h', 'urgencyThreshold = 72' in dcode or 'urgency_hours <= 72' in dcode)

    # Branch C: Hot Lead
    hotlead = get_node(wf2, 'Evaluate Hot Lead')
    test('WF-02 has Evaluate Hot Lead node', hotlead is not None)
    if hotlead:
        hcode = hotlead['parameters'].get('jsCode', '')
        test('WF-02 hot lead: property >= $2M', '2000000' in hcode)
        test('WF-02 hot lead: auto >= $180K', '180000' in hcode)

    # Execute Workflow to WF-03
    exec_wf = get_node(wf2, 'Trigger WF-03 Transfer')
    test('WF-02 has Execute Workflow to WF-03', exec_wf is not None)
    if exec_wf:
        test('WF-02 WF-03 reference has correct ID', WF_IDS['WF-03'] in exec_wf['parameters'].get('workflowId', ''))

# ==============================================================
# TEST SUITE 4: WF-03 Hot Lead Transfer Handler
# ==============================================================
print()
print('=' * 60)
print('TEST SUITE 4: WF-03 Hot Lead Transfer Handler')
print('=' * 60)

if 'WF-03' in workflows:
    wf3 = workflows['WF-03']

    recv = get_node(wf3, 'Receive Input Data')
    test('WF-03 receives input data', recv is not None)

    transfer = get_node(wf3, 'Send VAPI Transfer Command')
    test('WF-03 sends VAPI transfer', transfer is not None)
    if transfer:
        test('WF-03 transfer uses HTTP POST', transfer['parameters'].get('method') == 'POST')
        test('WF-03 transfer uses warm mode', 'warm' in json.dumps(transfer['parameters']))
        test('WF-03 transfer URL includes VAPI_API_BASE', 'VAPI_API_BASE' in json.dumps(transfer['parameters']))

    wait = get_node(wf3, 'Wait for Transfer Result')
    test('WF-03 has wait node', wait is not None)

    if_success = get_node(wf3, 'IF Transfer Success')
    test('WF-03 branches on transfer result', if_success is not None)

    success_sheet = get_node(wf3, 'Update Lead (Success)')
    test('WF-03 updates sheet on success', success_sheet is not None)
    if success_sheet:
        test('WF-03 success status=transferred_hot_lead', 'transferred_hot_lead' in json.dumps(success_sheet['parameters']))

    failure_sheet = get_node(wf3, 'Update Lead (Failure)')
    test('WF-03 updates sheet on failure', failure_sheet is not None)
    if failure_sheet:
        test('WF-03 failure status=transfer_failed_hot_lead', 'transfer_failed_hot_lead' in json.dumps(failure_sheet['parameters']))
        test('WF-03 failure priority=critical', 'critical' in json.dumps(failure_sheet['parameters']))

    urgent = get_node(wf3, 'Send URGENT Notification')
    test('WF-03 sends urgent email on failure', urgent is not None)
    if urgent:
        test('WF-03 urgent email to Val and Davin', 'NOTIFY_EMAIL_VAL' in json.dumps(urgent['parameters']) and 'NOTIFY_EMAIL_DAVIN' in json.dumps(urgent['parameters']))

# ==============================================================
# TEST SUITE 5: WF-04 Existing Customer Handler
# ==============================================================
print()
print('=' * 60)
print('TEST SUITE 5: WF-04 Existing Customer Handler')
print('=' * 60)

if 'WF-04' in workflows:
    wf4 = workflows['WF-04']

    wh4 = get_node(wf4, 'Webhook Trigger')
    test('WF-04 webhook path=/vapi-existing-customer', wh4 and wh4['parameters'].get('path') == 'vapi-existing-customer')

    extract4 = get_node(wf4, 'Extract Customer Data')
    test('WF-04 extracts customer data', extract4 is not None)

    ticket = get_node(wf4, 'Create Ticket Row')
    test('WF-04 creates ticket in Google Sheets', ticket is not None)
    if ticket:
        params_str = json.dumps(ticket['parameters'])
        test('WF-04 ticket uses TICKETS sheet', 'GOOGLE_SHEET_TICKETS_ID' in params_str)
        test('WF-04 ticket status=pending', 'pending' in params_str)
        test('WF-04 ticket assigned_to=Val', 'Val' in params_str)

    email4 = get_node(wf4, 'Send Notification to Val')
    test('WF-04 sends email to Val', email4 is not None)
    if email4:
        test('WF-04 email to Val address', 'NOTIFY_EMAIL_VAL' in json.dumps(email4['parameters']))

    resp4 = get_node(wf4, 'Respond to VAPI')
    test('WF-04 responds to VAPI', resp4 is not None)

# ==============================================================
# TEST SUITE 6: WF-05 Claims Router
# ==============================================================
print()
print('=' * 60)
print('TEST SUITE 6: WF-05 Claims Router')
print('=' * 60)

if 'WF-05' in workflows:
    wf5 = workflows['WF-05']

    wh5 = get_node(wf5, 'Webhook Trigger')
    test('WF-05 webhook path=/vapi-claim', wh5 and wh5['parameters'].get('path') == 'vapi-claim')

    extract5 = get_node(wf5, 'Extract Claim Data')
    test('WF-05 extracts claim data', extract5 is not None)

    hours5 = get_node(wf5, 'Check Business Hours')
    test('WF-05 checks business hours', hours5 is not None)
    if hours5:
        code5 = hours5['parameters'].get('jsCode', '')
        test('WF-05 uses same HST logic as WF-01', 'utcHours - 10' in code5)

    if_hours5 = get_node(wf5, 'IF Business Hours')
    test('WF-05 branches on business hours', if_hours5 is not None)

    transfer5 = get_node(wf5, 'Send VAPI Transfer Command')
    test('WF-05 attempts transfer during hours', transfer5 is not None)

    notif5 = get_node(wf5, 'Send Priority Notification')
    test('WF-05 sends priority notification', notif5 is not None)
    if notif5:
        p5_str = json.dumps(notif5['parameters'])
        test('WF-05 notification to BOTH Val and Davin', 'NOTIFY_EMAIL_VAL' in p5_str and 'NOTIFY_EMAIL_DAVIN' in p5_str)
        test('WF-05 notification priority=HIGH', 'HIGH' in p5_str)

    resp5 = get_node(wf5, 'Respond to VAPI')
    test('WF-05 responds to VAPI', resp5 is not None)

# ==============================================================
# TEST SUITE 7: WF-06 Post-Call Processor
# ==============================================================
print()
print('=' * 60)
print('TEST SUITE 7: WF-06 Post-Call Processor')
print('=' * 60)

if 'WF-06' in workflows:
    wf6 = workflows['WF-06']

    wh6 = get_node(wf6, 'Webhook Trigger')
    test('WF-06 webhook path=/vapi-call-ended', wh6 and wh6['parameters'].get('path') == 'vapi-call-ended')

    extract6 = get_node(wf6, 'Extract All Data')
    test('WF-06 extracts all VAPI data', extract6 is not None)
    if extract6:
        e6_str = json.dumps(extract6['parameters'])
        test('WF-06 extracts call_id', 'call.id' in e6_str)
        test('WF-06 extracts transcript', 'transcript' in e6_str)
        test('WF-06 extracts recording_url', 'recordingUrl' in e6_str)
        test('WF-06 extracts duration', 'duration' in e6_str)
        test('WF-06 extracts cost', 'cost' in e6_str)

    read6 = get_node(wf6, 'Read Lead Record')
    test('WF-06 reads lead from Google Sheets', read6 is not None)

    merge6 = get_node(wf6, 'Merge Data')
    test('WF-06 merges VAPI + lead data', merge6 is not None)

    migration6 = get_node(wf6, 'Add Migration Flag')
    test('WF-06 adds migration flag', migration6 is not None)
    if migration6:
        test('WF-06 migration flag=VAPI_AI_COLLECTED', 'VAPI_AI_COLLECTED' in json.dumps(migration6['parameters']))

    crm6 = get_node(wf6, 'Write to QQ Catalyst')
    test('WF-06 attempts CRM write', crm6 is not None)
    if crm6:
        test('WF-06 CRM write uses HTTP POST', crm6['parameters'].get('method') == 'POST')

    fallback6 = get_node(wf6, 'CRM Write Fallback')
    test('WF-06 has CRM fallback', fallback6 is not None)

    fallback_sheet6 = get_node(wf6, 'Fallback to Google Sheet')
    test('WF-06 falls back to Google Sheet', fallback_sheet6 is not None)

    email_builder = get_node(wf6, 'Build Summary Email')
    test('WF-06 builds summary email', email_builder is not None)
    if email_builder:
        eb_code = email_builder['parameters'].get('jsCode', '')
        test('WF-06 email: hot lead format', 'HOT LEAD' in eb_code)
        test('WF-06 email: disqualified format', 'DISQUALIFIED' in eb_code)
        test('WF-06 email: transfer failed format', 'TRANSFER FAILED' in eb_code)
        test('WF-06 email: claim format', 'CLAIM' in eb_code)
        test('WF-06 email: existing customer format', 'EXISTING' in eb_code)
        test('WF-06 email: partial intake format', 'PARTIAL' in eb_code)
        test('WF-06 email: qualified lead format', 'QUALIFIED' in eb_code)

    send_email6 = get_node(wf6, 'Send Summary Email')
    test('WF-06 sends summary email', send_email6 is not None)

    analytics6 = get_node(wf6, 'Log Analytics Row')
    test('WF-06 logs analytics', analytics6 is not None)
    if analytics6:
        a6_str = json.dumps(analytics6['parameters'])
        test('WF-06 analytics uses ANALYTICS sheet', 'GOOGLE_SHEET_ANALYTICS_ID' in a6_str)

    transcript6 = get_node(wf6, 'Save Transcript')
    test('WF-06 saves transcript', transcript6 is not None)

    error_handler = get_node(wf6, 'Error Trigger')
    test('WF-06 has Error Trigger handler', error_handler is not None)

    error_log = get_node(wf6, 'Log Error to Sheet')
    test('WF-06 logs errors to Errors sheet', error_log is not None)
    if error_log:
        test('WF-06 error log uses ERRORS sheet', 'GOOGLE_SHEET_ERRORS_ID' in json.dumps(error_log['parameters']))

# ==============================================================
# TEST SUITE 8: WF-07 Escalation Monitor
# ==============================================================
print()
print('=' * 60)
print('TEST SUITE 8: WF-07 Escalation Monitor')
print('=' * 60)

if 'WF-07' in workflows:
    wf7 = workflows['WF-07']

    cron7 = get_node(wf7, 'Cron Trigger')
    test('WF-07 has Schedule Trigger', cron7 is not None)
    if cron7:
        cron_str = json.dumps(cron7['parameters'])
        test('WF-07 cron: */30 schedule', '*/30' in cron_str)
        test('WF-07 cron: business hours 9-16', '9-16' in cron_str)
        test('WF-07 cron: weekdays only 1-5', '1-5' in cron_str)

    read7 = get_node(wf7, 'Read Pending Tickets')
    test('WF-07 reads pending tickets', read7 is not None)
    if read7:
        test('WF-07 reads from TICKETS sheet', 'GOOGLE_SHEET_TICKETS_ID' in json.dumps(read7['parameters']))
        test('WF-07 filters status=pending', 'pending' in json.dumps(read7['parameters']))

    filter7 = get_node(wf7, 'Filter Overdue')
    test('WF-07 filters overdue tickets', filter7 is not None)
    if filter7:
        f7_code = filter7['parameters'].get('jsCode', '')
        test('WF-07 filter: 2-hour threshold', '2 * 60 * 60 * 1000' in f7_code)
        test('WF-07 filter: checks pending status', "status === 'pending'" in f7_code)

    esc_email = get_node(wf7, 'Send Escalation to Davin')
    test('WF-07 sends escalation email', esc_email is not None)
    if esc_email:
        test('WF-07 escalation to Davin', 'NOTIFY_EMAIL_DAVIN' in json.dumps(esc_email['parameters']))
        test('WF-07 escalation subject mentions ESCALATION', 'ESCALATION' in json.dumps(esc_email['parameters']))

    update7 = get_node(wf7, 'Update Ticket Status')
    test('WF-07 updates ticket to escalated', update7 is not None)
    if update7:
        test('WF-07 sets status=escalated', 'escalated' in json.dumps(update7['parameters']))

# ==============================================================
# TEST SUITE 9: Cross-Workflow Integration
# ==============================================================
print()
print('=' * 60)
print('TEST SUITE 9: Cross-Workflow Integration')
print('=' * 60)

# WF-02 -> WF-03 sub-workflow link
if 'WF-02' in workflows:
    exec_node = get_node(workflows['WF-02'], 'Trigger WF-03 Transfer')
    if exec_node:
        test('WF-02 -> WF-03: correct workflow ID linked',
             WF_IDS['WF-03'] in exec_node['parameters'].get('workflowId', ''))

# Webhook paths are unique across workflows
all_paths = []
for wf_name, wf in workflows.items():
    for n in wf.get('nodes', []):
        if n['type'] == 'n8n-nodes-base.webhook':
            all_paths.append(n['parameters'].get('path', ''))
test('All webhook paths are unique', len(all_paths) == len(set(all_paths)), f'paths: {all_paths}')

# All workflows reference correct Google Sheet env vars
for wf_name, wf in workflows.items():
    wf_str = json.dumps(wf)
    if 'googleSheets' in wf_str:
        test(f'{wf_name} uses env vars for Sheet IDs (not hardcoded)',
             'GOOGLE_SHEET_' in wf_str)

# ==============================================================
# TEST SUITE 10: Compliance & Business Rules
# ==============================================================
print()
print('=' * 60)
print('TEST SUITE 10: Compliance & Business Rules')
print('=' * 60)

if 'WF-01' in workflows:
    biz_resp = get_node(workflows['WF-01'], 'Return Business Hours Config')
    if biz_resp:
        body = biz_resp['parameters'].get('responseBody', '')
        test('COMPLIANCE: Non-affiliation with Tulsa OK stated', 'Tulsa, Oklahoma' in body)
        test('COMPLIANCE: No coverage advice rule', 'NEVER give coverage guarantees' in body)
        test('COMPLIANCE: No PMI/Federal loans', 'Private Mortgage Insurance' in body)
        test('COMPLIANCE: No pet/travel insurance', 'Pet Insurance' in body and 'Travel Insurance' in body)
        test('COMPLIANCE: Quotes take 24-72 hours', '24 to 72 hours' in body)
        test('COMPLIANCE: $150 minimum premium', '$150' in body)
        test('COMPLIANCE: # key for human agent', 'pound' in body.lower())

if 'WF-02' in workflows:
    disq_node = get_node(workflows['WF-02'], 'Evaluate Disqualifier Rules')
    if disq_node:
        dc = disq_node['parameters'].get('jsCode', '')
        test('RULE: Claims disqualifier >= 3', '3' in dc and 'claims' in dc.lower())
        test('RULE: Urgency disqualifier <= 72h', '72' in dc and 'urgency' in dc.lower())

    hl_node = get_node(workflows['WF-02'], 'Evaluate Hot Lead')
    if hl_node:
        hc = hl_node['parameters'].get('jsCode', '')
        test('RULE: Property hot lead >= $2M', '2000000' in hc)
        test('RULE: Auto hot lead >= $180K', '180000' in hc)

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
