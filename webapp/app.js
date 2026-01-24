// ========================================
// TELEGRAM WEB APP INITIALIZATION
// ========================================
const tg = window.Telegram?.WebApp;
if (tg) {
  tg.expand();
  tg.ready();
}

// ========================================
// CONFIGURATION
// ========================================
const CONFIG = {
  // API Base URL - Must use HTTPS to avoid "Failed to fetch" errors
  // If hosted on the same domain, use '/api' (requires Nginx proxy)
  // Or use full URL: 'https://cinetimetv.store/api'
  API_BASE_URL: 'https://cinetimetv.store/api',
  MAX_GROUPS: 10,  // Updated from 5 to 10
  MIN_INTERVAL_MINUTES: 20,
  GROUP_DELAY_SECONDS: 60,
  MESSAGE_DELAY_SECONDS: 60,
  OTP_LENGTH: 6,
  TOAST_DURATION: 3000,
  OWNER_USERNAME: '@spinify'
};

// ========================================
// STATE MANAGEMENT
// ========================================
const state = {
  currentStep: 1,
  credentials: {
    apiId: null,
    apiHash: null
  },
  auth: {
    phone: null,
    otp: null,
    isAuthenticated: false
  },
  access: {
    hasAccess: false,
    accessRequested: false,
    userId: null
  },
  campaign: {
    intervalMinutes: 60,  // Default 1 hour
    nightModeEnabled: false
  },
  groups: [],
  messages: [],
  schedulerRunning: false
};

// ========================================
// UTILITY FUNCTIONS
// ========================================

/**
 * Show toast notification
 */
function showToast(message, type = 'info') {
  const toast = document.getElementById('toast');
  toast.textContent = message;
  toast.className = `toast show ${type}`;

  setTimeout(() => {
    toast.classList.remove('show');
  }, CONFIG.TOAST_DURATION);
}

/**
 * Clear error message for a field
 */
function clearError(fieldId) {
  const errorElement = document.getElementById(`${fieldId}_error`);
  if (errorElement) {
    errorElement.textContent = '';
  }
}

/**
 * Show error message for a field
 */
function showError(fieldId, message) {
  const errorElement = document.getElementById(`${fieldId}_error`);
  if (errorElement) {
    errorElement.textContent = message;
  }
}

/**
 * Validate email format
 */
function isValidPhone(phone) {
  // Basic phone validation - starts with + and has 10-15 digits
  return /^\+\d{10,15}$/.test(phone);
}

/**
 * Update progress bar
 */
function updateProgress(step) {
  const progress = (step / 5) * 100;
  const progressFill = document.getElementById('progress-fill');
  const stepIndicator = document.getElementById('step-indicator');

  if (progressFill) {
    progressFill.style.width = `${progress}%`;
  }

  if (stepIndicator) {
    stepIndicator.textContent = `Step ${step} of 5`;
  }
}

/**
 * Set loading state for button
 */
function setButtonLoading(button, isLoading) {
  if (isLoading) {
    button.classList.add('loading');
    button.disabled = true;
  } else {
    button.classList.remove('loading');
    button.disabled = false;
  }
}

// ========================================
// STEP NAVIGATION
// ========================================

/**
 * Navigate to a specific step
 */
function goToStep(stepNumber) {
  // Hide all steps
  document.querySelectorAll('.step').forEach(step => {
    step.classList.remove('active');
  });

  // Show target step
  const targetStep = document.getElementById(`step-${stepNumber}`);
  if (targetStep) {
    targetStep.classList.add('active');
    state.currentStep = stepNumber;
    updateProgress(stepNumber);

    // Scroll to top smoothly
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }
}

// ========================================
// VALIDATION FUNCTIONS
// ========================================

/**
 * Validate and navigate to next step
 */
function validateAndGoToStep(nextStep) {
  const currentStep = state.currentStep;

  // Clear all errors
  clearError('api_id');
  clearError('api_hash');

  if (currentStep === 1) {
    // Validate API credentials
    const apiId = document.getElementById('api_id').value.trim();
    const apiHash = document.getElementById('api_hash').value.trim();

    let isValid = true;

    if (!apiId) {
      showError('api_id', 'API ID is required');
      isValid = false;
    } else if (!/^\d+$/.test(apiId)) {
      showError('api_id', 'API ID must be numeric');
      isValid = false;
    }

    if (!apiHash) {
      showError('api_hash', 'API Hash is required');
      isValid = false;
    } else if (apiHash.length < 10) {
      showError('api_hash', 'API Hash seems too short');
      isValid = false;
    }

    if (isValid) {
      state.credentials.apiId = apiId;
      state.credentials.apiHash = apiHash;
      showToast('✓ Credentials saved!', 'success');
      goToStep(nextStep);
    }
  }
}

/**
 * Validate groups input
 */
function validateGroups() {
  clearError('groups');

  const groupsText = document.getElementById('groups').value.trim();

  if (!groupsText) {
    showError('groups', 'Please enter at least one group link');
    return;
  }

  const groupLinks = groupsText.split('\n')
    .map(link => link.trim())
    .filter(link => link.length > 0);

  if (groupLinks.length === 0) {
    showError('groups', 'Please enter at least one group link');
    return;
  }

  if (groupLinks.length > CONFIG.MAX_GROUPS) {
    showError('groups', `Maximum ${CONFIG.MAX_GROUPS} groups allowed`);
    return;
  }

  // Basic validation - check if links contain t.me
  const invalidLinks = groupLinks.filter(link => !link.includes('t.me'));
  if (invalidLinks.length > 0) {
    showError('groups', 'All links must be valid Telegram group links (containing t.me)');
    return;
  }

  // TODO: Call backend API to verify groups
  state.groups = groupLinks;
  showToast(`✓ ${groupLinks.length} group(s) added!`, 'success');
  goToStep(4);
}

/**
 * Validate messages before proceeding
 */
function validateMessages() {
  if (state.messages.length === 0) {
    showToast('Please add at least one message', 'error');
    return;
  }

  showToast('✓ Messages ready!', 'success');
  goToStep(5);
}

// ========================================
// AUTHENTICATION
// ========================================

/**
 * Send OTP to phone number
 */
async function sendOTP() {
  clearError('phone');

  const phone = document.getElementById('phone').value.trim();

  if (!phone) {
    showError('phone', 'Phone number is required');
    return;
  }

  if (!isValidPhone(phone)) {
    showError('phone', 'Please enter a valid phone number with country code (e.g., +1234567890)');
    return;
  }

  const button = document.getElementById('verify-btn');
  setButtonLoading(button, true);

  try {
    // Real API call to send OTP
    const response = await fetch(`${CONFIG.API_BASE_URL}/auth/send-otp`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        phone: phone,
        api_id: parseInt(state.credentials.apiId),
        api_hash: state.credentials.apiHash,
        nickname: phone.replace('+', '') // Use phone as default nickname
      })
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to send OTP');
    }

    const data = await response.json();

    // Store session data for verification
    state.auth.phone = phone;
    state.auth.phone_code_hash = data.phone_code_hash;
    state.auth.session_string = data.session_string;

    // Show OTP input field
    document.getElementById('otp-group').style.display = 'block';

    // Add resend button if not exists
    if (!document.getElementById('resend-otp-btn')) {
      const resendBtn = document.createElement('button');
      resendBtn.id = 'resend-otp-btn';
      resendBtn.className = 'btn-resend';
      resendBtn.innerHTML = '🔄 Resend OTP';
      resendBtn.onclick = resendOTP;
      resendBtn.style.marginTop = '10px';
      document.getElementById('otp-group').appendChild(resendBtn);
    }

    button.textContent = 'Verify OTP';
    button.onclick = verifyOTP;

    showToast('✓ OTP sent to your Telegram!', 'success');

  } catch (error) {
    console.error('OTP send error:', error);
    showError('phone', error.message || 'Failed to send OTP');
    showToast('Failed to send OTP: ' + error.message, 'error');
  } finally {
    setButtonLoading(button, false);
  }
}

/**
 * Resend OTP
 */
async function resendOTP() {
  const button = document.getElementById('resend-otp-btn');
  button.disabled = true;
  button.textContent = 'Sending...';

  try {
    await sendOTP();
    showToast('✓ OTP resent successfully!', 'success');
  } finally {
    button.disabled = false;
    button.textContent = '🔄 Resend OTP';
  }
}

/**
 * Verify OTP code
 */
async function verifyOTP() {
  clearError('otp');

  const otp = document.getElementById('otp').value.trim();

  if (!otp) {
    showError('otp', 'OTP is required');
    return;
  }

  // Validate OTP is exactly 6 digits
  if (!/^\d{6}$/.test(otp)) {
    showError('otp', 'OTP must be exactly 6 digits');
    return;
  }

  const button = document.getElementById('verify-btn');
  setButtonLoading(button, true);

  try {
    // Real API call to verify OTP
    const response = await fetch(`${CONFIG.API_BASE_URL}/auth/verify-otp`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        phone: state.auth.phone,
        otp: otp,
        phone_code_hash: state.auth.phone_code_hash,
        session_string: state.auth.session_string,
        api_id: parseInt(state.credentials.apiId),
        api_hash: state.credentials.apiHash
      })
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Invalid OTP');
    }

    const data = await response.json();

    // Store authentication success
    state.auth.otp = otp;
    state.auth.isAuthenticated = true;
    state.auth.account_id = data.account_id;

    showToast('✓ Authentication successful!', 'success');
    goToStep(3);

  } catch (error) {
    console.error('OTP verification error:', error);
    showError('otp', error.message || 'Invalid OTP. Please try again.');
    showToast('Invalid OTP: ' + error.message, 'error');
  } finally {
    setButtonLoading(button, false);
  }
}

// Add input event listener to only allow digits in OTP field
document.addEventListener('DOMContentLoaded', () => {
  const otpInput = document.getElementById('otp');
  if (otpInput) {
    otpInput.addEventListener('input', (e) => {
      // Remove any non-digit characters
      e.target.value = e.target.value.replace(/\D/g, '');
    });
  }
});

// ========================================
// MESSAGE MANAGEMENT
// ========================================

/**
 * Add a new message to the list
 */
function addMessage() {
  clearError('message');

  const messageInput = document.getElementById('message');
  const messageText = messageInput.value.trim();

  if (!messageText) {
    showError('message', 'Message cannot be empty');
    return;
  }

  if (messageText.length < 10) {
    showError('message', 'Message is too short (minimum 10 characters)');
    return;
  }

  state.messages.push(messageText);
  messageInput.value = '';
  renderMessages();
  showToast('✓ Message added!', 'success');
}

/**
 * Delete a message from the list
 */
function deleteMessage(index) {
  if (index >= 0 && index < state.messages.length) {
    state.messages.splice(index, 1);
    renderMessages();
    showToast('Message removed', 'info');
  }
}

/**
 * Render the message list
 */
function renderMessages() {
  const messageList = document.getElementById('messageList');

  if (state.messages.length === 0) {
    messageList.innerHTML = '<div style="text-align: center; color: var(--text-muted); padding: 2rem;">No messages added yet</div>';
    return;
  }

  messageList.innerHTML = state.messages.map((msg, index) => `
    <div class="message-item">
      <div class="message-content">
        <strong>Ad ${index + 1}:</strong> ${msg.length > 100 ? msg.substring(0, 100) + '...' : msg}
      </div>
      <button class="message-delete" onclick="deleteMessage(${index})">Delete</button>
    </div>
  `).join('');
}

// ========================================
// SCHEDULER CONTROLS
// ========================================

/**
 * Start the ad scheduler
 */
async function startScheduler() {
  const startBtn = document.getElementById('start-btn');
  const stopBtn = document.getElementById('stop-btn');
  const statusContainer = document.getElementById('status-container');
  const statusMessage = document.getElementById('status-message');

  setButtonLoading(startBtn, true);

  try {
    // TODO: Replace with actual backend API call
    // Simulating API call
    await new Promise(resolve => setTimeout(resolve, 1000));

    /*
    const response = await fetch(`${CONFIG.API_BASE_URL}/campaign/start`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        user_id: state.access.userId,
        api_id: state.credentials.apiId,
        api_hash: state.credentials.apiHash,
        phone: state.auth.phone,
        groups: state.groups,
        messages: state.messages,
        interval_minutes: state.campaign.intervalMinutes,
        night_mode_enabled: state.campaign.nightModeEnabled,
        group_delay: CONFIG.GROUP_DELAY_SECONDS,
        message_delay: CONFIG.MESSAGE_DELAY_SECONDS
      })
    });
    
    if (!response.ok) {
      throw new Error('Failed to start campaign');
    }
    */

    state.schedulerRunning = true;

    // Update UI
    startBtn.disabled = true;
    stopBtn.disabled = false;
    statusContainer.classList.add('active');
    const intervalText = state.campaign.intervalMinutes >= 60
      ? `${state.campaign.intervalMinutes / 60} hour(s)`
      : `${state.campaign.intervalMinutes} minutes`;
    statusMessage.textContent = `🚀 Campaign running (every ${intervalText})`;

    showToast('✓ Campaign started successfully!', 'success');

  } catch (error) {
    showToast('Failed to start scheduler: ' + error.message, 'error');
  } finally {
    setButtonLoading(startBtn, false);
  }
}

/**
 * Stop the ad scheduler
 */
async function stopScheduler() {
  const startBtn = document.getElementById('start-btn');
  const stopBtn = document.getElementById('stop-btn');
  const statusContainer = document.getElementById('status-container');
  const statusMessage = document.getElementById('status-message');

  setButtonLoading(stopBtn, true);

  try {
    // TODO: Replace with actual backend API call
    // Simulating API call
    await new Promise(resolve => setTimeout(resolve, 1000));

    /*
    const response = await fetch(`${CONFIG.API_BASE_URL}/scheduler/stop`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    });
    
    if (!response.ok) {
      throw new Error('Failed to stop scheduler');
    }
    */

    state.schedulerRunning = false;

    // Update UI
    startBtn.disabled = false;
    stopBtn.disabled = true;
    statusContainer.classList.remove('active');
    statusMessage.textContent = 'Campaign stopped';

    showToast('Scheduler stopped', 'info');

  } catch (error) {
    showToast('Failed to stop scheduler: ' + error.message, 'error');
  } finally {
    setButtonLoading(stopBtn, false);
  }
}

// ========================================
// INITIALIZATION
// ========================================

// ========================================
// ACCESS CONTROL
// ========================================

/**
 * Check if user has access to the app
 */
async function checkAccessStatus() {
  // Grant access to all users - no approval needed
  state.access.hasAccess = true;
  state.access.userId = tg?.initDataUnsafe?.user?.id || 'demo_user';

  // Show main app directly, hide access banner
  document.getElementById('access-banner').style.display = 'none';
  document.getElementById('main-app').style.display = 'block';
}

/**
 * Request access from owner
 */
async function requestAccess() {
  const button = document.getElementById('request-access-btn');
  setButtonLoading(button, true);

  try {
    // TODO: Replace with actual backend API call
    await new Promise(resolve => setTimeout(resolve, 1500));

    /*
    const response = await fetch(`${CONFIG.API_BASE_URL}/auth/request-access`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        telegram_id: tg?.initDataUnsafe?.user?.id,
        username: tg?.initDataUnsafe?.user?.username
      })
    });
    
    if (!response.ok) {
      throw new Error('Failed to request access');
    }
    */

    state.access.accessRequested = true;

    // Update UI
    document.getElementById('access-status-text').textContent =
      'Access request sent! Waiting for approval from @spinify';
    button.disabled = true;
    button.textContent = 'Request Sent';

    showToast('✓ Access request sent to owner!', 'success');

  } catch (error) {
    showToast('Failed to request access: ' + error.message, 'error');
  } finally {
    setButtonLoading(button, false);
  }
}

// ========================================
// CAMPAIGN CONFIGURATION
// ========================================

/**
 * Update campaign interval
 */
function updateInterval() {
  const selector = document.getElementById('interval-selector');
  const minutes = parseInt(selector.value);

  if (minutes < CONFIG.MIN_INTERVAL_MINUTES) {
    showToast(`Minimum interval is ${CONFIG.MIN_INTERVAL_MINUTES} minutes`, 'error');
    selector.value = CONFIG.MIN_INTERVAL_MINUTES;
    return;
  }

  state.campaign.intervalMinutes = minutes;
  showToast(`✓ Interval set to ${minutes} minutes`, 'success');
}

/**
 * Toggle night mode
 */
function toggleNightMode() {
  const toggle = document.getElementById('night-mode-toggle');
  const status = document.getElementById('night-mode-status');

  state.campaign.nightModeEnabled = toggle.checked;

  if (toggle.checked) {
    status.textContent = 'Enabled';
    status.style.color = '#43e97b';
    showToast('✓ Night mode enabled (10 PM - 6 AM)', 'success');
  } else {
    status.textContent = 'Disabled';
    status.style.color = 'var(--text-secondary)';
    showToast('Night mode disabled', 'info');
  }
}

/**
 * Initialize the app
 */
function initApp() {
  console.log('🚀 Spinify Ads initialized');

  // Check user access status
  checkAccessStatus();

  // Set initial progress
  updateProgress(1);

  // Render empty message list
  renderMessages();

  // Add keyboard shortcuts
  document.addEventListener('keydown', (e) => {
    // Enter key to submit forms
    if (e.key === 'Enter' && !e.shiftKey) {
      const activeStep = document.querySelector('.step.active');
      if (activeStep) {
        const primaryButton = activeStep.querySelector('.btn-primary');
        if (primaryButton && !primaryButton.disabled) {
          e.preventDefault();
          primaryButton.click();
        }
      }
    }
  });

  console.log('✅ App ready');
}

// Initialize when DOM is loaded
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initApp);
} else {
  initApp();
}
