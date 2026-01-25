const CONFIG = {
  API_BASE_URL: 'https://api.cinetimetv.store'
};

const state = {
  phone: '',
  phone_code_hash: '',
  session_string: ''
};

// =========================================
// INIT
// =========================================
document.addEventListener('DOMContentLoaded', () => {
  // 1. Auto-Redirect Check
  if (localStorage.getItem('user_phone')) {
    console.log("Session found, redirecting...");
    window.location.href = 'dashboard.html';
    return;
  }
  console.log("App initialized");
});

// =========================================
// AUTH FUNCTIONS
// =========================================
async function sendOTP() {
  const phone = document.getElementById('phone').value;
  if (!phone) return showToast("Please enter phone number");

  const btn = document.getElementById('login-btn');
  btn.innerText = "Sending...";
  btn.disabled = true;

  try {
    const res = await fetch(`${CONFIG.API_BASE_URL}/auth/send-otp`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ phone })
    });

    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Failed to send OTP");

    state.phone = phone;
    state.phone_code_hash = data.phone_code_hash;

    // UI Update
    document.getElementById('otp-group').style.display = 'block';
    btn.innerText = "Verify OTP";
    btn.onclick = verifyOTP;
    btn.disabled = false;
    showToast("OTP Sent! Check Telegram.");

  } catch (e) {
    showToast(e.message);
    btn.innerText = "Send OTP";
    btn.disabled = false;
  }
}

async function verifyOTP() {
  const otp = document.getElementById('otp-input').value;
  if (!otp) return showToast("Enter OTP");

  const btn = document.getElementById('login-btn');
  btn.innerText = "Verifying...";
  btn.disabled = true;

  try {
    const res = await fetch(`${CONFIG.API_BASE_URL}/auth/verify-otp`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        phone: state.phone,
        otp: otp,
        phone_code_hash: state.phone_code_hash,
        api_id: 0, // Backend handles fallback/creation
        api_hash: ""
      })
    });

    const data = await res.json();

    // Handle 2FA
    if (res.status === 401 && data.detail?.includes('2FA')) {
      document.getElementById('otp-group').style.display = 'none';
      document.getElementById('password-group').style.display = 'block';
      btn.innerText = "Verify Password";
      btn.onclick = verifyPassword;
      btn.disabled = false;
      return showToast("Two-Step Verification Required");
    }

    if (!res.ok) throw new Error(data.detail || "Verification Failed");

    // Success
    localStorage.setItem('user_phone', state.phone);
    showToast("Login Successful! Redirecting...");

    setTimeout(() => {
      window.location.href = 'dashboard.html';
    }, 1000);

  } catch (e) {
    showToast(e.message);
    btn.innerText = "Verify OTP";
    btn.disabled = false;
  }
}

async function verifyPassword() {
  const password = document.getElementById('password').value;
  const btn = document.getElementById('login-btn');
  btn.innerText = "Checking...";
  btn.disabled = true;

  try {
    const res = await fetch(`${CONFIG.API_BASE_URL}/auth/2fa`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        phone: state.phone,
        password: password,
        phone_code_hash: state.phone_code_hash
      })
    });

    if (!res.ok) throw new Error("Invalid Password");

    localStorage.setItem('user_phone', state.phone);
    showToast("Login Successful!");
    window.location.href = 'dashboard.html';

  } catch (e) {
    showToast(e.message);
    btn.innerText = "Verify Password";
    btn.disabled = false;
  }
}

// =========================================
// UTILS
// =========================================
function showToast(msg) {
  const t = document.getElementById('toast');
  t.innerText = msg;
  t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 3000);
}
