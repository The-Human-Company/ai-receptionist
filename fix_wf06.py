#!/usr/bin/env python3
"""Fix WF-06: Make Read Lead Record resilient to missing lead records"""
import json, os

TEMP = os.environ.get('TEMP', os.path.join(os.path.expanduser('~'), 'AppData', 'Local', 'Temp'))
wf_path = os.path.join(TEMP, 'wf06.json')

with open(wf_path, encoding='utf-8') as f:
    wf = json.load(f)

nodes = wf['nodes']
for i, n in enumerate(nodes):
    if n['name'] == 'Read Lead Record':
        nodes[i]['alwaysOutputData'] = True
        nodes[i]['onError'] = 'continueRegularOutput'
        print('Updated Read Lead Record: alwaysOutputData=true, onError=continueRegularOutput')

    if n['name'] == 'Merge and Flag':
        new_code = (
            '// Merge call data with lead record and add migration flag\n'
            'const callData = $("Extract All Data").item.json;\n'
            'const leadItems = $("Read Lead Record").all();\n'
            'const leadData = (leadItems.length > 0 && Object.keys(leadItems[0].json).length > 0) ? leadItems[0].json : {};\n'
            '\n'
            '// Lead data as base, call data overwrites\n'
            'const merged = { ...leadData, ...callData };\n'
            "merged.migration_flag = 'VAPI_AI_COLLECTED';\n"
            'merged.migration_date = new Date().toISOString();\n'
            '\n'
            'return [{ json: merged }];'
        )
        nodes[i]['parameters']['jsCode'] = new_code
        print('Updated Merge and Flag: handles empty lead data')

wf['nodes'] = nodes
with open(wf_path, 'w', encoding='utf-8') as f:
    json.dump(wf, f)
print('Saved updated workflow to ' + wf_path)
