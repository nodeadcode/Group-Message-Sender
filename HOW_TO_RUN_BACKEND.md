# 🚀 How to Run the Backend

## Quick Start (3 Commands)

```bash
# 1. Go to backend folder
cd backend

# 2. Start the server
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 3. Open in browser
# Visit: http://localhost:8000/docs
```

## Detailed Steps

### Option 1: Development Mode (Recommended)

```bash
cd backend
uvicorn main:app --reload
```

**What this does:**
- Starts backend on `http://localhost:8000`
- Auto-reloads when you edit code
- Perfect for development

### Option 2: Production Mode

```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

**What this does:**
- Accessible from other devices on network
- 4 worker processes for better performance
- Production-ready

### Option 3: Custom Port

```bash
cd backend
uvicorn main:app --port 5000
```

**What this does:**
- Runs on port 5000 instead of 8000
- Useful if 8000 is already in use

## ✅ Verify It's Working

Once started, you should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Test the API:**
1. Open browser: http://localhost:8000
2. API docs: http://localhost:8000/docs
3. Health check: http://localhost:8000/health

## 🔧 Common Issues

### "Command not found: uvicorn"
```bash
pip install uvicorn
```

### "Port already in use"
```bash
# Find what's using port 8000
netstat -ano | findstr :8000

# Kill it or use different port
uvicorn main:app --port 8001
```

### "Module not found"
```bash
# Install all dependencies
pip install -r ../requirements.txt
```

## 📊 What's Running

When backend is running, these endpoints are available:

**Authentication:**
- `POST /auth/telegram` - Login with Telegram
- `POST /auth/send-otp` - Send OTP
- `POST /auth/verify-otp` - Verify OTP

**Accounts:**
- `GET /accounts` - List accounts
- `POST /accounts` - Add account
- `DELETE /accounts/{id}` - Remove account

**Campaigns:**
- `POST /campaign/create` - Create campaign
- `POST /campaign/start` - Start campaign
- `POST /campaign/stop` - Stop campaign

**Full API docs:** http://localhost:8000/docs

## 🎯 Connect Frontend

After backend is running, make sure frontend points to it:

**In `webapp/app.js` line 15:**
```javascript
API_BASE_URL: 'http://localhost:8000',
```

Then frontend can make API calls!

## 🛑 Stop the Backend

Press `CTRL + C` in the terminal

---

**That's it!** Backend should now be running and ready to handle requests.
