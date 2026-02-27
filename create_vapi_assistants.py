"""Create Business Hours and After Hours assistants on VAPI."""
import json
import urllib.request
import ssl

VAPI_KEY = '35c9ce5b-63f5-46a2-91e3-0d5275567738'
N8N_BASE = 'https://solarexpresss.app.n8n.cloud/webhook'

# Read system prompts from vapi-web-test.html
with open('vapi-web-test.html', 'r', encoding='utf-8') as f:
    html = f.read()

biz_prompt = html.split('const SYSTEM_PROMPT_BUSINESS = `')[1].split('`;')[0]
ah_prompt = html.split('const SYSTEM_PROMPT_AFTERHOURS = `')[1].split('`;')[0]

# Shared configs
shared_voice_biz = {
    'provider': '11labs', 'voiceId': 'EXAVITQu4vr4xnSDxMaL',
    'stability': 0.55, 'similarityBoost': 0.8, 'style': 0.45, 'speed': 0.92,
    'useSpeakerBoost': True, 'model': 'eleven_turbo_v2_5',
    'chunkPlan': {'enabled': True, 'minCharacters': 30}
}
shared_voice_ah = {
    'provider': '11labs', 'voiceId': 'sarah',
    'stability': 0.55, 'similarityBoost': 0.8, 'style': 0.45, 'speed': 0.92,
    'useSpeakerBoost': True, 'model': 'eleven_turbo_v2_5',
    'chunkPlan': {'enabled': True, 'minCharacters': 30}
}
shared_transcriber = {
    'provider': 'deepgram', 'model': 'nova-3',
    'language': 'en', 'smartFormat': True,
    'keywords': ['Equity:2', 'Honolulu:2', 'Hawaii:2', 'Tulsa:1', 'Oklahoma:1',
                 'renters:1', 'homeowners:1', 'auto:1', 'liability:1', 'deductible:1',
                 'premium:1', 'VIN:2', 'lienholder:2', 'Davin:2', 'Val:1']
}

# Tool definitions
tool_save_field_biz = {
    'type': 'function',
    'function': {
        'name': 'save_field',
        'description': 'Save a collected data field from the caller to the system. Call this after collecting each piece of information.',
        'parameters': {
            'type': 'object',
            'properties': {
                'call_id': {'type': 'string', 'description': 'The unique call identifier'},
                'field_name': {'type': 'string', 'enum': [
                    'caller_name','caller_phone','caller_address','caller_dob','caller_occupation',
                    'policy_type','auto_vehicle_info','auto_vin','auto_violations',
                    'home_owner_or_renter','home_property_address','home_claims_losses','home_property_type',
                    'biz_name','biz_ein','biz_start_date','biz_revenue','biz_industry','biz_contact',
                    'claims_count','claims_details'
                ]},
                'field_value': {'type': 'string', 'description': 'The value collected from the caller'}
            },
            'required': ['call_id', 'field_name', 'field_value']
        }
    },
    'server': {'url': f'{N8N_BASE}/vapi-save-field'}
}

tool_save_field_ah = {
    'type': 'function',
    'function': {
        'name': 'save_field',
        'description': 'Save a collected data field to the system',
        'parameters': {
            'type': 'object',
            'properties': {
                'call_id': {'type': 'string'},
                'field_name': {'type': 'string', 'enum': ['caller_name', 'caller_phone', 'reason_for_calling']},
                'field_value': {'type': 'string'}
            },
            'required': ['call_id', 'field_name', 'field_value']
        }
    },
    'server': {'url': f'{N8N_BASE}/vapi-save-field'}
}

tool_check_disqualifier = {
    'type': 'function',
    'function': {
        'name': 'check_disqualifier',
        'description': 'Check if the caller is disqualified based on claims history or coverage urgency.',
        'parameters': {
            'type': 'object',
            'properties': {
                'call_id': {'type': 'string', 'description': 'The unique call identifier'},
                'claims_count_worst_year': {'type': 'integer', 'description': 'The highest number of claims in any single year'},
                'urgency_hours': {'type': 'integer', 'description': 'How many hours until coverage is needed'}
            },
            'required': ['call_id', 'claims_count_worst_year', 'urgency_hours']
        }
    },
    'server': {'url': f'{N8N_BASE}/vapi-check-disqualifier'}
}

tool_check_hot_lead = {
    'type': 'function',
    'function': {
        'name': 'check_hot_lead',
        'description': 'Check if the caller qualifies as a high-value hot lead for immediate agent transfer.',
        'parameters': {
            'type': 'object',
            'properties': {
                'call_id': {'type': 'string', 'description': 'The unique call identifier'},
                'policy_type': {'type': 'string', 'description': 'The type of insurance policy'},
                'estimated_value': {'type': 'number', 'description': 'The estimated property or auto value in dollars'}
            },
            'required': ['call_id', 'policy_type', 'estimated_value']
        }
    },
    'server': {'url': f'{N8N_BASE}/vapi-check-hotlead'}
}

tool_route_existing = {
    'type': 'function',
    'function': {
        'name': 'route_existing_customer',
        'description': 'Route an existing customer request. Creates a support ticket and notifies the team.',
        'parameters': {
            'type': 'object',
            'properties': {
                'call_id': {'type': 'string', 'description': 'The unique call identifier'},
                'caller_name': {'type': 'string', 'description': 'The existing customer name'},
                'caller_phone': {'type': 'string', 'description': 'The customer phone number'},
                'policy_type': {'type': 'string', 'description': 'The type of policy they have or are asking about'},
                'request_description': {'type': 'string', 'description': 'What the customer is asking for specifically'}
            },
            'required': ['call_id', 'caller_name', 'caller_phone', 'request_description']
        }
    },
    'server': {'url': f'{N8N_BASE}/vapi-existing-customer'}
}

tool_route_claim = {
    'type': 'function',
    'function': {
        'name': 'route_claim',
        'description': 'Route a claim call. Attempts to transfer to claims agent and sends priority notification.',
        'parameters': {
            'type': 'object',
            'properties': {
                'call_id': {'type': 'string', 'description': 'The unique call identifier'},
                'caller_name': {'type': 'string', 'description': 'The caller name'},
                'caller_phone': {'type': 'string', 'description': 'The caller phone number'},
                'policy_number': {'type': 'string', 'description': 'The policy number if available'},
                'claim_type': {'type': 'string', 'description': 'The type of claim (auto, property, etc.)'},
                'claim_description': {'type': 'string', 'description': 'Description of the claim'}
            },
            'required': ['call_id', 'caller_name', 'caller_phone', 'claim_type', 'claim_description']
        }
    },
    'server': {'url': f'{N8N_BASE}/vapi-claim'}
}

tool_route_claim_ah = {
    'type': 'function',
    'function': {
        'name': 'route_claim',
        'description': 'Route an urgent claim to the claims team for priority handling',
        'parameters': {
            'type': 'object',
            'properties': {
                'call_id': {'type': 'string'},
                'caller_name': {'type': 'string'},
                'caller_phone': {'type': 'string'},
                'claim_type': {'type': 'string', 'enum': ['Auto', 'Property', 'Business', 'Other']},
                'claim_description': {'type': 'string'}
            },
            'required': ['call_id', 'caller_name', 'caller_phone', 'claim_type', 'claim_description']
        }
    },
    'server': {'url': f'{N8N_BASE}/vapi-claim'}
}

# Shared behavior
shared_behavior = {
    'endCallFunctionEnabled': True,
    'dialKeypadFunctionEnabled': True,
    'serverUrl': f'{N8N_BASE}/vapi-call-ended',
    'stopSpeakingPlan': {
        'numWords': 2, 'voiceSeconds': 0.2, 'backoffSeconds': 1.2,
        'acknowledgementPhrases': ['okay','got it','mm-hmm','uh-huh','right','sure','yep'],
        'interruptionPhrases': ['wait','hold on','stop','actually','excuse me']
    },
    'startSpeakingPlan': {
        'waitSeconds': 0.4,
        'smartEndpointingPlan': {'provider': 'livekit'},
        'transcriptionEndpointingPlan': {
            'onPunctuationSeconds': 0.3, 'onNoPunctuationSeconds': 1.2, 'onNumberSeconds': 0.6
        }
    },
    'keypadInputPlan': {
        'enabled': True, 'timeoutSeconds': 5, 'delimiters': ['#']
    },
    'backchannelingEnabled': False,
    'silenceTimeoutSeconds': 30,
    'backgroundDenoisingEnabled': False,
    'backgroundSpeechDenoisingPlan': {
        'smartDenoisingPlan': {'enabled': False},
        'fourierDenoisingPlan': {'enabled': False}
    }
}

def create_assistant(config):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    data = json.dumps(config).encode('utf-8')
    req = urllib.request.Request(
        'https://api.vapi.ai/assistant',
        data=data,
        headers={
            'Authorization': f'Bearer {VAPI_KEY}',
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 VAPI-Setup/1.0'
        },
        method='POST'
    )
    resp = urllib.request.urlopen(req, context=ctx)
    return json.loads(resp.read().decode('utf-8'))

# === Create Business Hours Assistant ===
biz_config = {
    'name': 'Equity Insurance - Business Hours',
    'firstMessage': 'Aloha, thank you for calling Equity Insurance in Honolulu, Hawaii -- not affiliated with Equity Insurance in Tulsa, Oklahoma. Just so you know, I\'m an AI assistant here to help get things started. How can I help you today?',
    'model': {
        'provider': 'openai', 'model': 'gpt-4o-mini', 'temperature': 0.5, 'maxTokens': 300,
        'messages': [{'role': 'system', 'content': biz_prompt}],
        'tools': [tool_save_field_biz, tool_check_disqualifier, tool_check_hot_lead, tool_route_existing, tool_route_claim]
    },
    'voice': shared_voice_biz,
    'transcriber': shared_transcriber,
    **shared_behavior
}

print('Creating Business Hours assistant...')
biz_result = create_assistant(biz_config)
biz_id = biz_result.get('id', 'FAILED')
print(f'  ID: {biz_id}')
print(f'  Name: {biz_result.get("name")}')
print(f'  Model: {biz_result.get("model", {}).get("model")}')
print(f'  Voice: {biz_result.get("voice", {}).get("voiceId")}')
print(f'  Tools: {len(biz_result.get("model", {}).get("tools", []))}')
print()

# === Create After Hours Assistant ===
ah_config = {
    'name': 'Equity Insurance - After Hours',
    'firstMessage': 'Aloha, thank you for calling Equity Insurance in Honolulu, Hawaii. We\'re currently closed -- our business hours are 9 AM to 5 PM Hawaii time, Monday through Friday. I\'m an AI assistant, but I can take a message and have someone call you back. May I have your name?',
    'model': {
        'provider': 'openai', 'model': 'gpt-4o-mini', 'temperature': 0.5, 'maxTokens': 300,
        'messages': [{'role': 'system', 'content': ah_prompt}],
        'tools': [tool_save_field_ah, tool_route_claim_ah]
    },
    'voice': shared_voice_ah,
    'transcriber': shared_transcriber,
    **shared_behavior
}

print('Creating After Hours assistant...')
ah_result = create_assistant(ah_config)
ah_id = ah_result.get('id', 'FAILED')
print(f'  ID: {ah_id}')
print(f'  Name: {ah_result.get("name")}')
print(f'  Model: {ah_result.get("model", {}).get("model")}')
print(f'  Voice: {ah_result.get("voice", {}).get("voiceId")}')
print(f'  Tools: {len(ah_result.get("model", {}).get("tools", []))}')
print()

print('=== SUMMARY ===')
print(f'Business Hours Assistant ID: {biz_id}')
print(f'After Hours Assistant ID:    {ah_id}')
