import re

with open('ai-receptionist-docs.html', 'r', encoding='utf-8') as f:
    content = f.read()

new_css = """<style>
  :root {
    --bg: #ffffff;
    --surface: #ffffff;
    --surface-2: #f4f4f5;
    --surface-3: #e4e4e7;
    --border: #18181b;
    --border-light: #d4d4d8;
    --text: #09090b;
    --text-dim: #3f3f46;
    --text-muted: #71717a;
    
    /* Technical Colors for Guidance */
    --primary: #2563eb;
    --primary-bg: #eff6ff;
    --success: #16a34a;
    --success-bg: #f0fdf4;
    --warning: #d97706;
    --warning-bg: #fffbeb;
    --danger: #dc2626;
    --danger-bg: #fef2f2;
    --info: #0284c7;
    --info-bg: #f0f9ff;
    --purple: #7c3aed;
    --purple-bg: #f5f3ff;
  }

  * { margin: 0; padding: 0; box-sizing: border-box; }

  body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.6;
    overflow-x: hidden;
    -webkit-font-smoothing: antialiased;
  }

  code, .flow-node, .wf-flow, .sheet-col .col-name, .hero-badge, .toc a, .section-label, .flow-label, .branch-label, .timeline-dot, .wf-icon, .wf-subtitle, .wf-tag, .data-table th, .badge, .convo-info .name, .convo-info .status, .msg .sender, .convo-action, .sheet-card .tab-name, .email-subject, .rule-threshold, footer {
    font-family: 'JetBrains Mono', 'Fira Code', Consolas, monospace;
  }

  /* ── Hero ── */
  .hero {
    padding: 100px 40px 80px;
    text-align: center;
    background: var(--bg);
    border-bottom: 2px solid var(--border);
    position: relative;
  }
  .hero::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background-image: linear-gradient(var(--surface-3) 1px, transparent 1px), linear-gradient(90deg, var(--surface-3) 1px, transparent 1px);
    background-size: 32px 32px;
    z-index: 0;
    opacity: 0.6;
  }
  .hero > * {
    position: relative;
    z-index: 1;
  }
  .hero-badge {
    display: inline-flex; align-items: center; gap: 8px;
    padding: 8px 16px; border: 2px solid var(--border);
    font-size: 13px; font-weight: 700;
    text-transform: uppercase;
    margin-bottom: 24px;
    background: var(--primary-bg);
    color: var(--primary);
    box-shadow: 4px 4px 0px var(--border);
  }
  .hero h1 {
    font-size: 64px; font-weight: 800; letter-spacing: -0.03em;
    color: var(--text);
    margin-bottom: 24px;
    text-transform: uppercase;
  }
  .hero p { font-size: 20px; color: var(--text-dim); max-width: 680px; margin: 0 auto 40px; font-weight: 500; }
  .hero-stats {
    display: flex; justify-content: center; gap: 32px; flex-wrap: wrap;
    padding-top: 16px;
  }
  .hero-stat {
    text-align: center;
    border: 2px solid var(--border);
    padding: 24px 40px;
    background: var(--bg);
    box-shadow: 6px 6px 0px var(--border);
    min-width: 160px;
  }
  .hero-stat .num { font-size: 40px; font-weight: 800; font-family: monospace; color: var(--primary); }
  .hero-stat .label { font-size: 13px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-top: 8px; }

  /* ── Nav ── */
  .toc {
    position: sticky; top: 0; z-index: 100;
    background: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(8px);
    border-bottom: 2px solid var(--border);
    padding: 0 24px;
    overflow-x: auto;
  }
  .toc-inner {
    display: flex; gap: 16px; max-width: 1200px; margin: 0 auto;
    padding: 16px 0;
  }
  .toc a {
    color: var(--text); text-decoration: none; font-size: 14px; font-weight: 700;
    padding: 8px 16px; border: 2px solid transparent;
    transition: all 0.2s;
    text-transform: uppercase;
  }
  .toc a:hover { border-color: var(--border); background: var(--primary-bg); color: var(--primary); box-shadow: 4px 4px 0px var(--border); }

  /* ── Container ── */
  .container { max-width: 1200px; margin: 0 auto; padding: 0 24px; }

  /* ── Sections ── */
  section { padding: 100px 0; }
  section + section { border-top: 4px solid var(--border); }

  .section-label {
    font-size: 14px; text-transform: uppercase; letter-spacing: 2px;
    font-weight: 800; margin-bottom: 20px;
    display: inline-block; padding: 8px 16px; background: var(--primary); color: white;
  }
  .section-title {
    font-size: 40px; font-weight: 800; letter-spacing: -0.02em; margin-bottom: 20px; text-transform: uppercase;
  }
  .section-desc {
    font-size: 20px; color: var(--text-dim); max-width: 720px; margin-bottom: 56px; font-weight: 500;
  }

  /* ── Cards ── */
  .card {
    background: var(--bg);
    border: 2px solid var(--border);
    padding: 40px;
    margin-bottom: 32px;
    box-shadow: 8px 8px 0px var(--border);
  }
  .card h3 {
    font-size: 22px; font-weight: 800; margin-bottom: 16px;
    display: flex; align-items: center; gap: 12px;
    text-transform: uppercase; letter-spacing: 0.5px;
    border-bottom: 2px solid var(--border);
    padding-bottom: 16px;
  }
  .card p { color: var(--text-dim); font-size: 16px; font-weight: 500; }

  /* ── Flow Diagram ── */
  .flow-diagram {
    position: relative;
    padding: 60px 40px;
    overflow-x: auto;
    background: var(--surface-2);
    border: 2px solid var(--border);
    margin-top: 32px;
    background-image: radial-gradient(var(--border-light) 2px, transparent 2px);
    background-size: 24px 24px;
  }
  .flow-row {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 16px;
    margin-bottom: 32px;
    flex-wrap: wrap;
  }
  .flow-node {
    position: relative;
    padding: 20px 32px;
    border: 2px solid var(--border);
    background: var(--bg);
    font-size: 15px;
    font-weight: 800;
    text-align: center;
    min-width: 180px;
    max-width: 260px;
    line-height: 1.5;
    flex-shrink: 0;
    box-shadow: 6px 6px 0px var(--border);
    text-transform: uppercase;
  }
  .flow-node small {
    display: block; font-weight: 600; color: var(--text-dim); margin-top: 12px; font-family: 'Inter', sans-serif; font-size: 13px; text-transform: none; border-top: 2px dashed var(--border-light); padding-top: 12px;
  }
  .flow-node.decision {
    background: var(--text);
    color: var(--bg);
  }
  .flow-node.decision small { color: var(--surface-3); border-top-color: var(--text-dim); }
  
  /* Adding colored borders/shadows to flow nodes for guidance */
  .flow-node.phone { border-color: var(--purple); box-shadow: 6px 6px 0px var(--purple); }
  .flow-node.talkroute { border-color: var(--warning); box-shadow: 6px 6px 0px var(--warning); }
  .flow-node.vapi { border-color: var(--primary); box-shadow: 6px 6px 0px var(--primary); }
  .flow-node.n8n { border-color: var(--success); box-shadow: 6px 6px 0px var(--success); }
  .flow-node.sheets { border-color: var(--info); box-shadow: 6px 6px 0px var(--info); }
  .flow-node.email { border-color: var(--danger); box-shadow: 6px 6px 0px var(--danger); }
  .flow-node.crm { border-color: var(--warning); box-shadow: 6px 6px 0px var(--warning); }

  /* Arrows styling to point correctly */
  .flow-arrow {
    color: var(--text);
    font-size: 28px;
    font-weight: 900;
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .flow-arrow-down {
    text-align: center;
    color: var(--text);
    font-size: 28px;
    font-weight: 900;
    padding: 16px 0;
    display: flex;
    justify-content: center;
  }
  .flow-label {
    font-size: 13px;
    font-weight: 800;
    color: var(--bg);
    text-align: center;
    padding: 8px 20px;
    background: var(--text);
    display: inline-block;
    border: 2px solid var(--border);
    margin: 0 auto;
    text-transform: uppercase;
    box-shadow: 4px 4px 0px var(--border-light);
  }
  .flow-branch {
    display: flex;
    gap: 48px;
    justify-content: center;
    flex-wrap: wrap;
    margin: 40px 0;
    align-items: flex-start;
  }
  .flow-branch-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 24px;
    padding: 32px;
    border: 2px dashed var(--border);
    background: var(--bg);
    min-width: 320px;
    box-shadow: 8px 8px 0px var(--border-light);
  }
  .flow-branch-item.new-customer { border-color: var(--info); box-shadow: 8px 8px 0px var(--info-bg); }
  .flow-branch-item.existing-customer { border-color: var(--success); box-shadow: 8px 8px 0px var(--success-bg); }
  .flow-branch-item.insurance-claim { border-color: var(--danger); box-shadow: 8px 8px 0px var(--danger-bg); }
  
  .branch-label {
    font-size: 14px;
    font-weight: 800;
    padding: 10px 24px;
    border: 2px solid var(--border);
    background: var(--text);
    color: var(--bg);
    text-transform: uppercase;
    box-shadow: 4px 4px 0px var(--border-light);
  }
  .branch-label.info { background: var(--info); border-color: var(--info); box-shadow: 4px 4px 0px var(--info-bg); color: white;}
  .branch-label.success { background: var(--success); border-color: var(--success); box-shadow: 4px 4px 0px var(--success-bg); color: white;}
  .branch-label.danger { background: var(--danger); border-color: var(--danger); box-shadow: 4px 4px 0px var(--danger-bg); color: white;}

  /* ── Big Flow (Master Diagram) ── */
  .master-flow {
    background: var(--bg);
    border: 4px solid var(--border);
    padding: 60px 40px;
    overflow-x: auto;
    box-shadow: 12px 12px 0px var(--border);
    background-image: radial-gradient(var(--surface-3) 2px, transparent 2px);
    background-size: 24px 24px;
  }
  .master-flow h3 {
    text-align: center; font-size: 28px; font-weight: 800; margin-bottom: 60px; text-transform: uppercase; letter-spacing: 2px;
    background: var(--text); color: var(--bg); display: inline-block; padding: 12px 32px; border: 2px solid var(--border);
  }

  /* ── Step Timeline ── */
  .timeline {
    position: relative;
    padding-left: 80px;
  }
  .timeline::before {
    content: '';
    position: absolute;
    left: 28px; top: 0; bottom: 0;
    width: 4px;
    background: var(--surface-3);
  }
  .timeline-item {
    position: relative;
    margin-bottom: 64px;
  }
  .timeline-dot {
    position: absolute;
    left: -80px; top: 0;
    width: 60px; height: 60px;
    background: var(--bg);
    border: 4px solid var(--text);
    display: flex; align-items: center; justify-content: center;
    font-size: 24px; font-weight: 800;
    box-shadow: 6px 6px 0px var(--border);
  }
  .timeline-dot.step1 { border-color: var(--purple); color: var(--purple); box-shadow: 6px 6px 0px var(--purple-bg); }
  .timeline-dot.step2 { border-color: var(--info); color: var(--info); box-shadow: 6px 6px 0px var(--info-bg); }
  .timeline-dot.step3 { border-color: var(--success); color: var(--success); box-shadow: 6px 6px 0px var(--success-bg); }
  .timeline-dot.step4 { border-color: var(--warning); color: var(--warning); box-shadow: 6px 6px 0px var(--warning-bg); }
  .timeline-dot.step5 { border-color: var(--danger); color: var(--danger); box-shadow: 6px 6px 0px var(--danger-bg); }
  .timeline-dot.step6 { border-color: var(--primary); color: var(--primary); box-shadow: 6px 6px 0px var(--primary-bg); }
  
  .timeline-content h4 { font-size: 24px; font-weight: 800; margin-bottom: 16px; text-transform: uppercase; }
  .timeline-content p { color: var(--text-dim); font-size: 18px; font-weight: 500; }
  .timeline-detail {
    margin-top: 24px;
    background: var(--surface-2);
    border: 2px solid var(--border);
    padding: 24px 32px;
    box-shadow: 6px 6px 0px var(--border);
  }
  .timeline-detail ul { list-style: none; }
  .timeline-detail li {
    padding: 10px 0; font-size: 16px; color: var(--text-dim);
    display: flex; align-items: flex-start; gap: 16px;
    font-weight: 600;
  }
  .timeline-detail li::before { content: '>'; font-family: monospace; font-weight: 900; font-size: 18px; }
  .timeline-detail.primary li::before { color: var(--purple); }
  .timeline-detail.info li::before { color: var(--info); }
  .timeline-detail.success li::before { color: var(--success); }
  .timeline-detail.accent li::before { color: var(--warning); }
  .timeline-detail.danger li::before { color: var(--danger); }
  .timeline-detail.cyan li::before { color: var(--primary); }

  /* ── Workflow Cards ── */
  .wf-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(360px, 1fr));
    gap: 40px;
  }
  .wf-card {
    background: var(--bg);
    border: 2px solid var(--border);
    padding: 40px;
    box-shadow: 8px 8px 0px var(--border);
    transition: transform 0.2s, box-shadow 0.2s;
  }
  .wf-card:hover { transform: translate(-4px, -4px); box-shadow: 12px 12px 0px var(--border); }
  .wf-header {
    display: flex; align-items: center; gap: 20px; margin-bottom: 24px;
    border-bottom: 2px solid var(--border);
    padding-bottom: 20px;
  }
  .wf-icon {
    width: 64px; height: 64px;
    border: 2px solid var(--border);
    display: flex; align-items: center; justify-content: center;
    font-size: 28px; font-weight: 800;
    background: var(--text); color: var(--bg);
    flex-shrink: 0;
  }
  .wf-icon.wf1 { background: var(--primary-bg); color: var(--primary); border-color: var(--primary); }
  .wf-icon.wf2 { background: var(--info-bg); color: var(--info); border-color: var(--info); }
  .wf-icon.wf3 { background: var(--warning-bg); color: var(--warning); border-color: var(--warning); }
  .wf-icon.wf4 { background: var(--success-bg); color: var(--success); border-color: var(--success); }
  .wf-icon.wf5 { background: var(--danger-bg); color: var(--danger); border-color: var(--danger); }
  .wf-icon.wf6 { background: var(--purple-bg); color: var(--purple); border-color: var(--purple); }
  .wf-icon.wf7 { background: var(--info-bg); color: var(--info); border-color: var(--info); }

  .wf-title { font-size: 22px; font-weight: 800; text-transform: uppercase; }
  .wf-subtitle { font-size: 14px; color: var(--text-dim); margin-top: 6px; font-weight: 700; }
  .wf-body { font-size: 16px; color: var(--text-dim); margin-bottom: 24px; line-height: 1.6; font-weight: 500; }
  .wf-flow {
    background: var(--surface-2);
    border: 2px solid var(--border);
    padding: 24px;
    font-size: 14px;
    color: var(--text);
    line-height: 1.8;
    overflow-x: auto;
    white-space: pre;
    font-weight: 700;
  }
  .wf-tags {
    display: flex; gap: 12px; flex-wrap: wrap; margin-top: 24px;
  }
  .wf-tag {
    padding: 8px 16px; border: 2px solid var(--border); font-size: 12px; font-weight: 800;
    background: var(--bg); text-transform: uppercase; box-shadow: 2px 2px 0px var(--border);
  }
  .wf-tag.webhook { border-color: var(--primary); color: var(--primary); }
  .wf-tag.sheets { border-color: var(--info); color: var(--info); }
  .wf-tag.gmail { border-color: var(--danger); color: var(--danger); }
  .wf-tag.subwf { border-color: var(--warning); color: var(--warning); }
  .wf-tag.cron { border-color: var(--success); color: var(--success); }
  .wf-tag.vapi-api { border-color: var(--purple); color: var(--purple); }

  /* ── Data Tables ── */
  .data-table {
    width: 100%; border-collapse: collapse; margin: 24px 0;
    font-size: 16px; border: 2px solid var(--border);
    background: var(--bg);
  }
  .data-table th {
    text-align: left; padding: 20px 24px;
    background: var(--text); color: var(--bg);
    font-weight: 800; font-size: 14px;
    border-bottom: 2px solid var(--border);
    border-right: 2px solid var(--border);
  }
  .data-table td {
    padding: 20px 24px; border-bottom: 2px solid var(--border);
    border-right: 2px solid var(--border);
    color: var(--text-dim); font-weight: 600;
  }
  .data-table tr:last-child td { border-bottom: none; }
  .data-table code {
    background: var(--surface-2); padding: 6px 12px; border: 2px solid var(--border);
    font-size: 14px; color: var(--text); font-weight: 800;
  }

  /* ── Badges ── */
  .badge {
    display: inline-flex; padding: 6px 16px; border: 2px solid var(--border);
    font-size: 12px; font-weight: 800; text-transform: uppercase;
    background: var(--text); color: var(--bg);
  }
  .badge.active { background: var(--success-bg); color: var(--success); border-color: var(--success); }
  .badge.pending { background: var(--warning-bg); color: var(--warning); border-color: var(--warning); }
  .badge.disabled { background: var(--surface-3); color: var(--text-muted); border-color: var(--border-light); }

  /* ── Output Cards ── */
  .output-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 40px;
  }
  .output-card {
    background: var(--bg);
    border: 2px solid var(--border);
    padding: 40px;
    box-shadow: 8px 8px 0px var(--border);
  }
  .output-card h4 {
    font-size: 20px; font-weight: 800; margin-bottom: 24px;
    display: flex; align-items: center; gap: 16px; border-bottom: 2px solid var(--border); padding-bottom: 20px;
    text-transform: uppercase;
  }
  .output-card .icon {
    width: 48px; height: 48px; border: 2px solid var(--border);
    display: flex; align-items: center; justify-content: center;
    font-size: 20px; background: var(--text); color: var(--bg);
  }
  .output-card:nth-child(1) .icon { background: var(--info-bg); color: var(--info); border-color: var(--info); }
  .output-card:nth-child(2) .icon { background: var(--success-bg); color: var(--success); border-color: var(--success); }
  .output-card:nth-child(3) .icon { background: var(--danger-bg); color: var(--danger); border-color: var(--danger); }
  .output-card:nth-child(4) .icon { background: var(--primary-bg); color: var(--primary); border-color: var(--primary); }
  .output-card:nth-child(5) .icon { background: var(--warning-bg); color: var(--warning); border-color: var(--warning); }
  .output-card:nth-child(6) .icon { background: var(--warning-bg); color: var(--warning); border-color: var(--warning); }
  
  .output-card ul {
    list-style: none;
  }
  .output-card li {
    padding: 10px 0; font-size: 16px; color: var(--text-dim); display: flex; align-items: flex-start; gap: 16px; font-weight: 600;
  }
  .output-card li::before { content: '■'; font-size: 12px; color: var(--text); margin-top: 4px; }

  /* ── Conversation Demo ── */
  .convo-demo {
    max-width: 680px; margin: 0 auto;
    background: var(--bg);
    border: 4px solid var(--border);
    box-shadow: 12px 12px 0px var(--border);
  }
  .convo-header {
    background: var(--text);
    padding: 24px 32px;
    display: flex; align-items: center; gap: 20px;
    border-bottom: 4px solid var(--border);
  }
  .convo-avatar {
    width: 56px; height: 56px; border: 2px solid var(--bg);
    background: var(--bg);
    display: flex; align-items: center; justify-content: center;
    font-size: 24px; color: var(--text);
  }
  .convo-info .name { font-size: 16px; font-weight: 800; color: var(--bg); text-transform: uppercase;}
  .convo-info .status { font-size: 13px; color: var(--success); font-weight: 700;}
  .convo-body { padding: 40px; display: flex; flex-direction: column; gap: 24px; background: var(--surface-2); }
  .msg {
    max-width: 85%; padding: 20px 24px;
    font-size: 16px; line-height: 1.6; font-weight: 600;
    border: 2px solid var(--border);
    background: var(--bg);
    box-shadow: 4px 4px 0px var(--border-light);
  }
  .msg.ai {
    align-self: flex-start;
    border-left: 8px solid var(--primary);
  }
  .msg.user {
    align-self: flex-end;
    border-right: 8px solid var(--text);
  }
  .msg .sender {
    font-size: 13px; font-weight: 800; margin-bottom: 12px;
    text-transform: uppercase; letter-spacing: 1px;
    border-bottom: 2px solid var(--border-light); padding-bottom: 6px; display: inline-block;
  }
  .msg.ai .sender { color: var(--primary); border-bottom-color: var(--primary); }
  .convo-action {
    margin: 16px 0;
    padding: 20px;
    background: var(--surface-3);
    border: 2px solid var(--border);
    font-size: 14px;
    color: var(--text);
    text-align: center;
    font-weight: 800;
    text-transform: uppercase;
    box-shadow: 4px 4px 0px var(--border-light);
  }
  .convo-action strong { color: var(--primary); }
  .convo-action.warning { background: var(--warning-bg); border-color: var(--warning); color: var(--warning); }
  .convo-action.danger { background: var(--danger-bg); border-color: var(--danger); color: var(--danger); }
  .convo-action.success { background: var(--success-bg); border-color: var(--success); color: var(--success); }

  /* ── Sheet Diagram ── */
  .sheet-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 40px;
  }
  .sheet-card {
    background: var(--bg);
    border: 2px solid var(--border);
    padding: 40px;
    box-shadow: 8px 8px 0px var(--border);
  }
  .sheet-card h4 {
    font-size: 20px; font-weight: 800; margin-bottom: 16px;
    display: flex; align-items: center; gap: 12px; text-transform: uppercase;
  }
  .sheet-card .tab-name {
    font-size: 14px; font-weight: 800; border-bottom: 2px solid var(--border); padding-bottom: 16px; margin-bottom: 24px;
    display: inline-block; background: var(--info-bg); color: var(--info); border-color: var(--info); padding: 8px 16px;
  }
  .sheet-cols {
    display: flex; flex-direction: column; gap: 16px;
  }
  .sheet-col {
    display: flex; align-items: center; gap: 20px;
    font-size: 15px; color: var(--text-dim); font-weight: 600;
  }
  .sheet-col .col-name {
    font-size: 13px; font-weight: 800; color: var(--info);
    background: var(--info-bg); border: 2px solid var(--info);
    padding: 6px 12px; flex-shrink: 0; min-width: 160px; text-align: right;
  }

  /* ── Email Samples ── */
  .email-preview {
    background: var(--bg);
    border: 4px solid var(--border);
    margin-bottom: 40px;
    box-shadow: 12px 12px 0px var(--border);
  }
  .email-header {
    padding: 24px 32px;
    background: var(--surface-2);
    border-bottom: 4px solid var(--border);
  }
  .email-subject {
    font-size: 20px; font-weight: 800; margin-bottom: 12px; text-transform: uppercase;
  }
  .email-meta { font-size: 15px; color: var(--text-dim); font-weight: 700; }
  .email-body {
    padding: 40px 32px; font-size: 16px; color: var(--text); line-height: 1.8; font-weight: 500;
  }

  /* ── Rules ── */
  .rule-card {
    display: flex; align-items: flex-start; gap: 32px;
    padding: 40px;
    background: var(--bg);
    border: 2px solid var(--border);
    margin-bottom: 32px;
    box-shadow: 8px 8px 0px var(--border);
  }
  .rule-icon {
    width: 80px; height: 80px; border: 4px solid var(--border); background: var(--text); color: var(--bg);
    display: flex; align-items: center; justify-content: center;
    font-size: 32px; flex-shrink: 0;
  }
  .rule-icon.danger { background: var(--danger-bg); color: var(--danger); border-color: var(--danger); }
  .rule-icon.warning { background: var(--warning-bg); color: var(--warning); border-color: var(--warning); }
  
  .rule-content h4 { font-size: 22px; font-weight: 800; margin-bottom: 12px; text-transform: uppercase; }
  .rule-content p { font-size: 16px; color: var(--text-dim); line-height: 1.6; font-weight: 600; }
  .rule-threshold {
    display: inline-flex; padding: 8px 20px; border: 2px solid var(--border);
    font-size: 14px; font-weight: 800; margin-top: 20px;
    background: var(--surface-2); color: var(--text); text-transform: uppercase;
    box-shadow: 4px 4px 0px var(--border);
  }
  .rule-threshold.danger { background: var(--danger-bg); color: var(--danger); border-color: var(--danger); box-shadow: 4px 4px 0px var(--danger); }
  .rule-threshold.warning { background: var(--warning-bg); color: var(--warning); border-color: var(--warning); box-shadow: 4px 4px 0px var(--warning); }

  /* ── Footer ── */
  footer {
    padding: 100px 24px;
    text-align: center;
    border-top: 4px solid var(--border);
    background: var(--text);
    color: var(--bg);
    font-weight: 800;
    font-size: 15px;
  }
  footer p { margin-bottom: 16px; text-transform: uppercase; }

  /* ── OVERRIDES for technical colored theme ── */
  [style*="color: var(--text) !important"] { color: inherit !important; }
  [style*="background: var(--bg) !important"] { background: inherit !important; border-color: inherit !important; }
  .convo-action[style] { background: inherit !important; color: inherit !important; border-color: inherit !important; }
  .branch-label[style] { background: inherit !important; color: inherit !important; }
  .flow-node[style] { background: inherit !important; color: inherit !important; border-color: inherit !important; }
  
  /* ── Responsive ── */
  @media (max-width: 768px) {
    .hero h1 { font-size: 40px; }
    .hero { padding: 80px 20px 60px; }
    section { padding: 60px 0; }
    .section-title { font-size: 32px; }
    .flow-row { flex-direction: column; align-items: stretch; }
    .flow-node { max-width: 100%; }
    .flow-arrow { transform: rotate(90deg); text-align: center; padding: 16px 0; }
    .wf-grid { grid-template-columns: 1fr; }
    .timeline-dot { width: 48px; height: 48px; left: -56px; font-size: 18px; }
    .timeline { padding-left: 32px; }
    .timeline::before { left: 15px; }
    .sheet-col { flex-direction: column; align-items: flex-start; gap: 8px; }
    .sheet-col .col-name { text-align: left; }
    .rule-card { flex-direction: column; gap: 16px; }
  }
</style>"""

# Replace CSS block
content = re.sub(r'<style>.*?</style>', new_css, content, flags=re.DOTALL)

# Fix filter grayscale on body
content = content.replace('filter: grayscale(100%);', '')

# Replace old arrows with correct pointing arrows in master flow
# Horizontal arrows (Right)
content = content.replace('<div class="flow-arrow">&#10132;</div>', '<div class="flow-arrow">&rarr;</div>')
# Vertical arrows (Down)
content = content.replace('<div class="flow-arrow-down">&#11015;</div>', '<div class="flow-arrow-down">&darr;</div>')

# Fix branches to use new classes for colored borders/shadows
content = content.replace('<div class="flow-branch-item">', '<div class="flow-branch-item">')
content = content.replace('<div class="branch-label" style="background: var(--info-glow); color: var(--info);">New Customer</div>', '<div class="branch-label info">New Customer</div>')
content = content.replace('<div class="branch-label" style="background: var(--success-glow); color: var(--success);">Existing Customer</div>', '<div class="branch-label success">Existing Customer</div>')
content = content.replace('<div class="branch-label" style="background: var(--danger-glow); color: var(--danger);">Insurance Claim</div>', '<div class="branch-label danger">Insurance Claim</div>')

# Add specific classes to branch items to inherit color styles
content = content.replace('<div class="flow-branch-item">\n          <div class="branch-label info">', '<div class="flow-branch-item new-customer">\n          <div class="branch-label info">')
content = content.replace('<div class="flow-branch-item">\n          <div class="branch-label success">', '<div class="flow-branch-item existing-customer">\n          <div class="branch-label success">')
content = content.replace('<div class="flow-branch-item">\n          <div class="branch-label danger">', '<div class="flow-branch-item insurance-claim">\n          <div class="branch-label danger">')


# Fix Convo action colors
content = content.replace('<div class="convo-action">&#9881; AI classifies intent', '<div class="convo-action">⚙️ AI classifies intent')
content = content.replace('<div class="convo-action">&#128190; <code>save_field</code>', '<div class="convo-action success">💾 <code>save_field</code>')
content = content.replace('<div class="convo-action">&#9989; <code>check_disqualifier</code>', '<div class="convo-action success">✅ <code>check_disqualifier</code>')
content = content.replace('<div class="convo-action" style="background: var(--accent-glow);  color: var(--accent);">&#128293; <code>check_hot_lead</code>', '<div class="convo-action warning">🔥 <code>check_hot_lead</code>')
content = content.replace('<div class="convo-action" style="background: var(--danger-glow);  color: var(--danger);">&#128222; WF-03: Warm transfer', '<div class="convo-action danger">📞 WF-03: Warm transfer')

# Fix Rule icons and thresholds colors
content = content.replace('<div class="rule-icon" style="background: var(--danger-glow);">', '<div class="rule-icon danger">')
content = content.replace('<div class="rule-icon" style="background: var(--accent-glow);">', '<div class="rule-icon warning">')
content = content.replace('<div class="rule-threshold" style="background: var(--danger-glow); color: var(--danger);">', '<div class="rule-threshold danger">')
content = content.replace('<div class="rule-threshold" style="background: var(--accent-glow); color: var(--accent);">', '<div class="rule-threshold warning">')

# Restore other specific node colors that were inline
content = content.replace('<div class="flow-node" style="background: var(--accent-glow);  color: var(--accent); font-size:12px;">', '<div class="flow-node crm" style="font-size:12px;">')
content = content.replace('<div class="flow-node" style="background: var(--surface-3); border: 1px solid var(--border); color: var(--text-dim); font-size: 13px;">', '<div class="flow-node" style="font-size: 13px;">')
content = content.replace('<div class="flow-node" style="background: var(--cyan-glow);  color: var(--cyan); font-size:13px;">', '<div class="flow-node sheets" style="font-size:13px;">')


with open('ai-receptionist-docs.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated ai-receptionist-docs.html successfully")
