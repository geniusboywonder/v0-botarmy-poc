#!/bin/bash

# BotArmy Full Setup Script
echo "🤖 BotArmy POC - Full Setup Script"
echo "=================================="

# Check if we're in the project root
if [ ! -f "package.json" ] || [ ! -f "backend/main.py" ]; then
    echo "❌ Please run this script from the BotArmy project root directory"
    exit 1
fi

echo "📍 Current directory: $(pwd)"

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file and add your OPENAI_API_KEY before running the application"
fi

# Backend Setup
echo ""
echo "🐍 Setting up Backend..."
echo "========================"

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "📍 Python version: $python_version"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "🔧 Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install backend dependencies
echo "📦 Installing backend dependencies..."
pip install -r backend/requirements.txt

# Test critical imports
echo "🧪 Testing Python imports..."
python3 -c "
import sys
print(f'Python version: {sys.version}')

try:
    import fastapi
    print('✅ FastAPI imported successfully')
except ImportError as e:
    print(f'❌ FastAPI import failed: {e}')
    sys.exit(1)

try:
    import controlflow
    print('✅ ControlFlow imported successfully') 
except ImportError as e:
    print(f'⚠️  ControlFlow import failed: {e}')
    print('   This may require additional setup or different Python version')

try:
    import openai
    print('✅ OpenAI imported successfully')
except ImportError as e:
    print(f'❌ OpenAI import failed: {e}')
    sys.exit(1)
"

if [ $? -ne 0 ]; then
    echo "❌ Backend setup failed. Please check the error messages above."
    exit 1
fi

# Frontend Setup
echo ""
echo "⚛️  Setting up Frontend..."
echo "=========================="

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+ and try again."
    exit 1
fi

node_version=$(node --version)
echo "📍 Node.js version: $node_version"

# Install frontend dependencies
if command -v pnpm &> /dev/null; then
    echo "📦 Installing frontend dependencies with pnpm..."
    pnpm install
elif command -v yarn &> /dev/null; then
    echo "📦 Installing frontend dependencies with yarn..."
    yarn install
else
    echo "📦 Installing frontend dependencies with npm..."
    npm install
fi

# Build check
echo "🔨 Running build check..."
if command -v pnpm &> /dev/null; then
    pnpm build
elif command -v yarn &> /dev/null; then
    yarn build  
else
    npm run build
fi

if [ $? -ne 0 ]; then
    echo "❌ Frontend build failed. Please check the error messages above."
    exit 1
fi

# Final checks
echo ""
echo "✅ Setup Complete!"
echo "=================="

echo "🔧 Configuration:"
echo "  - Backend: Python $python_version with FastAPI"
echo "  - Frontend: Node.js $node_version with Next.js"
echo "  - Environment: .env file created"

echo ""
echo "🚀 To start the application:"
echo ""
echo "1. Start the backend:"
echo "   source venv/bin/activate"
echo "   cd backend && python main.py"
echo ""
echo "2. In a new terminal, start the frontend:"
if command -v pnpm &> /dev/null; then
    echo "   pnpm dev"
elif command -v yarn &> /dev/null; then
    echo "   yarn dev"
else
    echo "   npm run dev"
fi
echo ""
echo "3. Open http://localhost:3000 in your browser"
echo ""

# Check for API key
if ! grep -q "your_openai_api_key_here" .env 2>/dev/null; then
    echo "✅ OpenAI API key appears to be configured"
else
    echo "⚠️  Remember to add your OpenAI API key to the .env file!"
fi

echo ""
echo "🎉 BotArmy setup complete! Happy coding!"
