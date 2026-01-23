# 🚀 Deploying Spinify Ads to cinetimetv.store

Complete deployment guide for hosting on **cinetimetv.store**

## 📋 Prerequisites Checklist

- ✅ VPS server with Ubuntu/Debian
- ✅ SSH access to your VPS
- ✅ Domain: cinetimetv.store
- ✅ DNS A record pointing to your VPS IP

## 🎯 Quick Deploy (5 Minutes)

### Step 1: Configure DNS

**Go to your domain registrar (where you bought cinetimetv.store):**

1. Find DNS settings
2. Add/Update A record:
   ```
   Type: A
   Host: @
   Value: YOUR_VPS_IP_ADDRESS
   TTL: 3600
   ```
3. Add www subdomain (optional):
   ```
   Type: A
   Host: www
   Value: YOUR_VPS_IP_ADDRESS
   TTL: 3600
   ```

**Wait 5-10 minutes for DNS propagation**

### Step 2: SSH into Your VPS

```bash
ssh root@YOUR_VPS_IP
```

### Step 3: Run Automated Deployment

```bash
# Download the deployment script
wget https://raw.githubusercontent.com/nodeadcode/Group-Message-Sender/main/deploy-vps.sh

# Make it executable
chmod +x deploy-vps.sh

# Edit the domain in the script
nano deploy-vps.sh
# Change: DOMAIN="your-domain.com"
# To: DOMAIN="cinetimetv.store"

# Run the deployment
./deploy-vps.sh
```

**The script will automatically:**
- Install all dependencies (Python, Nginx, etc.)
- Clone your repository
- Setup systemd service
- Configure Nginx for cinetimetv.store
- Setup SSL certificate via Let's Encrypt

### Step 4: Update Frontend API URL

After deployment, edit the frontend config:

```bash
nano /var/www/spinify-ads/webapp/app.js
```

Find and update:
```javascript
const CONFIG = {
  API_BASE_URL: 'https://cinetimetv.store/api',  // ← Change this
  // ... rest stays the same
};
```

Restart the service:
```bash
sudo systemctl restart spinify-ads
```

### Step 5: Verify Deployment

Visit **https://cinetimetv.store** - Your app should be live! 🎉

## 🔧 Manual Deployment (Step by Step)

If you prefer manual control:

### 1. System Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y python3 python3-pip python3-venv nginx git certbot python3-certbot-nginx
```

### 2. Clone Repository

```bash
# Create app directory
sudo mkdir -p /var/www/spinify-ads
cd /var/www/spinify-ads

# Clone from GitHub
git clone https://github.com/nodeadcode/Group-Message-Sender.git .
```

### 3. Setup Python Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Create Backend Service

```bash
sudo nano /etc/systemd/system/spinify-ads.service
```

Paste this:
```ini
[Unit]
Description=Spinify Ads - Telegram Ad Scheduler
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/var/www/spinify-ads
Environment="PATH=/var/www/spinify-ads/venv/bin"
ExecStart=/var/www/spinify-ads/venv/bin/uvicorn backend.main:app --host 127.0.0.1 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable spinify-ads
sudo systemctl start spinify-ads
sudo systemctl status spinify-ads
```

### 5. Configure Nginx

```bash
sudo nano /etc/nginx/sites-available/spinify-ads
```

Paste this configuration:
```nginx
server {
    listen 80;
    server_name cinetimetv.store www.cinetimetv.store;

    # Frontend - Serve static files
    location / {
        root /var/www/spinify-ads/webapp;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    # Backend API - Reverse proxy
    location /api {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Static assets caching
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        root /var/www/spinify-ads/webapp;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

Enable the site:
```bash
# Create symbolic link
sudo ln -s /etc/nginx/sites-available/spinify-ads /etc/nginx/sites-enabled/

# Remove default site
sudo rm /etc/nginx/sites-enabled/default

# Test configuration
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx
```

### 6. Setup SSL Certificate (HTTPS)

```bash
# Install Certbot if not already installed
sudo apt install certbot python3-certbot-nginx

# Get SSL certificate for cinetimetv.store
sudo certbot --nginx -d cinetimetv.store -d www.cinetimetv.store

# Follow the prompts:
# - Enter email for urgent renewal notices
# - Agree to terms of service (Y)
# - Redirect HTTP to HTTPS (recommended: 2)
```

Certbot will automatically:
- Get SSL certificate from Let's Encrypt
- Configure Nginx for HTTPS
- Setup auto-renewal

### 7. Update Frontend Configuration

```bash
nano /var/www/spinify-ads/webapp/app.js
```

Change:
```javascript
const CONFIG = {
  API_BASE_URL: 'https://cinetimetv.store/api',  // Updated
  MAX_GROUPS: 10,
  MIN_INTERVAL_MINUTES: 20,
  GROUP_DELAY_SECONDS: 60,
  MESSAGE_DELAY_SECONDS: 60,
  OTP_LENGTH: 6,
  TOAST_DURATION: 3000,
};
```

### 8. Setup Firewall

```bash
# Enable firewall
sudo ufw allow 22/tcp      # SSH
sudo ufw allow 80/tcp      # HTTP
sudo ufw allow 443/tcp     # HTTPS
sudo ufw enable
```

## ✅ Verify Everything Works

### Check Services
```bash
# Backend service
sudo systemctl status spinify-ads

# Nginx
sudo systemctl status nginx

# View logs
sudo journalctl -u spinify-ads -f
```

### Test URLs

1. **Frontend**: https://cinetimetv.store
2. **With www**: https://www.cinetimetv.store
3. **Backend API**: https://cinetimetv.store/api/docs (if FastAPI docs enabled)

## 🔄 Update Your App

When you push changes to GitHub:

```bash
cd /var/www/spinify-ads
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart spinify-ads
sudo systemctl restart nginx
```

## 📊 Monitoring

### View Logs
```bash
# Backend logs (real-time)
sudo journalctl -u spinify-ads -f

# Nginx access logs
sudo tail -f /var/log/nginx/access.log

# Nginx error logs
sudo tail -f /var/log/nginx/error.log
```

### Check SSL Certificate
```bash
sudo certbot certificates
```

### Auto-renewal Test
```bash
sudo certbot renew --dry-run
```

## 🐛 Troubleshooting

### Site Not Loading?

1. **Check DNS:**
   ```bash
   dig cinetimetv.store
   ping cinetimetv.store
   ```

2. **Check Nginx:**
   ```bash
   sudo nginx -t
   sudo systemctl status nginx
   ```

3. **Check Backend:**
   ```bash
   sudo systemctl status spinify-ads
   sudo journalctl -u spinify-ads -n 50
   ```

### SSL Issues?

```bash
# Check certificate status
sudo certbot certificates

# Renew manually
sudo certbot renew

# Force renewal
sudo certbot renew --force-renewal
```

### Backend Not Working?

```bash
# Check if backend is running
sudo systemctl status spinify-ads

# Restart it
sudo systemctl restart spinify-ads

# Check logs
sudo journalctl -u spinify-ads -f
```

## 🔒 Security Recommendations

1. **Disable root login:**
   ```bash
   sudo nano /etc/ssh/sshd_config
   # Set: PermitRootLogin no
   sudo systemctl restart sshd
   ```

2. **Install Fail2Ban:**
   ```bash
   sudo apt install fail2ban
   sudo systemctl enable fail2ban
   ```

3. **Regular updates:**
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

## 📌 Quick Commands Reference

```bash
# Restart backend
sudo systemctl restart spinify-ads

# Restart Nginx
sudo systemctl restart nginx

# View backend logs
sudo journalctl -u spinify-ads -f

# Update app
cd /var/www/spinify-ads && git pull && sudo systemctl restart spinify-ads

# Check SSL
sudo certbot certificates

# Renew SSL
sudo certbot renew
```

---

## 🎉 Your App is Live!

**Frontend**: https://cinetimetv.store  
**Backend API**: https://cinetimetv.store/api

**Next Steps:**
1. Test all features on the live site
2. Configure Google Analytics (optional)
3. Setup monitoring/alerting
4. Regular backups

Need help? Check the logs or refer to [DEPLOYMENT.md](DEPLOYMENT.md) for more details.
