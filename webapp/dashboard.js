const CONFIG = {
    API_BASE_URL: 'https://api.cinetimetv.store' // Ensure this matches production
};

// Simple view switcher
function switchView(viewName) {
    // Update Sidebar
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
        if (item.innerText.toLowerCase().includes(viewName) ||
            (viewName === 'home' && item.innerText.includes('Overview'))) {
            item.classList.add('active');
        }
    });

    // For now, simpler content replacement (Mock)
    const container = document.getElementById('view-container');

    if (viewName === 'home') {
        container.innerHTML = `
      <div id="view-home">
        <div class="content-header">
          <h1>Dashboard Overview</h1>
        </div>
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
      </div>`;
        loadStats();
    } else if (viewName === 'accounts') {
        container.innerHTML = `
      <div id="view-accounts">
        <div class="content-header">
           <h1>Telegram Accounts</h1>
           <button class="btn-primary" style="width: auto;" onclick="window.location.href='index.html'">+ Add New</button>
        </div>
        <div class="card">
           <div id="accounts-list" style="padding: 1rem;">Loading accounts...</div>
        </div>
      </div>`;
        loadAccounts();
    } else if (viewName === 'admin') {
        container.innerHTML = `
      <div id="view-admin">
        <div class="content-header">
           <h1>👑 Owner Controls</h1>
        </div>

        <!-- Admin Stats -->
        <div class="stats-grid">
          <div class="stat-card" style="border-color: var(--accent-gradient);">
            <div class="stat-label">Total Users</div>
            <div class="stat-value" id="admin-total-users">Loading...</div>
          </div>
          <div class="stat-card">
            <div class="stat-label">Active Automations</div>
            <div class="stat-value" id="admin-active-automations">Loading...</div>
          </div>
        </div>

        <!-- Broadcast -->
        <div class="card">
           <h2>📢 Broadcast Message</h2>
           <p style="color: var(--text-secondary); margin-bottom: 1rem;">Send a message to all bot users.</p>
           
           <div class="form-group">
              <textarea id="broadcast-msg" placeholder="Type your announcement..." style="height: 100px;"></textarea>
           </div>
           
           <button class="btn-primary" onclick="sendBroadcast()" style="background: var(--accent-gradient);">Send to All Users</button>
        </div>
      </div>`;
        loadAdminStats();
    } else {
        container.innerHTML = `
      <div id="view-automations">
        <div class="content-header">
           <h1>Automation Settings</h1>
        </div>
        
        <div class="card" style="max-width: 800px;">
           <div class="form-group">
              <label>Source Content</label>
              <div style="padding: 1rem; background: rgba(102, 126, 234, 0.1); border-radius: 8px; border: 1px solid rgba(102, 126, 234, 0.2);">
                 <span style="font-size: 1.2rem;">📂 Saved Messages</span>
                 <p style="margin: 0.5rem 0 0; font-size: 0.9rem; color: var(--text-secondary);">
                    Messages will be fetched automatically from your Telegram "Saved Messages".
                    Latest 10 messages will be cycled.
                 </p>
              </div>
           </div>

           <div class="form-group">
              <label>Target Groups (One per line)</label>
              <textarea id="groups-input" placeholder="https://t.me/group1\nhttps://t.me/group2" style="height: 150px;"></textarea>
           </div>
           
           <div class="form-group">
              <label>Loop Interval (Minutes)</label>
              <input type="number" id="interval-input" value="60" min="20" style="width: 100px;">
              <span style="font-size: 0.8rem; color: var(--text-muted); margin-left: 10px;">Min: 20 mins</span>
           </div>

           <div class="button-group">
              <button class="btn-primary" onclick="startAutomation()">▶ Start Automation</button>
              <button class="btn-stop" onclick="stopAutomation()">■ Stop</button>
           </div>
        </div>
      </div>`;
    } else {
        container.innerHTML = `<h1>${viewName.charAt(0).toUpperCase() + viewName.slice(1)}</h1><p>Coming soon...</p>`;
    }
}

async function loadStats() {
    // Mock for now, replace with API call
    setTimeout(() => {
        const el = document.getElementById('stat-accounts');
        if (el) el.innerText = "1";
    }, 500);
}

async function loadAccounts() {
    // Mock list
    setTimeout(() => {
        const el = document.getElementById('accounts-list');
        if (el) el.innerHTML = `
        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.1); padding: 1rem 0;">
            <div>
                <div style="font-weight: bold;">+91 76782 61583</div>
                <div style="font-size: 0.8rem; color: #38ef7d;">● Active</div>
            </div>
            <button class="btn-secondary" style="padding: 0.5rem 1rem;">Manage</button>
        </div>`;
    }, 500);
}

async function startAutomation() {
    const groups = document.getElementById('groups-input').value.split('\n').filter(g => g.trim());
    const interval = parseInt(document.getElementById('interval-input').value);

    if (groups.length === 0) {
        alert("Please add at least one group link.");
        return;
    }
    if (interval < 20) {
        alert("Minimum interval is 20 minutes.");
        return;
    }

    // Mock Account ID 1 for now - in production get from selected account
    try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/api/campaigns/start`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                account_id: 1, // TODO: Dynamic selection
                interval_minutes: interval,
                night_mode_enabled: false,
                groups: groups,
                messages: [] // Ignored by backend now
            })
        });

        if (response.ok) {
            alert("Automation Started! Messages will be forwarded from Saved Messages.");
        } else {
            alert("Failed to start.");
        }
    } catch (e) {
        console.error(e);
        alert("Error starting automation.");
    }
}

function stopAutomation() {
    alert("Stop feature pending backend user mapping (Phase 4).");
}

async function loadAdminStats() {
    try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/api/admin/stats`);
        const data = await response.json();

        document.getElementById('admin-total-users').innerText = data.total_users;
        document.getElementById('admin-active-automations').innerText = data.active_automations;
    } catch (e) {
        console.error("Admin stats error", e);
    }
}

async function sendBroadcast() {
    const msg = document.getElementById('broadcast-msg').value;
    if (!msg) return alert("Please enter a message");

    if (!confirm("Are you sure you want to send this to ALL users?")) return;

    try {
        await fetch(`${CONFIG.API_BASE_URL}/api/admin/broadcast`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: msg })
        });
        alert("Broadcast queued!");
        document.getElementById('broadcast-msg').value = "";
    } catch (e) {
        alert("Broadcast failed");
    }
}


// Init
document.addEventListener('DOMContentLoaded', () => {
    switchView('home');
});
