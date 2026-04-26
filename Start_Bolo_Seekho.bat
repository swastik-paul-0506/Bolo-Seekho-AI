@echo off
title Bolo Seekho AI Starter

:: This line makes the script work relative to where it is saved
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

echo [1] Starting Ollama Service...
:: This starts it silently in the background
start "" "ollama" serve

echo [2] Starting Django Backend...
:: Using the absolute path to your Django folder
start "DjangoServer" /d "C:\Users\SWASTIK\bolo_seekho_backend" cmd /k "python manage.py runserver"

echo ⏳ Waiting 12 seconds for systems to sync...
timeout /t 12 /nobreak

echo [3] Opening your Website...
:: This opens the index.html that is sitting right next to this .bat file
start "" "%SCRIPT_DIR%index.html"

echo.
echo ✅ ALL SYSTEMS GO!
echo You can minimize this window now.
pause