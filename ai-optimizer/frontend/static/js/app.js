// ─── UTILITIES ───────────────────────────────────────────────

function setStep(id, state) {
  const el = document.getElementById(id);
  el.className = 'step-item ' + state;
  const icon = el.querySelector('.step-icon');
  if (state === 'active') icon.innerHTML = '<div class="spinner" style="width:14px;height:14px;margin:0"></div>';
  else if (state === 'done') icon.innerHTML = '✓';
  else if (state === 'error') icon.innerHTML = '✗';
}

function showError(msg) {
  const box = document.getElementById('errorBox');
  box.textContent = '⚠ ' + msg;
  box.classList.add('active');
}

function scoreColor(s) {
  if (s >= 70) return 'var(--success)';
  if (s >= 40) return 'var(--warning)';
  return 'var(--danger)';
}

function scoreBadgeClass(s) {
  if (s >= 70) return 'score-good';
  if (s >= 40) return 'score-mid';
  return 'score-bad';
}

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

// ─── RENDER FUNCTIONS ────────────────────────────────────────

function renderScore(overall, shopName) {
  const color = scoreColor(overall);
  const label = overall >= 70 ? 'Good AI Readiness' : overall >= 40 ? 'Needs Improvement' : 'Poor AI Readiness';
  const r = 54, circ = 2 * Math.PI * r;
  const filled = (overall / 100) * circ;
  document.getElementById('scoreCard').innerHTML = `
    <div class="score-circle">
      <svg width="120" height="120" viewBox="0 0 120 120">
        <circle cx="60" cy="60" r="${r}" fill="none" stroke="var(--border)" stroke-width="8"/>
        <circle cx="60" cy="60" r="${r}" fill="none" stroke="${color}" stroke-width="8"
          stroke-dasharray="${filled} ${circ}" stroke-linecap="round"/>
      </svg>
      <div class="score-number" style="color:${color}">${overall}</div>
      <div class="score-label">/ 100</div>
    </div>
    <div class="score-info">
      <h2>${label}</h2>
      <p>Your store <strong>${shopName}</strong> scored <strong>${overall}/100</strong> on AI representation readiness.
      ${overall < 50 ? 'AI shopping agents may skip or misrepresent your store. Immediate action recommended.' :
        overall < 70 ? 'Some gaps exist that could cause AI agents to under-represent your products.' :
        'Your store is well-optimized for AI discovery.'}</p>
      <div class="score-breakdown">
        <span class="score-pill" style="background:rgba(108,99,255,0.1);color:var(--accent);border:1px solid rgba(108,99,255,0.2)">${overall >= 70 ? '✓ AI-Ready' : '⚠ Action Needed'}</span>
        <span class="score-pill" style="background:rgba(247,151,30,0.1);color:var(--warning);border:1px solid rgba(247,151,30,0.2)">Score: ${overall}/100</span>
      </div>
    </div>
  `;
}

function renderMetrics(metrics) {
  document.getElementById('metricsGrid').innerHTML = `
    <div class="metric-card">
      <div class="metric-label">Total Products</div>
      <div class="metric-value" style="color:var(--accent)">${metrics.total_products}</div>
      <div class="metric-sub">scanned & analyzed</div>
    </div>
    <div class="metric-card">
      <div class="metric-label">Missing Descriptions</div>
      <div class="metric-value" style="color:${metrics.missing_descriptions > 0 ? 'var(--danger)' : 'var(--success)'}">${metrics.missing_descriptions}</div>
      <div class="metric-sub">products need richer copy</div>
    </div>
    <div class="metric-card">
      <div class="metric-label">No/Few Images</div>
      <div class="metric-value" style="color:${metrics.no_images > 0 ? 'var(--warning)' : 'var(--success)'}">${metrics.no_images}</div>
      <div class="metric-sub">products lack visuals</div>
    </div>
    <div class="metric-card">
      <div class="metric-label">Weak Tag Coverage</div>
      <div class="metric-value" style="color:${metrics.weak_tags > 0 ? 'var(--warning)' : 'var(--success)'}">${metrics.weak_tags}</div>
      <div class="metric-sub">products missing tags</div>
    </div>
  `;
}

function renderPerception(perception) {
  document.getElementById('perceptionContent').innerHTML = `
    <div class="compare-grid">
      <div class="perception-box">
        <h4>🤖 How AI Agents See You Now</h4>
        <p>${perception.current_perception}</p>
      </div>
      <div class="perception-box">
        <h4>🎯 How You Want to Be Seen</h4>
        <p>${perception.ideal_perception}</p>
      </div>
    </div>
    <div class="perception-box" style="margin-top:0">
      <h4>📋 AI Agent Summary (Simulated)</h4>
      <p>${perception.agent_summary}</p>
    </div>
  `;
}

function renderGaps(gaps) {
  document.getElementById('gapList').innerHTML = gaps.map(g => `
    <div class="gap-item">
      <div class="gap-header">
        <span class="gap-name">${g.name}</span>
        <span class="gap-score" style="color:${scoreColor(g.score)}">${g.score}/100</span>
      </div>
      <div class="gap-bar"><div class="gap-fill" style="width:${g.score}%;background:${scoreColor(g.score)}"></div></div>
      <div class="gap-desc">${g.desc}</div>
    </div>
  `).join('');
}

function renderProducts(products) {
  document.getElementById('productTable').innerHTML = `
    <thead>
      <tr>
        <th>Product</th><th>AI Score</th><th>Description</th><th>Images</th><th>Tags</th><th>Top Issue</th>
      </tr>
    </thead>
    <tbody>
      ${products.slice(0, 15).map(p => `
        <tr>
          <td>${p.title}</td>
          <td><span class="score-badge ${scoreBadgeClass(p.score)}">${p.score}</span></td>
          <td style="color:${p.desc_len > 200 ? 'var(--success)' : p.desc_len > 50 ? 'var(--warning)' : 'var(--danger)'}">${p.desc_len} chars</td>
          <td style="color:${p.images >= 3 ? 'var(--success)' : p.images >= 1 ? 'var(--warning)' : 'var(--danger)'}">${p.images} imgs</td>
          <td style="color:${p.tags >= 5 ? 'var(--success)' : p.tags >= 2 ? 'var(--warning)' : 'var(--danger)'}">${p.tags} tags</td>
          <td style="color:var(--muted);font-size:12px">${(p.issues && p.issues[0]) || '✓ Good'}</td>
        </tr>
      `).join('')}
    </tbody>
  `;
}

function renderActions(actions) {
  const colors = ['var(--danger)', 'var(--warning)', 'var(--accent)', 'var(--success)', 'var(--muted)', 'var(--muted)'];
  document.getElementById('actionList').innerHTML = actions.map((a, i) => `
    <div class="action-item">
      <div class="action-rank" style="background:rgba(108,99,255,0.1);color:${colors[Math.min(i, 5)]}">#${i + 1}</div>
      <div class="action-content">
        <div class="action-title">${a.title}</div>
        <div class="action-desc">${a.description}</div>
        <div class="action-meta">
          <span class="tag tag-impact-${a.impact === 'High' ? 'high' : a.impact === 'Medium' ? 'med' : 'low'}">Impact: ${a.impact}</span>
          <span class="tag tag-effort">Effort: ${a.effort}</span>
          <span class="tag" style="color:var(--muted);border-color:var(--border)">${a.category}</span>
        </div>
      </div>
    </div>
  `).join('');
}

// ─── MAIN FLOW ───────────────────────────────────────────────

async function startAnalysis() {
  document.getElementById('errorBox').classList.remove('active');
  document.getElementById('analyzeBtn').disabled = true;
  document.getElementById('analyzeBtn').innerHTML = '<div class="spinner"></div> Analyzing...';
  document.getElementById('progressSection').classList.add('active');
  document.getElementById('resultsSection').classList.remove('active');

  // Animate steps
  const steps = ['step1', 'step2', 'step3', 'step4', 'step5'];
  steps.forEach(s => document.getElementById(s).className = 'step-item');

  try {
    // Animate progress steps while backend processes
    setStep('step1', 'active');
    await sleep(500);
    setStep('step1', 'done');
    setStep('step2', 'active');
    await sleep(400);
    setStep('step2', 'done');
    setStep('step3', 'active');
    await sleep(400);
    setStep('step3', 'done');
    setStep('step4', 'active');

    // Call backend
    const response = await fetch('/api/analyze/full', { method: 'POST' });
    if (!response.ok) {
      const err = await response.json();
      throw new Error(err.detail || 'Server error');
    }
    const data = await response.json();

    setStep('step4', 'done');
    setStep('step5', 'active');
    await sleep(300);
    setStep('step5', 'done');

    // Render results
    await sleep(300);
    document.getElementById('resultsSection').classList.add('active');

    const shopName = data.shop?.name || 'Your Store';
    renderScore(data.overall_score, shopName);
    renderMetrics(data.metrics);
    renderPerception(data.ai_perception);
    renderGaps(data.gaps);
    renderProducts(data.products);
    renderActions(data.actions);

    document.getElementById('resultsSection').scrollIntoView({ behavior: 'smooth', block: 'start' });

  } catch (err) {
    console.error(err);
    showError(err.message || 'Something went wrong. Check server logs.');
    steps.forEach(s => {
      if (document.getElementById(s).classList.contains('active')) setStep(s, 'error');
    });
  } finally {
    document.getElementById('analyzeBtn').disabled = false;
    document.getElementById('analyzeBtn').innerHTML = '🚀 Analyze AI Representation';
  }
}
