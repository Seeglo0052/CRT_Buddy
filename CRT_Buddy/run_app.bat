@echo off
REM CRT Buddy launcher script - avoids long path typing issues & PSReadLine glitches
SETLOCAL ENABLEDELAYEDEXPANSION

REM Move to script directory
cd /d "%~dp0"

REM If a virtual environment exists (.venv), activate it
IF EXIST .venv\Scripts\activate.bat (
  call .venv\Scripts\activate.bat
)

REM Show Python version
python --version || goto :error

ECHO =============================================
ECHO Launching CRT Buddy...
ECHO =============================================

python CRT_Buddy.py
IF ERRORLEVEL 1 goto :error

ECHO.
ECHO CRT Buddy exited. Press any key to close.
pause >nul
EXIT /b 0

:error
ECHO.
ECHO [ERROR] Failed to start CRT Buddy.
ECHO Ensure dependencies installed: PyQt6 Pillow numpy opencv-python pygame pywin32 requests
ECHO Run: python -m pip install PyQt6 Pillow numpy opencv-python pygame pywin32 requests
pause
EXIT /b 1
