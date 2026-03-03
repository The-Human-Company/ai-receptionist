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

### n8n Workflows (8 Active)

| WF | Name | File | Webhook |
| ---- | ------ | ------ | --------- |
| WF-01 | Inbound Call Router | `n8n-wf01-inbound-call-router.json` | `/vapi-call-started` |
| WF-02 | New Customer P&C Intake | `n8n-wf02-new-customer-intake.json` | `/vapi-save-field`, `/vapi-check-disqualifier`, `/vapi-check-hotlead` |
| WF-03 | Hot Lead Transfer | `n8n-wf03-hot-lead-transfer.json` | Sub-workflow |
| WF-04 | Existing Customer | `n8n-wf04-existing-customer.json` | `/vapi-existing-customer` |
| WF-05 | Claims Router | `n8n-wf05-claims-router.json` | `/vapi-claim` |
| WF-06 | Post-Call Processor | `n8n-wf06-post-call-processor.json` | `/vapi-call-ended` |
| WF-07 | Escalation Monitor | `n8n-wf07-escalation-monitor.json` | Cron schedule |
| WF-08 | SMS Form Sender | `n8n-wf08-sms-form-sender.json` | `/vapi-send-form` |

Legacy (kept as backup):
- **VAPI Call Handler** (`n8n-workflow-vapi-call-handler.json`) - Original monolithic workflow
- **Notifications** (`n8n-workflow-notifications.json`) - Original notification workflow

### Call Flow (3 Branches)
- **New Customer:** Classify -> Collect Data -> Check Disqualifiers -> Check Hot Lead -> Save -> Notify
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
1. Phone Number — via caller ID confirmation ("Is the best number to reach you the one you're calling from?"), press 1/yes to confirm. If not, collect and repeat back for confirmation.
2. Full Name — with last name spelling, read back for confirmation
3. Date of Birth — with confirmation
4. VIN — they won't always have it (numbers captured better than letters); fall back to make/model/year if unavailable
5. Profession — 4-year degree affects quotes
6. Accidents or violations in last 5 years — good to have
7. **SMS form sent** (must) — via Email-to-SMS gateway

## Data Fields — Home Insurance (Collection Order)
1. Phone Number — same caller ID confirmation flow
2. Full Name — with spelling confirmation
3. Date of Birth — with confirmation
4. Profession
5. Owner or Renter
6. Property Address — key info, needs confirmation
7. Claims or losses in last 5 years
8. Property Type — Condo, Single Family Home, other
9. **SMS form sent** (must) — via Email-to-SMS gateway

## SMS Delivery Method
- **Email-to-SMS Gateway** — sends email to carrier-specific addresses (e.g., `8085551234@txt.att.net`)
- Broadcasts to all major US carriers: AT&T, T-Mobile, Verizon, Sprint, US Cellular, Cricket, MetroPCS, Boost, Google Fi
- Only the correct carrier delivers; others silently fail
- Form URL: `https://docs.google.com/forms/d/1nXAAS4HKmuoofX9dqK5vF_llri1zEEThAyOJBI-midk/viewform`
- Twilio/Zapier NOT used (cost/registration barriers)

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
- Gmail credential ID: `YsqH9VLQvq5yEhqJ` (name: "Gmail account") — used by WF-02 through WF-08

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
| `llZY8q1babZHLMXZ` | WF-08 SMS Form Sender (Email-to-SMS Gateway) | Yes | `n8n-wf08-sms-form-sender.json` |

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
