# AI Receptionist Project - Equity Insurance

## Project Overview
Building a VAPI-powered AI receptionist for **Equity Insurance Inc.** (Davin Char), a 3rd-generation family-owned insurance agency in Honolulu, HI. The AI handles inbound calls on the main line (+1 808-593-7746), collects lead data for P&C policies, and routes calls to the human team.

## Tech Stack
- **Voice AI:** VAPI.ai + ElevenLabs (Female, Warm tone)
- **Orchestration:** n8n (workflow automation)
- **Phone System:** Talkroute (mainline with extensions/directory)
- **CRM:** QQ Catalyst (primary), Levitate AI (marketing/retention)
- **Language:** JavaScript/Node.js (n8n Code nodes)

## Key Architecture
```
Talkroute -> VAPI.ai (voice + LLM) -> n8n (orchestrator) -> QQ Catalyst + Email + Levitate
```

### n8n Workflows
1. **VAPI Call Handler** (`n8n-workflow-vapi-call-handler.json`) - Main webhook handler for all VAPI events
2. **Notifications** (`n8n-workflow-notifications.json`) - Email alerts + 2hr escalation to Davin
3. **CRM Sync** (TBD) - Push lead data to QQ Catalyst with migration flags
4. **After-Hours** (TBD) - Handle calls outside 9am-5pm HST

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

## Data Fields (Quote Collection Order)
1. Full Name (ask to spell)
2. Phone Number (repeat back, confirm)
3. Email Address (for sending quote)
4. Mailing Address (double-check spelling)
5. Date of Birth
6. Occupation (qualifies for P&C credits)
7. Insurance Type
8. Referral Source

## Project Files
- `deliverables/` - Client briefing documents, transcripts, analysis PDFs
- `n8n-workflow-analysis.md` - Complete workflow architecture & documentation
- `n8n-workflow-vapi-call-handler.json` - Main n8n workflow (importable)
- `n8n-workflow-notifications.json` - Notification/escalation workflow (importable)

## n8n Deployment
- **Instance:** https://n8n.nomanuai.com
- API key stored in `.env` (never committed to git)
- All workflows use `Pacific/Honolulu` timezone
- Execution data saved for debugging during pilot phase

### Live Workflow IDs
| n8n ID | Name | Active | Local File | Nodes |
|--------|------|--------|------------|-------|
| `1IX82-PqM5HiZq7sUSfpf` | Equity Insurance - VAPI AI Receptionist (Main) | Yes | `n8n-workflow-vapi-call-handler.json` | 13 nodes |
| `5LCW3l7WBBOClWIV` | Equity Insurance - Post-Call Notifications & Escalation | No* | `n8n-workflow-notifications.json` | 9 nodes |
| `kVAZboMRFcblG1qX` | WCRAv3 Error Handler | Yes | — | — |
| `O4Edwi1Wa1cSqbUz` | Weekly Campaign Report v3 | No | — | — |
| `bFjs13pY08N5Lnct` | Ravi-test | No | — | — |

*Notifications workflow needs SMTP credentials configured on n8n before activation.

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
