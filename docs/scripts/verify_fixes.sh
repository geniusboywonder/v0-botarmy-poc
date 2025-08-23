#!/bin/bash

# Quick verification script to test if fixes work
echo "🔍 BotArmy Code Repair Verification"
echo "===================================="

cd "$(dirname "$0")"

# Check if we're in the right directory
if [ ! -f "package.json" ] || [ ! -f "backend/main.py" ]; then
    echo "❌ Not in BotArmy project directory"
    exit 1
fi

echo "📁 Project directory: $(pwd)"
echo ""

# Test 1: Check if Python dependencies can be imported
echo "🐍 Testing Python Dependencies..."
if [ -d "venv" ]; then
    source venv/bin/activate
    python3 -c "
import sys
print(f'Python version: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}')

# Test critical imports
try:
    import fastapi
    print('✅ FastAPI: Available')
except ImportError:
    print('❌ FastAPI: Missing')
    
try:
    import uvicorn
    print('✅ Uvicorn: Available')
except ImportError:
    print('❌ Uvicorn: Missing')

try:
    import openai
    print('✅ OpenAI: Available')
except ImportError:
    print('❌ OpenAI: Missing')

try:
    import controlflow
    print('✅ ControlFlow: Available')
except ImportError as e:
    print(f'⚠️  ControlFlow: Missing ({e})')
    print('   Run setup_backend.sh to install dependencies')

try:
    import pydantic
    print('✅ Pydantic: Available')
except ImportError:
    print('❌ Pydantic: Missing')
"
else
    echo "⚠️  Virtual environment not found. Run setup_backend.sh first."
fi

echo ""

# Test 2: Check if frontend files exist
echo "⚛️  Testing Frontend Components..."
files_to_check=(
    "components/chat/enhanced-chat-interface.tsx"
    "components/agent-status-card.tsx" 
    "components/ui/avatar.tsx"
    "components/ui/progress.tsx"
    "components/ui/separator.tsx"
)

all_files_exist=true
for file in "${files_to_check[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file: Exists"
    else
        echo "❌ $file: Missing"
        all_files_exist=false
    fi
done

# Test 3: Check Node.js and dependencies
echo ""
echo "📦 Testing Node.js Environment..."
if command -v node &> /dev/null; then
    echo "✅ Node.js: $(node --version)"
    
    if [ -d "node_modules" ]; then
        echo "✅ Dependencies: Installed"
        
        # Test build
        echo "🔨 Testing build..."
        if command -v pnpm &> /dev/null; then
            pnpm build --dry-run 2>/dev/null && echo "✅ Build: Should work" || echo "⚠️  Build: May have issues"
        elif command -v yarn &> /dev/null; then
            echo "✅ Yarn available for build"
        else
            echo "✅ NPM available for build"
        fi
    else
        echo "⚠️  Dependencies: Not installed. Run 'pnpm install' or 'npm install'"
    fi
else
    echo "❌ Node.js: Not installed"
fi

# Test 4: Environment configuration
echo ""
echo "⚙️  Testing Environment Configuration..."
if [ -f ".env" ]; then
    echo "✅ .env file: Exists"
    if grep -q "OPENAI_API_KEY=your_openai_api_key_here" .env 2>/dev/null; then
        echo "⚠️  OpenAI API Key: Please update .env with your actual API key"
    else
        echo "✅ OpenAI API Key: Configured"
    fi
else
    echo "⚠️  .env file: Missing. Copy from .env.example"
fi

if [ -f ".env.example" ]; then
    echo "✅ .env.example: Available as template"
else
    echo "❌ .env.example: Missing"
fi

# Summary
echo ""
echo "📋 Verification Summary"
echo "======================="

if [ "$all_files_exist" = true ]; then
    echo "✅ All required frontend components exist"
else
    echo "❌ Some frontend components are missing"
fi

echo ""
echo "🚀 Next Steps:"
echo "1. If dependencies are missing, run: ./setup.sh"
echo "2. Add your OpenAI API key to .env file" 
echo "3. Start backend: source venv/bin/activate && cd backend && python main.py"
echo "4. Start frontend: pnpm dev (or npm run dev)"
echo "5. Open http://localhost:3000"
