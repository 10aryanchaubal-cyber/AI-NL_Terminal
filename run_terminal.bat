@echo off
title NL-Terminal Debug Mode
echo STARTING NL-TERMINAL (DEBUG MODE)
echo ---------------------------------------------------

:: Ensure we are running from the script's directory
cd /d "%~dp0"

echo [DEBUG] Script is located at: %~dp0
echo [DEBUG] Current working directory: %cd%

if not exist main.py (
    echo.
    echo [ERROR] 'main.py' not found in this directory!
    echo.
    echo It looks like you might have moved this batch file to the Desktop.
    echo Please make sure 'run_terminal.bat' is inside the 'nl-terminal - v2' folder.
    echo.
    echo Attempting to find the project folder...
    if exist "nl-terminal - v2\main.py" (
        cd "nl-terminal - v2"
        echo [INFO] Found project folder. Switching directory...
    ) else (
        echo [FATAL] Could not find the project files.
        pause
        exit /b
    )
)

echo [INFO] Checking Python version...
python --version
if %errorlevel% neq 0 (
    echo [ERROR] Python is not found in PATH!
    echo Please install Python and check "Add Python to PATH" during installation.
    pause
    exit /b
)

echo [INFO] Checking dependencies...
if exist requirements.txt (
    python -m pip install -r requirements.txt
) else (
    echo [WARNING] requirements.txt not found. Skipping dependency check.
)

echo.
echo [INFO] Launching Application...
echo ---------------------------------------------------
python main.py
if %errorlevel% neq 0 (
    echo.
    echo ---------------------------------------------------
    echo [CRITICAL] The application crashed with error code %errorlevel%.
    echo See the traceback above for details.
) else (
    echo.
    echo [INFO] Application exited normally.
)

echo.
pause
