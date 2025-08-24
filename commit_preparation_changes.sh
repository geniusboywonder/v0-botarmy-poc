#!/bin/bash

# Safe Commit Handler for Pre-Merge Changes
echo "🔧 BotArmy Pre-Merge Commit Handler"
echo "=================================="
echo "Date: $(date)"
echo

echo "📋 Current uncommitted changes:"
git status --short
echo

# Create meaningful commit for our Phase 1 and Phase 2 preparation work
echo "💾 Committing Phase 1-2 preparation changes..."

# Add all our preparation files
git add ClaudeProgress.md
git add MERGE_INSTRUCTIONS.md
git add backups/
git add check_git_status.sh
git add create_backup.sh
git add safe_branch_merge.sh
git add validate_environment.py

# Handle tests directory if it has content
if [ -d "tests" ] && [ "$(ls -A tests)" ]; then
    git add tests/
    echo "✅ Added tests directory"
fi

# Add gitignore changes if meaningful
git add .gitignore

# Skip .DS_Store (macOS system file)
echo "⏭️ Skipping .DS_Store (system file)"

# Create meaningful commit message
COMMIT_MSG="feat: Phase 1-2 integration preparation

- Add comprehensive backup system with rollback procedures
- Add environment validation and WebSocket URL corrections  
- Add safe branch merge scripts and documentation
- Update progress tracking for Phase 3 integration
- Prepare safety measures for Jules' work integration

Phase 1: ✅ Complete - Backup and environment validation
Phase 2: ⏳ Ready - Safe merge preparation complete"

git commit -m "$COMMIT_MSG"

if [ $? -eq 0 ]; then
    echo "✅ Pre-merge preparation changes committed successfully!"
    echo
    echo "📊 Current Status:"
    echo "Branch: $(git branch --show-current)"
    echo "Last commit: $(git log -1 --oneline)"
    echo "Working directory: $(git status --porcelain | wc -l) uncommitted files"
    
    if [ -z "$(git status --porcelain)" ]; then
        echo "✅ Working directory is now clean"
        echo
        echo "🚀 Ready to proceed with merge!"
        echo "You can now run: ./safe_branch_merge.sh"
    else
        echo "⚠️ Still some uncommitted changes:"
        git status --short
    fi
else
    echo "❌ Failed to commit changes"
    echo "Please check git status and resolve manually"
fi
