# VPS Deployment Guide - Spinify Ads

Complete guide for deploying Spinify Ads on your VPS server.

## 📋 Prerequisites

- Ubuntu 20.04+ or Debian 11+ VPS
- Root or sudo access
- Domain name (optional but recommended)
- Minimum 1GB RAM, 1 CPU core

## 🚀 Quick Deploy (Automated)

### Option 1: One-Line Deploy

```bash
curl -fsSL https://raw.githubusercontent.com/yourusername/Group-Message-Sender/main/deploy-vps.sh | bash
```

### Option 2: Manual Deploy

1. **Upload the deployment script:**
```bash
scp deploy-vps.sh root@your-vps-ip:/root/
```

2. **SSH into your VPS:**
```bash
ssh root@your-vps-ip
```

3. **Run the deployment script:**
```bash
chmod +x /root/deploy-vps.sh
/root/deploy-vps.sh
```

4. **Follow the prompts**

## ⚙️ Manual Setup (Step by Step)

If you prefer manual control:

### 1. Update System
```bash
sudo apt update && sudo apt upgrade -y
```

### 2. Install Dependencies
```bash
sudo apt install -y python3 python3-pip python3-venv nginx git
```

### 3. Clone Repository
```bash
sudo mkdir -p /var/www/spinify-ads
cd /var/www/spinify-ads
git clone https://github.com/yourusername/Group-Message-Sender.git .
```

### 4. Setup Python Environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 5. Create Systemd Service
```bash
sudo nano /etc/systemd/system/spinify-ads.service
```

Paste this configuration:
```ini
[Unit]
Description=Spinify Ads Backend
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
```

### 6. Configure Nginx
```bash
sudo nano /etc/nginx/sites-available/spinify-ads
```

Paste this configuration:
```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    # Frontend
    location / {
        root /var/www/spinify-ads/webapp;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/spinify-ads /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx
```

### 7. Setup SSL (HTTPS)
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

## 🔧 Configuration

### Update Frontend API URL
Edit `webapp/app.js`:
```javascript
const CONFIG = {
  API_BASE_URL: 'https://your-domain.com/api',
  // ... rest
};
```

### Environment Variables (Optional)
```bash
sudo nano /etc/systemd/system/spinify-ads.service
```

Add under `[Service]`:
```ini
Environment="DATABASE_URL=postgresql://..."
Environment="SECRET_KEY=your-secret-key"
```

## 📊 Monitoring & Maintenance

### View Logs
```bash
# Backend logs
sudo journalctl -u spinify-ads -f

# Nginx access logs
sudo tail -f /var/log/nginx/access.log

# Nginx error logs
sudo tail -f /var/log/nginx/error.log
```

### Check Status
```bash
# Backend status
sudo systemctl status spinify-ads

# Nginx status
sudo systemctl status nginx
```

### Restart Services
```bash
# Restart backend
sudo systemctl restart spinify-ads

# Restart Nginx
sudo systemctl restart nginx
```

### Update Application
```bash
cd /var/www/spinify-ads
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart spinify-ads
```

## 🔒 Security Hardening

### 1. Setup Firewall
```bash
sudo ufw allow 22    # SSH
sudo ufw allow 80    # HTTP
sudo ufw allow 443   # HTTPS
sudo ufw enable
```

### 2. Disable Root Login
```bash
sudo nano /etc/ssh/sshd_config
# Set: PermitRootLogin no
sudo systemctl restart sshd
```

### 3. Setup Fail2Ban
```bash
sudo apt install fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

### 4. Regular Updates
```bash
# Create auto-update script
sudo nano /etc/cron.daily/update-spinify

#!/bin/bash
cd /var/www/spinify-ads
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart spinify-ads
```

Make it executable:
```bash
sudo chmod +x /etc/cron.daily/update-spinify
```

## 🐛 Troubleshooting

### Backend Not Starting
```bash
# Check logs
sudo journalctl -u spinify-ads -n 50

# Check if port is in use
sudo netstat -tulpn | grep 8000

# Restart service
sudo systemctl restart spinify-ads
```

### Nginx Errors
```bash
# Test configuration
sudo nginx -t

# Check error logs
sudo tail -f /var/log/nginx/error.log
```

### Permission Issues
```bash
# Fix ownership
sudo chown -R www-data:www-data /var/www/spinify-ads/webapp
sudo chmod -R 755 /var/www/spinify-ads/webapp
```

## 📈 Performance Optimization

### Enable Gzip Compression
Add to Nginx config:
```nginx
gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_types text/plain text/css text/xml text/javascript application/javascript application/json;
```

### Enable Caching
```nginx
location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

### Use Process Manager
Consider using PM2 or supervisor for better process management.

## 🔄 CI/CD (Auto-Deploy from GitHub)

Setup webhook for automatic deployments:

```bash
# Install webhook
sudo apt install webhook

# Create webhook script
sudo nano /var/scripts/deploy-spinify.sh

#!/bin/bash
cd /var/www/spinify-ads
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart spinify-ads
```

## 📞 Support

If you encounter issues:
1. Check logs: `sudo journalctl -u spinify-ads -f`
2. Verify Nginx config: `sudo nginx -t`
3. Check firewall: `sudo ufw status`
4. Review GitHub issues

---

**Your app should now be live at: `https://your-domain.com` 🎉**
