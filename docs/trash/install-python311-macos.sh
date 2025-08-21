#!/bin/bash

# Install Python 3.11 on macOS for BotArmy
echo "🐍 Python 3.11 Installation for BotArmy"
echo "========================================"

# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    echo "❌ Homebrew is not installed. Installing Homebrew first..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    
    # Add Homebrew to PATH
    echo "🔧 Adding Homebrew to PATH..."
    echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
    eval "$(/opt/homebrew/bin/brew shellenv)"
fi

echo "✅ Homebrew is available"

# Install Python 3.11
echo "📦 Installing Python 3.11..."
brew install python@3.11

# Verify installation
if command -v python3.11 &> /dev/null; then
    version=$(python3.11 --version)
    echo "✅ Python 3.11 installed successfully: $version"
    
    # Make sure pip is available
    python3.11 -m ensurepip --upgrade
    
    echo ""
    echo "🎉 Python 3.11 is now ready!"
    echo "You can now run the main setup script:"
    echo "  ./setup.sh"
    
else
    echo "❌ Python 3.11 installation failed"
    echo "Please try manual installation:"
    echo "  brew install python@3.11"
fi

echo ""
echo "📍 Available Python versions:"
ls /opt/homebrew/bin/python* 2>/dev/null || ls /usr/local/bin/python* 2>/dev/null
