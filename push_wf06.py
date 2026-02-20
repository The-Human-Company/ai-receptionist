#!/usr/bin/env python3
"""Push updated WF-06 to n8n, filtering to only accepted PUT fields"""
import json, os, subprocess

TEMP = os.environ.get('TEMP', os.path.join(os.path.expanduser('~'), 'AppData', 'Local', 'Temp'))
wf_path = os.path.join(TEMP, 'wf06.json')

with open(wf_path, encoding='utf-8') as f:
    wf = json.load(f)

# Only include fields accepted by PUT API
put_payload = {
    'name': wf['name'],
    'nodes': wf['nodes'],
    'connections': wf['connections'],
    'settings': wf.get('settings', {}),
    'staticData': wf.get('staticData'),
}

put_path = os.path.join(TEMP, 'wf06_put.json')
with open(put_path, 'w', encoding='utf-8') as f:
    json.dump(put_payload, f)

result = subprocess.run(
    ['curl', '-s', '--ssl-no-revoke', '-X', 'PUT',
     'https://solarexpresss.app.n8n.cloud/api/v1/workflows/nKwYydxwd8n58ExN',
     '-H', 'X-N8N-API-KEY: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI4ZjkzZWVhYS1lZWQ5LTRlMDYtOWMxOC1mNmFjYThmZjA3YjMiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzcwOTI5NzMzLCJleHAiOjE3NzM1MDQwMDB9.ii-Qih5OEXeIaXwIeTfk4rUwoaegEk0-zppAnHfHShg',
     '-H', 'Content-Type: application/json',
     '-d', '@' + put_path],
    capture_output=True, text=True, encoding='utf-8'
)
resp = json.loads(result.stdout)
print(f"Updated: {resp.get('name', '?')} | Active: {resp.get('active', '?')} | Nodes: {len(resp.get('nodes', []))}")

# Verify the changes
for n in resp.get('nodes', []):
    if n['name'] == 'Read Lead Record':
        print(f"  Read Lead Record - alwaysOutputData: {n.get('alwaysOutputData')}, onError: {n.get('onError')}")
    if n['name'] == 'Merge and Flag':
        code = n['parameters']['jsCode']
        has_fix = 'leadItems.length > 0' in code
        print(f"  Merge and Flag - has empty check: {has_fix}")
