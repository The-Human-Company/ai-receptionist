Deploy, create, or update an n8n workflow on the Cloud instance via the REST API.

This skill builds the full API request dynamically - the AI fills in all variable fields from user input and workflow JSON files. The user NEVER has to manually construct JSON.

## Environment Variables (from `.env`)

```
N8N_INSTANCE_URL  = the n8n Cloud base URL (e.g. https://xyz.app.n8n.cloud)
N8N_API_KEY       = the n8n API key
```

## Step 1: Load Config

1. Read `.env` from the project root
2. Parse `N8N_INSTANCE_URL` and `N8N_API_KEY`
3. If either is missing or still has placeholder values (`your-instance-name`, `your-api-key-here`), ask the user to update `.env` first. NEVER ask them to paste the API key in chat.

## Step 2: Determine Action

Ask the user what they want to do:

| Action | API Method | Endpoint |
|--------|-----------|----------|
| **Create** new workflow | `POST` | `/api/v1/workflows` |
| **Update** existing workflow | `PUT` | `/api/v1/workflows/{WORKFLOW_ID}` |
| **List** all workflows | `GET` | `/api/v1/workflows` |
| **Get** one workflow | `GET` | `/api/v1/workflows/{WORKFLOW_ID}` |
| **Activate** a workflow | `PATCH` | `/api/v1/workflows/{WORKFLOW_ID}` |
| **Deactivate** a workflow | `PATCH` | `/api/v1/workflows/{WORKFLOW_ID}` |
| **Delete** a workflow | `DELETE` | `/api/v1/workflows/{WORKFLOW_ID}` |

## Step 3: Gather Variables

Based on the action, collect these variables from the user (or from the workflow JSON files in the project):

### Required Variables

| Variable | Source | Description |
|----------|--------|-------------|
| `WORKFLOW_NAME` | User input OR from JSON `.name` field | Display name in n8n |
| `WORKFLOW_ID` | User input (for update/delete/activate) | The n8n workflow ID (returned on create) |
| `NODES` | From workflow JSON `.nodes` array | All workflow nodes with their config |
| `CONNECTIONS` | From workflow JSON `.connections` object | How nodes are wired together |

### Settings Variables (with defaults for this project)

| Variable | Default | Description |
|----------|---------|-------------|
| `TIMEZONE` | `Pacific/Honolulu` | Workflow timezone |
| `SAVE_EXECUTION_PROGRESS` | `true` | Save progress during execution |
| `SAVE_MANUAL_EXECUTIONS` | `true` | Keep manual test runs |
| `SAVE_DATA_ERROR_EXECUTION` | `all` | Save data on error |
| `SAVE_DATA_SUCCESS_EXECUTION` | `all` | Save data on success |
| `EXECUTION_TIMEOUT` | `3600` | Max seconds per execution |
| `EXECUTION_ORDER` | `v1` | Node execution order |
| `CALLER_POLICY` | `workflowsFromSameOwner` | Who can call this workflow |

## Step 4: Build the Request Body

Use this template. Replace ALL `${VARIABLE}` placeholders with actual values:

```javascript
// === n8n API Request Template ===
// The AI fills ALL variables below from user input + workflow JSON files

const INSTANCE_URL = "${N8N_INSTANCE_URL}";    // from .env
const API_KEY      = "${N8N_API_KEY}";         // from .env
const WORKFLOW_ID  = "${WORKFLOW_ID}";          // user provides (for PUT/PATCH/DELETE)
const METHOD       = "${METHOD}";              // POST (create) or PUT (update)

// For POST (create):  /api/v1/workflows
// For PUT (update):   /api/v1/workflows/${WORKFLOW_ID}
const ENDPOINT = METHOD === "POST"
  ? `${INSTANCE_URL}/api/v1/workflows`
  : `${INSTANCE_URL}/api/v1/workflows/${WORKFLOW_ID}`;

const requestBody = {

  // --- WORKFLOW IDENTITY ---
  "name": "${WORKFLOW_NAME}",

  // --- NODES ---
  // Pulled directly from the workflow JSON file
  // Each node needs: id, name, type, typeVersion, position, parameters
  "nodes": ${NODES_JSON},

  // --- CONNECTIONS ---
  // Pulled directly from the workflow JSON file
  // Maps node outputs to node inputs
  "connections": ${CONNECTIONS_JSON},

  // --- SETTINGS ---
  "settings": {
    "saveExecutionProgress": ${SAVE_EXECUTION_PROGRESS},
    "saveManualExecutions": ${SAVE_MANUAL_EXECUTIONS},
    "saveDataErrorExecution": "${SAVE_DATA_ERROR_EXECUTION}",
    "saveDataSuccessExecution": "${SAVE_DATA_SUCCESS_EXECUTION}",
    "executionTimeout": ${EXECUTION_TIMEOUT},
    "timezone": "${TIMEZONE}",
    "executionOrder": "${EXECUTION_ORDER}",
    "callerPolicy": "${CALLER_POLICY}"
  },

  // --- STATIC DATA ---
  // Optional. Used by nodes that track state between executions
  "staticData": ${STATIC_DATA_JSON}
};
```

## Step 5: Execute via Bash

### CREATE (POST) - New Workflow

```bash
curl -s -X POST "${N8N_INSTANCE_URL}/api/v1/workflows" \
  -H "Content-Type: application/json" \
  -H "X-N8N-API-KEY: ${N8N_API_KEY}" \
  -d '${REQUEST_BODY_JSON}'
```

### UPDATE (PUT) - Existing Workflow

```bash
curl -s -X PUT "${N8N_INSTANCE_URL}/api/v1/workflows/${WORKFLOW_ID}" \
  -H "Content-Type: application/json" \
  -H "X-N8N-API-KEY: ${N8N_API_KEY}" \
  -d '${REQUEST_BODY_JSON}'
```

### ACTIVATE (PATCH)

```bash
curl -s -X PATCH "${N8N_INSTANCE_URL}/api/v1/workflows/${WORKFLOW_ID}" \
  -H "Content-Type: application/json" \
  -H "X-N8N-API-KEY: ${N8N_API_KEY}" \
  -d '{"active": true}'
```

### DEACTIVATE (PATCH)

```bash
curl -s -X PATCH "${N8N_INSTANCE_URL}/api/v1/workflows/${WORKFLOW_ID}" \
  -H "Content-Type: application/json" \
  -H "X-N8N-API-KEY: ${N8N_API_KEY}" \
  -d '{"active": false}'
```

### LIST (GET)

```bash
curl -s -X GET "${N8N_INSTANCE_URL}/api/v1/workflows" \
  -H "X-N8N-API-KEY: ${N8N_API_KEY}"
```

### GET ONE (GET)

```bash
curl -s -X GET "${N8N_INSTANCE_URL}/api/v1/workflows/${WORKFLOW_ID}" \
  -H "X-N8N-API-KEY: ${N8N_API_KEY}"
```

### DELETE

```bash
curl -s -X DELETE "${N8N_INSTANCE_URL}/api/v1/workflows/${WORKFLOW_ID}" \
  -H "X-N8N-API-KEY: ${N8N_API_KEY}"
```

## Step 6: Handle the Response

Parse the JSON response from n8n:

**On success (create/update):**
- Extract and display the `id` field (this is the WORKFLOW_ID for future updates)
- Show the workflow URL: `${N8N_INSTANCE_URL}/workflow/${id}`
- Ask if the user wants to activate it

**On success (list):**
- Show a table: ID | Name | Active | Created | Updated

**On error:**
- Show the error message
- Common fixes:
  - `401 Unauthorized` -> API key is wrong, check `.env`
  - `404 Not Found` -> Workflow ID doesn't exist
  - `400 Bad Request` -> Invalid JSON, show which field failed

## Step 7: Save the Workflow ID

After a successful CREATE, save the returned workflow ID back into the project:
1. Update `CLAUDE.md` with the deployed workflow ID
2. Optionally create a `.n8n-deployments.json` tracking file:

```json
{
  "deployments": {
    "vapi-call-handler": {
      "workflowId": "<returned_id>",
      "file": "n8n-workflow-vapi-call-handler.json",
      "lastDeployed": "<timestamp>",
      "active": false
    },
    "notifications": {
      "workflowId": "<returned_id>",
      "file": "n8n-workflow-notifications.json",
      "lastDeployed": "<timestamp>",
      "active": false
    }
  }
}
```

## Execution Rules

### IMPORTANT - For large workflow JSONs:
- The request body can be very large. Instead of passing it inline with `-d`, write the full request body to a temp file and use `-d @tempfile.json`
- Use `py -3 -c` to build the final JSON programmatically (merge the workflow JSON nodes/connections with the settings template) and write to a temp file
- Then curl with `-d @tempfile.json`

### IMPORTANT - Security:
- NEVER display or log the API key in any output
- NEVER hardcode the API key in any file other than `.env`
- Mask the API key in curl commands shown to the user (show `***` instead)
- The `.env` file is already in `.gitignore`

### IMPORTANT - Before deploying, ALWAYS:
1. Read the workflow JSON file
2. Validate it's valid JSON
3. Scan for placeholder values (`UPDATE`, `TBD`, `TODO`, `your-instance`)
4. Show the user a summary of what will be deployed
5. Get explicit confirmation before making the API call
6. For DELETE: double-confirm with the user

### Project-specific workflow files:
- `n8n-workflow-vapi-call-handler.json` - Main VAPI AI Receptionist call handler
- `n8n-workflow-notifications.json` - Post-call notifications & 2hr escalation to Davin
