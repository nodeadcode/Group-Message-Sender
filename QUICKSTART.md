# 🚀 Spinify Ads - Quick Start

## ✅ Simple 3-Step Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Your Owner ID
```bash
# Get your Telegram ID from @userinfobot
# Edit .env and set:
OWNER_TELEGRAM_ID=your_id_here
```

### 3. Initialize Database
```bash
python backend/init_db.py
```

## 🤖 Start the Bot

```bash
cd bot
python bot.py
```

## 📝 Bot Commands

### For Owner (You)
```
/generate weekly   → Create ₹99/week code
/generate monthly  → Create ₹299/month code
```

### For Users
```
/start           → Welcome message
/redeem CODE123  → Activate subscription
```

## 💡 How It Works

1. **Owner generates codes** with `/generate weekly` or `/generate monthly`
2. **Share code with users**
3. **Users redeem** with `/redeem CODE`
4. **Subscription activated** automatically!

## 🎯 Plans

- **Weekly:** ₹99 for 7 days
- **Monthly:** ₹299 for 30 days

Activated via access codes only - no payment gateway needed!

---

**Need detailed docs?** → See [SETUP_GUIDE.md](SETUP_GUIDE.md)
