Simulate a call flow through the n8n workflow to test logic paths.

Steps:
1. Read `n8n-workflow-vapi-call-handler.json` and `n8n-workflow-notifications.json`
2. Ask the user for a test scenario:
   - Caller type: New Customer / Existing Customer / Claim
   - Insurance type: Auto / Renters / Property / Business / Life / Medicare
   - Include specific test values (property value, claims count, etc.)
3. Walk through the workflow node by node, showing:
   - Which Switch branch is taken at each routing node
   - What each Code node outputs given the test input
   - Which notification emails would fire
   - Whether escalation timer would trigger
4. Flag any issues found:
   - Missing routing paths
   - Edge cases not handled
   - Data validation gaps
5. Suggest fixes if issues are found

Example scenarios to offer:
- "New customer wanting renters insurance, no claims"
- "New customer with $3M property (hot lead)"
- "Customer with 4 claims in past year (disqualified)"
- "Existing customer calling about policy change"
- "Call at 11pm HST (after hours)"
- "Caller asks for Davin for a P&C matter"
- "Life insurance inquiry (immediate transfer)"
