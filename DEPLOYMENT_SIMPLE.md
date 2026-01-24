# 🚀 Deployment Guide - Current Setup

## ✅ What's Already Deployed

### Frontend (Live)
- **Platform:** GitHub Pages
- **URL:** https://cinetimetv.store/webapp
- **Repository:** nodeadcode/Group-Message-Sender
- **Status:** ✅ Working perfectly

## ⚠️ What Needs to Be Deployed

### Backend (Not deployed yet)
- **Current:** Only runs locally
- **Needs:** VPS or cloud hosting
- **API Endpoints:** 20+ endpoints ready

## 🎯 Quick Backend Deployment Options

### Option 1: Railway.app (Easiest - 5 minutes)

1. **Go to:** https://railway.app
2. **Sign up** with GitHub
3. **New Project** → Deploy from GitHub repo
4. **Select:** nodeadcode/Group-Message-Sender
5. **Root Directory:** `/backend`
6. **Start Command:** `uvicorn main:app --host 0.0.0.0 --port 8000`
7. **Add environment variables** from your `.env` file
8. **Deploy!**

You'll get a URL like: `your-app.up.railway.app`

**Then update frontend:**
```javascript
// In webapp/app.js line 15:
API_BASE_URL: 'https://your-app.up.railway.app',

// Commit and push - GitHub Pages auto-updates
```

### Option 2: Your VPS (Full Control)

**If you have a VPS:**

```bash
# 1. SSH to your server
ssh user@your-vps-ip

# 2. Clone repo
git clone https://github.com/nodeadcode/Group-Message-Sender.git
cd Group-Message-Sender

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run backend
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000

# 5. Configure Nginx (optional but recommended)
# Point /api to localhost:8000
```

**Update frontend to point to your VPS:**
```javascript
API_BASE_URL: 'https://your-vps-domain.com/api',
```

### Option 3: Render.com (Free Tier)

1. **Sign up:** https://render.com
2. **New Web Service**
3. **Connect GitHub:** nodeadcode/Group-Message-Sender
4. **Settings:**
   - **Root Directory:** backend
   - **Build Command:** `pip install -r ../requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port 8000`
5. **Environment Variables:** Copy from `.env`
6. **Create Service**

**Note:** Free tier spins down after inactivity

## 🔗 Connecting Frontend to Backend

### Step 1: Deploy Backend (choose option above)

### Step 2: Get Your Backend URL
- Railway: `https://your-app.up.railway.app`
- VPS: `https://your-domain.com/api`
- Render: `https://your-app.onrender.com`

### Step 3: Update Frontend

**Edit `webapp/app.js` line 15:**
```javascript
const config = {
  API_BASE_URL: 'https://YOUR_BACKEND_URL',  // ← Update this
  DEBUG: false,
};
```

### Step 4: Push to GitHub

```bash
git add webapp/app.js
git commit -m "Connect frontend to backend"
git push origin main

# GitHub Pages auto-deploys in ~1 minute
```

### Step 5: Test

Visit https://cinetimetv.store/webapp and try logging in!

## 🤖 Bot Deployment

**Update `.env`:**
```env
WEBAPP_URL=https://cinetimetv.store/webapp
```

**Run the bot:**
```bash
# Option 1: On your local machine
cd bot
python bot.py

# Option 2: On your VPS
# (Same as above, but on server)

# Option 3: Screen session (keeps running)
screen -S bot
cd bot
python bot.py
# Press Ctrl+A then D to detach
```

## ✅ Deployment Checklist

### Current Status:
- [x] Frontend deployed to GitHub Pages
- [x] Custom domain (cinetimetv.store) configured
- [x] HTTPS enabled
- [ ] Backend deployed
- [ ] Frontend connected to backend
- [ ] Bot running
- [ ] Database migrated (optional)

### After Backend is Deployed:
- [ ] Update app.js with backend URL
- [ ] Test API connection
- [ ] Run bot
- [ ] Test full flow

## 💰 Cost Breakdown

**Current (Frontend only):**
- GitHub Pages: **$0**
- Domain: ~$10/year *(already have)*
- **Total: FREE**

**With Backend:**
- Railway Starter: **$5/month**
- OR VPS: **$5-10/month**
- **Total: $5-10/month**

## 🎯 Recommended: Railway.app

**Why Railway?**
- ✅ Easiest deployment (5 minutes)
- ✅ Auto-deploys on GitHub push
- ✅ Free $5 credit to start
- ✅ PostgreSQL database included
- ✅ No server management
- ✅ HTTPS included

**Start here:** https://railway.app

## 📞 Need Help?

**Check these docs:**
- `HOW_TO_RUN_BACKEND.md` - Running backend locally
- `SETUP_GUIDE.md` - Complete setup guide
- `QUICKSTART.md` - Quick start guide

**Test locally first:**
```bash
# Terminal 1: Backend
cd backend
uvicorn main:app --reload

# Terminal 2: Update app.js to localhost
# Then test at http://localhost:8080
```

---

**Your frontend is live! Just need to deploy the backend and connect them.** 🚀
