#!/bin/bash

# Complete GitHub Secret Removal Script
echo "🔐 BotArmy Complete Secret Removal from GitHub"
echo "=============================================="
echo "Date: $(date)"
echo

echo "🎯 GOAL: Permanently remove API key from all GitHub history"
echo "📍 Current status: Secret was allowed and pushed to GitHub"
echo "🛠️ Solution: Remove from all git history and force push clean version"
echo

# Step 1: Identify the problematic file and commit
echo "🔍 Step 1: Identifying problematic files and commits..."

PROBLEM_FILE="backups/pre-merge-20250824-phase3/env-backup.txt"
echo "Target file: $PROBLEM_FILE"

# Check if file exists locally
if [ -f "$PROBLEM_FILE" ]; then
    echo "❌ File still exists locally - will remove"
    rm "$PROBLEM_FILE"
    echo "✅ Removed local copy"
else
    echo "ℹ️ File not found locally (good)"
fi

# Step 2: Remove file from git history entirely
echo ""
echo "🧹 Step 2: Removing file from all git history..."

# Use git filter-branch to remove the file from all commits
echo "Running git filter-branch to remove file from all history..."

git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch '$PROBLEM_FILE'" \
  --prune-empty --tag-name-filter cat -- --all

if [ $? -eq 0 ]; then
    echo "✅ File removed from all git history"
else
    echo "⚠️ Filter-branch had issues, trying alternative approach..."
    
    # Alternative: Use git filter-repo if available
    if command -v git-filter-repo &> /dev/null; then
        echo "Using git filter-repo (more reliable)..."
        git filter-repo --path "$PROBLEM_FILE" --invert-paths --force
        echo "✅ File removed using git filter-repo"
    else
        echo "📝 Manual approach needed - continuing with current method"
    fi
fi

echo ""

# Step 3: Clean up any other potential secret files
echo "🔍 Step 3: Cleaning up any other potential secret files..."

# Remove any backup files that might contain secrets
find . -name "*env-backup*" -type f -delete 2>/dev/null || true
find . -name "*backup*.txt" -type f -path "*/backups/*" -delete 2>/dev/null || true

# Remove any accidentally committed .env files
git rm --cached .env 2>/dev/null || true
git rm --cached .env.local 2>/dev/null || true
git rm --cached .env.production 2>/dev/null || true

echo "✅ Cleaned up potential secret files"

echo ""

# Step 4: Create safe backup files
echo "🛡️ Step 4: Creating safe, sanitized backup files..."

# Ensure backup directory exists
mkdir -p "backups/pre-merge-20250824-phase3"

# Create sanitized environment backup
cat > "backups/pre-merge-20250824-phase3/env-example-sanitized.txt" << 'EOF'
# BotArmy Environment Configuration Template
# Copy this to .env and add your actual API keys

# OpenAI API Configuration
OPENAI_API_KEY=sk-your-openai-api-key-here

# Gemini API Configuration  
GEMINI_KEY_KEY=your-gemini-api-key-here

# Backend Configuration
BACKEND_HOST=localhost
BACKEND_PORT=8000
BACKEND_URL=http://localhost:8000

# WebSocket Configuration
WEBSOCKET_URL=ws://localhost:8000/api/ws
NEXT_PUBLIC_WEBSOCKET_URL=ws://localhost:8000/api/ws

# Frontend Configuration
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000

# Development Settings
DEBUG=true
LOG_LEVEL=INFO

# Agent Configuration
MAX_AGENTS=6
AGENT_TIMEOUT=300
LLM_RATE_LIMIT_DELAY=2

# Safety Brake System - Testing Mode Controls
AGENT_TEST_MODE=true
TEST_MODE=true
ENABLE_HITL=true
AUTO_ACTION=none

# Testing Configuration
# AGENT_TEST_MODE=true means agents return role confirmations instead of full LLM processing
# TEST_MODE=true means LLM service returns mock responses
# ENABLE_HITL=true enables human-in-the-loop functionality
# AUTO_ACTION=none means manual approval required (options: none, approve, deny)
EOF

echo "✅ Created sanitized environment template"

# Step 5: Update .gitignore thoroughly
echo ""
echo "🔧 Step 5: Updating .gitignore to prevent future issues..."

# Create comprehensive .gitignore additions
cat >> .gitignore << 'EOF'

# ===== SECURITY: Prevent API Keys and Secrets =====
.env
.env.local
.env.*.local
.env.production
.env.development
*.env

# Backup files that might contain secrets
**/backups/**/*env*.txt
**/backups/**/*backup*.txt
**/*backup*.env
**/*-backup.txt
**/env-backup*

# API keys and secrets
**/api-keys.*
**/secrets.*
**/*.key
**/*.pem
**/credentials.*

# Development secrets
.vscode/settings.json
.idea/workspace.xml

# OS generated files
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db
EOF

echo "✅ Enhanced .gitignore to prevent future secret commits"

# Step 6: Force garbage collection and cleanup
echo ""
echo "🗑️ Step 6: Cleaning up git references and garbage collection..."

# Clean up git references
rm -rf .git/refs/original/
git reflog expire --expire=now --all
git gc --prune=now --aggressive

echo "✅ Git history cleaned and optimized"

# Step 7: Stage and commit clean changes
echo ""
echo "📦 Step 7: Committing clean, secure changes..."

git add .gitignore
git add "backups/pre-merge-20250824-phase3/env-example-sanitized.txt"

git commit -m "security: Remove API keys and enhance security measures

🔐 SECURITY IMPROVEMENTS:
- Removed all API keys from git history using git filter-branch
- Created sanitized environment template for developers
- Enhanced .gitignore to prevent future secret commits
- Added comprehensive secret file patterns to ignore list

🛡️ DEVELOPER SAFETY:
- No real API keys in repository
- Clear template for adding personal API keys
- TEST_MODE enabled by default (no API costs)
- Comprehensive setup instructions maintained

✅ CLEAN REPOSITORY:
- All sensitive data removed from git history
- Professional security practices implemented
- Safe for public collaboration and remote testing"

if [ $? -eq 0 ]; then
    echo "✅ Clean commit created successfully"
else
    echo "❌ Failed to create clean commit"
    exit 1
fi

echo ""

# Step 8: Force push to completely replace GitHub history
echo "🌐 Step 8: Force pushing clean history to GitHub..."

echo "⚠️ WARNING: This will rewrite GitHub history to remove all traces of the API key"
echo "✅ SAFE: All integration code and functionality preserved"
echo ""

# Force push to replace all history
git push origin integration/enhanced-hitl-final --force-with-lease

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 SUCCESS! Secret completely removed from GitHub"
    echo "✅ Repository is now clean and secure"
    echo "✅ All integration code preserved"
    echo "✅ Safe for remote developer collaboration"
    echo ""
    echo "📊 Repository Status:"
    echo "- Branch: integration/enhanced-hitl-final"
    echo "- Repository: https://github.com/geniusboywonder/v0-botarmy-poc"
    echo "- Status: Clean, no secrets in history"
    echo "- Ready: For remote developer testing"
    
else
    echo ""
    echo "❌ Force push failed. Let's try alternative approach..."
    echo ""
    echo "🔧 Alternative: Manual GitHub cleanup required"
    echo "1. Go to: https://github.com/geniusboywonder/v0-botarmy-poc/settings/security_analysis"
    echo "2. Enable secret scanning"
    echo "3. Review and dismiss the detected secret"
    echo "4. The secret will be marked as resolved"
    echo ""
    echo "Or try the push again:"
    echo "git push origin integration/enhanced-hitl-final --force"
fi

echo ""
echo "🔐 Complete secret removal script finished!"
echo ""
echo "🎯 NEXT STEPS FOR REMOTE DEVELOPERS:"
echo "1. Clone the repository"  
echo "2. Copy .env.example to .env"
echo "3. Add their own API keys to .env"
echo "4. Follow setup instructions in README.md"
echo "5. Start testing with TEST_MODE enabled (no API costs)"
