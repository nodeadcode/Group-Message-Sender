# 🚀 Setup Guide - Spinify Ads

Complete setup guide for deploying and running the Spinify Ads Telegram application.

## 📋 Prerequisites

- Python 3.8 or higher
- Telegram account
- Telegram API credentials
- (Optional) Razorpay account for INR payments
- (Optional) CoinGate account for crypto payments

## 🔧 Step 1: Get Telegram API Credentials

### Method 1: For User Accounts (Telethon)

1. Visit [https://my.telegram.org/apps](https://my.telegram.org/apps)
2. Log in with your phone number
3. Click "API Development Tools"
4. Fill in the form:
   - **App title:** Spinify Ads
   - **Short name:** spinify
   - **Platform:** Other
   - **Description:** Group message scheduler
5. You'll receive:
   - `api_id` - numeric ID
   - `api_hash` - 32-character hex string
6. **Save these credentials** - you'll need them!

### Method 2: For Bot (python-telegram-bot)

1. Open Telegram and search for `@BotFather`
2. Send `/newbot`
3. Follow the prompts:
   - Choose a name (e.g., "Spinify Ads Bot")
   - Choose a username (must end in 'bot', e.g., "spinify_ads_bot")
4. You'll receive a **Bot Token** like: `123456789:ABCdefGhIjKlmnoPQRsTUVwxyz`
5. **Save this token!**

## 📦 Step 2: Clone and Install

```bash
# Clone repository
git clone https://github.com/yourusername/Group-Message-Sender.git
cd Group-Message-Sender

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\\Scripts\\activate
# On Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## ⚙️ Step 3: Configure Environment Variables

1. Copy the example environment file:
```bash
copy .env.example .env
```

2. Edit `.env` and fill in your credentials:

```env
# Application URLs
API_BASE_URL=http://localhost:8000
WEBAPP_URL=http://localhost:8080

# Telegram Bot
BOT_TOKEN=your_bot_token_here  # From @BotFather
OWNER_TELEGRAM_ID=your_telegram_user_id  # Your Telegram user ID

# Security
SESSION_SECRET=long_random_string_here
JWT_SECRET=another_long_random_string

# Database
DATABASE_URL=sqlite:///./app.db

# Payment Gateways (Optional)
RAZORPAY_KEY_ID=rzp_test_xxxxx
RAZORPAY_KEY_SECRET=xxxxx
RAZORPAY_WEBHOOK_SECRET=xxxxx

COINGATE_API_TOKEN=xxxxx
COINGATE_ENVIRONMENT=sandbox  # or 'live' for production
```

### Finding Your Telegram User ID

1. Message `@userinfobot` on Telegram
2. It will reply with your User ID
3. Copy this number to `OWNER_TELEGRAM_ID`

### Generating Secure Secrets

```python
import secrets
print("SESSION_SECRET:", secrets.token_urlsafe(32))
print("JWT_SECRET:", secrets.token_urlsafe(32))
```

## 🗄️ Step 4: Initialize Database

```bash
cd backend
python -c "from database import init_db; init_db()"
```

This creates the SQLite database with all required tables.

## 🤖 Step 5: Run the Telegram Bot

In a new terminal:

```bash
cd bot
python bot.py
```

You should see:
```
🤖 Bot is running...
Owner ID: <your_id>
```

### Test Bot Commands

1. Open Telegram and find your bot
2. Send `/start` - you should get the welcome message
3. Send `/generate weekly` (owner only) - generates access code
4. Send `/redeem <code>` - redeem the code

## 🌐 Step 6: Run the Backend API

In another terminal:

```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Access API docs at: [http://localhost:8000/docs](http://localhost:8000/docs)

## 💻 Step 7: Run the Frontend

In another terminal:

```bash
python -m http.server 8080 --directory webapp
```

Access webapp at: [http://localhost:8080](http://localhost:8080)

## 🔐 Step 8: Payment Gateway Setup (Optional)

### Razorpay (INR Payments)

1. Sign up at [https://razorpay.com](https://razorpay.com)
2. Go to Dashboard → Settings → API Keys
3. Generate Test/Live Keys
4. Update `.env` with:
   - `RAZORPAY_KEY_ID`
   - `RAZORPAY_KEY_SECRET`
5. Setup webhook:
   - URL: `https://your-domain.com/payments/razorpay/webhook`
   - Events: `payment.captured`, `payment.failed`

### CoinGate (Crypto Payments)

1. Sign up at [https://coingate.com](https://coingate.com)
2. Go to Account → API
3. Generate API credentials
4. Update `.env` with:
   - `COINGATE_API_TOKEN`
   - `COINGATE_ENVIRONMENT` (sandbox for testing)

## 🧪 Step 9: Test the Application

### Test User Flow

1. **Login:**
   - Click "Login with Telegram" on webapp
   - Authorize the application
   - Your profile should appear

2. **Redeem Subscription:**
   - In Telegram bot, send: `/generate weekly`
   - Copy the code
   - Send: `/redeem <code>`
   - Subscription activated!

3. **Add Telegram Account:**
   - Enter API ID and API Hash
   - Enter phone number
   - Verify OTP from Telegram

4. **Create Campaign:**
   - Add group links
   - Add messages
   - Set interval and night mode
   - Start campaign!

### Test Auto-Reply

1. Go to "Manage Accounts"
2. Enable auto-reply for an account
3. Set custom message: "Hi {name}, I'll reply soon!"
4. Save settings
5. Send a message to that account from another phone
6. Should auto-reply after 2-5 seconds!

## 🚨 Troubleshooting

### "Module not found" errors
```bash
pip install -r requirements.txt
```

### Database errors
```bash
rm app.db  # Delete old database
python -c "from database import init_db; init_db()"  # Recreate
```

### Bot not responding
- Check BOT_TOKEN is correct
- Check bot is running (`python bot.py`)
- Check OWNER_TELEGRAM_ID matches your ID

### OTP not received
- Check API_ID and API_HASH are correct
- Check phone number has country code (+91, +1, etc.)
- Check Telegram Saved Messages for OTP

## 📝 Owner Commands

- `/generate weekly` - Generate ₹99/week access code
- `/generate monthly` - Generate ₹299/month access code

## 👤 User Commands

- `/start` - Welcome message and web app link
- `/redeem <code>` - Activate subscription with code

## 🔄 Updates and Maintenance

### Update Code
```bash
git pull
pip install -r requirements.txt
```

### Backup Database
```bash
cp app.db app.db.backup
```

### View Logs
Check console output of backend/bot for logs

## 🌐 Production Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment guide.

## 💡 Tips

1. **Use .env file** - Never commit secrets to Git
2. **Test in sandbox** - Use test credentials before going live
3. **Monitor logs** - Check for errors regularly
4. **Backup database** - Schedule regular backups
5. **Update dependencies** - Keep packages up to date

## 📞 Support

For issues:
1. Check this guide first
2. Check logs for errors
3. Contact [@spinify](https://t.me/spinify)

---

Made with ❤️ by @spinify
