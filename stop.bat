@echo off
echo ================================================
echo  Spinify Ads - Windows Stop Script
echo ================================================
echo.

echo Stopping all Spinify services...

REM Kill bot windows
taskkill /F /FI "WINDOWTITLE eq Spinify Bot*" 2>nul

REM Kill backend windows
taskkill /F /FI "WINDOWTITLE eq Spinify Backend*" 2>nul

REM Kill any remaining Python processes for this app
taskkill /F /IM python.exe /FI "WINDOWTITLE eq Spinify*" 2>nul

timeout /t 2 >nul

echo.
echo [32m✓ All services stopped[0m
echo.
pause
