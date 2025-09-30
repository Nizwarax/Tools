#!/usr/bin/env bash

# Function to print messages
log() {
    echo "[*] $1"
}

# Detect package manager
if command -v pkg &> /dev/null; then
    # Termux
    log "Termux detected. Using 'pkg' for system dependencies."

    # Update and upgrade packages
    pkg update -y && pkg upgrade -y

    # Install dependencies
    log "Installing git and python..."
    pkg install git python -y

    # Install Python packages
    log "Installing Python packages from requirements.txt..."
    pip install --upgrade pip
    pip install -r requirements.txt

elif command -v apt-get &> /dev/null; then
    # Debian/Ubuntu
    log "Debian/Ubuntu detected. Using 'apt-get' for system dependencies."

    # Update packages
    sudo apt-get update -y

    # Install dependencies
    log "Installing git, python3, and python3-pip..."
    sudo apt-get install git python3 python3-pip -y

    # Install Python packages
    log "Installing Python packages from requirements.txt..."
    pip3 install --upgrade pip
    pip3 install -r requirements.txt

else
    log "Unsupported package manager. Please install dependencies manually."
    log "Required: git, python, pip"
    exit 1
fi

log "Installation complete!"
log "To run the script: python main.py"