#!/bin/bash

# BotArmy Frontend Recovery - Step 2: Clean Install
echo "🔧 BotArmy Frontend Recovery - Phase 2"
echo "====================================="
echo ""

echo "📊 Current Status:"
echo "✅ Switched to main branch (working code)"
echo "✅ Cleaned node_modules and package-lock.json"
echo "✅ Cleaned .next build directory"
echo ""

echo "🔧 Starting fresh npm install..."
cd "/Users/neill/Documents/AI Code/Projects/v0-botarmy-poc"

# Check that we're in the right directory and on main branch
echo "📁 Current directory: $(pwd)"
echo "🌿 Git branch: $(git branch --show-current)"
echo ""

echo "📦 Installing dependencies..."
npm install

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Dependencies installed successfully!"
    echo ""

    echo "🏗️  Testing build process..."
    npm run build

    if [ $? -eq 0 ]; then
        echo ""
        echo "🎉 RECOVERY SUCCESSFUL!"
        echo "====================="
        echo "✅ Switched to main branch"
        echo "✅ Clean dependency install"
        echo "✅ Build completed successfully"
        echo ""
        echo "🚀 Ready to start development:"
        echo "   npm run dev"
        echo ""
        echo "Expected result: Green themed UI like Replit screenshot"
        echo ""

        echo "🧪 Quick dev server test (5 seconds)..."
        timeout 5s npm run dev &
        DEV_PID=$!
        sleep 6
        kill $DEV_PID 2>/dev/null

        echo "✅ Dev server started successfully"
        echo ""
        echo "🎊 FRONTEND RECOVERY COMPLETE!"
        echo "Your local environment should now match Replit functionality"

    else
        echo ""
        echo "❌ Build failed - investigating..."
        echo ""
        echo "Build error details:"
        npm run build 2>&1 | tail -20
    fi
else
    echo ""
    echo "❌ npm install failed"
    echo ""
    echo "Install error details:"
    npm install 2>&1 | tail -10
fi

echo ""
echo "Recovery script complete."
