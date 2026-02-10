Add a new VAPI function call handler to the main n8n workflow.

Steps:
1. Read the current `n8n-workflow-vapi-call-handler.json`
2. Ask the user what the new function should do (name, purpose, input parameters, logic)
3. Create a new Code node with the function logic that:
   - Extracts parameters from `$input.first().json.message.functionCall.parameters`
   - Returns a `results` array with `toolCallId` and `result` (JSON stringified)
4. Add the new function name to the "Route Function Call" Switch node
5. Connect the new node to the "Respond to VAPI" node
6. Write the updated workflow JSON back to disk
7. Show the user what was added

Always maintain the existing node structure and connections.
