Add a new notification type to the post-call notification workflow.

Steps:
1. Read `n8n-workflow-notifications.json`
2. Ask the user what the notification is for (trigger condition, recipient, priority, content)
3. Add a new route in the "Route Notification Type" Switch node
4. Create a new Email Send node with an HTML template containing the relevant lead data fields
5. If the notification needs escalation, connect it to the "Wait 2 Hours" -> "Escalate to Davin" chain
6. Update the "Parse & Classify Notification" Code node to detect the new notification type
7. Write the updated workflow JSON back to disk
8. Show the user what was added
