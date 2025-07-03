@echo off
REM Batch file to activate Python virtual environment in .venv.
REM If .venv does not exist, this script will attempt to create it.
REM This script launches PowerShell, sets the execution policy
REM to Bypass for the current session only, then activates the venv.
REM 
REM This script should be run from the project root directory.
REM If called from scripts/ directory, it will navigate to parent directory.

REM Get the directory where this script is located
SET SCRIPT_DIR=%~dp0

REM If script is in scripts/ subdirectory, navigate to parent (project root)
IF EXIST "%SCRIPT_DIR%\..\src" (
    cd /d "%SCRIPT_DIR%\.."
    echo INFO: Navigated to project root directory from scripts/
) ELSE (
    REM Already in project root
    cd /d "%SCRIPT_DIR%"
)

echo Starting PowerShell to activate or create+activate virtual environment...
echo Project Root: %CD%
echo Target venv directory: %CD%\.venv
echo Target venv activation script: %CD%\.venv\Scripts\activate.ps1
echo.

REM Check if the activate.ps1 script (indicator of an existing venv) exists
IF NOT EXIST ".\.venv\Scripts\activate.ps1" (
    echo INFO: Virtual environment activation script not found at ".\.venv\Scripts\activate.ps1".
    echo INFO: Attempting to create a new virtual environment in '.\.venv\'...
    echo.
    python -m venv .venv
    
    REM Check if the python command itself failed (e.g., python not found, venv module issue)
    IF ERRORLEVEL 1 (
        echo.
        echo ERROR: Failed to execute 'python -m venv .venv'.
        echo Please ensure Python is installed, added to your PATH, and the 'venv' module is available.
        pause
        goto :eof
    )
    
    REM Verify creation by checking for the activation script again
    IF NOT EXIST ".\.venv\Scripts\activate.ps1" (
        echo.
        echo ERROR: Virtual environment creation command 'python -m venv .venv' seemed to run, 
        echo but the activation script ".\.venv\Scripts\activate.ps1" is still missing.
        echo This might indicate an issue with your Python installation or the 'venv' module.
        pause
        goto :eof
    )
    echo.
    echo INFO: Virtual environment created successfully in '.\.venv\'.
) ELSE (
    echo INFO: Existing virtual environment found in '.\.venv\'.
)

echo.
echo Launching PowerShell to activate the virtual environment...
echo.

REM Launch PowerShell, set execution policy for this session, activate venv, and set window title.
REM THE FOLLOWING 'powershell.exe' COMMAND MUST BE ON A SINGLE LINE IN YOUR .BAT FILE
powershell.exe -NoProfile -NoExit -ExecutionPolicy Bypass -Command "& {Write-Host 'Attempting to activate virtual environment...'; $ScriptPath = '.\.venv\Scripts\activate.ps1'; if (Test-Path $ScriptPath) { & $ScriptPath; $newTitle = 'VENV Activated: ' + (Get-Location).Path; $Host.UI.RawUI.WindowTitle = $newTitle; Write-Host -ForegroundColor Green 'Virtual environment activated successfully.'; Write-Host -ForegroundColor Green ('Window title set to: ' + $newTitle); Write-Host 'You are now in the virtual environment.'; Write-Host 'Type ''exit'' to close this PowerShell session and return to CMD.'; } else { Write-Host -ForegroundColor Red ('ERROR: Activation script not found at ' + $ScriptPath + ' inside PowerShell.'); Write-Host -ForegroundColor Red 'This should not happen if the pre-checks in the batch script passed.'; Read-Host 'Press Enter to exit PowerShell'; } }"

REM Install dependencies from requirements.txt
IF EXIST "requirements.txt" (
    echo INFO: Installing dependencies from requirements.txt...
    .\.venv\Scripts\pip install -r requirements.txt
    IF ERRORLEVEL 1 (
        echo.
        echo ERROR: Failed to install dependencies from requirements.txt.
        echo Please ensure pip is installed and requirements.txt is valid.
        pause
        goto :eof
    )
    echo INFO: Dependencies installed successfully.
) ELSE (
    echo WARNING: requirements.txt not found. Skipping dependency installation.
)

echo.
echo PowerShell window has been launched.
echo If the window closed immediately or showed an error, the activation might have failed.
echo If successful, the PowerShell window title will indicate the activated venv path.

:eof
