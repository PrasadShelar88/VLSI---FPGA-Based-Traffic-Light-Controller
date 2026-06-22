const $ = (id) => document.getElementById(id);
const urlInput = $('backendUrl');
const statusEl = $('connectionStatus');
const bodyEl = $('recordsBody');
const codeBox = $('codeBox');
const codeTitle = $('codeTitle');

urlInput.value = localStorage.getItem('trafficBackendUrl') || 'http://127.0.0.1:8000';

function backendUrl() {
  return urlInput.value.replace(/\/$/, '');
}

function setStatus(text, cls = 'muted') {
  statusEl.textContent = text;
  statusEl.className = `status ${cls}`;
}

async function api(path, options = {}) {
  const res = await fetch(`${backendUrl()}${path}`, options);
  if (!res.ok) {
    let msg = await res.text();
    throw new Error(msg || `HTTP ${res.status}`);
  }
  const type = res.headers.get('content-type') || '';
  return type.includes('application/json') ? res.json() : res.text();
}

function getPayload() {
  return {
    cycles: Number($('cycles').value),
    ns_sensor: $('nsSensor').checked,
    ew_sensor: $('ewSensor').checked,
    pedestrian_request: $('pedRequest').checked,
    emergency: $('emergency').checked,
    night_mode: $('nightMode').checked,
    green_time: Number($('greenTime').value),
    yellow_time: Number($('yellowTime').value),
    all_red_time: Number($('allRedTime').value),
    walk_time: Number($('walkTime').value),
    start_state: $('startState').value
  };
}

function clearLights(id) {
  document.querySelectorAll(`#${id} .lamp`).forEach(l => {
    l.classList.remove('active', 'blink');
  });
}

function setLight(id, value) {
  clearLights(id);
  const upper = String(value || '').toUpperCase();
  if (upper.includes('RED')) {
    const lamp = document.querySelector(`#${id} .red`);
    lamp.classList.add('active');
    if (upper.includes('BLINK')) lamp.classList.add('blink');
  }
  if (upper.includes('YELLOW')) {
    const lamp = document.querySelector(`#${id} .yellow`);
    lamp.classList.add('active');
    if (upper.includes('BLINK')) lamp.classList.add('blink');
  }
  if (upper.includes('GREEN')) {
    document.querySelector(`#${id} .green`).classList.add('active');
  }
}

function updateDashboard(record, result = null) {
  if (!record) return;
  $('currentState').textContent = record.state;
  $('stateNote').textContent = record.note || 'OK';
  $('nsOutput').textContent = record.ns;
  $('ewOutput').textContent = record.ew;
  $('pedOutput').textContent = record.pedestrian;
  $('pedIcon').textContent = record.pedestrian === 'WALK' ? '🚶' : '✋';
  setLight('nsLight', record.ns);
  setLight('ewLight', record.ew);
  const pass = record.safe === true;
  $('safetyBadge').textContent = `Safety: ${pass ? 'PASS' : 'FAIL'}`;
  $('safetyBadge').className = `badge ${pass ? 'pass' : 'fail'}`;
  if (result) {
    $('metricCycles').textContent = result.total_cycles;
    $('metricFinal').textContent = result.final_state;
    $('metricSafety').textContent = result.safety_check;
  }
}

function renderRecords(records = []) {
  if (!records.length) {
    bodyEl.innerHTML = '<tr><td colspan="7" class="empty">No records found.</td></tr>';
    return;
  }
  bodyEl.innerHTML = records.slice(-80).reverse().map(r => `
    <tr>
      <td>${r.cycle}</td>
      <td><strong>${r.state}</strong></td>
      <td>${r.ns}</td>
      <td>${r.ew}</td>
      <td>${r.pedestrian}</td>
      <td>${r.safe ? 'PASS' : 'FAIL'}</td>
      <td>${r.note || ''}</td>
    </tr>
  `).join('');
}

async function testConnection() {
  try {
    const data = await api('/health');
    setStatus(`Backend connected: ${data.message}`, 'ok');
  } catch (err) {
    setStatus(`Backend connection error: ${err.message}. Make sure FastAPI is running on ${backendUrl()}`, 'err');
  }
}

async function simulate() {
  try {
    setStatus('Running FSM simulation...', 'muted');
    const result = await api('/simulate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(getPayload())
    });
    renderRecords(result.records);
    updateDashboard(result.records[result.records.length - 1], result);
    setStatus(`Simulation completed. Safety check: ${result.safety_check}`, result.safety_check === 'PASS' ? 'ok' : 'err');
  } catch (err) {
    setStatus(`Simulation error: ${err.message}`, 'err');
  }
}

async function loadLogs() {
  try {
    const data = await api('/logs');
    renderRecords(data.records || []);
    updateDashboard((data.records || []).slice(-1)[0]);
    setStatus(`Loaded ${data.count} backend log records.`, 'ok');
  } catch (err) {
    setStatus(`Log error: ${err.message}`, 'err');
  }
}

async function clearLogs() {
  try {
    await api('/logs/clear', { method: 'DELETE' });
    renderRecords([]);
    setStatus('Logs cleared.', 'ok');
  } catch (err) {
    setStatus(`Clear error: ${err.message}`, 'err');
  }
}

function download(path) {
  window.open(`${backendUrl()}${path}`, '_blank');
}

async function loadSource(path, title) {
  try {
    const text = await api(path);
    codeTitle.textContent = title;
    codeBox.textContent = text;
  } catch (err) {
    codeBox.textContent = `Error loading source: ${err.message}`;
  }
}

function setScenario(mode) {
  $('nsSensor').checked = false;
  $('ewSensor').checked = true;
  $('pedRequest').checked = false;
  $('emergency').checked = false;
  $('nightMode').checked = false;
  $('startState').value = 'NS_GREEN';
  if (mode === 'ped') $('pedRequest').checked = true;
  if (mode === 'emergency') $('emergency').checked = true;
  if (mode === 'night') $('nightMode').checked = true;
}

$('saveUrlBtn').addEventListener('click', () => {
  localStorage.setItem('trafficBackendUrl', backendUrl());
  setStatus(`Saved backend URL: ${backendUrl()}`, 'ok');
});
$('testBtn').addEventListener('click', testConnection);
$('simulateBtn').addEventListener('click', simulate);
$('logsBtn').addEventListener('click', loadLogs);
$('clearBtn').addEventListener('click', clearLogs);
$('csvBtn').addEventListener('click', () => download('/download/csv'));
$('pdfBtn').addEventListener('click', () => download('/download/pdf'));
$('rtlBtn').addEventListener('click', () => loadSource('/source/rtl', 'RTL Verilog Source'));
$('tbBtn').addEventListener('click', () => loadSource('/source/testbench', 'Verilog Testbench Source'));
$('copyCodeBtn').addEventListener('click', async () => {
  await navigator.clipboard.writeText(codeBox.textContent);
  setStatus('Code copied to clipboard.', 'ok');
});

document.querySelectorAll('.scenario').forEach(btn => {
  btn.addEventListener('click', () => setScenario(btn.dataset.mode));
});

renderRecords([]);
