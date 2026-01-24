#!/bin/bash

echo "================================================"
echo " Spinify Ads - Stop Script"
echo "================================================"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

# Kill bot process
echo "Stopping Telegram Bot..."
pkill -f "python bot/bot.py"
screen -S spinify-bot -X quit 2>/dev/null

# Kill backend process
echo "Stopping Backend API..."
pkill -f "uvicorn main:app"
screen -S spinify-backend -X quit 2>/dev/null

sleep 2

# Verify processes are stopped
if pgrep -f "python bot/bot.py" > /dev/null || pgrep -f "uvicorn main:app" > /dev/null; then
    echo -e "${RED}✗ Some processes may still be running${NC}"
    echo "Use: ps aux | grep -E 'bot.py|uvicorn' to check"
else
    echo -e "${GREEN}✓ All services stopped successfully${NC}"
fi

echo ""
