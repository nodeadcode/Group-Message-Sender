const tg = window.Telegram.WebApp;
tg.expand();

let messages = [];

function goToStep(step) {
  document.querySelectorAll('.step').forEach(s => s.classList.remove('active'));
  document.getElementById(`step-${step}`).classList.add('active');
}

function addMessage() {
  const msg = document.getElementById("message").value.trim();
  if (!msg) return;

  messages.push(msg);
  document.getElementById("message").value = "";
  renderMessages();
}

function renderMessages() {
  const list = document.getElementById("messageList");
  list.innerHTML = "";

  messages.forEach((m, i) => {
    const li = document.createElement("li");
    li.textContent = `Ad ${i + 1}: ${m.substring(0, 40)}...`;
    list.appendChild(li);
  });
}

function startScheduler() {
  alert("Scheduler started (backend will handle logic)");
}

function stopScheduler() {
  alert("Scheduler stopped");
}
