#!/bin/bash

# Automated deployment script for GitHub Actions / Vercel
# This script ensures the environment is properly configured for Vercel deployment

set -e  # Exit on any error

echo "🚀 Preparing BotArmy for Vercel deployment..."

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    echo "❌ Error: package.json not found. Please run from project root."
    exit 1
fi

# Environment setup
export VERCEL=1
export VERCEL_ENV=${VERCEL_ENV:-production}

echo "📋 Environment:"
echo "  - VERCEL: $VERCEL"
echo "  - VERCEL_ENV: $VERCEL_ENV"
echo "  - NODE_ENV: ${NODE_ENV:-production}"

# Check Python version
echo "🐍 Python version:"
python3 --version

# Install Node.js dependencies
echo "📦 Installing Node.js dependencies..."
npm ci

# Build Next.js application
echo "🔨 Building Next.js application..."
npm run build

# Verify critical files exist
echo "🔍 Verifying deployment files..."

critical_files=(
    "api/index.py"
    "backend/main.py"
    "backend/runtime_env.py"
    "requirements.txt"
    "vercel.json"
)

for file in "${critical_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ Critical file missing: $file"
        exit 1
    else
        echo "✅ Found: $file"
    fi
done

# Check Python dependencies will work
echo "🔧 Checking Python requirements..."
if [ -f "requirements.txt" ]; then
    echo "✅ requirements.txt found"
    echo "📋 Dependencies that will be installed:"
    cat requirements.txt | grep -v "^#" | grep -v "^$" | head -10
    echo "..."
else
    echo "❌ requirements.txt not found"
    exit 1
fi

# Verify environment variables are set
echo "🔐 Checking environment variables..."
required_env_vars=(
    "GOOGLE_API_KEY"
)

missing_vars=()
for var in "${required_env_vars[@]}"; do
    if [ -z "${!var}" ]; then
        missing_vars+=("$var")
    else
        echo "✅ $var is set"
    fi
done

if [ ${#missing_vars[@]} -ne 0 ]; then
    echo "⚠️  Warning: Missing environment variables:"
    for var in "${missing_vars[@]}"; do
        echo "  - $var"
    done
    echo "💡 Make sure these are set in your Vercel dashboard"
fi

# Test import of critical modules
echo "🧪 Testing Python imports..."
python3 -c "
import sys
sys.path.insert(0, '.')

try:
    from backend.runtime_env import IS_VERCEL, get_environment_info
    print('✅ Runtime environment detection works')
    
    from backend.main import app
    print('✅ Main application imports successfully')
    
    from backend.agents.base_agent import BaseAgent
    print('✅ Base agent imports successfully')
    
    print('🎯 Import test completed successfully')
    
except Exception as e:
    print(f'❌ Import test failed: {e}')
    sys.exit(1)
"

if [ $? -ne 0 ]; then
    echo "❌ Python import test failed"
    exit 1
fi

echo ""
echo "✅ Deployment preparation completed successfully!"
echo ""
echo "📝 Summary:"
echo "  - Environment: Vercel production mode"
echo "  - Dependencies: Optimized for 250MB limit"
echo "  - Features: Full API with conditional heavy dependencies"
echo "  - Fallbacks: Graceful degradation for missing dependencies"
echo ""
echo "🚀 Ready for Vercel deployment!"
echo "💡 The application will:"
echo "   - Use lightweight dependencies in Vercel"
echo "   - Maintain full functionality through adaptive agents"
echo "   - Provide graceful fallbacks for heavy operations"
echo "   - Support real-time WebSocket connections"
