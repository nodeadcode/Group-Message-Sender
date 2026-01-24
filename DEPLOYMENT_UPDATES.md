# 🔄 Updates Needed for Live Deployment

## ✅ What Needs to Change

Your frontend is hosted on **cinetimetv.store**, but the configuration still points to localhost. Here's what needs updating:

### 1. **`.env` File** ⚠️ CRITICAL
```env
# Current (localhost):
API_BASE_URL=http://localhost:8000
WEBAPP_URL=http://localhost:8080

# Should be (production):
API_BASE_URL=https://cinetimetv.store/api
WEBAPP_URL=https://cinetimetv.store/webapp
```

### 2. **`webapp/app.js`** ⚠️ CRITICAL
```javascript
// Line 15 currently:
API_BASE_URL: 'http://localhost:8000',

// Should be:
API_BASE_URL: 'https://cinetimetv.store/api',
```

### 3. **Backend Deployment** ⚠️ REQUIRED
Your backend (FastAPI) needs to be deployed to cinetimetv.store and accessible at `/api`

Options:
- Deploy backend to same server at `/api` path
- Or use a subdomain like `api.cinetimetv.store`

---

## 📋 Step-by-Step Fix

### Option A: Deploy Backend to Production (Recommended)

1. **Update `.env` for production:**
   ```env
   API_BASE_URL=https://cinetimetv.store/api
   WEBAPP_URL=https://cinetimetv.store/webapp
   ```

2. **Update `webapp/app.js`:**
   ```javascript
   API_BASE_URL: 'https://cinetimetv.store/api',
   ```

3. **Deploy backend to server:**
   ```bash
   # On your server (VPS):
   cd /path/to/backend
   uvicorn main:app --host 0.0.0.0 --port 8000
   
   # Configure Nginx to proxy /api to backend
   ```

4. **Update Nginx config:**
   ```nginx
   location /api/ {
       proxy_pass http://localhost:8000/;
   }
   
   location /webapp/ {
       alias /path/to/webapp/;
   }
   ```

### Option B: Keep Backend Local for Testing

1. **Create separate env files:**
   - `.env.local` (for localhost)
   - `.env.production` (for live)

2. **Frontend points to local backend:**
   ```javascript
   API_BASE_URL: 'http://YOUR_IP:8000',
   ```

3. **Expose backend port:**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

---

## 🚨 Current Issues

### Frontend (✅ Working)
- Hosted on cinetimetv.store/webapp
- Styles loading perfectly
- Forms displaying correctly

### Backend (❌ Not Connected)
- Still pointing to localhost:8000
- Won't work from live site
- API calls will fail

### Bot (⚠️ Partial)
- Bot token configured ✅
- Owner ID configured ✅
- WEBAPP_URL still localhost ❌

---

## 🔧 Quick Fix Commands

### Update for Production:

```bash
# 1. Update .env
echo "API_BASE_URL=https://cinetimetv.store/api" > .env.prod
echo "WEBAPP_URL=https://cinetimetv.store/webapp" >> .env.prod

# 2. Update app.js
# (manual edit line 15)

# 3. Commit and push
git add .
git commit -m "Update URLs for production deployment"
git push
```

### Test Backend Locally First:

```bash
# Start backend
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000

# Update frontend to point to your IP
# In app.js: API_BASE_URL: 'http://YOUR_IP:8000'
```

---

## 📊 Summary

| Component | Status | Action Needed |
|-----------|--------|---------------|
| Frontend | ✅ Deployed | Update API URL in app.js |
| Backend | ❌ Not deployed | Deploy to server OR expose locally |
| Database | ✅ Local | Deploy with backend |
| Bot | ⚠️ Partial | Update WEBAPP_URL in .env |
| Sessions | ✅ Ready | Will work when backend deployed |

---

## 🎯 Recommended Next Steps

1. **Decide deployment strategy:**
   - Full production (both on server)
   - Hybrid (frontend on server, backend local)

2. **Update configuration files**

3. **Test the connection**

4. **Deploy bot** (if not already running)

---

**Want me to update the files for production deployment?**
