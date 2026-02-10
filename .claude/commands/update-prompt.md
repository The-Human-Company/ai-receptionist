Update the VAPI AI assistant system prompt based on new requirements.

Steps:
1. Read the current system prompt from Section 5 of `n8n-workflow-analysis.md`
2. Ask the user what needs to change (new rules, new scripts, updated compliance, new FAQ answers, etc.)
3. Update the relevant section of the system prompt in `n8n-workflow-analysis.md`
4. If the change affects n8n workflow logic (new disqualifiers, new hot lead thresholds, new routing rules), also update the corresponding Code nodes in `n8n-workflow-vapi-call-handler.json`
5. Show a diff of what changed

Sections that can be updated:
- IDENTITY & COMPLIANCE rules
- GREETING script
- ROUTING RULES
- DATA COLLECTION order/fields
- DISQUALIFIER thresholds
- HOT LEAD thresholds
- FAQ ANSWERS
- CROSS-SELL prompts
- AFTER-HOURS message
