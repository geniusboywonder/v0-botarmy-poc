#!/bin/bash

# Script to rebuild virtual environment with updated requirements.txt
set -e

PROJECT_ROOT="/Users/neill/Documents/AI Code/Projects/v0-botarmy-poc"
cd "$PROJECT_ROOT"

echo "🔄 Rebuilding virtual environment..."

# Remove existing virtual environment
if [ -d "venv" ]; then
    echo "📁 Removing existing virtual environment..."
    rm -rf venv
fi

# Create new virtual environment
echo "🆕 Creating new virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📦 Installing dependencies from requirements.txt..."
pip install -r requirements.txt

# Verify installation
echo "✅ Verifying installation..."
python test_imports.py

echo "🎉 Virtual environment rebuild complete!"
echo "💡 To activate: source venv/bin/activate"
