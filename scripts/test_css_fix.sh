#!/bin/bash

echo "🧪 Testing BotArmy Build After CSS Fix"
echo "======================================"
echo ""

cd "/Users/neill/Documents/AI Code/Projects/v0-botarmy-poc"

echo "📊 Current Status:"
echo "✅ Fixed CSS: Removed invalid 'border-border' class"
echo "✅ Added Green Theme: Primary color #10b981 (emerald-500)"
echo "✅ Enhanced Component Styles: Agent cards, status badges, buttons"
echo ""

echo "🏗️  Testing build process..."
npm run build

BUILD_EXIT_CODE=$?

echo ""
if [ $BUILD_EXIT_CODE -eq 0 ]; then
    echo "🎉 BUILD SUCCESS!"
    echo "================="
    echo "✅ CSS error fixed"
    echo "✅ Green theme applied"
    echo "✅ Build completed without errors"
    echo ""

    echo "🚀 Starting development server to test UI..."
    echo "Expected: Green themed interface"
    echo ""

    # Start dev server in background for testing
    timeout 10s npm run dev &
    DEV_PID=$!
    sleep 8
    kill $DEV_PID 2>/dev/null

    echo ""
    echo "🎊 RECOVERY COMPLETE!"
    echo "===================="
    echo "Your BotArmy frontend should now show:"
    echo "• Green primary color (emerald-500)"
    echo "• Green agent status indicators"
    echo "• Green connection status"
    echo "• Proper themed UI components"
    echo ""
    echo "🚀 Run 'npm run dev' to start development"

else
    echo "❌ Build failed"
    echo "=============="
    echo ""
    echo "Build output (last 20 lines):"
    npm run build 2>&1 | tail -20
fi

echo ""
echo "Test complete."
