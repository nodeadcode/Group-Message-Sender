#!/bin/bash

# ============================================
# Spinify Ads - VPS Deployment Script
# Automated setup for Ubuntu/Debian servers
# ============================================

set -e  # Exit on any error

echo "🚀 Starting Spinify Ads VPS Deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
APP_NAME="spinify-ads"
APP_DIR="/var/www/$APP_NAME"
DOMAIN="your-domain.com"  # Change this to your domain
BACKEND_PORT=8000

echo -e "${GREEN}📦 Step 1: Installing system dependencies...${NC}"
sudo apt update
sudo apt install -y python3 python3-pip python3-venv nginx git certbot python3-certbot-nginx

echo -e "${GREEN}📂 Step 2: Creating application directory...${NC}"
sudo mkdir -p $APP_DIR
sudo chown -R $USER:$USER $APP_DIR

echo -e "${GREEN}📥 Step 3: Cloning repository...${NC}"
if [ -d "$APP_DIR/.git" ]; then
    echo "Repository already exists, pulling latest changes..."
    cd $APP_DIR
    git pull origin main
else
    git clone https://github.com/yourusername/Group-Message-Sender.git $APP_DIR
fi

cd $APP_DIR

echo -e "${GREEN}🐍 Step 4: Creating Python virtual environment...${NC}"
python3 -m venv venv
source venv/bin/activate

echo -e "${GREEN}📚 Step 5: Installing Python dependencies...${NC}"
pip install --upgrade pip
pip install -r requirements.txt

echo -e "${GREEN}⚙️  Step 6: Creating systemd service...${NC}"
sudo tee /etc/systemd/system/$APP_NAME.service > /dev/null <<EOF
[Unit]
Description=Spinify Ads - Telegram Ad Scheduler
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$APP_DIR
Environment="PATH=$APP_DIR/venv/bin"
ExecStart=$APP_DIR/venv/bin/uvicorn backend.main:app --host 127.0.0.1 --port $BACKEND_PORT
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

echo -e "${GREEN}🌐 Step 7: Configuring Nginx...${NC}"
sudo tee /etc/nginx/sites-available/$APP_NAME > /dev/null <<EOF
server {
    listen 80;
    server_name $DOMAIN www.$DOMAIN;

    # Frontend
    location / {
        root $APP_DIR/webapp;
        index index.html;
        try_files \$uri \$uri/ /index.html;
    }

    # Backend API
    location /api {
        proxy_pass http://127.0.0.1:$BACKEND_PORT;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    # Static files
    location /static {
        alias $APP_DIR/webapp;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
EOF

# Enable site
sudo ln -sf /etc/nginx/sites-available/$APP_NAME /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

echo -e "${GREEN}🔄 Step 8: Starting services...${NC}"
sudo systemctl daemon-reload
sudo systemctl enable $APP_NAME
sudo systemctl start $APP_NAME
sudo systemctl restart nginx

echo -e "${GREEN}🔒 Step 9: Setting up SSL with Let's Encrypt...${NC}"
echo -e "${YELLOW}NOTE: Make sure your domain DNS is pointing to this server!${NC}"
read -p "Do you want to setup SSL now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    sudo certbot --nginx -d $DOMAIN -d www.$DOMAIN --non-interactive --agree-tos --email admin@$DOMAIN
fi

echo -e "${GREEN}✅ Deployment complete!${NC}"
echo ""
echo "================================================"
echo "🎉 Spinify Ads is now live!"
echo "================================================"
echo "📱 Frontend: http://$DOMAIN"
echo "🔌 Backend API: http://$DOMAIN/api"
echo ""
echo "📝 Useful commands:"
echo "  - View logs: sudo journalctl -u $APP_NAME -f"
echo "  - Restart app: sudo systemctl restart $APP_NAME"
echo "  - Check status: sudo systemctl status $APP_NAME"
echo "  - Update app: cd $APP_DIR && git pull && sudo systemctl restart $APP_NAME"
echo ""
echo "🔐 Don't forget to:"
echo "  1. Update app.js API_BASE_URL to: https://$DOMAIN/api"
echo "  2. Configure environment variables if needed"
echo "  3. Set up database (if using one)"
echo "================================================"
