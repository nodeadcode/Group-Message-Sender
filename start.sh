#!/bin/bash

echo "================================================"
echo " Spinify Ads - Startup Script"
echo "================================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${RED}Error: Virtual environment not found!${NC}"
    echo "Run ./setup.sh first"
    exit 1
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo -e "${RED}Error: .env file not found!${NC}"
    echo "Copy .env.example to .env and configure it"
    exit 1
fi

# Stop any existing instances
echo -e "${BLUE}[1/4] Stopping existing instances...${NC}"
pkill -f "python bot/bot.py" 2>/dev/null
pkill -f "uvicorn main:app" 2>/dev/null
sleep 2

# Start Bot in screen
echo -e "${BLUE}[2/4] Starting Telegram Bot...${NC}"
screen -dmS spinify-bot bash -c "cd $(pwd) && source venv/bin/activate && python bot/bot.py"
sleep 2

# Check if bot started
if screen -list | grep -q "spinify-bot"; then
    echo -e "${GREEN}✓ Bot started successfully${NC}"
else
    echo -e "${RED}✗ Bot failed to start${NC}"
fi

# Start Backend in screen
echo -e "${BLUE}[3/4] Starting Backend API...${NC}"
screen -dmS spinify-backend bash -c "cd $(pwd)/backend && source ../venv/bin/activate && uvicorn main:app --host 0.0.0.0 --port 8000 --reload"
sleep 2

# Check if backend started
if screen -list | grep -q "spinify-backend"; then
    echo -e "${GREEN}✓ Backend started successfully${NC}"
else
    echo -e "${RED}✗ Backend failed to start${NC}"
fi

# Show status
echo ""
echo -e "${BLUE}[4/4] Status Check${NC}"
echo "================================================"
screen -list
echo "================================================"
echo ""
echo -e "${GREEN}✓ All services started!${NC}"
echo ""
echo "📝 Useful Commands:"
echo "  • View bot logs:     screen -r spinify-bot"
echo "  • View backend logs: screen -r spinify-backend"
echo "  • Detach screen:     Ctrl+A then D"
echo "  • Stop all:          ./stop.sh"
echo ""
echo "🌐 Access Points:"
echo "  • Backend API: http://$(hostname -I | awk '{print $1}'):8000"
echo "  • API Docs:    http://$(hostname -I | awk '{print $1}'):8000/docs"
echo "  • WebApp:      https://cinetimetv.store/webapp"
echo ""
