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

// VAPI Assistant IDs (created via API with full tool + n8n webhook config)
const ASSISTANT_ID_BUSINESS = 'bbf67fe2-99dc-427a-a546-37892f58a796';
const ASSISTANT_ID_AFTERHOURS = '8ae61948-d6c5-4586-9f55-b7c1416db25b';

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
            const assistantId = currentMode === 'business' ? ASSISTANT_ID_BUSINESS : ASSISTANT_ID_AFTERHOURS;
            logSystem(`Initializing call (${currentMode} mode, assistant: ${assistantId.slice(0, 8)}...)...`);
            await vapi.start(assistantId);
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
    document.getElementById('field-count').textContent = `${rows.length} / 8`;
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
