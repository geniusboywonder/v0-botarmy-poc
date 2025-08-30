#!/bin/bash

# BotArmy HITL Branch Merge - Safe Execution Script
# This script creates a merge branch and attempts to merge the HITL feature

echo "=== BotArmy HITL Feature Merge Process ==="
echo "Date: $(date)"
echo "Working directory: $(pwd)"
echo

# Navigate to project directory
cd "/Users/neill/Documents/AI Code/Projects/v0-botarmy-poc" || exit 1

# Verify we're in the right place
if [ ! -f "package.json" ] || [ ! -d "backend" ]; then
    echo "❌ Error: Not in the correct project directory"
    exit 1
fi

echo "✅ Project directory confirmed"

# Check current branch and status
echo
echo "📋 Current Repository State:"
echo "Current branch: $(git branch --show-current)"
echo "Git status:"
git status --porcelain

# Fetch latest remote changes
echo
echo "🔄 Fetching latest remote changes..."
git fetch origin

# Verify the HITL branch exists
echo
echo "🔍 Checking for HITL branch..."
if git show-ref --verify --quiet refs/remotes/origin/feature/human-in-the-loop; then
    echo "✅ origin/feature/human-in-the-loop branch found"
    echo "Latest commit:"
    git log origin/feature/human-in-the-loop --oneline -1
else
    echo "❌ Error: origin/feature/human-in-the-loop branch not found"
    echo "Available remote branches:"
    git branch -r
    exit 1
fi

# Create merge branch for safety
echo
echo "🌿 Creating merge branch..."
if git show-ref --verify --quiet refs/heads/merge/human-in-the-loop; then
    echo "Branch merge/human-in-the-loop already exists. Deleting..."
    git branch -D merge/human-in-the-loop
fi

git checkout -b merge/human-in-the-loop

# Perform the merge (without committing)
echo
echo "🔀 Attempting to merge origin/feature/human-in-the-loop..."
if git merge origin/feature/human-in-the-loop --no-commit --no-ff; then
    echo "✅ Merge completed successfully"
    echo
    echo "📊 Merge Status:"
    git status --short
    echo
    echo "📝 Files changed:"
    git diff --cached --name-only
    echo
    echo "🎯 Ready for review and testing"
    echo "To complete the merge: git commit"
    echo "To abort the merge: git merge --abort"
else
    echo "⚠️ Merge conflicts detected"
    echo
    echo "📊 Conflict Status:"
    git status --short
    echo
    echo "🔧 Files with conflicts:"
    git diff --name-only --diff-filter=U
    echo
    echo "Next steps:"
    echo "1. Resolve conflicts manually"
    echo "2. Stage resolved files: git add <file>"
    echo "3. Complete merge: git commit"
    echo "4. Or abort: git merge --abort"
fi

echo
echo "=== Merge preparation complete ==="
