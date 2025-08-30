#!/bin/bash

# BotArmy Git Status Utility
# Comprehensive git status and branch information for the project

set -e

PROJECT_PATH="/Users/neill/Documents/AI Code/Projects/v0-botarmy-poc"

echo "🔍 BotArmy Git Status & Branch Information"
echo "========================================="
echo "Date: $(date)"
echo "Working Directory: $PROJECT_PATH"
echo

# Change to project directory
cd "$PROJECT_PATH"

echo "📍 Current Branch:"
current_branch=$(git branch --show-current)
echo "  → $current_branch"
echo

echo "📊 Git Status:"
if [ -z "$(git status --porcelain)" ]; then
    echo "  ✅ Working directory is clean"
else
    echo "  ⚠️  Uncommitted changes detected:"
    git status --short | sed 's/^/    /'
fi
echo

echo "📚 Recent Commits (Last 5):"
git log --oneline -5 | sed 's/^/  /'
echo

echo "🌍 Remote Branches:"
git branch -r | sed 's/^/  /'
echo

echo "💻 Local Branches:"
git branch | sed 's/^/  /'
echo

echo "🔄 Remote Status Check:"
echo "  Fetching latest from remote..."
git fetch origin --quiet
echo "  ✅ Remote fetch complete"

# Check for specific branches of interest
echo "🔎 Special Branch Check:"
if git show-ref --verify --quiet refs/remotes/origin/feature/human-in-the-loop; then
    echo "  ✅ human-in-the-loop branch exists on remote"
else
    echo "  ❌ human-in-the-loop branch not found on remote"
fi

if git show-ref --verify --quiet refs/remotes/origin/main; then
    echo "  ✅ main branch exists on remote"
else
    echo "  ❌ main branch not found on remote"
fi

echo
echo "✨ Git Status Check Complete"
