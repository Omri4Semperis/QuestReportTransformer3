@echo off
setlocal enabledelayedexpansion

:: =============================================================================
:: Git Diff File Generator (with Dynamic Directory Name) - v8 (Fixed Version)
::
:: Description:
::   This script interactively generates individual .diff files for each file
::   that has changed between two user-selected Git branches. It creates a
::   dynamically named directory (e.g., 'diff_main_vs_my-feature_20250618_143022') 
::   in the repository root to store these files, with detailed logging.
::
:: Usage:
::   1. Place this .bat file in the root directory of your Git repository.
::   2. Run the script by double-clicking it or executing it from the command line.
::   3. Follow the on-screen prompts.
:: =============================================================================

:: Initialize log file variable
set "LOG_FILE="

:: --- Main Script ---
:main
cls
echo.
echo  =========================================
echo   Git Individual Diff File Generator
echo  =========================================
echo.
echo  This script will save a separate .diff file for each changed
echo  file between two branches into a new directory.
echo.
echo.

:: --- Step 1: List Branches and Get User Selection ---
call :list_branches
if %errorlevel% neq 0 (
    echo.
    echo  ERROR: This does not appear to be a Git repository, or you don't have
    echo  any branches yet.
    echo.
    echo Press any key to exit...
    pause >nul
    goto :end
)

echo.
set /p "branch1_num= > Enter the number for the FIRST branch (e.g., the target, like 'main'): "
call :validate_input %branch1_num% %branch_count%
if %errorlevel% neq 0 goto :main

set /p "branch2_num= > Enter the number for the SECOND branch (e.g., your feature branch): "
call :validate_input %branch2_num% %branch_count%
if %errorlevel% neq 0 goto :main

if "%branch1_num%"=="%branch2_num%" (
    echo.
    echo  ERROR: You selected the same branch twice. Please try again.
    pause
    goto :main
)

:: --- Step 2: Set Dynamic Names with Timestamp ---
set "branch1_name=!branches[%branch1_num%]!"
set "branch2_name=!branches[%branch2_num%]!"

:: Get current timestamp using the corrected method
call :get_timestamp

:: Create the dynamic directory name from the selected branches with timestamp
set "DIFF_DIR=diff_!branch1_name!_vs_!branch2_name!_!timestamp!"

cls
echo.
echo  =========================================
echo             Action Summary
echo  =========================================
echo.
echo  The script will perform the following actions:
echo.
echo    1. Create a directory named '!DIFF_DIR!'.
echo    2. Find all file differences between:
echo       - Branch 1: !branch1_name!
echo       - Branch 2: !branch2_name!
echo    3. Save each change as a separate '.diff' file inside '!DIFF_DIR!' (flat structure).
echo    4. Create a detailed log file inside the directory.
echo.
echo  -----------------------------------------
echo.
set /p "confirm=Are you sure you want to proceed? (Y/N): "
if /i not "%confirm%"=="Y" (
    echo.
    echo  Operation cancelled by user.
    echo.
    echo Press any key to exit...
    pause >nul
    goto :end
)

:: --- Step 3: Execute Diff ---
echo.
echo  Preparing to create diffs...
echo.

:: Clean up old directory if it exists
if exist "!DIFF_DIR!\" (
    echo  Removing existing '!DIFF_DIR!' directory...
    echo [DEBUG] Removing existing directory: !DIFF_DIR!
    rmdir /s /q "!DIFF_DIR!"
    if exist "!DIFF_DIR!\" (
        echo  ERROR: Failed to remove existing directory
        echo [DEBUG] ERROR: Failed to remove existing directory
        echo.
        echo Press any key to exit...
        pause >nul
        goto :end
    ) else (
        echo [DEBUG] Successfully removed existing directory
    )
)

:: Create fresh directory
echo  Creating new '!DIFF_DIR!' directory...
mkdir "!DIFF_DIR!"
if not exist "!DIFF_DIR!\" (
    echo  ERROR: Failed to create directory '!DIFF_DIR!'
    echo [DEBUG] FATAL ERROR: Failed to create directory !DIFF_DIR!
    echo.
    echo Press any key to exit...
    pause >nul
    goto :end
) else (
    echo [DEBUG] Successfully created directory: !DIFF_DIR!
)

:: Initialize the log file now that directory exists
set "LOG_FILE=!DIFF_DIR!\_operation_log.txt"
echo === Git Diff Generator Log === > "!LOG_FILE!"
echo Timestamp: !timestamp! >> "!LOG_FILE!"
echo Branch 1: !branch1_name! >> "!LOG_FILE!"
echo Branch 2: !branch2_name! >> "!LOG_FILE!"
echo Output Directory: !DIFF_DIR! >> "!LOG_FILE!"
echo Current Working Directory: %CD% >> "!LOG_FILE!"
echo. >> "!LOG_FILE!"
echo === Starting diff generation process === >> "!LOG_FILE!"
echo. >> "!LOG_FILE!"

:: Check if git is available and we're in a git repo
echo [DEBUG] Checking git availability and repository status...
call :log "Checking git availability and repository status..."
git --version >nul 2>&1
if %errorlevel% neq 0 (
    call :log "ERROR: Git is not available or not in PATH"
    echo [DEBUG] ERROR: Git is not available or not in PATH
    echo  ERROR: Git is not available
    goto :end
)
call :log "Git is available"
echo [DEBUG] Git is available

git rev-parse --git-dir >nul 2>&1
if %errorlevel% neq 0 (
    call :log "ERROR: Current directory is not a git repository"
    echo  ERROR: Not in a git repository
    goto :end
)
call :log "Confirmed we are in a git repository"

:: Verify branches exist
call :log "Verifying branches exist..."
git rev-parse --verify !branch1_name! >nul 2>&1
if %errorlevel% neq 0 (
    call :log "ERROR: Branch '!branch1_name!' does not exist"
    echo  ERROR: Branch '!branch1_name!' does not exist
    goto :end
)
call :log "Branch '!branch1_name!' verified"

git rev-parse --verify !branch2_name! >nul 2>&1
if %errorlevel% neq 0 (
    call :log "ERROR: Branch '!branch2_name!' does not exist"
    echo  ERROR: Branch '!branch2_name!' does not exist
    goto :end
)
call :log "Branch '!branch2_name!' verified"

echo  Generating diff files...
echo.
set "file_count=0"
set "success_count=0"

call :log "Getting list of changed files..."
call :log "Command: git diff --name-only !branch1_name! !branch2_name!"

:: First, let's see what files git finds
git diff --name-only !branch1_name! !branch2_name! > "!DIFF_DIR!\_changed_files_list.txt" 2>&1
if %errorlevel% neq 0 (
    call :log "ERROR: Failed to get list of changed files"
    echo  ERROR: Failed to get list of changed files
    goto :end
)

:: Check if there are any changed files
for /f %%i in ("!DIFF_DIR!\_changed_files_list.txt") do set "listSize=%%~zi"
if %listSize% equ 0 (
    call :log "No files changed between branches"
    echo  No files changed between the selected branches.
    goto :success_end
)

call :log "Found changed files (saved to _changed_files_list.txt)"
call :log "Processing each changed file..."
call :log ""

for /f "usebackq tokens=*" %%F in ("!DIFF_DIR!\_changed_files_list.txt") do (
    set "filePath=%%F"
    call :log "--- Processing file: !filePath! ---"
    
    :: Create a flat filename by replacing path separators with underscores
    set "flatFileName=!filePath:/=_!"
    set "flatFileName=!flatFileName:\=_!"
    call :log "Flat filename: !flatFileName!"
    
    echo   - Creating diff for: !filePath!
    
    :: Generate the diff and capture any errors
    set "diffFile=!DIFF_DIR!\!flatFileName!.diff"
    call :log "Target diff file: !diffFile!"
    
    call :log "Executing git diff command..."
    call :log "Command: git diff --no-prefix !branch1_name! !branch2_name! -- \"!filePath!\""
    
    git diff --no-prefix !branch1_name! !branch2_name! -- "!filePath!" > "!diffFile!" 2>&1
    set "gitExitCode=!errorlevel!"
    call :log "Git diff exit code: !gitExitCode!"
    
    :: Check if the file was actually created and has content
    if exist "!diffFile!" (
        call :log "Diff file exists on filesystem"
        :: Check if file has content (not just empty)
        for %%I in ("!diffFile!") do set "fileSize=%%~zI"
        call :log "Diff file size: !fileSize! bytes"
        
        if !fileSize! gtr 0 (
            set /a success_count+=1
            call :log "SUCCESS: Diff file created successfully with content"
            echo     SUCCESS: Diff file created successfully
        ) else (
            call :log "WARNING: Diff file created but is empty"
            echo     WARNING: Diff file created but is empty
        )
    ) else (
        call :log "ERROR: Diff file does not exist after git diff command"
        echo     ERROR: Failed to create diff file
    )
    
    call :log "--- End processing file: !filePath! ---"
    call :log ""
    set /a file_count+=1
)

:success_end
echo.
echo  =========================================
if %success_count% equ %file_count% (
    echo                Success!
    call :log "=== OPERATION COMPLETED SUCCESSFULLY ==="
) else (
    echo              Partial Success
    call :log "=== OPERATION COMPLETED WITH ISSUES ==="
)
echo  =========================================
echo.
echo  Processed %file_count% files.
echo  Successfully created %success_count% diff files in the '!DIFF_DIR!' directory.
call :log "Final results: Processed %file_count% files, %success_count% successful"

if %success_count% neq %file_count% (
    set /a failed_count=%file_count%-%success_count%
    echo  Failed to create !failed_count! diff files.
    call :log "Failed to create !failed_count! diff files"
)
echo.
echo  Log file saved as: !LOG_FILE!
call :log "=== END OF LOG ==="
goto :end


:: --- Subroutine: Get Timestamp ---
:get_timestamp
    wmic os get localdatetime /format:list >nul 2>nul
    if %errorlevel% equ 0 (
        for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /format:list') do set "datetime=%%I"
        set "timestamp=!datetime:~0,4!!datetime:~4,2!!datetime:~6,2!_!datetime:~8,2!!datetime:~10,2!!datetime:~12,2!"
        goto :eof
    )
    :: Fallback method if wmic fails
    set "timestamp=%date%_%time%"
    set "timestamp=!timestamp:/=-!" 
    set "timestamp=!timestamp: =_!" 
    set "timestamp=!timestamp::=-!" 
    set "timestamp=!timestamp:,=-!" 
    set "timestamp=!timestamp:.=-!"
    goto :eof


:: --- Subroutine: List Branches ---
:list_branches
echo  Available local branches:
echo  -------------------------
set "branch_count=0"
for /f "tokens=*" %%B in ('git branch') do (
    set "branch=%%B"
    :: Clean up branch name, removing the '*' and leading/trailing spaces
    set "branch=!branch:* =!"
    set "branch=!branch: =!"
    
    set /a branch_count+=1
    set "branches[!branch_count!]=!branch!"
    
    if "%%B" equ "!branch!" (
        echo    !branch_count!. !branch!
    ) else (
        echo    !branch_count!. !branch!  (* current branch)
    )
)
if %branch_count% equ 0 exit /b 1
exit /b 0


:: --- Subroutine: Validate User Input ---
:validate_input
set "input_num=%1"
set "max_num=%2"
if "%input_num%"=="" (
    echo ERROR: No input provided.
    pause
    exit /b 1
)
if %input_num% gtr %max_num% (
    echo ERROR: Invalid selection. Please enter a number between 1 and %max_num%.
    pause
    exit /b 1
)
if %input_num% lss 1 (
    echo ERROR: Invalid selection. Please enter a number between 1 and %max_num%.
    pause
    exit /b 1
)
exit /b 0


:: --- Subroutine: Logging ---
:log
if not "!LOG_FILE!"=="" (
    if exist "!DIFF_DIR!" (
        echo %~1 >> "!LOG_FILE!"
    )
)
echo [DEBUG] %~1
exit /b 0


:end
echo.
if not "!LOG_FILE!"=="" (
    echo  Log file location: !LOG_FILE!
    if exist "!LOG_FILE!" (
        echo  Log file was created successfully.
    ) else (
        echo  WARNING: Log file was not created.
    )
)
echo.
echo Press any key to exit...
pause >nul
exit