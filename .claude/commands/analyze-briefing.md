Analyze a new briefing document or meeting notes and extract actionable items for the AI receptionist build.

Steps:
1. Read all files in the `deliverables/` directory to understand existing context
2. Read the new document the user provides (path or pasted content)
3. Extract and categorize findings into:
   - **Confirmed Items** - New decisions or approvals
   - **Changed Requirements** - Anything that modifies existing workflow logic
   - **New Data Fields** - Additional info the AI needs to collect
   - **New Business Rules** - Disqualifiers, routing changes, compliance updates
   - **Resolved Blockers** - Items from the pending blockers list that are now answered
   - **New Blockers** - New questions or dependencies discovered
4. For each changed requirement, identify which files need updating:
   - `n8n-workflow-analysis.md` (architecture doc)
   - `n8n-workflow-vapi-call-handler.json` (main workflow)
   - `n8n-workflow-notifications.json` (notifications)
   - `CLAUDE.md` (project context)
5. Ask the user if they want to apply the changes automatically
