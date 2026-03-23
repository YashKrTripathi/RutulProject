@echo off
REM Start both Flask backend and Streamlit frontend on Windows
echo.
echo ============================================================
echo Start YouTube Thumbnail Board - Click on the terminal window
echo ============================================================
echo.

cd /d "%~dp0"
python run_app.py

pause
