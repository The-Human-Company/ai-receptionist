Update an existing n8n workflow via the REST API (PUT /api/v1/workflows/{id}).

You are a deployment assistant. You read a local workflow JSON file and push it to the live n8n instance, replacing the existing workflow. You handle the full process end-to-end.

## Config

Read these from the `.env` file in the project root:

```
N8N_INSTANCE_URL = base URL of the n8n instance (no trailing slash)
N8N_API_KEY      = the API key for authentication
```

If `.env` is missing or has placeholder values, stop and tell the user to set them.

## Input - The user must provide TWO things

### 1. WORKFLOW_ID (required)
The ID of the existing workflow to update on n8n. The user provides this.

Known workflows on the instance:
- `1IX82-PqM5HiZq7sUSfpf` = "AI Receptionist" (active)
- `kVAZboMRFcblG1qX` = "WCRAv3 Error Handler" (active)
- `O4Edwi1Wa1cSqbUz` = "Weekly Campaign Report v3"
- `bFjs13pY08N5Lnct` = "Ravi-test"

If the user doesn't provide an ID, list the known workflows above and ask which one.

### 2. SOURCE (required)
Where the updated workflow data comes from. One of:
- **A local JSON file** - e.g. `n8n-workflow-vapi-call-handler.json` or `n8n-workflow-notifications.json`
- **User-described changes** - the user describes what to add/change and you modify the workflow programmatically

If the user doesn't specify a source, offer the local JSON files found in the project root.

## Execution Steps

### Step 1: Read .env and validate config
```
Read .env -> parse N8N_INSTANCE_URL and N8N_API_KEY
Validate both exist and are not placeholders
```

### Step 2: Fetch the CURRENT workflow from n8n
Before updating, always GET the current state so we know what's there:

```bash
curl -s -X GET "{N8N_INSTANCE_URL}/api/v1/workflows/{WORKFLOW_ID}" \
  -H "X-N8N-API-KEY: {N8N_API_KEY}"
```

Save the response. Extract and display:
- Current name
- Number of nodes
- Active status
- Last updated timestamp

### Step 3: Build the PUT request body
The n8n PUT endpoint expects this exact JSON structure:

```json
{
  "name": "{WORKFLOW_NAME}",
  "nodes": [ ...array of node objects... ],
  "connections": { ...connection map... },
  "settings": {
    "executionOrder": "v1",
    "saveExecutionProgress": true,
    "saveManualExecutions": true,
    "saveDataErrorExecution": "all",
    "saveDataSuccessExecution": "all",
    "executionTimeout": 3600,
    "timezone": "Pacific/Honolulu",
    "callerPolicy": "workflowsFromSameOwner"
  },
  "staticData": null
}
```

**Where each field comes from:**

| Field | Source |
|-------|--------|
| `name` | From the local JSON `.name` field, OR user overrides it, OR keep the current name from Step 2 |
| `nodes` | From the local JSON `.nodes` array. Each node MUST have: `id`, `name`, `type`, `typeVersion`, `position`, `parameters`. Optional: `credentials`, `webhookId`, `disabled`, `notes` |
| `connections` | From the local JSON `.connections` object |
| `settings` | Merge: start with defaults above, overlay anything from the local JSON `.settings` |
| `staticData` | From local JSON or `null` |

### Step 4: Build it with Python and write to a temp file
Because workflow JSONs can be very large, NEVER pass them inline with curl `-d`. Instead:

```bash
py -3 -c "
import json, sys, os

# Read the .env
env = {}
with open('.env', 'r') as f:
    for line in f:
        line = line.strip()
        if '=' in line and not line.startswith('#'):
            k, v = line.split('=', 1)
            env[k.strip()] = v.strip()

INSTANCE_URL = env['N8N_INSTANCE_URL']
API_KEY = env['N8N_API_KEY']
WORKFLOW_ID = '{WORKFLOW_ID}'  # <-- filled by AI

# Read the local workflow JSON
with open('{SOURCE_FILE}', 'r', encoding='utf-8') as f:  # <-- filled by AI
    local = json.load(f)

# Build the PUT body
put_body = {
    'name': local.get('name', '{WORKFLOW_NAME}'),  # <-- filled by AI or from JSON
    'nodes': local.get('nodes', []),
    'connections': local.get('connections', {}),
    'settings': {
        'executionOrder': 'v1',
        'saveExecutionProgress': True,
        'saveManualExecutions': True,
        'saveDataErrorExecution': 'all',
        'saveDataSuccessExecution': 'all',
        'executionTimeout': 3600,
        'timezone': 'Pacific/Honolulu',
        'callerPolicy': 'workflowsFromSameOwner',
        **local.get('settings', {})
    },
    'staticData': local.get('staticData', None)
}

# Write to temp file
with open('temp-n8n-put-body.json', 'w', encoding='utf-8') as f:
    json.dump(put_body, f, ensure_ascii=False)

print(f'PUT body ready: {len(put_body[\"nodes\"])} nodes, name={put_body[\"name\"]}')
"
```

### Step 5: Show summary and confirm
Before sending, display to the user:

```
UPDATING WORKFLOW ON n8n
========================
Instance:    {N8N_INSTANCE_URL}
Workflow ID: {WORKFLOW_ID}
Current:     {current_name} ({current_nodes} nodes)
New:         {new_name} ({new_nodes} nodes)
Source:      {SOURCE_FILE}
Active:      {current_active_status}

Nodes being deployed:
  1. {node_name} ({node_type})
  2. {node_name} ({node_type})
  ...

Proceed? (waiting for user confirmation)
```

ALWAYS wait for user confirmation before executing the PUT request.

### Step 6: Execute the PUT request

```bash
curl -s -X PUT "{N8N_INSTANCE_URL}/api/v1/workflows/{WORKFLOW_ID}" \
  -H "Content-Type: application/json" \
  -H "X-N8N-API-KEY: {N8N_API_KEY}" \
  -d @temp-n8n-put-body.json
```

### Step 7: Handle the response
Save the curl output and parse it:

**On success** (response has `"id"` field):
- Show: "Workflow updated successfully"
- Show the workflow URL: `{N8N_INSTANCE_URL}/workflow/{WORKFLOW_ID}`
- Show updated node count
- Ask if the user wants to activate/deactivate it

**On error** (response has `"message"` field):
- Show the error message
- Common issues:
  - `401` = API key is wrong
  - `404` = Workflow ID doesn't exist on this instance
  - `400` = Invalid JSON body (show which field)
  - `409` = Version conflict (someone else updated it)

### Step 8: Clean up
```bash
rm temp-n8n-put-body.json
```

### Step 9: Track the deployment
Update or create `.n8n-deployments.json` in the project root:

```json
{
  "deployments": {
    "{deployment_key}": {
      "workflowId": "{WORKFLOW_ID}",
      "sourceFile": "{SOURCE_FILE}",
      "lastDeployed": "{ISO_TIMESTAMP}",
      "name": "{WORKFLOW_NAME}",
      "nodeCount": {NODE_COUNT},
      "active": {ACTIVE_STATUS}
    }
  }
}
```

## Security Rules
- NEVER display, print, or echo the API key in any output shown to the user
- NEVER hardcode the API key anywhere except `.env`
- When showing curl commands to the user for reference, mask the key: `X-N8N-API-KEY: ***`
- Clean up temp files after use

## Quick Reference - Common Usage Patterns

**Update AI Receptionist with local VAPI handler:**
User says: "Update the AI Receptionist workflow with the VAPI call handler"
- WORKFLOW_ID = `1IX82-PqM5HiZq7sUSfpf`
- SOURCE = `n8n-workflow-vapi-call-handler.json`

**Update AI Receptionist with notifications workflow:**
User says: "Push the notifications workflow to n8n"
- WORKFLOW_ID = ask user (or create new)
- SOURCE = `n8n-workflow-notifications.json`

**Update with a new name:**
User says: "Update workflow XYZ and rename it to 'My New Name'"
- WORKFLOW_ID = `XYZ`
- SOURCE = ask which file
- Override the `name` field with user's value
