@echo off
echo ============================================================
echo Restarting Instagram Scraper Server
echo ============================================================
echo.

echo Stopping any running Python servers...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq *server.py*" 2>nul
timeout /t 2 /nobreak >nul

echo.
echo Starting Python backend server...
echo.
echo ============================================================
echo.

cd /d "%~dp0"
python server.py

pause
