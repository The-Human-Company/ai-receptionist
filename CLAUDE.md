# AI Receptionist Project - Equity Insurance

## Project Overview
Building a VAPI-powered AI receptionist for **Equity Insurance Inc.** (Davin Char), a 3rd-generation family-owned insurance agency in Honolulu, HI. The AI handles inbound calls on the main line (+1 808-593-7746), collects lead data for P&C policies, and routes calls to the human team.

## Tech Stack
- **Voice AI:** VAPI.ai + ElevenLabs (Female, Warm tone)
- **Orchestration:** n8n (workflow automation)
- **Phone System:** Talkroute (mainline with extensions/directory)
- **CRM:** QQ Catalyst (primary), Levitate AI (marketing/retention)
- **SMS:** Twilio (outbound SMS for Google Form links)
- **Language:** JavaScript/Node.js (n8n Code nodes)

## Key Architecture
```
Talkroute -> VAPI.ai (voice + LLM) -> n8n (orchestrator) -> QQ Catalyst + Email + Levitate
```

### n8n Workflows (9 Active)

| WF | Name | File | Webhook |
| ---- | ------ | ------ | --------- |
| WF-01 | Inbound Call Router | `n8n-wf01-inbound-call-router.json` | `/vapi-call-started` |
| WF-02 | New Customer P&C Intake | `n8n-wf02-new-customer-intake.json` | `/vapi-save-field`, `/vapi-check-disqualifier`, `/vapi-check-hotlead` |
| WF-03 | Hot Lead Transfer + Flag | `n8n-wf03-hot-lead-transfer.json` | Sub-workflow (SMS flag to Val + transfer) |
| WF-04 | Existing Customer | `n8n-wf04-existing-customer.json` | `/vapi-existing-customer` |
| WF-05 | Claims Router | `n8n-wf05-claims-router.json` | `/vapi-claim` |
| WF-06 | Post-Call Processor | `n8n-wf06-post-call-processor.json` | `/vapi-call-ended` |
| WF-07 | Escalation + ACK Monitor | `n8n-wf07-escalation-monitor.json` | Cron (every 10 min) + `/vapi-ack-escalation` |
| WF-08 | SMS Form Sender | `n8n-wf08-sms-form-sender.json` | `/vapi-send-form` |
| WF-09 | Form Reminder Monitor | `n8n-wf09-form-reminder-monitor.json` | Cron (every 1 hour, multi-tier) |

Legacy (kept as backup):
- **VAPI Call Handler** (`n8n-workflow-vapi-call-handler.json`) - Original monolithic workflow
- **Notifications** (`n8n-workflow-notifications.json`) - Original notification workflow

### Call Flow (3 Branches)
- **New Customer:** Classify -> Collect Data -> Check Disqualifiers -> Check Hot Lead -> Save -> Send Intake Form -> Confirm Receipt -> End Call
- **Existing Customer:** Collect request + contact -> Notify Val -> 2hr escalation
- **Claim:** Route to claims agent directly

## Business Rules (CRITICAL)
- AI must NEVER give coverage advice, bind policies, sign, underwrite, or guarantee anything
- AI must ALWAYS state non-affiliation with Equity Insurance in Tulsa, Oklahoma
- All AI-collected data MUST be flagged with `VAPI_AI_COLLECTED` for future CRM migration
- Hot leads: Property > $2M or Auto > $180K -> immediate human transfer
- Disqualifiers: 3+ claims/year or 72hr urgency (property) -> polite redirect
- Caller can press # at ANY time to reach human agent
- Business hours: 9am-5pm HST (UTC-10)

## Key Contacts
- **Davin Char** - CEO/Owner (Life/Medicare + high-value leads)
- **Val Char** - P&C Agent, Davin's mother (+1 808 780 0473, val@equityinsurance.services)
- **Domain:** equityinsurance.services

## Data Fields — Auto Insurance (Collection Order)

1. Phone Number — caller ID confirmation ("Is the best number to reach you the one you're calling from?"), press 1/yes. If not, collect and READ BACK full number for confirmation.
2. Full Name — with last name spelling. READ back full name AND SPELL back last name letter by letter for confirmation.
3. Date of Birth — READ back to confirm. Then say: "We'll text you an intake form right away to get everything confirmed."
4. VIN — fall back to a) Make b) Model c) Year if unavailable. READ back to confirm.
5. Profession — 4-year degree affects quotes
6. Traffic violations or accidents in last 5 years — for each, ask what happened and outcome
7. Closing — brief recap, confirm → call `send_form_link` → AI says "I just sent you your intake form via text" → confirms prospect received SMS → invites them to fill out and submit → thanks and ends call

## Data Fields — Home Insurance (Collection Order)

1. Phone Number — same caller ID confirmation flow as auto
2. Full Name — same READ back + SPELL back as auto
3. Date of Birth — READ back to confirm. Then say: "We'll text you an intake form right away to get everything confirmed."
4. Profession — discount mention
5. Owner or Renter — determines policy type and form routing (homeowners/condo/renters)
6. Property Address — key info, MUST READ back full address and confirm (DTMF 1/2)
7. Claims or losses in last 5 years — for each, ask what happened and outcome
8. Property Type — Condo, Single Family Home, other
9. Closing — same as auto: recap → send form → confirm receipt → invite to fill out → end call

## Post-Call Form Monitoring (WF-09)

- WF-08 logs every SMS sent to `FormTracking` Google Sheet tab (call_id, phone, name, type, form_url, timestamp)
- WF-09 runs **every 1 hour** with multi-tier reminders:
  - **Tier 1 (1 hour):** Gentle nudge — "Just a friendly reminder to fill out your intake form..."
  - **Tier 2 (12 hours):** Half-day — "We noticed your intake form hasn't been submitted yet..."
  - **Tier 3 (24 hours):** Final reminder — "This is our final reminder about your intake form..."
- Tracks `reminder_count` (1/2/3) instead of boolean, so each tier fires once
- Emails Val about each reminder sent
- **Form Completion Detection:** Google Apps Script (`google-apps-script-form-completion.js`) installed on each Google Form:
  - Detects form submission → marks `form_completed=true` in FormTracking sheet
  - Sends confirmation SMS to prospect: "We received your intake form — mahalo!"
  - Notifies Val via email that form was completed
  - Sends webhook to n8n (`/vapi-form-completed`) to stop reminder loop

## Hot Lead Escalation Acknowledgment Loop

- When AI detects a hot lead during a call (Property >$2M, Auto >$180K):
  1. **Immediate SMS to Val** with prospect details + "Reply ACK to confirm"
  2. Logged to `EscalationTracking` Google Sheet tab
  3. Call transferred to Val via VAPI
- **WF-07 monitors every 10 minutes:**
  - If Val doesn't ACK within 30 min → SMS escalation to Davin
  - If Davin doesn't ACK within 30 min → URGENT email to both Val + Davin
  - When someone replies "ACK" → marked as acknowledged, loop ends
- **Twilio inbound webhook** (`/vapi-ack-escalation`) handles ACK SMS replies

## SMS Delivery Method
- **Twilio SMS** — sends SMS directly via Twilio API (n8n Twilio node)
- Phone numbers formatted as E.164 (e.g., `+18085551234`)
- Twilio credential in n8n: `twilioApi` (Account SID + Auth Token)
- Twilio phone number set via n8n environment variable `TWILIO_PHONE_NUMBER`
- Form URLs (routed by `insurance_type` in WF-08):

| Insurance Type | Form Name | Form ID |
|----------------|-----------|---------|
| `auto` / `vehicle` | Vehicle Insurance Intake Form | `1nXAAS4HKmuoofX9dqK5vF_llri1zEEThAyOJBI-midk` |
| `commercial_auto` / `business` | Commercial Auto Insurance Intake Form | `1ye5IHu-M60EVFPcmfYjQ53zoHLFVSuOp9yoVJ-dYmFY` |
| `homeowners` / `home` / `property` | Home Insurance Policy Intake Form | `1ZkpKXF_ikkMHCrbYMa7Nw5M8x7STbU6nOXe18kSa0RI` |
| `condo` | Homeowners Condo Policy Quote Intake Form | `1a4SelYXb12Ihofm2G4Z8Kmj1vilLvhcFI5QvzufBg_4` |
| `renters` | Homeowners/Renters Policy Quote Intake Form | `1UJZb20UgfubgeLkqe3BhmSwQVcDJke_5X8X17p2m_kc` |
| `dwelling_fire` | Dwelling Fire Policy Quote Intake Form | `1xPRCet_wFHhITOHsa8aEcSc__n5gtXhf18SKuHUBoIM` |

## Project Files
- `deliverables/` - Client briefing documents, transcripts, analysis PDFs
- `n8n-workflow-analysis.md` - Complete workflow architecture & documentation
- `n8n-workflow-vapi-call-handler.json` - Main n8n workflow (importable)
- `n8n-workflow-notifications.json` - Notification/escalation workflow (importable)

## n8n Deployment
- **Primary Instance:** https://n8n.nomanuai.com (self-hosted, N8N_API_KEY_2 / N8N_INSTANCE_URL_2)
- **Legacy Instance:** https://solarexpresss.app.n8n.cloud/ (execution limit reached, N8N_API_KEY / N8N_INSTANCE_URL)
- API keys stored in `.env` (never committed to git)
- All workflows use `Pacific/Honolulu` timezone
- Execution data saved for debugging during pilot phase
- Gmail credential ID: `YsqH9VLQvq5yEhqJ` (name: "Gmail account") — used by WF-02 through WF-07
- Twilio credential: `twilioApi` (Account SID + Auth Token) — used by WF-08, WF-09
- Twilio from-number: `+18087451420` (hardcoded in WF-08 and WF-09 Twilio nodes)

### Live Workflow IDs (n8n.nomanuai.com)
| n8n ID | Name | Active | Local File |
|--------|------|--------|------------|
| `uDw59X1Z2JR7qd5Q` | Equity Insurance - VAPI AI Receptionist (Main) | Yes | `n8n-workflow-vapi-call-handler.json` |
| `K24yQ9qLJzSJy8n1` | WF-01 Inbound Call Router | Yes | `n8n-wf01-inbound-call-router.json` |
| `iR0Y35KkqyJkEVVG` | WF-02 New Customer P&C Intake | Yes | `n8n-wf02-new-customer-intake.json` |
| `ZAUyRX2R5zBpE4YA` | WF-03 Hot Lead Transfer Handler | Yes | `n8n-wf03-hot-lead-transfer.json` |
| `EXIC9N6XRr3NMX1h` | WF-04 Existing Customer Handler | Yes | `n8n-wf04-existing-customer.json` |
| `gSAwJdQndD8qq8TW` | WF-05 Claims Router | Yes | `n8n-wf05-claims-router.json` |
| `zBApWWRhk7QbEgyT` | WF-06 Post-Call Processor | Yes | `n8n-wf06-post-call-processor.json` |
| `OY8BUOfSoFZ5BJfb` | WF-07 Escalation Monitor | Yes | `n8n-wf07-escalation-monitor.json` |
| `llZY8q1babZHLMXZ` | WF-08 SMS Form Sender (Twilio) | Yes | `n8n-wf08-sms-form-sender.json` |
| `biRgLz1LTLgX10s3` | WF-09 Form Reminder Monitor | Yes | `n8n-wf09-form-reminder-monitor.json` |

**Note:** Self-hosted n8n wraps webhook POST body under `$json.body`, so expressions use `($json.body?.message || $json.message)` for cross-instance compatibility.

## Slash Commands

### n8n API Skills (Full REST API coverage)
| Command | Purpose |
|---------|---------|
| `/n8n-api` | **Master router** — routes to any n8n API endpoint (start here if unsure) |
| `/n8n-workflows` | Manage workflows: list, get, create, update, delete, activate, deactivate, transfer, tags |
| `/n8n-executions` | Manage executions: list, get, delete, retry |
| `/n8n-credentials` | Manage credentials: list, create, update, delete, get schema, transfer |
| `/n8n-tags` | Manage tags: list, get, create, update, delete |
| `/n8n-variables` | Manage environment variables: list, create, update, delete |
| `/n8n-projects` | Manage projects: list, create, update, delete, user management |
| `/n8n-users` | Manage users: list, get, invite, delete, change role |
| `/n8n-datatables` | Manage DataTables: CRUD tables + CRUD rows |
| `/n8n-audit` | Run security audit + source control pull |

### Legacy/Specialized Deploy Skills
| Command | Purpose |
|---------|---------|
| `/update-n8n-workflow` | Update an existing workflow via PUT (guided step-by-step) |
| `/deploy-workflow` | Deploy workflow with full template system (guided step-by-step) |

### Project Skills
| Command | Purpose |
|---------|---------|
| `/workflow-status` | Audit workflow JSONs for completeness |
| `/add-vapi-function` | Add new VAPI function handler node |
| `/update-prompt` | Modify VAPI system prompt |
| `/add-notification` | Add notification type to escalation workflow |
| `/analyze-briefing` | Ingest new briefing docs and extract changes |
| `/blockers` | Manage project blockers list |
| `/test-flow` | Simulate a call scenario through workflow logic |

## Pending Blockers
1. Talkroute access/credentials (SIP/API connection method)
2. QQ Catalyst API access
3. Transfer person details (name, role, phone per branch)
4. Life/Medicare transfer script
5. Val interview for call-handling nuances
6. Existing Customer workflow details
7. After-Hours script approval
8. Recorded call samples delivery
