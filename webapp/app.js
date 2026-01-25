const CONFIG = {
  // API_BASE_URL: 'http://localhost:8000' // DEV
  API_BASE_URL: 'https://api.cinetimetv.store' // PROD
};

const state = {
  phone: '',
  phone_code_hash: '',
  api_id: null,
  api_hash: null,
  user: null
};

// =========================================
// INIT & ROUTING
// =========================================
document.addEventListener('DOMContentLoaded', () => {
  initOTPHandlers(); // Setup the OTP box logic

  // Check Session
  const savedPhone = localStorage.getItem('user_phone');
  if (savedPhone) {
    state.phone = savedPhone;
    state.api_id = localStorage.getItem('api_id');
    state.api_hash = localStorage.getItem('api_hash');
    showDashboard();
  } else {
    showAuth();
  }
});

function showAuth() {
  document.getElementById('auth-view').classList.remove('hidden');
  document.getElementById('dashboard-view').classList.remove('active');
}

function showDashboard() {
  document.getElementById('auth-view').classList.add('hidden');
  document.getElementById('dashboard-view').classList.add('active');
  router('overview'); // Load default view
}

// =========================================
// AUTH LOGIC
// =========================================
async function handleSendOTP() {
  const phone = document.getElementById('phone_number').value;
  const api_id = document.getElementById('api_id').value;
  const api_hash = document.getElementById('api_hash').value;

  if (!phone) return showToast("Phone number required");

  setLoading('btn-send-otp', true, "Sending...");

  try {
    const res = await apiCall('/auth/send-otp', 'POST', {
      phone,
      api_id: parseInt(api_id) || 0,
      api_hash: api_hash || ""
    });

    // Store temp state
    state.phone = phone;
    state.phone_code_hash = res.phone_code_hash;
    state.api_id = parseInt(api_id);
    state.api_hash = api_hash;

    // Switch to OTP Step
    switchAuthStep('step-otp');
    showToast("Code sent to Telegram App 📲");

  } catch (e) {
    showToast(e.message || "Failed to send OTP");
  } finally {
    setLoading('btn-send-otp', false, "Send Access Code");
  }
}

async function handleVerifyOTP() {
  // Collect OTP from boxes
  let otpCode = '';
  for (let i = 1; i <= 6; i++) {
    otpCode += document.getElementById(`otp-${i}`).value;
  }

  if (otpCode.length < 5) return showToast("Please enter full code");

  setLoading('btn-verify-otp', true, "Verifying...");

  try {
    const res = await apiCall('/auth/verify-otp', 'POST', {
      phone: state.phone,
      otp: otpCode,
      phone_code_hash: state.phone_code_hash,
      api_id: state.api_id || 0,
      api_hash: state.api_hash || ""
    });

    completeLogin();

  } catch (e) {
    // Handle 2FA
    if (e.status === 401 && e.message.includes('2FA')) {
      showToast("2FA Required 🔒");
      switchAuthStep('step-2fa');
      return;
    }
    showToast(e.message || "Invalid Code");
  } finally {
    setLoading('btn-verify-otp', false, "Verify & Proceed");
  }
}

async function handleVerify2FA() {
  const password = document.getElementById('password-input').value;
  if (!password) return showToast("Password required");

  setLoading('btn-verify-2fa', true, "Unlocking...");

  try {
    await apiCall('/auth/2fa', 'POST', {
      phone: state.phone,
      password: password,
      phone_code_hash: state.phone_code_hash
    });

    completeLogin();

  } catch (e) {
    showToast("Incorrect Password");
  } finally {
    setLoading('btn-verify-2fa', false, "Unlock Account");
  }
}

function completeLogin() {
  // Save Session
  localStorage.setItem('user_phone', state.phone);
  if (state.api_id) localStorage.setItem('api_id', state.api_id);
  if (state.api_hash) localStorage.setItem('api_hash', state.api_hash);

  showToast("Login Success! Welcome ✨");
  setTimeout(showDashboard, 1000);
}

function resetToPhone() {
  switchAuthStep('step-phone');
  state.phone_code_hash = '';
}

function switchAuthStep(stepId) {
  document.querySelectorAll('.auth-step').forEach(el => el.classList.remove('active'));
  document.getElementById(stepId).classList.add('active');
}

// =========================================
// OTP BOX HANDLER (Segmented Inputs)
// =========================================
function initOTPHandlers() {
  const inputs = document.querySelectorAll('.otp-input');
  inputs.forEach((input, index) => {
    input.addEventListener('input', (e) => {
      // Only allow numbers
      e.target.value = e.target.value.replace(/[^0-9]/g, '');

      if (e.target.value.length === 1) {
        // Move to next
        if (index < inputs.length - 1) inputs[index + 1].focus();
      }
    });

    input.addEventListener('keydown', (e) => {
      if (e.key === 'Backspace' && !e.target.value) {
        // Move to previous
        if (index > 0) inputs[index - 1].focus();
      }
    });

    // Paste support
    input.addEventListener('paste', (e) => {
      e.preventDefault();
      const pasteData = e.clipboardData.getData('text').slice(0, 6);
      if (!/^\d+$/.test(pasteData)) return; // Only digits

      pasteData.split('').forEach((char, i) => {
        if (inputs[i]) inputs[i].value = char;
      });
      // Focus last filled
      if (inputs[pasteData.length - 1]) inputs[pasteData.length - 1].focus();
      if (pasteData.length < 6) inputs[pasteData.length].focus();
    });
  });
}

// =========================================
// DASHBOARD LOGIC (View Switcher)
// =========================================
async function router(view) {
  // Highlight sidebar
  document.querySelectorAll('.nav-item').forEach(el => {
    el.classList.remove('active');
    if (el.innerText.toLowerCase().includes(view)) el.classList.add('active');
  });

  const content = document.getElementById('main-content');
  content.innerHTML = '<div style="padding:2rem;"><h3>Loading...</h3></div>';

  try {
    if (view === 'overview') await renderOverview(content);
    else if (view === 'accounts') await renderAccounts(content);
    else if (view === 'automations') await renderAutomations(content);
    else if (view === 'admin') await renderAdmin(content);
  } catch (e) {
    content.innerHTML = `<div style="padding:2rem; color:var(--color-danger);">Error loading view: ${e.message}</div>`;
  }
}

// --- RENDERERS ---

async function renderOverview(container) {
  container.innerHTML = `
        <div style="padding: 2rem;">
            <h1 style="margin-bottom: 2rem;">Dashboard Overview</h1>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1.5rem;">
                <!-- Stat 1 -->
                <div class="glass-panel" style="padding: 1.5rem;">
                    <div style="color: var(--text-muted); font-size: 0.9rem;">Active Accounts</div>
                    <div style="font-size: 2.5rem; font-weight: bold; color: var(--color-primary);" id="stat-acc">...</div>
                </div>
                <!-- Stat 2 -->
                <div class="glass-panel" style="padding: 1.5rem;">
                    <div style="color: var(--text-muted); font-size: 0.9rem;">Campaigns Running</div>
                    <div style="font-size: 2.5rem; font-weight: bold; color: var(--color-accent);">0</div>
                </div>
            </div>
        </div>
    `;

  // Mock Data Fetch
  setTimeout(() => {
    if (document.getElementById('stat-acc')) document.getElementById('stat-acc').innerText = "1";
  }, 500);
}

async function renderAccounts(container) {
  container.innerHTML = `
        <div style="padding: 2rem;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:2rem;">
                <h1>Connected Accounts</h1>
                <button class="btn" style="width:auto;" onclick="handleLogout()">+ Add New</button>
            </div>
            <div class="glass-panel" id="acc-list" style="padding: 1rem;">
                Loading accounts...
            </div>
        </div>
    `;

  const data = await apiCall('/api/accounts', 'GET');
  const html = data.map(acc => `
        <div style="
            display:flex; justify-content:space-between; align-items:center; 
            padding: 1rem; border-bottom: 1px solid rgba(255,255,255,0.05);
        ">
            <div>
                <div style="font-weight:bold; font-size:1.1rem;">${acc.phone}</div>
                <div style="font-size:0.8rem; opacity:0.7;">API ID: ${acc.api_id}</div>
            </div>
            <div style="
                padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.8rem;
                background: ${acc.is_active ? 'rgba(0,255,100,0.1)' : 'rgba(255,50,50,0.1)'};
                color: ${acc.is_active ? '#00ff88' : '#ff4444'};
            ">
                ${acc.is_active ? '● Active' : '● Inactive'}
            </div>
        </div>
    `).join('');

  document.getElementById('acc-list').innerHTML = html || '<div style="padding:1rem;">No accounts found.</div>';
}

async function renderAutomations(container) {
  container.innerHTML = `
        <div style="padding: 2rem;">
            <h1>Automation Engine</h1>
            <div class="glass-panel" style="padding: 2rem; max-width: 600px; margin-top: 2rem;">
                <div class="input-group">
                    <label>Target Groups (one per line)</label>
                    <textarea id="auto-groups" rows="5" placeholder="https://t.me/marketing_group" 
                     style="width:100%; background:rgba(0,0,0,0.2); border:1px solid rgba(255,255,255,0.1); color:white; padding:1rem; border-radius:8px;"></textarea>
                </div>
                <div class="input-group">
                    <label>Interval (minutes)</label>
                    <input type="number" id="auto-interval" value="60" min="20">
                </div>
                <button class="btn" onclick="startCampaign()">🚀 Launch Campaign</button>
            </div>
        </div>
    `;
}

async function renderAdmin(container) {
  container.innerHTML = `
        <div style="padding: 2rem;">
            <h1>Admin Controls</h1>
            <p>Broadcast messages to all users.</p>
        </div>
    `;
}

// =========================================
// API & UTILS
// =========================================
async function apiCall(endpoint, method = 'GET', body = null) {
  const opts = {
    method,
    headers: {
      'Content-Type': 'application/json'
    }
  };
  if (body) opts.body = JSON.stringify(body);

  const res = await fetch(`${CONFIG.API_BASE_URL}${endpoint}`, opts);
  const data = await res.json();

  if (!res.ok) {
    // Pass complete error object including status for 2FA handling
    const err = new Error(data.detail || "Request failed");
    err.status = res.status;
    throw err;
  }
  return data;
}

function handleLogout() {
  localStorage.clear();
  location.reload();
}

function showToast(msg) {
  const t = document.getElementById('toast');
  t.innerText = msg;
  t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 3000);
}

function setLoading(btnId, isLoading, text) {
  const btn = document.getElementById(btnId);
  if (!btn) return;
  btn.disabled = isLoading;
  btn.innerText = text;
  btn.style.opacity = isLoading ? '0.7' : '1';
}

// Placeholder for Campaign Start
async function startCampaign() {
  const groups = document.getElementById('auto-groups').value;
  if (!groups) return showToast("Enter target groups");
  showToast("Campaign Started (Simulated)");
}