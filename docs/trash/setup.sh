#!/bin/bash

# BotArmy Setup Script with Python 3.11 Support
echo "🤖 BotArmy POC - Setup Script (Python 3.11 Required)"
echo "======================================================="

# Check if we're in the project root
if [ ! -f "package.json" ] || [ ! -f "backend/main.py" ]; then
    echo "❌ Please run this script from the BotArmy project root directory"
    exit 1
fi

echo "📍 Current directory: $(pwd)"

# Function to check Python version
check_python_version() {
    local python_cmd=$1
    if command -v $python_cmd &> /dev/null; then
        local version=$($python_cmd --version 2>&1 | awk '{print $2}')
        local major=$(echo $version | cut -d. -f1)
        local minor=$(echo $version | cut -d. -f2)
        echo "Found $python_cmd: $version"
        
        if [[ $major -eq 3 && $minor -eq 11 ]]; then
            echo "✅ $python_cmd is Python 3.11 - perfect for ControlFlow!"
            PYTHON_CMD=$python_cmd
            return 0
        elif [[ $major -eq 3 && $minor -lt 11 ]]; then
            echo "⚠️  $python_cmd is Python 3.$minor - too old for ControlFlow (needs 3.11)"
            return 1
        elif [[ $major -eq 3 && $minor -gt 11 ]]; then
            echo "⚠️  $python_cmd is Python 3.$minor - may not work with ControlFlow (needs 3.11)"
            return 1
        fi
    fi
    return 1
}

# Find compatible Python version
echo ""
echo "🐍 Checking Python versions..."
echo "==============================="

PYTHON_CMD=""

# Check common Python commands
python_commands=("python3.11" "python3" "python")

for cmd in "${python_commands[@]}"; do
    if check_python_version $cmd; then
        break
    fi
done

if [ -z "$PYTHON_CMD" ]; then
    echo ""
    echo "❌ No compatible Python 3.11 found!"
    echo ""
    echo "ControlFlow requires Python 3.11. Please install it:"
    echo ""
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macOS:"
        echo "  brew install python@3.11"
        echo "  # Then run: python3.11 -m venv venv"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "Ubuntu/Debian:"
        echo "  sudo apt update"
        echo "  sudo apt install python3.11 python3.11-venv python3.11-dev"
        echo ""
        echo "CentOS/RHEL:"
        echo "  sudo dnf install python3.11 python3.11-pip"
    fi
    echo ""
    echo "After installing Python 3.11, rerun this script."
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo ""
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file and add your OPENAI_API_KEY before running the application"
fi

# Backend Setup
echo ""
echo "🐍 Setting up Backend with $PYTHON_CMD..."
echo "========================================="

# Remove existing venv if it exists and was created with wrong Python version
if [ -d "venv" ]; then
    echo "🔍 Checking existing virtual environment..."
    if [ -f "venv/pyvenv.cfg" ]; then
        existing_python=$(grep "executable" venv/pyvenv.cfg | awk '{print $3}')
        existing_version=$($existing_python --version 2>&1 | awk '{print $2}' | cut -d. -f1-2)
        echo "Existing venv uses Python $existing_version"
        
        if [[ "$existing_version" != "3.11" ]]; then
            echo "🗑️  Removing incompatible virtual environment..."
            rm -rf venv
        fi
    fi
fi

# Create virtual environment with Python 3.11
if [ ! -d "venv" ]; then
    echo "🔧 Creating Python 3.11 virtual environment..."
    $PYTHON_CMD -m venv venv
    
    if [ $? -ne 0 ]; then
        echo "❌ Failed to create virtual environment"
        echo "Make sure Python 3.11 has venv module installed:"
        echo "  sudo apt install python3.11-venv  # Ubuntu/Debian"
        exit 1
    fi
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Verify we're using the right Python
python_in_venv=$(python --version 2>&1 | awk '{print $2}' | cut -d. -f1-2)
echo "Python in venv: $python_in_venv"

if [[ "$python_in_venv" != "3.11" ]]; then
    echo "❌ Virtual environment is not using Python 3.11"
    echo "Please remove the venv directory and rerun this script"
    exit 1
fi

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install dependencies with latest stable versions
echo "📦 Installing backend dependencies with latest ControlFlow..."
echo "This may take a few minutes..."

# Install Prefect 3.0+ first
pip install "prefect>=3.0.0"
if [ $? -ne 0 ]; then
    echo "❌ Failed to install Prefect 3.0+. This is required for ControlFlow."
    exit 1
fi

# Install latest ControlFlow (0.11+)
echo "Installing ControlFlow (latest version)..."
pip install "controlflow>=0.11.0"
if [ $? -ne 0 ]; then
    echo "⚠️  Failed to install ControlFlow 0.11+"
    echo "Trying to install any available ControlFlow version..."
    pip install controlflow
    if [ $? -ne 0 ]; then
        echo "❌ ControlFlow installation failed completely"
        echo "💡 Would you like to continue with minimal setup (no ControlFlow)? [y/N]"
        read -r response
        if [[ "$response" =~ ^[Yy]$ ]]; then
            echo "Installing minimal requirements without ControlFlow..."
            pip install -r backend/requirements-minimal.txt
            echo "⚠️  Backend will run in minimal mode without agent orchestration"
            MINIMAL_MODE=true
        else
            echo "Setup cancelled. Please check ControlFlow compatibility."
            exit 1
        fi
    fi
fi

# Install remaining dependencies
pip install -r backend/requirements.txt

# Test critical imports
echo ""
echo "🧪 Testing Python imports..."
python -c "
import sys
print(f'Python version: {sys.version}')

try:
    import fastapi
    print('✅ FastAPI imported successfully')
except ImportError as e:
    print(f'❌ FastAPI import failed: {e}')
    sys.exit(1)

try:
    import prefect
    prefect_version = prefect.__version__
    major, minor = prefect_version.split('.')[:2]
    if int(major) >= 3:
        print(f'✅ Prefect imported successfully (version: {prefect_version}) - Compatible with ControlFlow')
    else:
        print(f'⚠️  Prefect version {prefect_version} detected - ControlFlow requires 3.0+')
except ImportError as e:
    print(f'❌ Prefect import failed: {e}')
    sys.exit(1)

try:
    import controlflow
    cf_version = controlflow.__version__
    major, minor = cf_version.split('.')[:2]
    if int(major) == 0 and int(minor) >= 11:
        print(f'✅ ControlFlow imported successfully (version: {cf_version}) - Latest stable version')
    elif int(major) == 0 and int(minor) >= 9:
        print(f'✅ ControlFlow imported successfully (version: {cf_version}) - Compatible with Prefect 3.0+')
    else:
        print(f'⚠️  ControlFlow version {cf_version} detected - Consider upgrading to 0.11+')
except ImportError as e:
    if [ "${MINIMAL_MODE:-false}" = "true" ]; then
        print('⚠️  ControlFlow not available (minimal mode) - Agent orchestration disabled')
    else:
        print(f'❌ ControlFlow import failed: {e}')
        print('This is a critical dependency for the backend.')
        sys.exit(1)

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
echo "  - Backend: Python $python_in_venv with FastAPI and ControlFlow"
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
if grep -q "your_openai_api_key_here" .env 2>/dev/null; then
    echo "⚠️  Remember to add your OpenAI API key to the .env file!"
else
    echo "✅ OpenAI API key appears to be configured"
fi

echo ""
echo "🎉 BotArmy setup complete! Happy coding!"
