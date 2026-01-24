# 📋 Configuration Checklist

## Before You Start

Go through this checklist to ensure everything is configured correctly.

### ✅ Step 1: Get Telegram Credentials

- [ ] **Bot Token** (from @BotFather)
  - Open Telegram
  - Search for `@BotFather`
  - Send `/newbot`
  - Follow prompts
  - Copy token (looks like: `123456789:ABCdefGhIjKlmnoPQRsTUVwxyz`)

- [ ] **Your Telegram User ID** (from @userinfobot)
  - Open Telegram
  - Search for `@userinfobot`
  - Start the bot
  - Copy your User ID (just numbers, e.g., `123456789`)

### ✅ Step 2: Configure .env File

Open `.env` and fill in these values:

```env
# Required - Your bot token
BOT_TOKEN=paste_your_bot_token_here

# Required - Your Telegram user ID
OWNER_TELEGRAM_ID=paste_your_user_id_here
```

**Important:** Don't add quotes, just paste the values directly!

✅ **Correct:**
```env
BOT_TOKEN=123456789:ABCdefGhIjKlmnoPQRsTUVwxyz
OWNER_TELEGRAM_ID=987654321
```

❌ **Wrong:**
```env
BOT_TOKEN="123456789:ABCdefGhIjKlmnoPQRsTUVwxyz"
OWNER_TELEGRAM_ID="987654321"
```

### ✅ Step 3: Optional - Payment Gateways

Only fill these if you want to accept payments:

**Razorpay (for INR payments):**
- [ ] Sign up at https://razorpay.com
- [ ] Get API keys from Dashboard → Settings → API Keys
- [ ] Update in `.env`:
  ```env
  RAZORPAY_KEY_ID=your_key_id
  RAZORPAY_KEY_SECRET=your_secret
  ```

**CoinGate (for Crypto payments):**
- [ ] Sign up at https://coingate.com
- [ ] Get API token from Account → API
- [ ] Update in `.env`:
  ```env
  COINGATE_API_TOKEN=your_token
  COINGATE_ENVIRONMENT=sandbox
  ```

**Note:** You can skip payment gateways and just use access codes!

### ✅ Step 4: Verify Installation

Run the setup script:

**Windows:**
```bash
setup.bat
```

**Linux/Mac:**
```bash
chmod +x setup.sh
./setup.sh
```

All steps should show ✅

### ✅ Step 5: Test Everything

**Test Bot:**
```
1. Run: cd bot && python bot.py
2. Open Telegram
3. Find your bot
4. Send: /start
5. Should see welcome message ✅
```

**Test Backend:**
```
1. Run: cd backend && uvicorn main:app --reload
2. Open: http://localhost:8000/docs
3. Should see API documentation ✅
```

**Test Frontend:**
```  
1. Run: python -m http.server 8080 --directory webapp
2. Open: http://localhost:8080
3. Should see Spinify dashboard ✅
```

## Common Issues

### "Bot not responding"
- ✅ Check BOT_TOKEN is correct
- ✅ Check bot.py is running
- ✅ Try `/start` command again

### "Not owner" error
- ✅ Check OWNER_TELEGRAM_ID matches your ID
- ✅ No quotes in .env file
- ✅ Restart bot after changing .env

### "Module not found" errors
- ✅ Activate virtual environment first
- ✅ Run: `pip install -r requirements.txt`
- ✅ Check Python version (need 3.8+)

### "Database error"
- ✅ Delete app.db file
- ✅ Run: `python backend/init_db.py`
- ✅ Check file permissions

## All Set? 🎉

Once everything above is ✅, you're ready to:

1. Generate access codes with `/generate weekly`
2. Redeem codes with `/redeem CODE`
3. Add Telegram accounts via dashboard
4. Create and schedule campaigns!

Need help? Check [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed instructions.
