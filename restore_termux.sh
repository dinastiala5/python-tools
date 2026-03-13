#!/data/data/com.termux/files/usr/bin/bash

echo "Updating Termux..."
pkg update -y
pkg upgrade -y

echo "Installing basic tools..."
pkg install git python -y

echo "Cloning your toolkit..."
git clone https://github.com/dinastiala5/python-tools.git

cd python-tools

echo "Installing Termux packages..."
pkg install $(cat packages.txt)

echo "Installing Python libraries..."
pip install -r requirements.txt

echo "Setup complete!"
