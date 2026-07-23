@echo off
setlocal
cd /d "%~dp0"

if exist ".venv311\Scripts\python.exe" (
    ".venv311\Scripts\python.exe" "cv_rating_app.py"
) else (
    echo.
    echo Could not find the Python 3.11 virtual environment.
    echo Please create it first with:
    echo   py -3.11 -m venv .venv311
    echo   .venv311\Scripts\python.exe -m pip install -r requirements.txt
    echo.
    pause
)
