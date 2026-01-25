# 🚀 Spinify Ads - Telegram Group Advertisement Automation

[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)](https://github.com/yourusername/Group-Message-Sender)
[![License](https://img.shields.io/badge/License-MIT-blue)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8+-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green)](https://fastapi.tiangolo.com/)

> **Your all-in-one solution for automated Telegram group advertising with multi-account management, smart scheduling, and auto-reply features.**

![Spinify Ads](https://via.placeholder.com/800x400/6366f1/ffffff?text=Spinify+Ads+Dashboard)

## 📋 Table of Contents

- [Features](#-features)
- [Quick Start](#-quick-start)
- [Technology Stack](#-technology-stack)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [API Documentation](#-api-documentation)
- [Deployment](#-deployment)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Features

### 🎯 Core Features

- **📱 Multi-Account Management** - Add and manage multiple Telegram accounts
- **🔄 Smart Message Scheduling** - Schedule and send messages to multiple groups
- **⏰ Intelligent Scheduling** - Configurable intervals (20min - 4 hours)
- **🌙 Night Mode** - Auto-pause campaigns (10 PM - 6 AM)
- **🤖 Auto-Reply System** - Respond to personal messages automatically
- **💬 Multi-Group Support** - Send to up to 10 groups per campaign
- **🎯 Real-Time Control** - Start/stop campaigns instantly
- **📲 OTP Authentication** - Secure Telegram account verification with resend OTP option
- **🔐 2FA Support** - Two-factor authentication for enhanced security

### 🛡️ Security & Privacy

- **🔐 Encrypted Sessions** - Secure Telethon session storage in dedicated sessions folder
- **🔑 JWT Authentication** - Token-based API security
- **🛡️ Rate Limiting** - Built-in 60-second delays between messages and groups
- **🔒 Secure Credentials** - API credentials handled securely

### 🎨 User Interface

- **✨ Modern Glassmorphic Design** - Beautiful translucent UI with smooth animations
- **📊 Progressive Step Form** - Intuitive 5-step setup process
- **📱 Fully Responsive** - Optimized for mobile, tablet, and desktop
- **🌐 Web-Based Dashboard** - No installation required, works in any browser
- **🎯 Real-Time Feedback** - Toast notifications and status updates

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Telegram account
- Telegram API credentials ([Get here](https://my.telegram.org/apps))
- (Optional) Razorpay account for payments
- (Optional) CoinGate account for crypto payments

### Quick Setup

```bash
# 1. Clone repository
git clone https://github.com/yourusername/Group-Message-Sender.git
cd Group-Message-Sender

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
# Create .env file with your credentials:
# BOT_TOKEN=your_bot_token
# OWNER_TELEGRAM_ID=your_telegram_id
# JWT_SECRET=your_secret_key
# API_BASE_URL=http://localhost:8000
# WEBAPP_URL=http://localhost:8080

# 4. Initialize database
python backend/init_db.py

# 5. Start components (3 separate terminals):
# Terminal 1 - Bot:
python bot/bot.py

# Terminal 2 - Backend API:
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 3 - Frontend:
cd webapp
python -m http.server 8080
```

Visit: `http://localhost:8080` 🎉

## 🛠️ Technology Stack

### Backend
- **FastAPI** - Modern async web framework
- **SQLAlchemy** - Database ORM
- **Telethon** - Telegram MTProto client library
- **python-telegram-bot** - Telegram bot framework
- **PyJWT** - JWT token authentication
- **APScheduler** - Advanced Python scheduler
- **Uvicorn** - ASGI server

### Frontend
- **Vanilla JavaScript** - Lightweight, no framework overhead
- **HTML5/CSS3** - Semantic markup with modern glassmorphic styling
- **Google Fonts (Inter)** - Premium typography

### Database
- **SQLite** - Default (easy setup, portable)
- **PostgreSQL** - Production recommended

## 📦 Installation

### Manual Installation

If you prefer to install manually without the setup scripts:

```bash
# Install dependencies
pip install -r requirements.txt

# Initialize database
python backend/init_db.py

# Run components separately
python bot/bot.py                    # Terminal 1: Bot
uvicorn backend.main:app --reload    # Terminal 2: Backend API
python -m http.server 8080           # Terminal 3: Frontend (in webapp/)
```

### Docker Installation (Coming Soon)

```bash
docker-compose up -d
```

## ⚙️ Configuration

### Environment Variables

Create `.env` file in root directory:

```env
# Bot Configuration
BOT_TOKEN=your_bot_token_from_botfather
OWNER_TELEGRAM_ID=your_telegram_user_id

# API URLs
API_BASE_URL=http://localhost:8000
WEBAPP_URL=http://localhost:8080

# Security
JWT_SECRET=your_random_jwt_secret_key_here
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=168

# Telegram Bot Username
BOT_USERNAME=your_bot_username

# Database (SQLite by default)
DATABASE_URL=sqlite:///./app.db
# For PostgreSQL: postgresql://user:password@localhost/dbname
```

### Getting Credentials

**Telegram API:**
1. Visit https://my.telegram.org/apps
2. Create new application
3. Copy API ID and API Hash

**Bot Token:**
1. Message @BotFather on Telegram
2. Create new bot with `/newbot`
3. Copy the token

**Your Telegram User ID:**
1. Message @userinfobot on Telegram
2. Copy your User ID for OWNER_TELEGRAM_ID in .env

## 📖 Usage

### Web Application Workflow

1. **Open Dashboard** - Navigate to `http://localhost:8080`
2. **Step 1: API Credentials** - Enter your Telegram API ID and Hash
3. **Step 2: Phone Verification** 
   - Enter phone number with country code (e.g., +1234567890)
   - Click "Send OTP" to receive verification code
   - Enter 6-digit OTP from Telegram
   - Click "Verify OTP" (supports 2FA if enabled)
4. **Step 3: Add Groups** - Paste Telegram group links (max 10)
5. **Step 4: Create Messages** - Write and save your ad messages
6. **Step 5: Configure & Launch**
   - Set campaign interval (20min - 4 hours)
   - Toggle night mode (10 PM - 6 AM pause)
   - Start/stop campaign with one click

### Bot Commands

- `/start` - Welcome message and bot information
- Additional commands can be added in `bot/bot.py`

## 📡 API Documentation

### Authentication Endpoints

```http
POST   /auth/telegram          # Telegram widget authentication
POST   /auth/send-otp          # Send OTP to phone number
POST   /auth/verify-otp        # Verify OTP code
POST   /auth/2fa               # Verify 2FA password
```

### User Profile

```http
GET    /user/profile           # Get current user profile
PUT    /user/profile           # Update user profile
```

### Account Management

```http
GET    /accounts               # List all Telegram accounts
DELETE /accounts/{id}          # Delete account
PUT    /accounts/{id}/activate # Set account as active
GET    /accounts/{id}/status   # Check account status
```

### Campaign Management

```http
POST   /campaign/create        # Create new campaign
POST   /campaign/start         # Start campaign
POST   /campaign/stop          # Stop campaign
PUT    /campaign/update        # Update campaign settings
GET    /campaign/status        # Get campaign status
```

### Auto-Reply Settings

```http
GET    /auto-reply/settings/{account_id}  # Get auto-reply settings
PUT    /auto-reply/settings/{account_id}  # Update auto-reply settings
POST   /auto-reply/toggle/{account_id}    # Toggle auto-reply on/off
```

### Health Check

```http
GET    /health                 # API health check
GET    /                       # API root info
```

**Full API Docs:** Visit `http://localhost:8000/docs` when backend is running.

## 🏗️ Project Structure

```
Group-Message-Sender/
├── backend/              # FastAPI backend API
│   ├── main.py          # Main API endpoints & CORS config
│   ├── auth.py          # Authentication routes (OTP, 2FA)
│   ├── models.py        # SQLAlchemy database models
│   ├── database.py      # Database configuration
│   ├── config.py        # App settings & environment vars
│   ├── scheduler.py     # Campaign scheduler logic
│   ├── auto_reply.py    # Auto-reply message handler
│   ├── telegram_auth.py # Telegram login verification
│   ├── telethon_login.py # Telethon session management
│   ├── group_verify.py  # Group validation utilities
│   └── init_db.py       # Database initialization script
├── bot/                 # Telegram bot
│   └── bot.py          # Bot commands & handlers
├── webapp/              # Frontend web application
│   ├── index.html      # Main HTML structure
│   ├── app.js          # Frontend logic & API calls
│   ├── style.css       # Main styles (glassmorphic design)
│   └── otp-styles.css  # Additional OTP-specific styles
├── sessions/            # Telethon session files (auto-created)
├── .env                # Environment variables (create manually)
├── .gitignore          # Git ignore rules
├── requirements.txt    # Python dependencies
├── app.db              # SQLite database (auto-created)
└── README.md           # This file
```

## 🚀 Deployment

### VPS Deployment

For production deployment:

1. **Install Python 3.8+** and pip
2. **Clone repository** and install dependencies
3. **Configure .env** with production settings
4. **Set up systemd services** for bot and backend
5. **Configure Nginx** as reverse proxy for backend/frontend
6. **Use PostgreSQL** instead of SQLite (update DATABASE_URL)
7. **Set up SSL** with Let's Encrypt

Example systemd service (`/etc/systemd/system/spinify-bot.service`):
```ini
[Unit]
Description=Spinify Ads Bot
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/Group-Message-Sender
ExecStart=/usr/bin/python3 /path/to/Group-Message-Sender/bot/bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

### Recommended Hosting

- **Backend:** DigitalOcean, Heroku, Railway
- **Database:** PostgreSQL on Supabase, Railway
- **Frontend:** Vercel, Netlify, Cloudflare Pages

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

## 👨‍💻 Author

**@spinify**

- Telegram: [@spinify](https://t.me/spinify)
- GitHub: [@yourusername](https://github.com/yourusername)

## 🙏 Acknowledgments

- [Telethon](https://github.com/LonamiWebs/Telethon) - Excellent Telegram client library
- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) - Bot framework

## 📞 Support

- 💬 Telegram: [@spinify](https://t.me/spinify)
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/Group-Message-Sender/issues)
- 📖 API Docs: Run backend and visit `http://localhost:8000/docs`

## ⭐ Star History

If you find this project useful, please consider giving it a star!

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/Group-Message-Sender&type=Date)](https://star-history.com/#yourusername/Group-Message-Sender&Date)

---

**Made with ❤️ by @spinify** | **⭐ Star this repo if you find it useful!**