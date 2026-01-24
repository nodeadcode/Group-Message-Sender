@echo off
echo ================================================
echo  Spinify Ads - Windows Startup Script
echo ================================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Error: Virtual environment not found!
    echo Run setup.bat first
    pause
    exit /b 1
)

REM Check if .env exists
if not exist ".env" (
    echo Error: .env file not found!
    echo Create .env file with BOT_TOKEN, OWNER_TELEGRAM_ID, JWT_SECRET
    pause
    exit /b 1
)

REM Stop any existing instances
echo [1/3] Stopping existing instances...
taskkill /F /FI "WINDOWTITLE eq Spinify Bot*" 2>nul
taskkill /F /FI "WINDOWTITLE eq Spinify Backend*" 2>nul
timeout /t 2 >nul

REM Start Bot in new window
echo [2/3] Starting Telegram Bot...
start "Spinify Bot" cmd /k "cd /d %~dp0 && call venv\Scripts\activate && python bot\bot.py"
timeout /t 2 >nul

REM Start Backend in new window  
echo [3/3] Starting Backend API...
start "Spinify Backend" cmd /k "cd /d %~dp0backend && call ..\venv\Scripts\activate && uvicorn main:app --host 0.0.0.0 --port 8000 --reload"
timeout /t 2 >nul

echo.
echo ================================================
echo.
echo [32m✓ All services started![0m
echo.
echo 📝 Two windows should have opened:
echo   • Spinify Bot - Telegram Bot
echo   • Spinify Backend - FastAPI Server
echo.
echo 🌐 Access Points:
echo   • Backend API: http://localhost:8000
echo   • API Docs:    http://localhost:8000/docs
echo   • WebApp:      Open webapp\index.html
echo.
echo 💡 To stop: Close the terminal windows or run stop.bat
echo.
pause
