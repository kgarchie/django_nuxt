#!/bin/bash

# Check if Python is installed
if ! command -v python &>/dev/null; then
    echo "Python is not installed. Please download and install Python from:"
    echo "https://www.python.org/downloads/"
    exit 1
else
    echo "Python is installed, proceeding to check for Node.js"
fi

# Check if Node.js is installed
if ! command -v node &>/dev/null; then
    echo "Node.js is not installed. Please download and install Node.js from:"
    echo "https://nodejs.org/en/download/"
    exit 1
else
    echo "Node.js is installed, proceeding."
fi

VENV_FOLDER=venv

# Check if virtual environment exists
if [ -d "$VENV_FOLDER" ]; then
    echo "Virtual environment exists. Activating..."
else
    echo "Creating virtual environment"
    python -m venv $VENV_FOLDER
fi

source $VENV_FOLDER/bin/activate

pip install -r requirements.txt

# Start the backend server in the background
python manage.py runserver &

# Start the frontend server in the background
(cd frontend && npm install && npm run dev) &

deactivate
