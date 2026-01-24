@echo off
echo ===============================================
echo  Spinify Ads - Complete Setup Script
echo ===============================================
echo.

REM Check Python
echo [1/6] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from python.org
    pause
    exit /b 1
)
python --version
echo.

REM Create virtual environment
echo [2/6] Creating virtual environment...
if exist venv (
    echo Virtual environment already exists, skipping...
) else (
    python -m venv venv
    echo Virtual environment created!
)
echo.

REM Activate and install dependencies
echo [3/6] Installing dependencies...
call venv\Scripts\activate.bat
pip install -r requirements.txt
echo.

REM Check .env file
echo [4/6] Checking configuration...
if not exist .env (
    echo WARNING: .env file not found!
    echo.
    echo IMPORTANT: Create .env file with required variables:
    echo   - BOT_TOKEN
    echo   - OWNER_TELEGRAM_ID
    echo   - JWT_SECRET
    echo.
    echo Cannot proceed without .env file.
    pause
    exit /b 1
)
echo Configuration file: .env
echo.

REM Initialize database
echo [5/6] Initializing database...
cd backend
python init_db.py
if errorlevel 1 (
    echo.
    echo ERROR: Database initialization failed
    echo Please check the error message above
    cd ..
    pause
    exit /b 1
)
cd ..
echo.

REM Run tests
echo [6/6] Running system tests...
cd backend
python test_system.py
cd ..
echo.

echo ===============================================
echo  Setup Complete!
echo ===============================================
echo.
echo Next steps:
echo   1. Edit .env and set your OWNER_TELEGRAM_ID
echo   2. Run these commands in separate terminals:
echo.
echo      Terminal 1: cd bot ^& venv\Scripts\activate ^& python bot.py
echo      Terminal 2: cd backend ^& venv\Scripts\activate ^& uvicorn main:app --reload
echo      Terminal 3: venv\Scripts\activate ^& python -m http.server 8080 --directory webapp
echo.
echo   3. Open http://localhost:8080 in your browser
echo.
pause
