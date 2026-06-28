@echo off
echo Starting Beds24-AirBnB Sync...

cd /d "%~dp0"

:: Start the sync server
start /min "Beds24Sync" python auto_update.py

:: Wait for server to be ready
timeout /t 10 /nobreak > nul

:: Start ngrok
start /min "Ngrok" ngrok http 8080

echo Started! Check ngrok dashboard at http://localhost:4040
