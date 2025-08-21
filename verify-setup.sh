#!/bin/bash

# BotArmy Installation Verification Script
echo "🔍 BotArmy Installation Verification"
echo "===================================="

# Check project structure
echo "📁 Checking project structure..."

required_files=(
    "package.json"
    "backend/main.py"
    "backend/requirements.txt"
    "components/chat/enhanced-chat-interface.tsx"
    "components/agent-status-card.tsx"
    "components/ui/avatar.tsx"
    ".env.example"
)

missing_files=()

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file"
    else
        echo "❌ $file"
        missing_files+=("$file")
    fi
done

if [ ${#missing_files[@]} -gt 0 ]; then
    echo ""
    echo "❌ Missing required files. Please ensure you're in the project root."
    exit 1
fi

echo ""
echo "🐍 Checking Python setup..."

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "✅ Virtual environment exists"
    
    # Activate and check Python packages
    source venv/bin/activate
    
    # Check critical packages
    python3 -c "
import sys
import importlib
packages = ['fastapi', 'uvicorn', 'pydantic', 'openai']
missing = []

for pkg in packages:
    try:
        importlib.import_module(pkg)
        print(f'✅ {pkg}')
    except ImportError:
        print(f'❌ {pkg} - not installed')
        missing.append(pkg)

# Special check for ControlFlow (might fail)
try:
    import controlflow
    print('✅ controlflow')
except ImportError:
    print('⚠️  controlflow - may need additional setup')
    
if missing:
    print(f'Missing packages: {missing}')
    sys.exit(1)
"
    
    if [ $? -ne 0 ]; then
        echo "❌ Python dependencies not properly installed"
        echo "💡 Try running: ./setup.sh"
        exit 1
    fi
    
else
    echo "❌ Virtual environment not found"
    echo "💡 Try running: ./setup.sh"
    exit 1
fi

echo ""
echo "⚛️  Checking Node.js setup..."

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found"
    exit 1
fi

echo "✅ Node.js: $(node --version)"

# Check if node_modules exists
if [ -d "node_modules" ]; then
    echo "✅ Node modules installed"
else
    echo "❌ Node modules not installed"
    echo "💡 Try running: pnpm install"
    exit 1
fi

# Check for .env file
echo ""
echo "🔧 Checking environment configuration..."

if [ -f ".env" ]; then
    echo "✅ .env file exists"
    
    # Check for API key
    if grep -q "your_openai_api_key_here" .env 2>/dev/null; then
        echo "⚠️  OpenAI API key not configured in .env"
        echo "💡 Edit .env and add your OpenAI API key"
    else
        echo "✅ OpenAI API key appears to be configured"
    fi
else
    echo "⚠️  .env file not found"
    echo "💡 Copy .env.example to .env and configure"
fi

echo ""
echo "🎉 Installation Verification Complete!"
echo ""
echo "🚀 To start BotArmy:"
echo "1. Backend: source venv/bin/activate && cd backend && python main.py"
echo "2. Frontend: pnpm dev (in new terminal)"
echo "3. Open: http://localhost:3000"
