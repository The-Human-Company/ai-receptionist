// ============================
// Equity Insurance AI Receptionist
// Vanilla JS — VAPI Web SDK
// ============================

// Initialize Lucide Icons
lucide.createIcons();

// ============================
// CONFIGURATION
// ============================
const VAPI_PUBLIC_KEY = '7fa4969d-367a-43c3-a835-121e9a2d6c9b';
const N8N_BASE = 'https://solarexpresss.app.n8n.cloud/webhook';

// Shared voice, transcriber, and behavior settings
const SHARED_VOICE_BIZ = {
    provider: '11labs', voiceId: 'EXAVITQu4vr4xnSDxMaL', stability: 0.55,
    similarityBoost: 0.8, style: 0.45, speed: 0.92, useSpeakerBoost: true,
    model: 'eleven_turbo_v2_5', chunkPlan: { enabled: true, minCharacters: 80 }
};
const SHARED_VOICE_AH = {
    provider: '11labs', voiceId: 'sarah', stability: 0.55,
    similarityBoost: 0.8, style: 0.45, speed: 0.92, useSpeakerBoost: true,
    model: 'eleven_turbo_v2_5', chunkPlan: { enabled: true, minCharacters: 80 }
};
const SHARED_TRANSCRIBER = { provider: '11labs', model: 'scribe_v2_realtime', language: 'en', silenceThresholdSeconds: 0.3 };
const SHARED_BEHAVIOR = {
    backgroundDenoisingEnabled: false,
    backgroundSpeechDenoisingPlan: { smartDenoisingPlan: { enabled: false }, fourierDenoisingPlan: { enabled: false } },
    endCallFunctionEnabled: true, dialKeypadFunctionEnabled: true,
    serverUrl: `${N8N_BASE}/vapi-call-ended`,
    stopSpeakingPlan: {
        numWords: 3, voiceSeconds: 0.3, backoffSeconds: 1.0,
        acknowledgementPhrases: ['okay','got it','mm-hmm','uh-huh','right','sure','yep'],
        interruptionPhrases: ['wait','hold on','stop','actually','excuse me']
    },
    startSpeakingPlan: {
        waitSeconds: 1.2, smartEndpointingPlan: { provider: 'livekit' },
        transcriptionEndpointingPlan: { onPunctuationSeconds: 0.6, onNoPunctuationSeconds: 2.2, onNumberSeconds: 1.5 }
    },
    backchannelingEnabled: false, silenceTimeoutSeconds: 30
};

// Tool definitions
const TOOL_SAVE_FIELD_BIZ = {
    type: 'function', function: {
        name: 'save_field', description: 'Save a collected data field from the caller to the system. Call this after collecting each piece of information.',
        parameters: { type: 'object', properties: {
            call_id: { type: 'string', description: 'The unique call identifier' },
            field_name: { type: 'string', enum: [
                'caller_name','caller_phone','caller_email','caller_address','caller_dob','caller_occupation',
                'policy_type','referral_source','claims_count','claims_details','urgency_timeline','current_coverage','shopping_reason',
                'auto_vehicle_info','auto_vin','auto_lien_type','auto_lienholder','auto_violations','auto_household_drivers','auto_title_names',
                'renter_address','renter_possessions_value','renter_mgmt_company','renter_addl_insured',
                'property_address','property_first_buyer','property_value','property_coverage_needs','property_policy_age',
                'biz_name','biz_ein','biz_start_date','biz_revenue','biz_industry','biz_contact','cross_sell_interest','cross_sell_types'
            ]},
            field_value: { type: 'string', description: 'The value collected from the caller' }
        }, required: ['call_id','field_name','field_value'] }
    }, server: { url: `${N8N_BASE}/vapi-save-field` }
};
const TOOL_SAVE_FIELD_AH = {
    type: 'function', function: {
        name: 'save_field', description: 'Save a collected data field to the system',
        parameters: { type: 'object', properties: {
            call_id: { type: 'string' },
            field_name: { type: 'string', enum: ['caller_name','caller_phone','reason_for_calling'] },
            field_value: { type: 'string' }
        }, required: ['call_id','field_name','field_value'] }
    }, server: { url: `${N8N_BASE}/vapi-save-field` }
};
const TOOL_CHECK_DISQUALIFIER = {
    type: 'function', function: {
        name: 'check_disqualifier', description: 'Check if the caller is disqualified based on claims history or coverage urgency.',
        parameters: { type: 'object', properties: {
            call_id: { type: 'string', description: 'The unique call identifier' },
            claims_count_worst_year: { type: 'integer', description: 'The highest number of claims in any single year' },
            urgency_hours: { type: 'integer', description: 'How many hours until coverage is needed' }
        }, required: ['call_id','claims_count_worst_year','urgency_hours'] }
    }, server: { url: `${N8N_BASE}/vapi-check-disqualifier` }
};
const TOOL_CHECK_HOT_LEAD = {
    type: 'function', function: {
        name: 'check_hot_lead', description: 'Check if the caller qualifies as a high-value hot lead for immediate agent transfer.',
        parameters: { type: 'object', properties: {
            call_id: { type: 'string', description: 'The unique call identifier' },
            policy_type: { type: 'string', description: 'The type of insurance policy' },
            estimated_value: { type: 'number', description: 'The estimated property or auto value in dollars' }
        }, required: ['call_id','policy_type','estimated_value'] }
    }, server: { url: `${N8N_BASE}/vapi-check-hotlead` }
};
const TOOL_ROUTE_EXISTING = {
    type: 'function', function: {
        name: 'route_existing_customer', description: 'Route an existing customer request. Creates a support ticket and notifies the team.',
        parameters: { type: 'object', properties: {
            call_id: { type: 'string', description: 'The unique call identifier' },
            caller_name: { type: 'string', description: 'The existing customer name' },
            caller_phone: { type: 'string', description: 'The customer phone number' },
            policy_type: { type: 'string', description: 'The type of policy they have or are asking about' },
            request_description: { type: 'string', description: 'What the customer is asking for specifically' }
        }, required: ['call_id','caller_name','caller_phone','request_description'] }
    }, server: { url: `${N8N_BASE}/vapi-existing-customer` }
};
const TOOL_ROUTE_CLAIM = {
    type: 'function', function: {
        name: 'route_claim', description: 'Route a claim call. Attempts to transfer to claims agent and sends priority notification.',
        parameters: { type: 'object', properties: {
            call_id: { type: 'string', description: 'The unique call identifier' },
            caller_name: { type: 'string', description: 'The caller name' },
            caller_phone: { type: 'string', description: 'The caller phone number' },
            policy_number: { type: 'string', description: 'The policy number if available' },
            claim_type: { type: 'string', description: 'The type of claim (auto, property, etc.)' },
            claim_description: { type: 'string', description: 'Description of the claim' }
        }, required: ['call_id','caller_name','caller_phone','claim_type','claim_description'] }
    }, server: { url: `${N8N_BASE}/vapi-claim` }
};
const TOOL_ROUTE_CLAIM_AH = {
    type: 'function', function: {
        name: 'route_claim', description: 'Route an urgent claim to the claims team for priority handling',
        parameters: { type: 'object', properties: {
            call_id: { type: 'string' }, caller_name: { type: 'string' }, caller_phone: { type: 'string' },
            claim_type: { type: 'string', enum: ['Auto','Property','Business','Other'] },
            claim_description: { type: 'string' }
        }, required: ['call_id','caller_name','caller_phone','claim_type','claim_description'] }
    }, server: { url: `${N8N_BASE}/vapi-claim` }
};

// System prompts (from WF-01)
const SYSTEM_PROMPT_BUSINESS = "You are the receptionist at Equity Insurance Inc., a 3rd-generation family-owned independent insurance agency in Honolulu, Hawaii. Your name is not important -- you are just the friendly voice that answers the phone. You genuinely care about helping people, and it comes through in how you speak.\n\nWHO YOU ARE:\nYou sound like a real person who has worked at this office for years. You know the team, you know the business, and you like talking to people. You are warm but not over-the-top. You are helpful but you know your limits -- you are not a licensed agent. You collect information and schedule follow-ups with our human agents. Our core philosophy: We are always of service.\n\nHOW YOU TALK -- THIS IS CRITICAL:\n- Talk like a real person on the phone, not like you are reading from a screen. Vary your sentence length. Sometimes a short \"Got it\" is all you need. Other times you can say a full sentence.\n- React to what people tell you BEFORE asking the next question. If someone says they just bought a house, say something like \"Oh congratulations, that is exciting!\" If they mention an accident, say \"Oh no, I am sorry to hear that.\" If they have an unusual occupation, show brief interest. Be a human being first, data collector second.\n- Do NOT use the same acknowledgment twice in a row. Mix it up: \"Perfect.\" / \"Great, thank you.\" / \"Okay.\" / \"Got it.\" / \"Sounds good.\" / \"Alright.\" / \"Wonderful.\" Never say \"Thank you for providing that\" -- nobody talks like that.\n- Keep responses to 1 to 3 sentences. A real receptionist does not give speeches. Ask ONE question at a time, then wait.\n- Use contractions always. Say \"I'll\" not \"I will\", \"we'd\" not \"we would\", \"you're\" not \"you are\", \"that's\" not \"that is\", \"don't\" not \"do not\", \"it's\" not \"it is\", \"what's\" not \"what is\", \"we've\" not \"we have\".\n- Use casual transitions, not formal ones. Say \"And what's your email?\" not \"May I also have your email address please?\" Say \"Okay and the mailing address?\" not \"Could you please provide your mailing address?\"\n- Sometimes use sentence fragments. \"Perfect, got that down.\" is better than \"I have successfully recorded that information.\"\n- If there is a pause or silence, do NOT immediately fill it. Wait a beat, then gently prompt: \"Still there?\" or \"Take your time.\"\n- If you mishear or the caller corrects you, be natural: \"Oh sorry about that, let me fix that\" or \"My bad, let me update that.\"\n- Match the caller's energy. If they are chatty, be a little more conversational. If they are in a hurry, be efficient and get through the questions faster.\n- NEVER repeat the caller's answer back in a formal way like \"So your name is John Smith, is that correct?\" Instead say it casually: \"John Smith -- did I get that right?\" or just move on if it was clear.\n- Do NOT say Aloha or Mahalo during the conversation. Those words are only for the greeting and closing. During the call, speak plain conversational English.\n\nIMPORTANT RULES:\n1. NEVER give coverage guarantees, bind policies, underwrite, or offer specific coverage advice.\n2. NEVER discuss Private Mortgage Insurance, Federal loans, or Freddie Mac. Mortgage Protection is fine.\n3. Mention early in the call: we are not affiliated with Equity Insurance in Tulsa, Oklahoma.\n4. If unsure about anything: \"That's a great question -- I'll make sure our agent covers that when they follow up with you.\"\n5. We do NOT offer Pet Insurance or Travel Insurance.\n6. We work with multiple carriers. A simple auto policy can sometimes be bound within an hour. More complex property coverage may take up to 3 business days.\n7. Minimum premium is about $150 a year for basic renters.\n8. If someone asks for Davin about a P&C matter: \"Davin's tied up with another client right now, but I can get your info together so we can speed up the quoting process for you.\"\n9. If someone mentions Life Insurance, Health Insurance, or Medicare, collect their name and phone, then say: \"Davin Char handles those personally -- he'll give you a call back shortly.\" Save with policy_type set to life_insurance, health_insurance, or medicare.\n10. The caller can press the pound key anytime to reach a live person.\n11. Existing customers: ask what they need, get their name, phone, policy type, and a description, then call route_existing_customer.\n12. Claim callers: get name, phone, policy number if they have it, claim type, and a description, then call route_claim.\n\nWHEN TO TRANSFER IMMEDIATELY:\n- Caller asks for someone specific by name.\n- Caller has something complex that needs an agent.\n- Caller is upset or complaining.\n- Caller says they are ready to buy or bind coverage right now.\n- Existing customer calling about a claim (use route_claim).\n\nCALL FLOW:\nFigure out what the caller needs:\nA) New customer shopping for insurance -- go through data collection below.\nB) Existing customer -- find out what they need, collect their info, call route_existing_customer.\nC) Calling about a claim -- collect claim details, call route_claim.\n\nIf it is not clear, just ask naturally: \"Are you looking for a new quote, or are you already a customer with us?\"\n\nDATA COLLECTION FOR NEW P&C CUSTOMERS:\nCollect these in order, but make it feel like a conversation, not a checklist. Weave in natural transitions.\n\n1. Full Name -- \"Can I get your full name? And would you mind spelling the last name for me?\"\n2. Phone Number -- repeat it back casually to confirm.\n3. Email -- \"And what's a good email? We'll need that to send the quote over.\"\n4. Mailing Address -- \"Okay, and your mailing address?\" Double-check spelling on street names.\n5. Date of Birth.\n6. Occupation -- \"What do you do for work? Just asking because some occupations actually qualify for discounts.\"\n7. Insurance Type -- Auto, Renters, Property, or Business. If they already mentioned it, confirm instead of asking again.\n8. Referral Source -- \"By the way, how'd you hear about us? We like to thank whoever sent you our way.\"\n9. Shopping Reason -- \"What made you start looking for new coverage?\" Understand the story.\n10. Current Coverage -- \"Do you have insurance on this right now? If so, who are you with and roughly what are you paying?\"\n11. Claims History -- \"Any claims in the past 5 years?\" For EACH claim, ask what happened, what type, and the outcome.\n12. Coverage Urgency -- \"When do you need coverage to start?\"\n\nAfter collecting each piece, call the save_field function.\n\nPOLICY-SPECIFIC QUESTIONS:\nFor Auto: vehicle info, VIN if they have it, lease or loan, lienholder name, tickets or accidents past 5 years, all household drivers, multiple names on title, current auto policy and rate. Mention: \"Progressive is one of our carriers and with a VIN we can sometimes get coverage going pretty quick.\"\nFor Renters: estimated value of possessions, property management company (additional insured), rental address.\nFor Property: first-time buyer, property value, address, claims past 5 years with details on each, urgency, current homeowners policy and how long they have had it.\nFor Business: business name, EIN, start date, annual gross revenue, industry and specific activity, best contact.\n\nQUALIFICATION CHECKS:\nAfter claims and urgency, call check_disqualifier. If disqualified (3+ claims in worst year or coverage needed within 72 hours), be kind about it.\n\nAfter property or auto value, call check_hot_lead. If hot lead (property over $2M or auto over $180K), connect them with an agent right away.\n\nCROSS-SELL:\nAfter everything is collected and the lead qualifies, naturally offer ONE related coverage.\n\nENDING THE CALL:\nYou can end the call after the caller says goodbye. Always wait for the caller to say goodbye first.\n\nCLOSING:\nBriefly recap what you collected and confirm. Then close warmly: \"Mahalo for calling Equity Insurance! Val's going to look over everything and get back to you with your quote. We're always happy to help. Have a great day!\"";

const SYSTEM_PROMPT_AFTERHOURS = "You are the after-hours receptionist at Equity Insurance Inc., a 3rd-generation family-owned insurance agency in Honolulu, Hawaii. The office is closed right now -- business hours are 9 AM to 5 PM Hawaii time, Monday through Friday.\n\nBe warm and brief. You are just here to take a quick message so someone can call them back.\n\nHOW YOU TALK:\n- Sound like a real person, not a robot. Use contractions. Keep it short.\n- Vary your acknowledgments. Don't say the same thing twice.\n- React naturally to what people say.\n- 1 to 2 sentences max per response.\n\nCollect only:\n1. Full Name -- ask them to spell it.\n2. Phone Number -- repeat it back to confirm.\n3. Reason for calling -- brief description of what they need.\n\nIf they have an urgent claim or emergency, collect the details (name, phone, claim type, description) and call route_claim to trigger a priority alert to our team.\n\nRULES:\n- Never give coverage advice or make promises.\n- We are not affiliated with Equity Insurance in Tulsa, Oklahoma.\n- We don't offer Pet Insurance or Travel Insurance.\n- If unsure: \"Great question -- our team will cover that when they follow up with you.\"\n\nAfter collecting info, call save_field for each piece. Then close: \"Mahalo for calling Equity Insurance! Someone from our team will get back to you on the next business day. Have a good evening!\" Then wait for them to say goodbye, and end the call.\n\nENDING THE CALL:\nYou can end the call. Do it after the caller says goodbye or any farewell. Always let them say bye first -- don't hang up abruptly.";

// Inline assistant config builder (matches WF-01 exactly)
function getAssistantConfig(mode) {
    const isBiz = mode === 'business';
    const tools = isBiz
        ? [TOOL_SAVE_FIELD_BIZ, TOOL_CHECK_DISQUALIFIER, TOOL_CHECK_HOT_LEAD, TOOL_ROUTE_EXISTING, TOOL_ROUTE_CLAIM]
        : [TOOL_SAVE_FIELD_AH, TOOL_ROUTE_CLAIM_AH];
    return {
        firstMessage: isBiz
            ? "Aloha, thank you for calling Equity Insurance in Honolulu, Hawaii -- not affiliated with Equity Insurance in Tulsa, Oklahoma. How can I help you today?"
            : "Aloha, thank you for calling Equity Insurance in Honolulu, Hawaii. We are currently closed -- our business hours are 9 AM to 5 PM Hawaii time, Monday through Friday. I can take a message and have someone call you back. May I have your name?",
        model: {
            provider: 'openai', model: 'gpt-4o', temperature: 0.5, maxTokens: 300,
            messages: [{ role: 'system', content: isBiz ? SYSTEM_PROMPT_BUSINESS : SYSTEM_PROMPT_AFTERHOURS }],
            tools: tools
        },
        voice: isBiz ? SHARED_VOICE_BIZ : SHARED_VOICE_AH,
        transcriber: SHARED_TRANSCRIBER,
        ...SHARED_BEHAVIOR
    };
}

// ============================
// STATE
// ============================
let vapi = null;
let callActive = false;
let isMuted = false;
let currentMode = 'business';
let durationInterval = null;
let callStartTime = null;

// ============================
// CALL LIFECYCLE
// ============================
function activateCall() {
    if (callActive) return;
    callActive = true;
    callStartTime = Date.now();
    startDurationTimer();
    updateUI('active');
    updateCallStage('idle');
    logSystem('Call connection established.');

    // Ensure mic is unmuted when call starts
    isMuted = false;
    if (vapi) {
        try { vapi.setMuted(false); } catch (e) {}
    }
    const muteBtn = document.getElementById('muteBtn');
    if (muteBtn) {
        muteBtn.classList.remove('bg-danger', 'text-white', 'border-transparent');
        muteBtn.classList.add('glass', 'text-zinc-400');
        const muteIcon = muteBtn.querySelector('i') || muteBtn.querySelector('svg');
        if (muteIcon) muteIcon.setAttribute('data-lucide', 'mic');
    }

    document.getElementById('ambient-glow').classList.remove('opacity-0');
    document.getElementById('ring-1').classList.remove('opacity-0');
    document.getElementById('ring-2').classList.remove('opacity-0');
    document.getElementById('circle-visualizer').classList.remove('opacity-0');
    const micIcon = document.getElementById('main-mic-icon');
    if (micIcon) {
        micIcon.classList.add('text-primary');
        micIcon.classList.remove('text-zinc-500');
    }
    const micBar = document.getElementById('mic-level-bar');
    if (micBar) micBar.classList.remove('opacity-0');
}

function deactivateCall() {
    callActive = false;
    stopDurationTimer();
    updateUI('ended');
    logSystem('Call terminated.');
    document.getElementById('typing-indicator').classList.add('hidden');
    updateCallStage('complete');

    document.getElementById('ambient-glow').classList.add('opacity-0');
    document.getElementById('ring-1').classList.add('opacity-0');
    document.getElementById('ring-2').classList.add('opacity-0');
    document.getElementById('circle-visualizer').classList.add('opacity-0');
    const micIcon = document.getElementById('main-mic-icon');
    if (micIcon) {
        micIcon.classList.remove('text-primary');
        micIcon.classList.add('text-zinc-500');
    }
    const micBar = document.getElementById('mic-level-bar');
    if (micBar) micBar.classList.add('opacity-0');
    const partialEl = document.getElementById('partial-transcript');
    if (partialEl) { partialEl.textContent = ''; partialEl.classList.add('hidden'); }
}

// ============================
// VAPI INITIALIZATION
// ============================
function initVapi() {
    vapi = new Vapi(VAPI_PUBLIC_KEY);

    vapi.on('call-start', activateCall);
    vapi.on('call-started', activateCall);

    vapi.on('call-end', deactivateCall);
    vapi.on('call-ended', deactivateCall);

    vapi.on('speech-start', () => {
        activateCall();
        document.getElementById('typing-indicator').classList.remove('hidden');
        updateConnectionStatus('AI Speaking', 'text-primary', 'bg-primary');
        const micBar = document.getElementById('mic-level-bar');
        if (micBar) micBar.style.opacity = '0.3';
    });

    vapi.on('speech-end', () => {
        document.getElementById('typing-indicator').classList.add('hidden');
        updateConnectionStatus('Listening', 'text-success', 'bg-success');
        const micBar = document.getElementById('mic-level-bar');
        if (micBar) micBar.style.opacity = '1';
    });

    vapi.on('volume-level', (level) => {
        const bars = document.querySelectorAll('#circle-visualizer > div');
        const micBar = document.getElementById('mic-level-fill');
        if (micBar) {
            micBar.style.width = Math.min(level * 200, 100) + '%';
            micBar.style.backgroundColor = level > 0.05 ? '#22c55e' : '#71717a';
        }
        if (bars.length && callActive) {
            const h = [8, 12, 6];
            bars.forEach((bar, i) => {
                const boost = level * 40;
                bar.style.height = (h[i] + boost * (0.8 + Math.random() * 0.4)) + 'px';
            });
        }
    });

    vapi.on('message', (message) => {
        activateCall();

        if (message.type === 'transcript' && message.transcriptType === 'partial') {
            const partialEl = document.getElementById('partial-transcript');
            if (partialEl && message.role === 'user') {
                partialEl.textContent = message.transcript;
                partialEl.classList.remove('hidden');
            }
        }

        if (message.type === 'transcript' && message.transcriptType === 'final') {
            const partialEl = document.getElementById('partial-transcript');
            if (partialEl) {
                partialEl.textContent = '';
                partialEl.classList.add('hidden');
            }
            addTranscriptMessage(message.role, message.transcript);
        }
        if (message.type === 'function-call') {
            handleFunctionCall(message.functionCall);
        }
        if (message.type === 'tool-calls' && message.toolCalls) {
            message.toolCalls.forEach(tc => {
                if (tc.function) handleFunctionCall(tc.function);
            });
        }
        if (message.type === 'tool-calls-result' && message.toolCallResult) {
            handleToolCallResult(message.toolCallResult.id, message.toolCallResult.result);
        }
        if (message.type === 'function-call-result' || message.type === 'tool-call-result') {
            const result = message.result || message.functionCallResult?.result || '';
            handleToolCallResult(message.toolCallId || '', result);
        }
    });

    vapi.on('error', (error) => {
        console.error('VAPI Error (full):', JSON.stringify(error, null, 2));
        let errMsg;
        try {
            const inner = error?.error?.error || error?.error || error;
            errMsg = typeof inner?.message === 'string' ? inner.message
                   : typeof inner?.message === 'object' ? JSON.stringify(inner.message)
                   : JSON.stringify(inner);
        } catch (e) {
            errMsg = String(error);
        }
        const errStatus = error?.error?.statusCode || error?.statusCode || '';

        const isKrisp = errMsg?.includes('Krisp') || errMsg?.includes('krisp')
            || errMsg?.includes('SAMPLE_RATE') || errMsg?.includes('mic processor');
        if (isKrisp) {
            console.warn('Non-fatal Krisp/audio warning (suppressed):', errMsg);
            logSystem('<span class="text-amber-400">AUDIO</span> Noise filter unavailable (non-fatal) — call continues');
            return;
        }

        const isEjection = errMsg?.includes('ejected') || errMsg?.includes('Meeting has ended');
        if (isEjection) {
            logSystem(`<span class="text-red-400">EJECTED</span> Daily.co session ended — type: ${error?.type}, action: ${error?.error?.action}`);
            if (callActive) deactivateCall();
            else updateUI('error');
            return;
        }

        const isFatal = error?.type === 'start-method-error'
            || errStatus >= 400
            || errMsg?.includes('start')
            || errMsg?.includes('unauthorized');
        if (isFatal && !callActive) {
            updateUI('error');
        }
        logSystem(`${isFatal ? 'FATAL' : 'Warning'}: ${errMsg}`);
    });
}

// ============================
// FUNCTION CALL HANDLERS
// ============================
function handleFunctionCall(fn) {
    const args = (() => {
        try { return typeof fn.arguments === 'string' ? JSON.parse(fn.arguments) : (fn.arguments || {}); }
        catch (e) { console.error('Error parsing args for', fn.name, e); return {}; }
    })();

    switch (fn.name) {
        case 'save_field':
            logSystem(`<span class="text-blue-400">SAVE</span> ${args.field_name} = "${args.field_value}"`);
            updateDataTable(args.field_name, args.field_value);
            updateCallStage('collecting');
            break;
        case 'check_disqualifier':
            logSystem('<span class="text-amber-400">RULE CHECK</span> Disqualifier evaluation triggered');
            updateStatusBadge('disqualifier', 'checking', 'Evaluating...');
            updateCallStage('evaluating');
            break;
        case 'check_hot_lead':
            logSystem('<span class="text-amber-400">RULE CHECK</span> Hot lead evaluation triggered');
            updateStatusBadge('hotlead', 'checking', 'Evaluating...');
            updateCallStage('evaluating');
            break;
        case 'route_existing_customer':
            logSystem('<span class="text-purple-400">ROUTE</span> Existing customer → Ticket + Val notification');
            updateStatusBadge('calltype', 'info', 'Existing Customer');
            updateCallStage('routing');
            break;
        case 'route_claim':
            logSystem('<span class="text-red-400">ROUTE</span> Claim filed → Priority notification sent');
            updateStatusBadge('calltype', 'urgent', 'Claim Filed');
            updateCallStage('routing');
            break;
        default:
            logSystem(`Function: ${fn.name}`);
    }
}

function handleToolCallResult(toolCallId, result) {
    const r = (result || '').toLowerCase();
    if (r.includes('not disqualified') || r.includes('qualifies')) {
        updateStatusBadge('disqualifier', 'pass', 'Qualified');
        logSystem('<span class="text-emerald-400">PASS</span> Caller qualifies — no disqualifiers');
    } else if (r.includes('disqualified')) {
        updateStatusBadge('disqualifier', 'fail', 'Disqualified');
        logSystem('<span class="text-red-400">FAIL</span> Caller disqualified');
    }
    if (r.includes('hot lead') || r.includes('high value') || r.includes('transfer')) {
        updateStatusBadge('hotlead', 'hot', 'HOT LEAD — Transfer');
        logSystem('<span class="text-orange-400">HOT LEAD</span> High-value — transferring to agent');
        updateCallStage('routing');
    } else if (r.includes('not a hot lead') || r.includes('standard') || r.includes('not hot')) {
        updateStatusBadge('hotlead', 'pass', 'Standard Lead');
        logSystem('<span class="text-emerald-400">PASS</span> Standard lead — continue intake');
    }
    if (r.includes('ticket created') || r.includes('notification sent')) {
        updateCallStage('complete');
        logSystem('<span class="text-emerald-400">DONE</span> Workflow actions completed');
    }
}

// ============================
// CALL CONTROLS
// ============================
async function toggleCall() {
    if (callActive) {
        logSystem('Ending call...');
        try {
            vapi.stop();
        } catch (err) {
            console.error('Error stopping call:', err);
        }
        setTimeout(() => {
            if (callActive) {
                logSystem('Force-ending call (event timeout).');
                deactivateCall();
            }
        }, 3000);
    } else {
        updateUI('connecting');
        try {
            const config = getAssistantConfig(currentMode);
            logSystem(`Initializing call (${currentMode} mode, inline config, voice: ${config.voice.voiceId})...`);
            await vapi.start(config);
        } catch (err) {
            updateUI('error');
            console.error('Start call error (full):', JSON.stringify(err, null, 2));
            let detail;
            try {
                const inner = err?.error?.error || err?.error || err;
                detail = typeof inner?.message === 'string' ? inner.message
                       : typeof inner?.message === 'object' ? JSON.stringify(inner.message)
                       : err?.message || JSON.stringify(err);
            } catch (e) {
                detail = String(err);
            }
            logSystem('Failed to start: ' + detail);
        }
    }
}

function toggleMute() {
    if (!callActive) return;
    isMuted = !isMuted;
    vapi.setMuted(isMuted);
    const btn = document.getElementById('muteBtn');
    const icon = btn.querySelector('i') || btn.querySelector('svg');

    if (isMuted) {
        btn.classList.add('bg-danger', 'text-white', 'border-transparent');
        btn.classList.remove('glass', 'text-zinc-400');
        if (icon) icon.setAttribute('data-lucide', 'mic-off');
    } else {
        btn.classList.remove('bg-danger', 'text-white', 'border-transparent');
        btn.classList.add('glass', 'text-zinc-400');
        if (icon) icon.setAttribute('data-lucide', 'mic');
    }
    lucide.createIcons();
}

function setMode(mode) {
    if (callActive) return;
    currentMode = mode;
    const bizBtn = document.getElementById('mode-biz');
    const ahBtn = document.getElementById('mode-ah');

    if (mode === 'business') {
        bizBtn.className = 'px-4 py-2 rounded-md text-xs font-semibold transition-all duration-200 bg-primary text-white shadow-lg shadow-primary/25';
        ahBtn.className = 'px-4 py-2 rounded-md text-xs font-semibold transition-all duration-200 text-zinc-400 hover:text-white hover:bg-white/5';
    } else {
        ahBtn.className = 'px-4 py-2 rounded-md text-xs font-semibold transition-all duration-200 bg-primary text-white shadow-lg shadow-primary/25';
        bizBtn.className = 'px-4 py-2 rounded-md text-xs font-semibold transition-all duration-200 text-zinc-400 hover:text-white hover:bg-white/5';
    }
}

// ============================
// UI UPDATES
// ============================
function updateUI(state) {
    const btn = document.getElementById('callBtn');
    const muteBtn = document.getElementById('muteBtn');
    const statusText = document.getElementById('call-state-text');
    const btnIcon = btn.querySelector('i') || btn.querySelector('svg');

    switch (state) {
        case 'connecting':
            btn.disabled = true;
            btn.classList.add('opacity-75');
            statusText.textContent = 'Connecting...';
            updateConnectionStatus('Connecting', 'text-accent', 'bg-accent');
            break;
        case 'active':
            btn.disabled = false;
            btn.classList.remove('opacity-75', 'bg-white', 'text-black');
            btn.classList.add('bg-danger', 'text-white', 'shadow-danger/40');
            if (btnIcon) btnIcon.setAttribute('data-lucide', 'phone-off');
            statusText.textContent = 'Live Call';
            muteBtn.disabled = false;
            updateConnectionStatus('Connected', 'text-success', 'bg-success');
            break;
        case 'ended':
        case 'error':
            btn.disabled = false;
            btn.classList.remove('opacity-75', 'bg-danger', 'text-white', 'shadow-danger/40');
            btn.classList.add('bg-white', 'text-black');
            if (btnIcon) btnIcon.setAttribute('data-lucide', 'phone');
            statusText.textContent = state === 'error' ? 'Connection Failed' : 'Call Ended';
            muteBtn.disabled = true;
            updateConnectionStatus('Disconnected', 'text-zinc-400', 'bg-zinc-500');
            break;
    }
    lucide.createIcons();
}

function updateConnectionStatus(text, textColor, dotColor) {
    const statusEl = document.getElementById('connection-status');
    const dotEl = document.getElementById('status-dot');
    const pingEl = document.getElementById('status-ping');

    statusEl.textContent = text;
    statusEl.className = `text-xs font-semibold uppercase tracking-wide ${textColor}`;
    dotEl.className = `relative w-2.5 h-2.5 rounded-full ${dotColor} transition-colors duration-300`;
    pingEl.className = `status-dot-pulse ${dotColor} ${text === 'Disconnected' ? 'hidden' : 'block'}`;
}

function updateDataTable(key, value) {
    const tbody = document.getElementById('data-table-body');
    if (tbody.querySelector('td[colspan="2"]')) {
        tbody.innerHTML = '';
    }

    let row = document.getElementById(`row-${key}`);
    if (!row) {
        row = document.createElement('tr');
        row.id = `row-${key}`;
        row.className = 'border-b border-white/5 hover:bg-white/5 transition-colors animate-slide-up';
        row.innerHTML = `
            <td class="px-6 py-3 font-mono text-xs text-zinc-500">${key}</td>
            <td class="px-6 py-3 text-sm text-zinc-200 font-medium" id="val-${key}"></td>
        `;
        tbody.appendChild(row);
    }

    const valCell = row.querySelector(`#val-${key}`);
    valCell.textContent = value;
    valCell.classList.add('text-accent');
    setTimeout(() => valCell.classList.remove('text-accent'), 1500);

    const rows = tbody.querySelectorAll('tr');
    const total = currentMode === 'business' ? 12 : 3;
    document.getElementById('field-count').textContent = `${rows.length} / ${total}+`;
}

const stageOrder = ['idle', 'collecting', 'evaluating', 'routing', 'complete'];

function updateCallStage(stage) {
    const idx = stageOrder.indexOf(stage);
    stageOrder.forEach((s, i) => {
        const el = document.getElementById(`stage-${s}`);
        if (!el) return;
        if (i < idx) {
            el.className = 'w-full h-1.5 rounded-full bg-success transition-all duration-500';
        } else if (i === idx) {
            el.className = 'w-full h-1.5 rounded-full bg-primary animate-pulse transition-all duration-500';
        } else {
            el.className = 'w-full h-1.5 rounded-full bg-zinc-700 transition-all duration-500';
        }
    });
}

function updateStatusBadge(type, status, text) {
    const container = document.getElementById('status-badges');
    const badge = document.getElementById(`badge-${type}`);
    const label = document.getElementById(`badge-${type}-text`);
    if (!badge || !label) return;

    container.classList.remove('hidden');
    badge.classList.remove('hidden');
    label.textContent = text;

    badge.className = 'flex items-center gap-2 px-3 py-1.5 rounded-lg border';
    const icon = badge.querySelector('svg, i');

    switch (status) {
        case 'checking':
            badge.classList.add('bg-amber-500/10', 'border-amber-500/20');
            label.classList.add('text-amber-400');
            if (icon) icon.classList.add('text-amber-400');
            break;
        case 'pass':
            badge.classList.add('bg-emerald-500/10', 'border-emerald-500/20');
            label.classList.add('text-emerald-400');
            if (icon) icon.classList.add('text-emerald-400');
            break;
        case 'fail':
            badge.classList.add('bg-red-500/10', 'border-red-500/20');
            label.classList.add('text-red-400');
            if (icon) icon.classList.add('text-red-400');
            break;
        case 'hot':
            badge.classList.add('bg-orange-500/10', 'border-orange-500/20');
            label.classList.add('text-orange-400');
            if (icon) icon.classList.add('text-orange-400');
            break;
        case 'info':
            badge.classList.add('bg-purple-500/10', 'border-purple-500/20');
            label.classList.add('text-purple-400');
            if (icon) icon.classList.add('text-purple-400');
            break;
        case 'urgent':
            badge.classList.add('bg-red-500/10', 'border-red-500/20');
            label.classList.add('text-red-400');
            if (icon) icon.classList.add('text-red-400');
            break;
        default:
            badge.classList.add('bg-surface', 'border-white/5');
    }
    lucide.createIcons();
}

// ============================
// TRANSCRIPT
// ============================
function addTranscriptMessage(role, text) {
    const container = document.getElementById('transcript');
    if (container.querySelector('.text-zinc-600')) {
        container.innerHTML = '';
    }

    const isAi = role === 'assistant';
    const div = document.createElement('div');
    div.className = `flex ${isAi ? 'justify-start' : 'justify-end'} animate-slide-up`;

    div.innerHTML = `
        <div class="max-w-[85%] ${isAi ? 'bg-surfaceHighlight border border-white/5 text-zinc-200' : 'bg-primary text-white shadow-lg shadow-primary/20'} rounded-2xl px-5 py-3.5 text-sm leading-relaxed">
            ${text}
        </div>
    `;

    container.appendChild(div);
    container.scrollTop = container.scrollHeight;
}

function clearTranscript() {
    document.getElementById('transcript').innerHTML = `
        <div class="h-full flex flex-col items-center justify-center text-zinc-600 gap-4 opacity-50">
            <i data-lucide="bot" class="w-12 h-12 stroke-1"></i>
            <p class="text-sm font-medium">Waiting for call to start...</p>
        </div>
    `;
    lucide.createIcons();
}

// ============================
// SYSTEM LOGS
// ============================
function logSystem(text) {
    const container = document.getElementById('system-logs');
    const div = document.createElement('div');
    const time = new Date().toLocaleTimeString('en-US', { hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' });
    div.className = 'text-zinc-500 hover:text-zinc-300 transition-colors';
    div.innerHTML = `<span class="text-zinc-700 mr-2">[${time}]</span>${text}`;
    container.appendChild(div);
    container.scrollTop = container.scrollHeight;
}

// ============================
// TIMER
// ============================
function startDurationTimer() {
    stopDurationTimer();
    durationInterval = setInterval(() => {
        if (!callStartTime) return;
        const elapsed = Math.floor((Date.now() - callStartTime) / 1000);
        const min = String(Math.floor(elapsed / 60)).padStart(2, '0');
        const sec = String(elapsed % 60).padStart(2, '0');
        document.getElementById('timer').textContent = min + ':' + sec;
    }, 1000);
}

function stopDurationTimer() {
    if (durationInterval) {
        clearInterval(durationInterval);
        durationInterval = null;
    }
}

// ============================
// MIC PATCH: Cap sample rate at 48kHz to prevent Krisp crash
// ============================
(function patchGetUserMedia() {
    const original = navigator.mediaDevices.getUserMedia.bind(navigator.mediaDevices);
    navigator.mediaDevices.getUserMedia = async function (constraints) {
        if (constraints && constraints.audio) {
            if (typeof constraints.audio === 'boolean') {
                constraints.audio = {
                    sampleRate: { ideal: 48000, max: 48000 },
                    echoCancellation: true,
                    noiseSuppression: true,
                    autoGainControl: true
                };
            } else if (typeof constraints.audio === 'object') {
                constraints.audio.sampleRate = { ideal: 48000, max: 48000 };
                if (constraints.audio.echoCancellation === undefined) constraints.audio.echoCancellation = true;
                if (constraints.audio.noiseSuppression === undefined) constraints.audio.noiseSuppression = true;
                if (constraints.audio.autoGainControl === undefined) constraints.audio.autoGainControl = true;
            }
            console.log('[MIC] getUserMedia audio constraints:', JSON.stringify(constraints.audio));
        }
        return original(constraints);
    };
})();

// Suppress uncaught Krisp promise rejections
window.addEventListener('unhandledrejection', (event) => {
    const msg = String(event.reason?.message || event.reason || '');
    if (msg.includes('Krisp') || msg.includes('krisp') || msg.includes('SAMPLE_RATE')) {
        event.preventDefault();
        console.warn('Suppressed Krisp error:', msg);
    }
});

// ============================
// BOOT — Load VAPI Web SDK
// ============================
async function boot() {
    try {
        const module = await import('https://cdn.jsdelivr.net/npm/@vapi-ai/web@latest/+esm');
        const VapiClass = module.default?.default || module.default || module.Vapi;
        if (!VapiClass || typeof VapiClass !== 'function') {
            console.log('Module exports:', Object.keys(module), 'default type:', typeof module.default);
            throw new Error('Could not find Vapi constructor in module');
        }
        window.Vapi = VapiClass;
        logSystem('VAPI SDK loaded successfully.');
        initVapi();
    } catch (err) {
        console.error('Failed to load VAPI SDK:', err);
        logSystem('ERROR: Failed to load VAPI SDK — ' + err.message);
    }
}
boot();
