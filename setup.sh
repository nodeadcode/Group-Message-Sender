#!/bin/bash

echo "==============================================="
echo " Spinify Ads - Complete Setup Script"
echo "==============================================="
echo ""

# Check Python
echo "[1/6] Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8+ first"
    exit 1
fi
python3 --version
echo ""

# Create virtual environment
echo "[2/6] Creating virtual environment..."
if [ -d "venv" ]; then
    echo "Virtual environment already exists, skipping..."
else
    python3 -m venv venv
    echo "Virtual environment created!"
fi
echo ""

# Activate and install dependencies
echo "[3/6] Installing dependencies..."
source venv/bin/activate
pip install -r requirements.txt
echo ""

# Check .env file  
echo "[4/6] Checking configuration..."
if [ ! -f ".env" ]; then
    echo "WARNING: .env file not found!"
    echo "Creating from .env.example..."
    cp .env.example .env
    echo ""
    echo "IMPORTANT: Edit .env and set your OWNER_TELEGRAM_ID"
    echo "           Get your ID from @userinfobot on Telegram"
    echo ""
fi
echo "Configuration file: .env"
echo ""

# Initialize database
echo "[5/6] Initializing database..."
cd backend
python init_db.py
if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: Database initialization failed"
    echo "Please check the error message above"
    cd ..
    exit 1
fi
cd ..
echo ""

# Run tests
echo "[6/6] Running system tests..."
cd backend
python test_system.py
cd ..
echo ""

echo "==============================================="
echo " Setup Complete!"
echo "==============================================="
echo ""
echo "Next steps:"
echo "  1. Edit .env and set your OWNER_TELEGRAM_ID"
echo "  2. Run these commands in separate terminals:"
echo ""
echo "     Terminal 1: cd bot && source ../venv/bin/activate && python bot.py"
echo "     Terminal 2: cd backend && source ../venv/bin/activate && uvicorn main:app --reload"
echo "     Terminal 3: source venv/bin/activate && python -m http.server 8080 --directory webapp"
echo ""
echo "  3. Open http://localhost:8080 in your browser"
echo ""
