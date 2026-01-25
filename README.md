# 🚀 Spinify Ads - Telegram Group Advertisement Automation

> Automated Telegram group messaging with smart scheduling and message forwarding from Saved Messages

## ✨ Features

- **📱 Telegram Authentication** - Secure OTP-based login with 2FA support
- **📝 Message Forwarding** - Save messages to Saved Messages, then forward to groups
- **👥 Multi-Group Support** - Send to multiple groups (max 10)
- **⏰ Smart Scheduling** - Configurable intervals (20min - 4 hours)
- **🌙 Night Mode** - Auto-pause during night hours (10 PM - 6 AM)
- **🔐 Auto-Cleanup** - Expired/inaccessible groups automatically removed
- **✨ Modern UI** - Glassmorphic design, fully responsive

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Telegram account
- Telegram API credentials ([Get here](https://my.telegram.org/apps))

### Installation

```bash
# 1. Clone repository
git clone https://github.com/nodeadcode/Group-Message-Sender.git
cd Group-Message-Sender

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
# Create .env file:
BOT_TOKEN=your_bot_token
OWNER_TELEGRAM_ID=your_telegram_id
JWT_SECRET=your_secret_key
API_BASE_URL=http://localhost:8000
WEBAPP_URL=http://localhost:8080

# 4. Initialize database
python backend/init_db.py

# 5. Start application (3 terminals):
# Terminal 1 - Bot
python bot/bot.py

# Terminal 2 - Backend
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 3 - Frontend
cd webapp
python -m http.server 8080
```

Visit: `http://localhost:8080`

## 📖 Usage

1. **API Credentials** - Enter Telegram API ID and Hash
2. **Phone Verification** - Send OTP, enter code, verify
3. **Add Groups** - Paste group links (must be member)
4. **Create Messages** - Write ads (saved to Telegram Saved Messages)
5. **Start Campaign** - Configure interval and start forwarding

## 🛠️ Technology Stack

- **Backend:** FastAPI, Telethon, SQLAlchemy
- **Frontend:** Vanilla JavaScript, HTML5/CSS3
- **Database:** SQLite (PostgreSQL for production)

## ⚙️ Configuration

### Environment Variables

```env
# Required
BOT_TOKEN=your_bot_token
OWNER_TELEGRAM_ID=your_telegram_id
JWT_SECRET=your_secret_key

# URLs
API_BASE_URL=http://localhost:8000
WEBAPP_URL=http://localhost:8080

# Database (optional)
DATABASE_URL=sqlite:///./app.db
```

### Getting API Credentials

1. **Telegram API**: Visit https://my.telegram.org/apps
2. **Bot Token**: Message @BotFather → `/newbot`
3. **User ID**: Message @userinfobot

## 🏗️ Project Structure

```
Group-Message-Sender/
├── backend/           # FastAPI API
│   ├── main.py       # Main endpoints
│   ├── auth.py       # OTP authentication
│   ├── models.py     # Database models
│   └── scheduler.py  # Message forwarding
├── bot/              # Telegram bot
├── webapp/           # Frontend
│   ├── index.html
│   ├── app.js
│   └── style.css
├── .env              # Configuration
└── requirements.txt  # Dependencies
```

## 📡 API Endpoints

- `POST /auth/send-otp` - Send verification code
- `POST /auth/verify-otp` - Verify code
- `POST /campaign/create` - Create campaign
- `POST /campaign/start` - Start forwarding
- `GET /health` - Health check

**Full docs:** `http://localhost:8000/docs`

## 🚀 Deployment

1. Install Python 3.8+ on VPS
2. Clone repo and install dependencies  
3. Configure `.env` with production URLs
4. Set up systemd services for bot/backend
5. Use Nginx as reverse proxy
6. Use PostgreSQL for production database
7. Set up SSL with Let's Encrypt

## 📞 Support

- Telegram: [@spinify](https://t.me/spinify)
- Issues: [GitHub Issues](https://github.com/nodeadcode/Group-Message-Sender/issues)

---

**Made with ❤️ by @spinify**