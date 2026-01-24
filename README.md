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
- **🔄 Smart Message Forwarding** - Auto-forward via Saved Messages to groups
- **⏰ Intelligent Scheduling** - Configurable intervals (20min - 4 hours)
- **🌙 Night Mode** - Auto-pause campaigns (12 AM - 6 AM)
- **🤖 Auto-Reply System** - Respond to personal messages automatically
- **💬 Multi-Group Support** - Send to up to 10 groups per campaign
- **🎯 Real-Time Control** - Start/stop campaigns instantly

### 💰 Subscription & Payments

- **💳 Multiple Payment Options:**
  - **Razorpay** - UPI, Cards, Net Banking, Wallets
  - **Crypto** - BTC, ETH, USDT, and 50+ cryptocurrencies
- **🎟️ Access Code System** - Generate and redeem subscription codes
- **📊 Flexible Plans:**
  - Weekly: ₹99 (7 days)
  - Monthly: ₹299 (30 days)

### 🛡️ Security & Privacy

- **🔐 Encrypted Sessions** - Secure Telethon session storage
- **🔑 JWT Authentication** - Token-based API security
- **🛡️ Rate Limiting** - Built-in delays to avoid spam detection
- **🔒 Encrypted Credentials** - API credentials stored securely

### 🎨 User Interface

- **📱 Telegram Web App** - Seamless in-app experience
advanced - **✨ Glassmorphic Design** - Modern translucent UI with animations
- **📊 Real-Time Dashboard** - Monitor campaign status live
- **🌐 Fully Responsive** - Works on mobile, tablet, desktop

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Telegram account
- Telegram API credentials ([Get here](https://my.telegram.org/apps))
- (Optional) Razorpay account for payments
- (Optional) CoinGate account for crypto payments

### 5-Minute Setup

```bash
# 1. Clone repository
git clone https://github.com/yourusername/Group-Message-Sender.git
cd Group-Message-Sender

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env with your credentials

# 4. Initialize database
cd backend
python -c "from database import init_db; init_db()"

# 5. Run the bot
cd ../bot
python bot.py

# 6. Run the backend (new terminal)
cd ../backend
uvicorn main:app --reload

# 7. Run the frontend (new terminal)
python -m http.server 8080 --directory webapp
```

Visit: `http://localhost:8080` 🎉

## 🛠️ Technology Stack

### Backend
- **FastAPI** - Modern async web framework
- **SQLAlchemy** - Database ORM
- **Telethon** - Telegram MTProto client
- **python-telegram-bot** - Bot framework
- **Razorpay** - Payment gateway (INR)
- **CoinGate** - Crypto payment processor

### Frontend
- **Vanilla JavaScript** - No framework overhead
- **HTML5/CSS3** - Semantic markup with modern styling
- **Telegram Web App** - Native Telegram integration

### Database
- **SQLite** - Development (easy setup)
- **PostgreSQL** - Production (recommended)

## 📦 Installation

### Detailed Installation

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for complete step-by-step instructions.

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

# Security
SESSION_SECRET=random_secret_string
JWT_SECRET=another_random_secret

# Database
DATABASE_URL=sqlite:///./app.db

# Payment Gateways (Optional)
RAZORPAY_KEY_ID=rzp_xxxxx
RAZORPAY_KEY_SECRET=xxxxx
COINGATE_API_TOKEN=xxxxx
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

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed instructions.

## 📖 Usage

### For Users

1. **Start the bot** - Send `/start` to your bot
2. **Redeem code** - `/redeem YOUR_CODE`
3. **Open dashboard** - Click "🚀 Open Dashboard"
4. **Add account** - Enter API ID, Hash, Phone
5. **Verify OTP** - Enter code from Telegram
6. **Add groups** - Paste group links
7. **Create messages** - Write your ads
8. **Start campaign** - Configure and launch!

### For Owners

Generate access codes:
```
/generate weekly   # Create ₹99 weekly code
/generate monthly  # Create ₹299 monthly code
```

### Bot Commands

- `/start` - Welcome message and dashboard
- `/redeem <code>` - Activate subscription
- `/generate <plan>` - Generate access code (owner only)

## 📡 API Documentation

### Authentication Endpoints

```http
POST /auth/telegram
POST /auth/send-otp
POST /auth/verify-otp
```

### Subscription Endpoints

```http
GET  /subscription/status
POST /subscription/validate
```

### Account Management

```http
GET    /accounts
POST   /accounts
DELETE /accounts/{id}
PUT    /accounts/{id}/activate
```

### Campaign Management

```http
POST   /campaign/create
POST   /campaign/start
POST   /campaign/stop
PUT    /campaign/update
GET    /campaign/status
```

### Payment Endpoints

```http
POST /payments/create
POST /payments/razorpay/verify
POST /payments/razorpay/webhook
POST /payments/coingate/webhook
GET  /payments/history
```

**Full API Docs:** Visit `http://localhost:8000/docs` when backend is running.

## 🏗️ Project Structure

```
Group-Message-Sender/
├── backend/              # FastAPI backend
│   ├── models.py        # Database models
│   ├── database.py      # DB configuration
│   ├── main.py          # API endpoints
│   ├── config.py        # Settings
│   ├── payments.py      # Payment integration
│   ├── auto_reply.py    # Auto-reply handler
│   └── telethon_login.py
├── bot/                 # Telegram bot
│   └── bot.py          # Bot commands
├── webapp/              # Frontend
│   ├── index.html
│   ├── app.js
│   └── style.css
├── .env.example         # Environment template
├── requirements.txt     # Dependencies
└── README.md           # This file
```

## 🚀 Deployment

### Production Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for VPS deployment guide.

Quick deploy to VPS:
```bash
./deploy-vps.sh
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

- 📧 Email: support@spinify.com
- 💬 Telegram: [@spinify](https://t.me/spinify)
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/Group-Message-Sender/issues)
- 📖 Docs: [Setup Guide](SETUP_GUIDE.md)

## ⭐ Star History

If you find this project useful, please consider giving it a star!

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/Group-Message-Sender&type=Date)](https://star-history.com/#yourusername/Group-Message-Sender&Date)

---

**Made with ❤️ by @spinify** | **⭐ Star this repo if you find it useful!**