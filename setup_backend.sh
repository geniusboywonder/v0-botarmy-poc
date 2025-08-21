#!/bin/bash

# BotArmy Backend Setup Script
echo "🚀 Setting up BotArmy Backend..."

# Check if we're in the project root
if [ ! -f "backend/main.py" ]; then
    echo "❌ Please run this script from the project root directory"
    exit 1
fi

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "📍 Python version: $python_version"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "🔧 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📦 Installing backend dependencies..."
pip install -r backend/requirements.txt

# Check if OpenAI API key is set
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  WARNING: OPENAI_API_KEY environment variable is not set"
    echo "   Please set it before running the backend:"
    echo "   export OPENAI_API_KEY='your-api-key-here'"
fi

# Test imports
echo "🧪 Testing critical imports..."
python3 -c "
try:
    import fastapi
    print('✅ FastAPI imported successfully')
except ImportError as e:
    print(f'❌ FastAPI import failed: {e}')

try:
    import controlflow
    print('✅ ControlFlow imported successfully')
except ImportError as e:
    print(f'❌ ControlFlow import failed: {e}')
    print('   This might require additional setup or a different Python version')

try:
    import openai
    print('✅ OpenAI imported successfully')
except ImportError as e:
    print(f'❌ OpenAI import failed: {e}')
"

echo "✅ Backend setup complete!"
echo "🏃 To start the backend, run:"
echo "   source venv/bin/activate"
echo "   cd backend && python main.py"
