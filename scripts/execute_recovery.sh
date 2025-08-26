#!/bin/bash

# BotArmy Frontend Recovery - Execute Git Checkout
echo "🎯 EXECUTING FRONTEND RECOVERY"
echo "=============================="
echo ""

echo "📊 DIAGNOSIS:"
echo "- Current branch: feature/enhanced-hitl-integration (BROKEN)"
echo "- Solution: Switch to main branch (WORKING)"
echo "- This is why local is broken but Replit works!"
echo ""

echo "🔧 EXECUTING RECOVERY:"
echo ""

cd "/Users/neill/Documents/AI Code/Projects/v0-botarmy-poc"

echo "Step 1: Switching to main branch..."
git checkout main

if [ $? -eq 0 ]; then
    echo "✅ Successfully switched to main branch!"
    echo ""

    echo "Step 2: Cleaning dependencies..."
    rm -rf node_modules package-lock.json .next
    echo "✅ Cleaned build artifacts"

    echo ""
    echo "Step 3: Fresh npm install..."
    npm install

    if [ $? -eq 0 ]; then
        echo "✅ Dependencies installed successfully"
        echo ""

        echo "Step 4: Testing build..."
        npm run build

        if [ $? -eq 0 ]; then
            echo ""
            echo "🎉 RECOVERY SUCCESSFUL!"
            echo "======================"
            echo "✅ Switched to main branch"
            echo "✅ Clean dependency install"
            echo "✅ Build completed successfully"
            echo ""
            echo "Next: Run 'npm run dev' to start development server"
            echo "Expected: Green themed UI like Replit screenshot"
        else
            echo "❌ Build failed - may need additional fixes"
        fi
    else
        echo "❌ npm install failed"
    fi
else
    echo "❌ Git checkout failed"
    echo "Current git status:"
    git status
fi

echo ""
echo "Recovery script complete."
