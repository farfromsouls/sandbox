@echo off
cd /d "%~dp0"
cls

if not exist "venv\Scripts\python.exe" (
    echo Creating virtual environment...
    python -m venv venv
    echo Installing dependencies...
    call venv\Scripts\pip install -r requirements.txt
)

echo Starting main script...
call venv\Scripts\activate.bat
python main.py
pause