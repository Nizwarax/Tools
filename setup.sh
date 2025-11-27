#!/usr/bin/env bash

# Function to print messages
log() {
    echo "[*] $1"
}

# Function to handle errors
handle_error() {
    log "An error occurred. Aborting installation."
    exit 1
}

# Trap errors
trap 'handle_error' ERR

# Detect package manager
if command -v pkg &> /dev/null; then
    # Termux
    log "Termux detected. Using 'pkg' for system dependencies."
    pkg update -y && pkg upgrade -y
    log "Installing git and python..."
    pkg install git python -y
    log "Installing Python packages from requirements.txt..."
    pip install --upgrade pip
    pip install -r requirements.txt

elif command -v apt-get &> /dev/null; then
    # Debian/Ubuntu
    log "Debian/Ubuntu detected. Using 'apt-get' for system dependencies."
    sudo apt-get update -y
    log "Installing git, python3, python3-pip, and build-essential..."
    sudo apt-get install -y git python3 python3-pip build-essential
    log "Installing Python packages from requirements.txt..."
    pip3 install --upgrade pip
    pip3 install -r requirements.txt

elif command -v dnf &> /dev/null; then
    # Fedora
    log "Fedora detected. Using 'dnf' for system dependencies."
    sudo dnf update -y
    log "Installing git, python3, python3-pip, and Development Tools..."
    sudo dnf install -y git python3 python3-pip
    sudo dnf groupinstall -y "Development Tools"
    log "Installing Python packages from requirements.txt..."
    pip3 install --upgrade pip
    pip3 install -r requirements.txt

elif command -v yum &> /dev/null; then
    # CentOS/RHEL
    log "CentOS/RHEL detected. Using 'yum' for system dependencies."
    sudo yum update -y
    log "Installing git, python3, python3-pip, and Development Tools..."
    # For CentOS 7, python3 might be in the EPEL repository
    if ! command -v python3 &> /dev/null; then
        sudo yum install -y epel-release
    fi
    sudo yum install -y git python3 python3-pip
    sudo yum groupinstall -y "Development Tools"
    log "Installing Python packages from requirements.txt..."
    pip3 install --upgrade pip
    pip3 install -r requirements.txt

else
    log "Unsupported package manager. Please install dependencies manually."
    log "Required: git, python3, pip3, and build tools."
    exit 1
fi

log "Installation complete!"
log "To run the script: python3 main.py"
