#!/bin/bash

VENV_FOLDER="venv"
P_VERSION=$(python3 --version 2>&1 | grep -oE '[0-9]+\.[0-9]+')

# Check if Python is installed
if ! command -v python3 &>/dev/null; then
    echo "Python 3 is not installed. Please download and install Python from:"
    echo "https://www.python.org/downloads/"
    exit 1
else
    echo "Python 3 is installed, proceeding to check for Node.js"
fi

# Check if Node.js is installed
if ! command -v node &>/dev/null; then
    echo "Node.js is not installed. Please download and install Node.js from:"
    echo "https://nodejs.org/en/download/"
    exit 1
else
    echo "Node.js is installed, proceeding."
fi

# Check if virtual environment exists
if [ ! -d "$VENV_FOLDER" ]; then
    echo "Creating virtual environment..."
    
    sudo apt install python$P_VERSION-venv

    python3 -m venv $VENV_FOLDER
else
    echo "Virtual environment exists, proceeding."
fi


# Activate virtual environment
source $VENV_FOLDER/bin/activate

corepack enable

# Install PsycoPG2
sudo apt-get install libpq-dev python3-dev

# Install Python dependencies
pip3 install -r requirements.txt

# Install Node.js dependencies
cd frontend && pnpm install && cd ..

# Run the application
python3 manage.py runserver 8000 &

cd frontend && pnpm run dev && cd ..

# Deactivate virtual environment
deactivate