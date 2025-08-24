#!/bin/bash

# BotArmy Frontend Recovery Script
# This script will attempt to restore the frontend to a working state

echo "🚀 Starting BotArmy Frontend Recovery..."
echo "======================================="

cd "/Users/neill/Documents/AI Code/Projects/v0-botarmy-poc"

# Phase 1: Create backup of broken state
echo "📦 Creating backup of current broken state..."
BACKUP_DIR="../v0-botarmy-poc-BROKEN-BACKUP-$(date +%Y%m%d_%H%M%S)"
cp -r . "$BACKUP_DIR"
echo "✅ Backup created at: $BACKUP_DIR"

# Phase 2: Check git status and recent commits
echo ""
echo "🔍 Checking git repository status..."
echo "Current branch:"
git branch --show-current

echo ""
echo "Recent commits (last 10):"
git log --oneline -10

echo ""
echo "Git status:"
git status --porcelain

# Phase 3: Attempt to identify the last working commit
echo ""
echo "🔎 Looking for commits from 2 days ago (Aug 21-22)..."
echo "Commits from Aug 21-22:"
git log --oneline --since="2025-08-21" --until="2025-08-23"

# Phase 4: Check for obvious issues
echo ""
echo "📋 Checking for obvious build issues..."

# Check if node_modules exists
if [ -d "node_modules" ]; then
    echo "✅ node_modules directory exists"
else
    echo "❌ node_modules directory missing"
fi

# Check key files
FILES_TO_CHECK=(
    "package.json"
    "package-lock.json"
    "next.config.mjs"
    "tailwind.config.ts"
    "app/layout.tsx"
    "app/page.tsx"
    "components/client-provider.tsx"
    "lib/stores/agent-store.ts"
)

echo ""
echo "Checking critical files:"
for file in "${FILES_TO_CHECK[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file exists"
    else
        echo "❌ $file MISSING"
    fi
done

echo ""
echo "🔧 Recovery script complete. Next steps:"
echo "1. Review the git commits above to find the last working state"
echo "2. If you identify a working commit, run: git reset --hard <COMMIT_ID>"
echo "3. Then run: rm -rf node_modules package-lock.json && npm install"
echo "4. Test with: npm run build"
echo ""
echo "💡 Suggested working commit might be from Aug 21-22"
echo "Look for commits with messages like 'fix', 'working', or 'stable'"
