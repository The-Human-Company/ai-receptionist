# n8n Workflow Analysis & Architecture
## Equity Insurance AI Receptionist (VAPI Integration)

---

## 1. PROJECT OVERVIEW

**Client:** Equity Insurance Inc. (Davin Char) - 3rd Generation, Honolulu, HI
**Main Number:** +1 808-593-7746
**Business Hours:** 9am - 5pm HST
**Call Volume:** ~15 calls/day
**Domain:** equityinsurance.services
**CRM:** QQ Catalyst (primary), Levitate AI (marketing/retention)
**Phone System:** Talkroute (mainline with extensions/directory)
**AI Voice Platform:** VAPI.ai + ElevenLabs (Female, Warm tone)

---

## 2. COMPLETE CALL FLOW ARCHITECTURE

```
INCOMING CALL (Talkroute -> VAPI)
         |
         v
[AI GREETING]
"Hello, thank you for calling Equity Insurance.
 I am your AI receptionist. How can I help you
 today, or what kind of insurance are you looking for?"
+ Non-affiliation disclaimer (Tulsa, OK)
         |
         v
[HOURS CHECK] -----> AFTER HOURS (before 6am / after 5pm HST)
    |                      |
    |                      v
    |              [AFTER-HOURS MESSAGE]
    |              "You've reached Equity Insurance outside
    |               of our regular office hours from 9am to 5pm.
    |               If you know your party's extension, dial it
    |               at any time. Otherwise, use our phone directory
    |               and enter the last name of the person you're
    |               trying to reach, or press # to connect with
    |               our AI receptionist, or leave a voice mail
    |               in our general mailbox."
    |
    v
[INTENT ROUTING / IVR MENU]
    |
    |--- [1] NEW CUSTOMER ---------> New Customer Flow
    |--- [2] EXISTING CUSTOMER ----> Existing Customer Flow
    |--- [3] CLAIM ----------------> Claims Flow
    |--- [*] PRESS # AT ANY TIME --> Transfer to Human Agent
```

---

## 3. DETAILED WORKFLOW BRANCHES

### BRANCH A: NEW CUSTOMER FLOW (Primary n8n Workflow)

```
[NEW CUSTOMER IDENTIFIED]
         |
         v
[INSURANCE TYPE DETECTION]
    |
    |--- Life Insurance / Medicare ---> IMMEDIATE TRANSFER TO DAVIN
    |                                   (Script TBD - ask Davin)
    |
    |--- P&C (Auto/Renters/Property/Business) ---> Continue Below
         |
         v
[MANAGING EXPECTATIONS - if Davin requested]
"Davin is currently assisting other clients, but I can
 gather your information now to speed up the quoting
 process for you."
         |
         v
[CORE DATA COLLECTION SEQUENCE]
    |
    |-- 1. Full Name (ask to spell)
    |-- 2. Phone Number (repeat back, confirm until approved)
    |-- 3. Email Address ("for sending your quote")
    |       -> If no email: confirm follow-up will be phone-based
    |-- 4. Mailing Address (double-check all spelling)
    |-- 5. Date of Birth
    |-- 6. Occupation (qualifies for P&C discounts/credits)
    |-- 7. Type of Insurance needed
    |-- 8. Referral Source ("Who referred you to Equity Insurance?
    |       If asked why: 'because we would like to thank the
    |       person who might have referred you.'")
         |
         v
[POLICY-SPECIFIC QUESTIONS]
    |
    |--- AUTO:
    |    - What automobile to insure?
    |    - Lease / bank loan? (additional insured)
    |    - Ticket or accident records?
    |    - Multiple names on title?
    |    - Other people in household with driver license?
    |    - Request copy of current auto policy (upload link in e-form)
    |    -> If auto value > $180,000: FLAG AS HOT LEAD
    |
    |--- RENTERS:
    |    - Estimate of value of possessions
    |    - Property management company (additional insured)
    |
    |--- PROPERTY:
    |    - First-time buyer? (Y/N)
    |    - Claims in past year? (>2 = disqualifier)
    |    - Urgency within 72 hours? (Y/N = disqualifier)
    |    - Claims in past 5 years?
    |    - Request copy of current homeowner's policy (upload link)
    |    -> If property value > $2,000,000: FLAG AS HOT LEAD
    |
    |--- BUSINESS:
    |    - Business start date
    |    - EIN
    |    - Gross Revenue
    |    - Industry & Activity
         |
         v
[CLAIMS CHECK]
"Do you have any current claims?"
    -> Ask type/history
    -> If 3+ claims in 1 year: DISQUALIFIED (polite redirect)
    -> Assure: "Our human agent will follow up to hear the full story"
         |
         v
[CROSS-SELL / PROMOTION OPPORTUNITY]
    -> Mention related policy types
    -> Time-pressure promotions if applicable
    -> Keep brief - defer complex cross-sell to follow-up call
         |
         v
[HOT LEAD CHECK]
    |
    |--- Property > $2M or Auto > $180K
    |    -> IMMEDIATE TRANSFER TO HUMAN
    |
    |--- Normal Lead
    |    -> Continue to wrap-up
         |
         v
[WRAP-UP & DATA SUBMISSION]
    -> Confirm all collected data back to caller
    -> "A member of our team will follow up with your quote"
    -> Provide coverage timeline estimate:
       "Within an hour for simple auto, up to 3 days for complex home"
    -> Thank caller
         |
         v
[n8n POST-CALL AUTOMATION]
    -> Save lead data to QQ Catalyst (with MIGRATION FLAG)
    -> Send notification email to Val (P&C leads)
    -> Send notification email to Val for Commercial follow-up
    -> If Val doesn't respond within 2 hours:
       Emergency notification to Davin
    -> Log call in call tracking system
```

### BRANCH B: EXISTING CUSTOMER FLOW

```
[EXISTING CUSTOMER IDENTIFIED]
         |
         v
[AI ASKS]
"What are you calling about specifically? How can I help you?"
         |
         v
[COLLECT INFO]
    -> Which policy type (new or existing) they need help with
    -> Contact info for callback
    -> Match policy type to appropriate team member
         |
         v
[DURING OFFICE HOURS]
    -> If customer asks for transfer: transfer to agent
    -> Otherwise: "A live agent will get back to you
       in the next few hours"
         |
         v
[OUTSIDE OFFICE HOURS]
    -> Send to voicemail
         |
         v
[n8n POST-CALL AUTOMATION]
    -> Send info to Val immediately
    -> If Val doesn't reply within 2 hours:
       Emergency notification to Davin
    -> Make collected info available to human agent (Knowledge base / RAG)
```

### BRANCH C: CLAIMS FLOW

```
[CLAIM IDENTIFIED]
         |
         v
[ROUTE TO EXISTING CLAIMS PROCESS]
    -> Transfer to appropriate agent
    -> If no answer: voicemail with callback promise
```

---

## 4. n8n WORKFLOW NODES (Technical Architecture)

### WORKFLOW 1: VAPI Call Handler (Main Orchestrator)

```
Node 1: [Webhook Trigger - VAPI Webhook]
    - Receives: call_started, call_ended, transcript, function_call events
    - From: VAPI.ai webhook endpoint
    |
    v
Node 2: [Switch Node - Event Router]
    - Routes based on event type:
      -> call_started -> Node 3
      -> function_call -> Node 4
      -> call_ended -> Node 10
    |
    v
Node 3: [Function Node - Hours Check]
    - Check current time against HST business hours (9am-5pm)
    - Output: { isBusinessHours: true/false }
    - If after hours -> trigger after-hours VAPI response
    |
    v
Node 4: [Switch Node - Function Router]
    - Routes based on VAPI function_call name:
      -> "classify_caller" -> Node 5
      -> "collect_data" -> Node 6
      -> "check_disqualifiers" -> Node 7
      -> "check_hot_lead" -> Node 8
      -> "transfer_call" -> Node 9
    |
    v
Node 5: [Function Node - Caller Classification]
    - Inputs: caller intent from VAPI transcript
    - Logic: Classify as NEW / EXISTING / CLAIM
    - For NEW: sub-classify as LIFE_MEDICARE or P_AND_C
    - Output: { callerType, insuranceCategory }
    |
    v
Node 6: [Function Node - Data Validator]
    - Validates collected fields:
      name, phone, email, address, dob, occupation, insurance_type,
      referral_source, policy_specific_data, claims_history
    - Flags missing required fields
    - Returns validation status to VAPI
    |
    v
Node 7: [Function Node - Disqualifier Check]
    - Rules:
      -> claims_past_year >= 3 -> DISQUALIFIED
      -> urgency_72h == true AND policy == "property" -> DISQUALIFIED
    - Output: { qualified: true/false, reason: string }
    |
    v
Node 8: [Function Node - Hot Lead Detection]
    - Rules:
      -> property_value > 2000000 -> HOT_LEAD
      -> auto_value > 180000 -> HOT_LEAD
    - Output: { isHotLead: true/false, reason: string }
    - If HOT_LEAD -> trigger immediate transfer via VAPI
    |
    v
Node 9: [HTTP Request Node - VAPI Transfer]
    - Calls VAPI API to transfer call to human agent
    - Transfer targets:
      -> Life/Medicare -> Davin's extension
      -> P&C Hot Lead -> Val / Davin (TBD)
      -> General P&C -> Val
      -> # pressed -> Next available agent
    |
    v
Node 10: [Function Node - Call End Handler]
    - Extracts final transcript and collected data
    - Prepares structured lead data object
    - Adds MIGRATION FLAG for future CRM migration
    - Triggers post-call workflows
```

### WORKFLOW 2: CRM Data Sync (Post-Call)

```
Node 1: [Webhook Trigger - Internal]
    - Receives structured lead data from Workflow 1
    |
    v
Node 2: [Function Node - Data Formatter]
    - Formats data for QQ Catalyst API
    - Adds migration_flag: "VAPI_AI_COLLECTED"
    - Adds timestamp, call_id, source: "ai_receptionist"
    - Structure:
      {
        migration_flag: "VAPI_AI_COLLECTED",
        caller_type: "new_customer",
        personal: { name, phone, email, address, dob, occupation },
        insurance: { type, policy_specific_data },
        qualification: { claims_history, disqualified, hot_lead },
        referral_source: string,
        call_metadata: { call_id, duration, timestamp, transcript_url }
      }
    |
    v
Node 3: [HTTP Request Node - QQ Catalyst API]
    - POST lead data to QQ Catalyst
    - Endpoint: TBD (needs Talkroute/QQ API access)
    - Auth: TBD (needs credentials from Davin)
    |
    v
Node 4: [IF Node - Success Check]
    -> Success -> Node 5
    -> Failure -> Node 7 (Error Handler)
    |
    v
Node 5: [Function Node - Confirmation]
    - Log successful CRM entry
    - Prepare notification data
```

### WORKFLOW 3: Notification & Escalation Engine

```
Node 1: [Webhook Trigger - Internal]
    - Receives lead data + notification type
    |
    v
Node 2: [Switch Node - Notification Router]
    -> new_p_and_c_lead -> Node 3
    -> hot_lead -> Node 4
    -> existing_customer -> Node 5
    -> escalation_timeout -> Node 6
    |
    v
Node 3: [Email Node - Val Notification]
    - To: val@equityinsurance.services
    - Subject: "New P&C Lead - [Name] - [Insurance Type]"
    - Body: Formatted lead summary
    - Include all collected data
    |
    v
Node 4: [Email Node - Hot Lead Alert]
    - To: Davin + Val
    - Subject: "HOT LEAD - [Name] - $[Value]"
    - Priority: HIGH
    - Body: Full details + "Immediate follow-up required"
    |
    v
Node 5: [Email Node - Existing Customer Info]
    - To: val@equityinsurance.services
    - Body: Customer request details + contact info
    |
    v
Node 6: [Wait Node - 2 Hour Timer]
    - Wait 2 hours
    - Check if Val has responded (via webhook/flag)
    |
    v
Node 6b: [IF Node - Val Response Check]
    -> Responded -> END
    -> No Response -> Node 7
    |
    v
Node 7: [Email/SMS Node - Davin Emergency Alert]
    - To: Davin (cell/email)
    - Subject: "URGENT: Unhandled Lead - [Name]"
    - "Val has not responded within 2 hours"
```

### WORKFLOW 4: After-Hours Handler

```
Node 1: [Webhook Trigger - VAPI After Hours]
    - Triggered when call comes in outside 9am-5pm HST
    |
    v
Node 2: [Function Node - After Hours Response]
    - Returns script for VAPI to speak:
      "You've reached Equity Insurance outside of our regular
       office hours from 9am to 5pm. If you know your party's
       extension, dial it at any time. Otherwise you can use
       our phone directory and enter the last name of the person
       you're trying to reach, or press # to connect with our
       AI receptionist, or leave a voice mail in our general
       mailbox."
    |
    v
Node 3: [IF Node - Caller Choice]
    -> # pressed -> Continue to AI Receptionist (Workflow 1)
    -> Extension dialed -> Talkroute handles
    -> Voicemail -> Node 4
    |
    v
Node 4: [Function Node - Voicemail Logger]
    - Log voicemail with timestamp
    - Send notification for morning callback
```

---

## 5. VAPI ASSISTANT CONFIGURATION

### System Prompt (Core Instructions)

```
You are the trained AI receptionist for Equity Insurance, a 3rd-generation
family-owned insurance agency in Honolulu, Hawaii.

IDENTITY:
- You are an AI receptionist, NOT a licensed agent
- You NEVER give coverage advice, bind policies, sign documents, or underwrite
- You NEVER offer guarantees of any kind
- You collect information and promote services ONLY

MANDATORY DISCLAIMER (say after greeting):
"Please note, we are not associated with Equity Insurance company in Tulsa, Oklahoma."

GREETING:
"Hello, thank you for calling Equity Insurance. I am your AI receptionist.
How can I help you today, or what kind of insurance are you looking for?"

TONE:
- Warm, friendly, empathetic
- Professional but approachable
- Acknowledge that insurance questions can feel complex
- Be patient when collecting sensitive data (claims, financial details)

ROUTING RULES:
- Life Insurance or Medicare -> Transfer to Davin immediately
- P&C (Auto, Renters, Property, Business) -> Collect information
- At ANY time caller presses # -> Transfer to human agent during hours
  or voicemail outside hours

DATA COLLECTION (in this order):
1. Full name (ask to spell)
2. Phone number (repeat back, confirm)
3. Email address ("for sending your quote") - if none, note phone follow-up
4. Mailing address (double-check spelling)
5. Date of birth
6. Occupation
7. Insurance type needed
8. Referral source

DISQUALIFIERS (handle politely):
- 3+ claims in past year -> "Based on the information you've shared,
  your situation may require specialized attention. Let me connect
  you with one of our agents who can better assist you."
- Needs coverage within 72 hours (property) -> Same polite redirect

HOT LEADS (transfer immediately):
- Property valued over $2,000,000
- Automobile valued over $180,000
- "This is something our senior team would love to help you with personally.
  Let me connect you right away."

COVERAGE TIMELINE (if asked):
- Simple auto: "within an hour in some cases"
- Complex home: "up to 3 days on average"
- General: "Depending on your situation, it can vary from within a day
  up to 3 days on average."

WHAT WE DO NOT OFFER:
- Pet Insurance
- Travel Insurance
- Private Mortgage Insurance (Federal loan, Freddie Mac)
  (BUT we DO offer Mortgage Protection)

CROSS-SELL:
- Briefly mention related coverage types
- Keep initial call focused on core data
- Defer complex cross-sell questions to follow-up

ALWAYS SAY:
"We are always of service, this is how we approach our duties."

IF ASKED "What do I need for a quote?":
"The basic information we need is your name, address, date of birth,
email address, phone number, and occupation."

IF DAVIN IS REQUESTED FOR P&C:
"Davin is currently assisting other clients, but I can gather your
information now to speed up the quoting process for you."
```

---

## 6. INTEGRATION MAP

```
+------------------+       +------------------+       +------------------+
|    TALKROUTE     |       |     VAPI.ai      |       |      n8n         |
|  (Phone System)  | ----> |  (AI Voice/LLM)  | ----> |  (Orchestrator)  |
|                  |       |  + ElevenLabs     |       |                  |
| - Mainline       |       |  (Voice)         |       | - Call Handler   |
| - Extensions     |       |                  |       | - CRM Sync       |
| - Directory      |       | - Greeting       |       | - Notifications  |
| - Call Recording |       | - Data Collection|       | - Escalation     |
+------------------+       | - Classification |       | - After Hours    |
                           | - Transfer       |       +--------+---------+
                           +------------------+                |
                                                               |
                    +------------------------------------------+
                    |                    |                      |
                    v                    v                      v
          +------------------+  +------------------+  +------------------+
          |   QQ CATALYST    |  |   EMAIL (SMTP)   |  |   LEVITATE AI    |
          |     (CRM)        |  |                  |  |   (Marketing)    |
          |                  |  | - Val alerts     |  |                  |
          | - Lead storage   |  | - Davin escalate |  | - Follow-up      |
          | - Migration flag |  | - Hot lead alert |  |   campaigns      |
          | - Policy data    |  | - After-hours    |  | - Cross-sell     |
          +------------------+  +------------------+  +------------------+
```

---

## 7. DATA SCHEMA (Lead Object)

```json
{
  "id": "uuid",
  "migration_flag": "VAPI_AI_COLLECTED",
  "source": "ai_receptionist",
  "created_at": "2026-02-10T14:30:00-10:00",
  "call_id": "vapi_call_123",
  "call_duration_seconds": 420,
  "caller_type": "new_customer | existing_customer | claim",

  "personal_info": {
    "full_name": "John Smith",
    "name_spelling_confirmed": true,
    "phone": "+18085551234",
    "phone_confirmed": true,
    "email": "john@example.com",
    "mailing_address": {
      "street": "123 Aloha St",
      "city": "Honolulu",
      "state": "HI",
      "zip": "96825"
    },
    "date_of_birth": "1985-03-15",
    "occupation": "Engineer"
  },

  "insurance_request": {
    "type": "auto | renters | property | business | life | medicare",
    "specific_needs": "Full coverage for new vehicle",
    "is_first_time_buyer": false,
    "current_policy_document_uploaded": false
  },

  "policy_specific_data": {
    "auto": {
      "vehicle_description": "2025 Toyota Camry",
      "estimated_value": 35000,
      "lease_or_loan": "loan",
      "additional_insured": "Bank of Hawaii",
      "tickets_accidents": "none",
      "multiple_title_names": false,
      "other_household_drivers": 1
    },
    "renters": {
      "possession_value_estimate": 15000,
      "property_management_company": "ABC Property Mgmt"
    },
    "property": {
      "property_value": 850000,
      "first_time_buyer": false,
      "claims_past_year": 0,
      "claims_past_5_years": 1,
      "urgency_72h": false,
      "specific_coverage": "hurricane"
    },
    "business": {
      "business_name": "ABC Corp",
      "start_date": "2020-01-15",
      "ein": "12-3456789",
      "annual_revenue": 500000,
      "industry": "Restaurant",
      "activity": "Food service"
    }
  },

  "qualification": {
    "qualified": true,
    "disqualified_reason": null,
    "is_hot_lead": false,
    "hot_lead_reason": null,
    "claims_history": {
      "has_current_claims": false,
      "claim_types": [],
      "claims_count_past_year": 0
    }
  },

  "referral_source": "Google Search",
  "cross_sell_opportunities": ["renters", "life"],
  "follow_up_method": "email",

  "routing": {
    "assigned_to": "Val",
    "transfer_attempted": false,
    "transfer_successful": false,
    "escalated_to_davin": false,
    "notification_sent_at": "2026-02-10T14:35:00-10:00",
    "escalation_deadline": "2026-02-10T16:35:00-10:00"
  },

  "transcript_url": "https://vapi.ai/transcripts/call_123"
}
```

---

## 8. IMPLEMENTATION PHASES

### Phase 1: Pilot (90 Days) - CURRENT
- VAPI + ElevenLabs voice setup
- n8n workflows 1-4 (Call Handler, CRM Sync, Notifications, After-Hours)
- QQ Catalyst integration (with migration flags)
- Talkroute connection
- New Customer P&C flow only
- Manual monitoring and tuning

### Phase 2: Expansion
- Existing Customer flow buildout
- Automated email to carriers with underwriting info (Davin requested this)
- Levitate AI integration for follow-up campaigns
- Cross-sell automation
- CRM consolidation/migration (using flagged data)

### Phase 3: Scale
- Full IVR menu implementation
- Knowledge base / RAG for existing customer lookups
- Advanced analytics dashboard
- Multi-agent routing optimization

---

## 9. BLOCKERS / DEPENDENCIES (Must Resolve Before Build)

| # | Blocker | Owner | Status |
|---|---------|-------|--------|
| 1 | Talkroute login/access + connection method (SIP/API/forwarding) | Davin | PENDING |
| 2 | QQ Catalyst API access + credentials | Davin | PENDING |
| 3 | Transfer person details (Name, Role, Phone for each branch) | Davin | PENDING |
| 4 | Existing Customer workflow definition | Davin + Val | PENDING |
| 5 | After-Hours exact script approval | Davin | PENDING |
| 6 | Recorded call samples delivery method | Davin | PENDING |
| 7 | Life/Medicare transfer script (ask Davin) | Davin | PENDING |
| 8 | Val interview for call-handling nuances | Francis | PENDING |

---

## 10. COMPLIANCE RULES (Hard-Coded)

1. AI must NEVER give specific coverage advice
2. AI must NEVER bind a policy or act as licensed agent
3. AI must NEVER offer guarantees
4. AI must NEVER sign or underwrite
5. AI must ALWAYS state non-affiliation with Equity Insurance (Tulsa, OK)
6. AI must ALWAYS state: "We are always of service"
7. All data collected must be flagged with `VAPI_AI_COLLECTED` for migration
8. Caller can ALWAYS press # to reach human during business hours / voicemail after hours
9. 24/7 troubleshooting available via email + live chat
