#!/bin/bash

# Merge Conflict Resolution Script
# Handles ClaudeProgress.md merge and forces local versions for other files

echo "🔀 Merge Conflict Resolution Script"
echo "===================================="

cd "/Users/neill/Documents/AI Code/Projects/v0-botarmy-poc"

echo "📍 Current directory: $(pwd)"
echo ""

# Check current merge status
echo "1. Checking current merge conflicts..."
git status --porcelain | grep "^UU\|^AA\|^DD\|^AU\|^UA\|^DU\|^UD"
echo ""

echo "2. 🎯 RESOLUTION STRATEGY:"
echo "   ✅ ClaudeProgress.md: Manual merge (preserve both versions)"
echo "   🔧 All other files: Use LOCAL versions (--ours)"
echo ""

# Handle ClaudeProgress.md merge
echo "3. 📝 Handling ClaudeProgress.md merge..."

# Extract both versions from git objects
git show HEAD:ClaudeProgress.md > ClaudeProgress_local.md 2>/dev/null
git show MERGE_HEAD:ClaudeProgress.md > ClaudeProgress_remote.md 2>/dev/null

# Create merged version
cat > ClaudeProgress.md << 'EOF'
# BotArmy Code Repair Progress Tracker

## 📊 MERGE SUMMARY
This file combines progress from both local and remote branches after git-filter-repo processing.

## LOCAL BRANCH PROGRESS
EOF

# Add local content (skip first line if it's the same header)
tail -n +2 ClaudeProgress_local.md >> ClaudeProgress.md

cat >> ClaudeProgress.md << 'EOF'

## REMOTE BRANCH PROGRESS  
EOF

# Add remote content (skip first line if it's the same header)
tail -n +2 ClaudeProgress_remote.md >> ClaudeProgress.md

cat >> ClaudeProgress.md << 'EOF'

## 🔄 POST-MERGE STATUS
- Repository successfully reconnected to GitHub remote
- Merge conflicts resolved with local versions taking precedence
- ClaudeProgress.md manually merged to preserve all history
- Ready for normal git operations (push/pull/commit)
EOF

echo "   ✅ ClaudeProgress.md merged successfully!"

echo ""
echo "4. 🔧 Resolving other conflicts with LOCAL versions..."

# Force local versions for all other conflicted files
git checkout --ours .DS_Store
git checkout --ours .gitignore
git checkout --ours backend/bridge.py
git checkout --ours backend/connection_manager.py
git checkout --ours backend/error_handler.py
git checkout --ours backend/main.py
git checkout --ours backend/requirements.txt
git checkout --ours backend/workflow.py
git checkout --ours hooks/use-websocket.ts
git checkout --ours lib/websocket/websocket-service.ts

# Stage all resolved files
git add .DS_Store .gitignore ClaudeProgress.md
git add backend/bridge.py backend/connection_manager.py backend/error_handler.py
git add backend/main.py backend/requirements.txt backend/workflow.py
git add hooks/use-websocket.ts lib/websocket/websocket-service.ts

echo ""
echo "5. 📊 Final merge status:"
git status

echo ""
echo "6. 🚀 Completing merge..."
git commit -m "Merge remote changes, keeping local versions

- ClaudeProgress.md: merged both local and remote progress
- All other files: kept local versions  
- Repository reconnected after git-filter-repo processing"

echo ""
echo "7. 📤 Pushing to remote..."
git push origin main

echo ""
echo "🎉 Merge conflict resolution completed!"
echo "✅ Repository is now synced with GitHub"

# Clean up
rm -f ClaudeProgress_local.md ClaudeProgress_remote.md