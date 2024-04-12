@echo off
setlocal

set COLOR_RESET=[0m
set COLOR_RED=[31m
set COLOR_GREEN=[32m
set COLOR_BLUE=[34m
set LOCATION=%CD%
set VENV_FOLDER=venv

python3 --version 2>NUL
if errorlevel 1 (
    echo %COLOR_RED%Python is not installed. Please download and install Python from:%COLOR_RESET%
    echo %COLOR_GREEN%https://www.python.org/downloads/%COLOR_RESET%
    exit 1
) else (
    echo %COLOR_GREEN%Python 3 is installed, proceeding to check for Node.js%COLOR_RESET%
)

where node 2>NUL
if errorlevel 1 (
    echo %COLOR_RED%Node.js is not installed. Please download and install Node.js from:%COLOR_RESET%
    echo %COLOR_GREEN%https://nodejs.org/en/download/%COLOR_RESET%
    exit 1
) else (
    echo %COLOR_GREEN%Node.js is installed, proceeding.%COLOR_RESET%
)

if exist %VENV_FOLDER% (
    echo %COLOR_GREEN%Virtual environment exists. Activating...%COLOR_RESET%
) else (
    echo %COLOR_BLUE%Creating virtual environment%COLOR_RESET%
    python3 -m venv %VENV_FOLDER%
)

call %LOCATION%\%VENV_FOLDER%\Scripts\activate
pip3 install -r requirements.txt

where pnpm 2>NUL
if errorlevel 1 (
    powershell -Command "Start-Process cmd -ArgumentList '/c corepack enable' -Verb RunAs" 2>NUL
    if errorlevel 1 (
        echo %COLOR_RED%Failed to enable corepack. Please run the command manually as admin.%COLOR_RESET%
        echo %COLOR_GREEN%corepack enable%COLOR_RESET%
        exit 1
    ) else (
        echo %COLOR_GREEN%corepack enabled%COLOR_RESET%
    )
) else (
    echo %COLOR_GREEN%pnpm is installed, proceeding.%COLOR_RESET%
)

:: Start the backend server
start /b cmd /c "%LOCATION%\%VENV_FOLDER%\Scripts\python manage.py runserver"

:: Start the frontend server
start /b cmd /c "cd .\frontend && pnpm install && npm run dev"

echo.
echo %COLOR_GREEN%All done!%COLOR_RESET%

echo %COLOR_BLUE%Close this terminal session to stop the services. They are running...%COLOR_RESET%
endlocal