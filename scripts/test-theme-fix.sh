#!/bin/bash
# Quick theme verification test

echo "🎨 BotArmy Theme Fix Verification"
echo "================================"

# Check if the theme provider file has been fixed
echo "✓ Checking client-provider.tsx fix..."
if grep -q 'defaultTheme="light"' /Users/neill/Documents/AI\ Code/Projects/v0-botarmy-poc/components/client-provider.tsx; then
    echo "  ✅ Theme provider now uses light theme"
else
    echo "  ❌ Theme provider still has issues"
fi

if grep -q 'enableSystem={false}' /Users/neill/Documents/AI\ Code/Projects/v0-botarmy-poc/components/client-provider.tsx; then
    echo "  ✅ System theme detection disabled"
else
    echo "  ⚠️ System theme detection might still interfere"
fi

# Check if green theme CSS is present
echo "✓ Checking green theme CSS..."
if grep -q '--primary: #10b981' /Users/neill/Documents/AI\ Code/Projects/v0-botarmy-poc/app/globals.css; then
    echo "  ✅ Green theme variables are configured"
else
    echo "  ❌ Green theme CSS missing"
fi

echo ""
echo "📋 Next Steps:"
echo "1. Run: npm run dev"
echo "2. Open: http://localhost:3000"
echo "3. Verify UI shows green theme instead of dark"
echo ""
echo "The UI should now display:"
echo "- White background"
echo "- Green primary colors (#10b981)"
echo "- Green accents for active states"
echo "- Light theme throughout"
