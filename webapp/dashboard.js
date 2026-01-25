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

function logout() {
    localStorage.clear();
    window.location.href = 'index.html';
}

// Init
document.addEventListener('DOMContentLoaded', () => {
    switchView('home');
});
