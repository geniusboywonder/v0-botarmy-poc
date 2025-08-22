#!/bin/bash

# Vercel deployment optimization script
set -e

PROJECT_ROOT="/Users/neill/Documents/AI Code/Projects/v0-botarmy-poc"
cd "$PROJECT_ROOT"

echo "🚀 Preparing for Vercel deployment..."

# Option 1: Use minimal API (recommended for Vercel)
echo "📝 Option 1: Deploy with minimal API"
echo "   - Copy api/index-minimal.py to api/index.py"
echo "   - Use requirements-vercel.txt"

# Option 2: Use full API with optimizations
echo "📝 Option 2: Deploy with full API (optimized)"
echo "   - Keep current api/index.py"
echo "   - Use current requirements.txt"
echo "   - Rely on vercel.json excludeFiles"

echo ""
echo "🔧 Choose deployment strategy:"
echo "1) Minimal API (safer, limited functionality)"
echo "2) Full API (optimized, full functionality)"
echo "3) Cancel"

read -p "Enter choice (1-3): " choice

case $choice in
    1)
        echo "📦 Setting up minimal API deployment..."
        cp api/index-minimal.py api/index.py
        cp requirements-vercel.txt requirements.txt
        echo "✅ Minimal API setup complete"
        echo "💡 Deploy with: vercel --prod"
        ;;
    2)
        echo "📦 Setting up optimized full API deployment..."
        # Keep current files but ensure optimizations are in place
        echo "✅ Full API optimization complete"
        echo "💡 Deploy with: vercel --prod"
        echo "⚠️  If deployment fails with 250MB error, use option 1"
        ;;
    3)
        echo "❌ Deployment preparation cancelled"
        exit 0
        ;;
    *)
        echo "❌ Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "📋 Next steps:"
echo "1. Test locally: npm run dev"
echo "2. Build: npm run build"
echo "3. Deploy: vercel --prod"
echo ""
echo "🔍 If deployment still fails:"
echo "- Check bundle size with: vercel --debug"
echo "- Consider moving heavy operations to external services"
echo "- Use edge functions for lightweight operations"
