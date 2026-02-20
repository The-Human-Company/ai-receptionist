# AI Receptionist System Guide
## Equity Insurance Inc. | Powered by VAPI + n8n

**Version:** 1.0
**Last Updated:** February 20, 2026
**Owner:** Equity Insurance Inc. (Davin Char)
**System URL:** https://solarexpresss.app.n8n.cloud

---

## Table of Contents

1. [System Overview](#1-system-overview)
2. [Architecture Diagram](#2-architecture-diagram)
3. [Call Flow Summary](#3-call-flow-summary)
4. [Workflow Reference (WF-01 through WF-07)](#4-workflow-reference)
5. [Google Sheets Data Model](#5-google-sheets-data-model)
6. [Email Notifications](#6-email-notifications)
7. [Business Rules](#7-business-rules)
8. [VAPI Assistant Configuration](#8-vapi-assistant-configuration)
9. [Troubleshooting](#9-troubleshooting)
10. [Test Suite](#10-test-suite)

---

## 1. System Overview

The AI Receptionist is an automated voice-based call handling system for Equity Insurance Inc., a 3rd-generation family-owned insurance agency in Honolulu, Hawaii. It answers all inbound calls on the main business line (+1 808-593-7746), collects lead data for Property & Casualty (P&C) insurance quotes, and intelligently routes calls to the human team.

### Key Components

| Component | Service | Purpose |
|-----------|---------|---------|
| **Voice AI** | VAPI.ai + ElevenLabs | Voice conversation with callers (Female, Warm tone) |
| **LLM** | GPT-4o | Natural language understanding and conversation flow |
| **Orchestration** | n8n Cloud | 7 workflows handling all business logic |
| **Phone System** | Talkroute | Main line routing (+1 808-593-7746) |
| **CRM** | QQ Catalyst | Primary CRM (integration pending) |
| **Data Storage** | Google Sheets | Lead records, tickets, analytics, transcripts |
| **Notifications** | Gmail | Email alerts to team members |

### Team Contacts

| Person | Role | Contact |
|--------|------|---------|
| **Davin Char** | CEO/Owner | davin@equityinsurance.services |
| **Val Char** | P&C Agent | val@equityinsurance.services / +1 808-780-0473 |

---

## 2. Architecture Diagram

```
                         INBOUND CALL
                              |
                              v
                    +------------------+
                    |    Talkroute     |
                    | (808-593-7746)  |
                    +--------+---------+
                             |
                             v
                    +------------------+
                    |     VAPI.ai      |
                    | (Voice AI + LLM) |
                    | ElevenLabs Voice |
                    |  GPT-4o Brain   |
                    +--------+---------+
                             |
              +--------------+--------------+
              |              |              |
              v              v              v
        +---------+   +-----------+   +----------+
        | WF-01   |   | WF-02     |   | WF-04/05 |
        | Call     |   | Data      |   | Existing/|
        | Router   |   | Collector |   | Claims   |
        +---------+   +-----+-----+   +-----+----+
              |              |               |
              |         +----+----+          |
              |         |         |          |
              |         v         v          v
              |    +---------+ +-------+ +----------+
              |    | WF-03   | |Google | | Tickets  |
              |    | Hot Lead| |Sheets | | Sheet    |
              |    | Transfer| |(Leads)| +----+-----+
              |    +---------+ +-------+      |
              |                               |
              v               v               v
        +---------+    +-----------+    +-----------+
        | VAPI    |    | WF-06     |    | WF-07     |
        | Config  |    | Post-Call |    | Escalation|
        | Return  |    | Processor |    | Monitor   |
        +---------+    +-----+-----+   +-----------+
                             |
                    +--------+--------+
                    |        |        |
                    v        v        v
              +--------+ +------+ +--------+
              |Analytics| |Email | |Transcr.|
              | Sheet   | |Alert | | Sheet  |
              +--------+ +------+ +--------+
```

---

## 3. Call Flow Summary

Every inbound call follows this lifecycle:

### Step 1: Call Arrives (WF-01)
1. Caller dials +1 808-593-7746
2. Talkroute forwards to VAPI
3. VAPI triggers `vapi-call-started` webhook
4. **WF-01** checks if it's business hours (Mon-Fri 9am-5pm HST)
5. Returns the appropriate VAPI assistant configuration (Business or After Hours)
6. AI greets caller: "Aloha! Thank you for calling Equity Insurance..."

### Step 2: Intent Classification (VAPI AI)
The AI determines the caller's intent through conversation:
- **New Customer** wanting an insurance quote -> WF-02
- **Existing Customer** with a service request -> WF-04
- **Insurance Claim** to report -> WF-05

### Step 3A: New Customer Quote Flow (WF-02)
1. AI collects data fields one at a time (name, phone, email, address, DOB, occupation, policy type)
2. Each field is saved to Google Sheets via `save_field` function call -> **WF-02 Sub-flow A**
3. After collecting key info, AI checks disqualification rules -> **WF-02 Sub-flow B**
4. If not disqualified, AI checks hot lead thresholds -> **WF-02 Sub-flow C**
5. If hot lead detected, triggers immediate transfer -> **WF-03**

### Step 3B: Existing Customer Flow (WF-04)
1. AI collects the customer's request summary
2. Creates a ticket in the Tickets Google Sheet
3. Sends email notification to Val
4. Tells caller: "I've created a ticket and notified Val. She'll call you back."

### Step 3C: Claims Flow (WF-05)
1. AI collects claim details (policy number, claim type, description)
2. During business hours: initiates warm transfer to Val + sends priority email
3. After hours: sends priority email, tells caller team will follow up next business day

### Step 4: Post-Call Processing (WF-06)
After every call ends, regardless of the call type:
1. VAPI sends `end-of-call-report` with transcript, duration, and call metadata
2. **WF-06** merges call data with lead record from Google Sheets
3. Attempts CRM sync to QQ Catalyst (currently disabled - placeholder)
4. Builds an intelligent summary email based on call outcome
5. Logs analytics data (duration, call type, qualification status, etc.)
6. Saves full transcript for review

### Step 5: Escalation Monitoring (WF-07)
- Runs every 30 minutes during business hours (Mon-Fri 9am-5pm HST)
- Checks for tickets pending 2+ hours without acknowledgment
- Sends escalation email to Davin for overdue tickets
- Updates ticket status to "escalated"

---

## 4. Workflow Reference

### WF-01: Inbound Call Router

| Property | Value |
|----------|-------|
| **n8n ID** | `mghU5hDPImnGTMKe` |
| **Webhook** | `POST /vapi-call-started` |
| **Nodes** | 6 |
| **Trigger** | VAPI call-started event |

**What it does:** Entry point for all calls. Checks business hours and returns the correct VAPI assistant configuration.

**Flow:**
```
Webhook Trigger
    -> Extract Call Data (call_id, caller_phone, timestamp)
    -> Check Business Hours (Mon-Fri 9am-5pm HST)
    -> IF Business Hours?
        YES -> Return Business Hours Config (full VAPI tools + prompt)
        NO  -> Return After-Hours Config (limited tools + after-hours prompt)
```

**Business Hours Logic:**
- Converts current UTC time to HST (UTC-10, no daylight saving)
- Business hours: Monday through Friday, 9:00 AM to 5:00 PM HST
- Outside these hours, the After Hours assistant is used

---

### WF-02: New Customer P&C Intake

| Property | Value |
|----------|-------|
| **n8n ID** | `BEOQVaIituRIqug9` |
| **Webhooks** | 3 endpoints (see below) |
| **Nodes** | 22 |
| **Trigger** | VAPI tool calls |

This is the largest workflow with 3 independent sub-flows:

#### Sub-Flow A: Save Field (`POST /vapi-save-field`)

**What it does:** Saves each data field collected by the AI to Google Sheets in real-time.

**Flow:**
```
Webhook -> Extract Field Parameters -> Validate Field -> IF Valid?
    YES -> Prepare Sheet Data -> Read Headers -> Build Upsert -> Write to Leads Sheet -> Return "saved successfully"
    NO  -> Return "validation error"
```

**Accepted Fields (30+):**
- `caller_name`, `caller_phone`, `caller_email`, `caller_address`
- `caller_dob`, `caller_occupation`, `policy_type`, `referral_source`
- `claims_count`, `claims_details`, `urgency_timeline`, `current_coverage`
- `auto_vehicle_info`, `auto_vin`, `auto_lien_type`, `auto_violations`
- `property_address`, `property_value`, `property_coverage_needs`
- `biz_name`, `biz_ein`, `biz_industry`, `biz_revenue`
- `cross_sell_interest`, `cross_sell_types`
- And more...

**Google Sheet:** Leads Sheet (`14FqFY4ZyGDeOluYPhbQKNWmZhyPOwi7FFHpnn5c7CG0`) -> Tab: `Leads`

**How upsert works:**
1. Uses n8n static data to accumulate fields per `call_id` in memory
2. Checks if a row with the same `call_id` already exists
3. If yes: updates the existing row (PUT)
4. If no: appends a new row (APPEND)

#### Sub-Flow B: Check Disqualifier (`POST /vapi-check-disqualifier`)

**What it does:** Evaluates whether a caller is disqualified from AI intake.

**Flow:**
```
Webhook -> Evaluate Rules -> Save Result to Leads Sheet -> Return Result
```

**Disqualification Rules:**
| Condition | Threshold | Reason |
|-----------|-----------|--------|
| Claims per year | 3 or more | "High claims frequency" |
| Urgency (property) | 72 hours or less | "Urgent property need - too time-sensitive for AI intake" |

**Returns:**
- `"Not disqualified"` - Caller passes, continue quote collection
- `"DISQUALIFIED: {reason}"` - AI politely redirects caller

#### Sub-Flow C: Check Hot Lead (`POST /vapi-check-hotlead`)

**What it does:** Checks if the caller qualifies as a high-value "hot lead" requiring immediate human transfer.

**Flow:**
```
Webhook -> Evaluate Hot Lead Thresholds -> IF Hot Lead?
    YES -> Trigger WF-03 (Transfer) + Send Pre-Transfer Email + Return "HOT LEAD"
    NO  -> Return "Not a hot lead"
```

**Hot Lead Thresholds:**
| Policy Type | Threshold | Action |
|-------------|-----------|--------|
| Property | $2,000,000+ estimated value | Immediate transfer to Val |
| Auto | $180,000+ estimated value | Immediate transfer to Val |

---

### WF-03: Hot Lead Transfer Handler

| Property | Value |
|----------|-------|
| **n8n ID** | `AxGXJxHIDQJILOtQ` |
| **Trigger** | Sub-workflow (called from WF-02) |
| **Nodes** | 14 |

**What it does:** Executes the actual call transfer to a human agent for hot leads. Has a primary and secondary transfer number with fallback logic.

**Flow:**
```
Receive from WF-02
    -> Transfer to Primary (Val: +1 808-780-0473)
    -> IF Transfer Success?
        YES -> Update Lead Sheet (transferred)
        NO  -> Try Secondary (+1 808-593-7746)
            -> IF Secondary Success?
                YES -> Update Lead Sheet (transferred via secondary)
                NO  -> Update Lead Sheet (failed)
                    -> Send URGENT Email (callback within 1 hour)
```

**Transfer Numbers:**
| Priority | Number | Person |
|----------|--------|--------|
| Primary | +1 808-780-0473 | Val Char (P&C Agent) |
| Secondary | +1 808-593-7746 | Main Office Line |

**On Transfer Failure:** Sends URGENT email with subject: `URGENT: Hot Lead Transfer Failed -- {name} -- CALLBACK WITHIN 1 HOUR`

---

### WF-04: Existing Customer Handler

| Property | Value |
|----------|-------|
| **n8n ID** | `BNsx9bdXMBKfJjCe` |
| **Webhook** | `POST /vapi-existing-customer` |
| **Nodes** | 5 |

**What it does:** Creates a service ticket for existing customer requests and notifies Val.

**Flow:**
```
Webhook -> Extract Customer Data -> Create Ticket Row -> Send Notification -> Respond to VAPI
```

**Ticket Data Saved:**
- `ticket_id`: Unique ID (call_id + '_existing')
- `caller_name`, `caller_phone`
- `policy_type`
- `request_description`: Summary of what the customer needs
- `status`: "pending"
- `assigned_to`: "Val"
- `created_at`: Timestamp

**Google Sheet:** Tickets Sheet (`1Obobj0x_BmjrnAnSO3DwLkGUd1GXtQvyIIGr4o1PpT8`) -> Tab: `Tickets`

**Email:** Subject: `[Existing Customer] {name} -- {policy_type} -- Callback Requested`

---

### WF-05: Claims Router

| Property | Value |
|----------|-------|
| **n8n ID** | `ZAoSyxR2U2lH2a7b` |
| **Webhook** | `POST /vapi-claim` |
| **Nodes** | 7 |

**What it does:** Handles insurance claim calls with business-hours-aware routing.

**Flow:**
```
Webhook -> Extract Claim Data -> Check Business Hours -> IF Business Hours?
    YES -> Transfer to Val + Send Priority Email -> Respond (transferring)
    NO  -> Send Priority Email -> Respond (callback next business day)
```

**During Business Hours:**
1. Initiates warm transfer to Val (+1 808-780-0473)
2. Sends priority email notification
3. Tells caller: "I'm transferring you to our claims specialist now."

**After Business Hours:**
1. Sends priority email notification
2. Tells caller: "Our team will follow up with you on the next business day."

**Email:** Subject: `CLAIM -- {claim_type} -- {name} -- TRANSFER VIA AI / AFTER HOURS` (HIGH priority)

---

### WF-06: Post-Call Processor

| Property | Value |
|----------|-------|
| **n8n ID** | `nKwYydxwd8n58ExN` |
| **Webhook** | `POST /vapi-call-ended` |
| **Nodes** | 16 |

**What it does:** The most complex workflow. Processes every completed call: merges data, attempts CRM sync, sends smart summary emails, logs analytics, and saves transcripts.

**Flow:**
```
Webhook -> Is End-of-Call Report?
    YES -> Extract All Data -> Read Lead Record -> Merge and Flag
            |
            +-> Write to QQ Catalyst (DISABLED)
            |     -> On Error: Fallback to Google Sheet
            |
            +-> Build Summary Email -> Send Email
                  -> Log Analytics Row -> Save Transcript -> Respond OK
    NO  -> Respond Skip (acknowledge event)
```

**Data Extraction:**
- `call_id`, `call_status`, `call_duration`
- `transcript` (full conversation text)
- `recording_url`
- `ended_reason`
- `caller_phone`, `cost`
- `analysis_summary`

**CRM Sync (QQ Catalyst):**
- Currently **DISABLED** (placeholder API URL)
- All data flagged with `migration_flag: VAPI_AI_COLLECTED`
- When CRM API is connected, data will sync automatically
- On CRM write failure, falls back to Google Sheets

**Smart Email Categories:**
The summary email automatically categorizes based on call outcome:

| Category | Subject Prefix | Triggered When |
|----------|---------------|----------------|
| Hot Lead Transferred | `[HOT LEAD TRANSFERRED]` | Lead was transferred to human agent |
| Disqualified | `[DISQUALIFIED]` | Caller failed qualification rules |
| Transfer Failed | `[TRANSFER FAILED]` | Transfer attempt did not connect |
| Claim | `[CLAIM]` | Call was a claim report |
| Existing Customer | `[EXISTING]` | Existing customer service request |
| Partial (Hung Up) | `[PARTIAL]` | Caller disconnected before completion |
| Qualified Lead | `[QUALIFIED]` | New lead passed all checks |

**Analytics Logged:**
- Date, time, day of week
- Call duration
- Caller phone (masked - last 4 digits only)
- Policy type, intent
- Qualification status, transfer status
- Cross-sell offered/accepted
- Referral source
- Business hours flag
- Priority level
- Call cost

**Transcript Storage:**
- `call_id`, date, `caller_name`
- Full `transcript_text`
- `recording_url` (when available)

**Google Sheets Used:**
- Leads Sheet -> `Leads` tab (read + fallback write)
- Leads Sheet -> `Transcripts` tab (write)
- Analytics Sheet -> `Analytics` tab (write)
- Errors Sheet -> `Errors` tab (error logging)

---

### WF-07: Escalation Monitor

| Property | Value |
|----------|-------|
| **n8n ID** | `aTOUUPC13xwUH6PI` |
| **Trigger** | Cron: every 30 min, Mon-Fri 9am-5pm HST |
| **Nodes** | 5 |

**What it does:** Monitors pending tickets and escalates to Davin if no response after 2 hours.

**Flow:**
```
Cron (every 30 min) -> Read Pending Tickets -> Filter Overdue (2+ hours) -> Send Escalation Email -> Update Ticket (status: escalated)
```

**Escalation Rules:**
- Checks tickets with `status: pending`
- Escalates if `(current_time - created_at) >= 2 hours`
- Sends email to Davin with ticket details
- Updates ticket status to `escalated`

**Email:** Subject: `ESCALATION: {name} waiting {X} hours for callback`

**Google Sheet:** Tickets Sheet (`1Obobj0x_BmjrnAnSO3DwLkGUd1GXtQvyIIGr4o1PpT8`) -> Tab: `Tickets`

---

## 5. Google Sheets Data Model

### Leads Sheet
**ID:** `14FqFY4ZyGDeOluYPhbQKNWmZhyPOwi7FFHpnn5c7CG0`

| Tab | Purpose | Written By | Read By |
|-----|---------|------------|---------|
| **Leads** | All lead data (one row per call) | WF-02, WF-06 | WF-06 |
| **Transcripts** | Full call transcripts | WF-06 | -- |

**Key Leads Columns:**
- `call_id` (unique identifier for each call)
- `caller_name`, `caller_phone`, `caller_email`, `caller_address`
- `caller_dob`, `caller_occupation`
- `policy_type` (home, auto, renters, commercial, etc.)
- `disqualified` (true/false), `disqualifier_reason`
- `hot_lead` (true/false), `hot_lead_reason`, `estimated_value`
- `call_status`, `call_duration`, `ended_reason`
- `migration_flag`: `VAPI_AI_COLLECTED` (for future CRM migration)
- `migration_date`: ISO timestamp

### Tickets Sheet
**ID:** `1Obobj0x_BmjrnAnSO3DwLkGUd1GXtQvyIIGr4o1PpT8`

| Tab | Purpose | Written By | Read By |
|-----|---------|------------|---------|
| **Tickets** | Service requests for existing customers | WF-04 | WF-07 |

**Key Tickets Columns:**
- `ticket_id`, `call_id`
- `caller_name`, `caller_phone`
- `policy_type`, `request_description`
- `status` (pending / escalated / resolved)
- `assigned_to` (Val)
- `escalated` (true/false), `escalated_at`
- `created_at`

### Analytics Sheet
**ID:** `1V2uXB0YuGrRNy8ZGjp1OpxI2OxheOsDRGDZHpwRBAR4`

| Tab | Purpose | Written By |
|-----|---------|------------|
| **Analytics** | Call metrics for reporting | WF-06 |

**Key Analytics Columns:**
- `date`, `time`, `day_of_week`
- `call_duration`, `caller_phone_masked` (last 4 digits)
- `policy_type`, `intent`
- `qualification_status`, `transfer_status`
- `cross_sell_offered`, `cross_sell_accepted`
- `referral_source`, `business_hours`
- `priority`, `cost`

### Errors Sheet
**ID:** `1qF-nC9GRGntn4i-REurbqtzfVii2K4vHc6GCVZ2PgvE`

| Tab | Purpose | Written By |
|-----|---------|------------|
| **Errors** | Error logging for debugging | WF-06 |

**Key Error Columns:**
- `timestamp`, `workflow_id`, `node_name`
- `error_message`, `call_id`
- `resolution_status` (open / resolved)

---

## 6. Email Notifications

All emails are sent via Gmail. During testing, all notifications go to `jephdaligdig98@gmail.com`. In production, they route to the appropriate team member.

### Notification Types

| Trigger | Sender Workflow | Subject Pattern | Priority | Production Recipient |
|---------|----------------|-----------------|----------|---------------------|
| Hot lead pre-transfer | WF-02 | `[HOT LEAD] {name} -- {type} -- ${value}` | Normal | Val |
| Transfer failed | WF-03 | `URGENT: Hot Lead Transfer Failed -- {name}` | HIGH | Val + Davin |
| Existing customer request | WF-04 | `[Existing Customer] {name} -- {type} -- Callback` | Normal | Val |
| Claim reported | WF-05 | `CLAIM -- {type} -- {name} -- TRANSFER/AFTER HOURS` | HIGH | Val |
| Post-call summary | WF-06 | `[{CATEGORY}] Call Summary -- {name}` | Varies | Val |
| Ticket escalation | WF-07 | `ESCALATION: {name} waiting {X} hours` | HIGH | Davin |

---

## 7. Business Rules

### Disqualification Rules
Callers are politely redirected if:
- **3+ insurance claims** in any single year
- **72-hour or less urgency** for property coverage (too time-sensitive for AI)

### Hot Lead Thresholds
Immediate human transfer triggered if:
- **Property estimated value >= $2,000,000**
- **Auto estimated value >= $180,000**

### AI Guardrails
The AI must **NEVER**:
- Give coverage advice
- Bind policies or give quotes
- Sign or underwrite anything
- Guarantee coverage or pricing
- Claim affiliation with Equity Insurance in Tulsa, Oklahoma

The AI must **ALWAYS**:
- State non-affiliation with Equity Insurance in Tulsa, OK
- Flag all AI-collected data with `VAPI_AI_COLLECTED`
- Allow caller to press `#` at any time to reach a human
- Double-check phone numbers (repeat back and confirm)
- Ask callers to spell their names

### Business Hours
- **Monday through Friday:** 9:00 AM - 5:00 PM HST (Hawaii Standard Time)
- **HST = UTC-10** (no daylight saving time in Hawaii)
- Outside business hours: After Hours assistant is used (limited tools, voicemail-style)

### Data Collection Order
1. Full Name (ask to spell)
2. Phone Number (repeat back, confirm)
3. Email Address (for sending quote)
4. Mailing Address (double-check spelling)
5. Date of Birth
6. Occupation (qualifies for P&C credits)
7. Insurance Type
8. Referral Source

---

## 8. VAPI Assistant Configuration

### Two Assistants

| Mode | Assistant ID | When Used |
|------|-------------|-----------|
| Business Hours | `bbf67fe2-99dc-427a-a546-37892f58a796` | Mon-Fri 9am-5pm HST |
| After Hours | `8ae61948-d6c5-4586-9f55-b7c1416db25b` | Evenings, weekends, holidays |

### Voice & Transcription

| Setting | Value |
|---------|-------|
| Voice Provider | ElevenLabs |
| Voice ID | `sarah` (Female, Warm) |
| Transcriber | Deepgram `scribe_v2_realtime` |
| LLM | GPT-4o |

### VAPI Tools (Function Calls)

| Tool Name | Webhook Target | Purpose |
|-----------|----------------|---------|
| `save_field` | WF-02 `/vapi-save-field` | Save individual data fields |
| `check_disqualifier` | WF-02 `/vapi-check-disqualifier` | Check disqualification rules |
| `check_hot_lead` | WF-02 `/vapi-check-hotlead` | Check hot lead thresholds |
| `route_existing_customer` | WF-04 `/vapi-existing-customer` | Handle existing customer requests |
| `route_claim` | WF-05 `/vapi-claim` | Handle insurance claims |

---

## 9. Troubleshooting

### Common Issues

| Issue | Likely Cause | Fix |
|-------|-------------|-----|
| Call goes to voicemail | VAPI not connected or Talkroute misconfigured | Check VAPI dashboard + Talkroute forwarding |
| "Credential access" errors in n8n | Google OAuth token expired | Re-authenticate in n8n Credentials |
| Emails not sending | Gmail OAuth token expired | Re-authenticate Gmail credential in n8n |
| Data not saving to sheets | Google Sheets credential issue | Check credential `6jzp7PcmqFZb8sKc` |
| Hot lead transfer fails | Val's phone unavailable | System tries secondary number, then sends URGENT email |
| Escalation emails not firing | WF-07 might be inactive | Activate WF-07 via n8n dashboard |
| After hours voice wrong | WF-01 After Hours config | Check voice = `sarah`, transcriber = `scribe_v2_realtime` |

### Checking Workflow Status

To verify all workflows are active, use the n8n API:
```bash
curl -s -X GET "https://solarexpresss.app.n8n.cloud/api/v1/workflows" \
  -H "X-N8N-API-KEY: {your-api-key}" | python -m json.tool
```

### Viewing Execution Logs

Recent executions with errors:
```bash
curl -s -X GET "https://solarexpresss.app.n8n.cloud/api/v1/executions?status=error&limit=10" \
  -H "X-N8N-API-KEY: {your-api-key}" | python -m json.tool
```

### Key Credentials

| Credential | n8n ID | Used For |
|-----------|--------|----------|
| Google Sheets OAuth2 | `6jzp7PcmqFZb8sKc` | All Google Sheets operations |
| Gmail OAuth2 | `P7kfjEjjwQs7JnSI` | All email notifications |
| VAPI API Key | `BxJCvZZfiIkt90Ua` | Call transfers (WF-03, WF-05) |

---

## 10. Test Suite

A comprehensive test suite (`test_suite.py`) validates all 7 workflows across 9 scenarios with 26 individual tests.

### Running Tests

```bash
python test_suite.py
```

### Test Scenarios

| Scenario | Tests | What's Validated |
|----------|-------|------------------|
| **S1: New Customer P&C Quote** | 10 | Call router, all save_field types, disqualifier (pass), hot lead (pass) |
| **S2: Hot Lead** | 4 | Save field, disqualifier pass, hot lead property $3.5M, hot lead auto $200K |
| **S3: Disqualified Caller** | 5 | Save field, 5 claims, 48hr urgency, 72hr boundary, 3 claims boundary |
| **S4: Existing Customer** | 1 | Ticket creation + notification |
| **S5: Claims Call** | 1 | Claim routing + priority notification |
| **S6: Post-Call Processing** | 2 | End-of-call for new customer + claim scenario |
| **S7: After Hours Config** | 1 | Voice, transcriber, tools present in after-hours config |
| **S8: Gmail Recipients** | 1 | All 6 Gmail nodes across WF-02 to WF-07 |
| **S9: Workflows Active** | 1 | All 7 workflows are active |

### Expected Output (All Pass)

```
================================================================
  AI RECEPTIONIST - COMPREHENSIVE SCENARIO TEST SUITE
================================================================

=== SCENARIO 1: New Customer P&C Quote Flow ===
S1-T1  PASS  WF-01 Call Router -> assistant config
S1-T2  PASS  save_field(caller_name=Sarah Tanaka)
...
S1-T10  PASS  check_hotlead($800K home) -> Not hot lead

=== SCENARIO 2: Hot Lead - $3.5M Property ===
S2-T1  PASS  save_field(caller_name=James Nakamura)
...
S2-T4  PASS  check_hotlead($200K auto) -> HOT LEAD!

=== SCENARIO 3-9: ... ===

================================================================
  FINAL RESULTS: 26 PASS / 0 FAIL / 26 total
================================================================
  ALL TESTS PASS!
```

---

## Appendix: Inter-Workflow Dependencies

```
WF-01 (routes call)
  |
  +---> VAPI assistant decides intent via conversation
          |
          +---> WF-02 (new customer data collection)
          |       |
          |       +---> WF-03 (hot lead transfer - sub-workflow)
          |
          +---> WF-04 (existing customer ticket)
          |       |
          |       +---> WF-07 (monitors tickets every 30 min)
          |
          +---> WF-05 (claims routing)

After EVERY call:
  +---> WF-06 (post-call processor: email + analytics + transcript)
```

## Appendix: Webhook Endpoints

| Full URL | Workflow |
|----------|----------|
| `https://solarexpresss.app.n8n.cloud/webhook/vapi-call-started` | WF-01 |
| `https://solarexpresss.app.n8n.cloud/webhook/vapi-save-field` | WF-02 (A) |
| `https://solarexpresss.app.n8n.cloud/webhook/vapi-check-disqualifier` | WF-02 (B) |
| `https://solarexpresss.app.n8n.cloud/webhook/vapi-check-hotlead` | WF-02 (C) |
| `https://solarexpresss.app.n8n.cloud/webhook/vapi-existing-customer` | WF-04 |
| `https://solarexpresss.app.n8n.cloud/webhook/vapi-claim` | WF-05 |
| `https://solarexpresss.app.n8n.cloud/webhook/vapi-call-ended` | WF-06 |
