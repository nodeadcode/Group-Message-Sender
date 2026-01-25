const CONFIG = {
    API_BASE_URL: 'https://api.cinetimetv.store'
};

// Global 401 Handler
async function fetchWithAuth(url, options = {}) {
    try {
        const response = await fetch(url, options);
        if (response.status === 401) {
            logout();
            return null;
        }
        return response;
    } catch (e) {
        console.error("API Error:", e);
        return null;
    }
}

// =========================================
// ROUTING / VIEW SWITCHER
// =========================================
function switchView(viewName) {
    // 1. Update Sidebar
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
        if (item.innerText.toLowerCase().includes(viewName)) {
            item.classList.add('active');
        }
    });

    const container = document.getElementById('view-container');

    // 2. Render Content
    if (viewName === 'home') {
        renderHome(container);
    } else if (viewName === 'accounts') {
        renderAccounts(container);
    } else if (viewName === 'automations') {
        renderAutomations(container);
    } else if (viewName === 'admin') {
        renderAdmin(container);
    }
}

// =========================================
// RENDER FUNCTIONS
// =========================================
function renderHome(container) {
    container.innerHTML = `
        <div class="content-header"><h1>Overview</h1></div>
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-label">Active Accounts</div>
                <div class="stat-value" id="stat-accounts">Loading...</div>
            </div>
            <div class="stat-card">
                 <div class="stat-label">Messages Sent</div>
                 <div class="stat-value">0</div>
            </div>
        </div>
    `;
    // Mock Load
    setTimeout(() => {
        if (document.getElementById('stat-accounts'))
            document.getElementById('stat-accounts').innerText = "1";
    }, 500);
}

async function renderAccounts(container) {
    container.innerHTML = `
        <div class="content-header">
            <h1>Telegram Accounts</h1>
            <button class="btn-secondary" onclick="window.location.href='index.html'">+ Add New</button>
        </div>
        <div class="card">
            <div id="accounts-list">Loading...</div>
        </div>
    `;

    // Fetch
    const res = await fetchWithAuth(`${CONFIG.API_BASE_URL}/api/accounts`);
    if (res) {
        const accounts = await res.json();
        const html = accounts.map(acc => `
            <div style="display:flex; justify-content:space-between; padding:1rem; border-bottom:1px solid rgba(255,255,255,0.1);">
                <div>
                    <b>${acc.phone}</b>
                    <div style="font-size:0.8rem; color:${acc.is_active ? '#00ff88' : 'red'}">● ${acc.is_active ? 'Active' : 'Inactive'}</div>
                </div>
            </div>
        `).join('');
        document.getElementById('accounts-list').innerHTML = html || 'No accounts found.';
    }
}

function renderAutomations(container) {
    container.innerHTML = `
        <div class="content-header"><h1>Automation Engine</h1></div>
        <div class="card" style="max-width:600px;">
            <div class="form-group">
                <label>Source: Saved Messages</label>
                <div style="padding:1rem; background:rgba(255,255,255,0.05); border-radius:8px;">
                     Using "Saved Messages" of connected account.
                </div>
            </div>
            <div class="form-group">
                <label>Target Groups (One per line)</label>
                <textarea id="groups-input" rows="5" placeholder="https://t.me/group1..."></textarea>
            </div>
            <div class="form-group">
                 <label>Loop Interval (Mins) - Min 20</label>
                 <input type="number" id="interval-input" value="60" min="20">
            </div>
            <div class="button-group">
                <button class="btn-primary" onclick="startCampaign()">Start Campaign</button>
                <button class="btn-stop" onclick="alert('Stop pending Phase 4 map')">Stop</button>
            </div>
        </div>
    `;
}

async function renderAdmin(container) {
    container.innerHTML = `
        <div class="content-header"><h1>Owner Controls</h1></div>
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-label">Total Users</div>
                <div class="stat-value" id="admin-users">...</div>
            </div>
            <div class="stat-card">
                 <div class="stat-label">Automations</div>
                 <div class="stat-value" id="admin-auto">...</div>
            </div>
        </div>
        <div class="card">
            <h2>Broadcast</h2>
            <textarea id="broadcast-msg" rows="3" placeholder="Message to all users..."></textarea>
            <button class="btn-primary" style="margin-top:1rem;" onclick="sendBroadcast()">Send</button>
        </div>
    `;

    const res = await fetchWithAuth(`${CONFIG.API_BASE_URL}/api/admin/stats`);
    if (res) {
        const data = await res.json();
        document.getElementById('admin-users').innerText = data.total_users;
        document.getElementById('admin-auto').innerText = data.active_automations;
    }
}

// =========================================
// ACTIONS
// =========================================
async function startCampaign() {
    const groups = document.getElementById('groups-input').value.split('\n').filter(g => g.trim());
    const interval = parseInt(document.getElementById('interval-input').value);

    if (interval < 20) return alert("Min interval is 20 mins");
    if (groups.length === 0) return alert("Add groups");

    const res = await fetchWithAuth(`${CONFIG.API_BASE_URL}/api/campaigns/start`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            account_id: 1, // Mock
            interval_minutes: interval,
            groups: groups
        })
    });

    if (res && res.ok) alert("Campaign Started!");
    else alert("Failed to start");
}

async function sendBroadcast() {
    const msg = document.getElementById('broadcast-msg').value;
    if (!msg) return;

    await fetchWithAuth(`${CONFIG.API_BASE_URL}/api/admin/broadcast`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: msg })
    });
    alert("Broadcast sent");
}

function logout() {
    localStorage.clear();
    window.location.href = 'index.html';
}

// Init
document.addEventListener('DOMContentLoaded', () => {
    switchView('home');
});
