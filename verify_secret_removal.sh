#!/bin/bash

# Secret Removal Verification Script
echo "🔐 BotArmy Secret Removal Verification"
echo "======================================"
echo "Date: $(date)"
echo

# Check 1: Verify problematic file is gone
echo "🔍 Check 1: Verifying problematic file removal..."
PROBLEM_FILE="backups/pre-merge-20250824-phase3/env-backup.txt"

if [ ! -f "$PROBLEM_FILE" ]; then
    echo "✅ Original secret file REMOVED: $PROBLEM_FILE"
else
    echo "❌ WARNING: Secret file still exists: $PROBLEM_FILE"
fi

# Check 2: Search for any remaining OpenAI API keys
echo ""
echo "🔍 Check 2: Searching for any remaining API key patterns..."

# Search for sk- pattern (OpenAI keys) excluding node_modules
SEARCH_RESULTS=$(grep -r "sk-[a-zA-Z0-9]" . --exclude-dir=node_modules --exclude-dir=node_modules_backup --exclude-dir=venv --exclude-dir=.git 2>/dev/null | grep -v "your-openai-api-key-here" | grep -v "sk-your" | grep -v "example" | grep -v "template")

if [ -z "$SEARCH_RESULTS" ]; then
    echo "✅ NO REAL API KEYS FOUND in project files"
else
    echo "⚠️ Potential API keys found:"
    echo "$SEARCH_RESULTS"
fi

# Check 3: Verify .env files are ignored
echo ""
echo "🔍 Check 3: Verifying .env files are properly ignored..."

if grep -q "\.env" .gitignore; then
    echo "✅ .env files are ignored in .gitignore"
else
    echo "❌ WARNING: .env not found in .gitignore"
fi

# Check if .env is tracked by git
if git ls-files | grep -q "\.env$"; then
    echo "❌ WARNING: .env is tracked by git"
else
    echo "✅ .env is NOT tracked by git"
fi

# Check 4: Verify safe replacement files exist
echo ""
echo "🔍 Check 4: Verifying safe replacement files..."

if [ -f "backups/pre-merge-20250824-phase3/SETUP_INSTRUCTIONS.md" ]; then
    echo "✅ Safe setup instructions exist"
else
    echo "⚠️ Setup instructions not found"
fi

if [ -f "backups/pre-merge-20250824-phase3/env-backup-sanitized.txt" ]; then
    echo "✅ Sanitized environment template exists"
else
    echo "⚠️ Sanitized env template not found"
fi

# Check 5: Git status
echo ""
echo "🔍 Check 5: Git repository status..."

# Check if there are uncommitted changes
git status --porcelain > /tmp/git_status
if [ -s /tmp/git_status ]; then
    echo "ℹ️ Uncommitted changes present:"
    cat /tmp/git_status
else
    echo "✅ Git working directory is clean"
fi

# Check latest commit
echo ""
echo "📊 Latest commit:"
git log -1 --oneline

# Check 6: Remote status
echo ""
echo "🔍 Check 6: Remote repository status..."

# Check if local is ahead of remote
git status | grep -q "ahead"
if [ $? -eq 0 ]; then
    echo "ℹ️ Local branch has unpushed commits"
    echo "Use: git push origin integration/enhanced-hitl-final"
else
    echo "✅ Local branch is in sync with remote"
fi

# Final Summary
echo ""
echo "📊 VERIFICATION SUMMARY"
echo "======================="

# Count checks
PASSED=0
WARNINGS=0

# File removal
if [ ! -f "$PROBLEM_FILE" ]; then
    ((PASSED++))
    echo "✅ Secret file removed"
else
    ((WARNINGS++))
    echo "❌ Secret file still present"
fi

# API key search
if [ -z "$SEARCH_RESULTS" ]; then
    ((PASSED++))
    echo "✅ No API keys found in code"
else
    ((WARNINGS++))
    echo "⚠️ Potential API keys detected"
fi

# .gitignore
if grep -q "\.env" .gitignore; then
    ((PASSED++))
    echo "✅ .env properly ignored"
else
    ((WARNINGS++))
    echo "❌ .env not ignored"
fi

# Safe files
if [ -f "backups/pre-merge-20250824-phase3/SETUP_INSTRUCTIONS.md" ]; then
    ((PASSED++))
    echo "✅ Safe setup instructions present"
else
    ((WARNINGS++))
    echo "⚠️ Setup instructions missing"
fi

echo ""
echo "📈 RESULTS: $PASSED checks passed, $WARNINGS warnings"

if [ $WARNINGS -eq 0 ]; then
    echo ""
    echo "🎉 SUCCESS! Repository is clean and secure"
    echo "✅ Safe for pushing to GitHub"
    echo "✅ Ready for remote developer collaboration"
    echo "✅ No API keys or secrets detected"
    echo ""
    echo "🚀 Next steps:"
    echo "1. Push to GitHub: git push origin integration/enhanced-hitl-final"
    echo "2. Repository will be safe for remote developers"
    echo "3. Developers can add their own API keys via .env"
else
    echo ""
    echo "⚠️ Some issues detected - review warnings above"
    echo "🔧 Consider running additional cleanup if needed"
fi

rm -f /tmp/git_status
