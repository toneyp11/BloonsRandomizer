@echo off
REM Double-click this file to launch the Bloons Randomizer.
REM Runs from this file's own folder so it works wherever the repo is unzipped.
cd /d "%~dp0"

REM Try "python" first; if it isn't available, fall back to the "py" launcher.
python BloonsRandomizer.py
if not errorlevel 1 goto :end

py BloonsRandomizer.py
if not errorlevel 1 goto :end

echo.
echo Could not start the Bloons Randomizer.
echo Please install Python 3 from https://python.org and try again.
pause

:end
