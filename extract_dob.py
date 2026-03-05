import json
with open('n8n-wf01-inbound-call-router.json', 'r') as f:
    data = json.load(f)
for node in data['nodes']:
    if node['name'] == 'Return Business Hours Config':
        rb = node['parameters']['responseBody']
        # Parse inner JSON to get the system prompt
        inner = rb[1:]  # strip leading =
        inner_data = json.loads(inner)
        content = inner_data['assistant']['model']['messages'][0]['content']
        # Find DOB sections with context
        idx = 0
        while True:
            pos = content.find('Date of Birth', idx)
            if pos == -1:
                break
            start = max(0, pos - 80)
            end = min(len(content), pos + 300)
            print(f'=== Found at pos {pos} ===')
            print(repr(content[start:end]))
            print()
            idx = pos + 1
        # Also find closing sections
        idx = 0
        while True:
            pos = content.find('Closing --', idx)
            if pos == -1:
                break
            start = max(0, pos - 30)
            end = min(len(content), pos + 400)
            print(f'=== CLOSING at pos {pos} ===')
            print(repr(content[start:end]))
            print()
            idx = pos + 1
        # Find the general CLOSING section
        pos = content.find('CLOSING:\n')
        if pos >= 0:
            end = min(len(content), pos + 500)
            print(f'=== GENERAL CLOSING at pos {pos} ===')
            print(repr(content[pos:end]))
