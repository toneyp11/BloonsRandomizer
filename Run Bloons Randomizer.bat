@echo off
REM Double-click this file to launch the Bloons Randomizer.
REM Runs from this file's own folder so it works wherever the repo is unzipped.
cd /d "%~dp0"

REM pythonw has no console window; "start" lets this script exit right away so
REM no command prompt lingers while the app runs.
where pythonw >nul 2>&1
if %errorlevel%==0 (
    start "" pythonw "%~dp0BloonsRandomizer.py"
    goto :end
)

REM Fall back to console python if pythonw isn't available.
where python >nul 2>&1
if %errorlevel%==0 (
    start "" python "%~dp0BloonsRandomizer.py"
    goto :end
)

echo Could not find Python. Install Python 3 from https://python.org and try again.
pause

:end
