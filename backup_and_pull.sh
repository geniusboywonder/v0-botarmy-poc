#!/bin/bash
set -e  # Exit on any error

echo "=== BotArmy Code Review - Backup & Branch Pull ==="
echo "Date: $(date)"

# Navigate to project directory
cd "/Users/neill/Documents/AI Code/Projects/v0-botarmy-poc"

echo "=== Step 1: Current Git Status Check ==="
echo "Current directory: $(pwd)"
current_branch=$(git branch --show-current 2>/dev/null || echo "detached")
echo "Current branch: $current_branch"

# Check for uncommitted changes
if [ ! -z "$(git status --porcelain 2>/dev/null)" ]; then
    echo "⚠️  Uncommitted changes detected:"
    git status --short
    echo "Creating stash before proceeding..."
    git stash push -m "Auto-stash before process-refactor review - $(date +%Y%m%d-%H%M%S)"
    echo "✅ Changes stashed successfully"
else
    echo "✅ Working directory clean"
fi

echo "=== Step 2: Create Backup of Current State ==="
backup_branch="backup-${current_branch}-$(date +%Y%m%d-%H%M%S)"
echo "Creating backup branch: $backup_branch"
git checkout -b "$backup_branch" 2>/dev/null || {
    echo "❌ Failed to create backup branch"
    exit 1
}

# Return to original branch
git checkout "$current_branch" 2>/dev/null || {
    echo "❌ Failed to return to original branch"
    exit 1
}

echo "✅ Backup created: $backup_branch"

echo "=== Step 3: Fetch Latest Remote Changes ==="
git fetch origin --prune
echo "✅ Remote changes fetched"

echo "=== Step 4: Check for Feature Branch ==="
if git show-ref --verify --quiet refs/remotes/origin/feature/process-view-refactor-1; then
    echo "✅ Feature branch found on remote: feature/process-view-refactor-1"
    
    echo "=== Step 5: Switch to Feature Branch ==="
    # Check if local branch exists
    if git show-ref --verify --quiet refs/heads/feature/process-view-refactor-1; then
        echo "Local branch exists, switching and updating..."
        git checkout feature/process-view-refactor-1
        git pull origin feature/process-view-refactor-1
    else
        echo "Creating new local tracking branch..."
        git checkout -b feature/process-view-refactor-1 origin/feature/process-view-refactor-1
    fi
    
    echo "✅ Successfully switched to feature branch"
    
    echo "=== Step 6: Verify Branch State ==="
    current_branch_final=$(git branch --show-current)
    echo "Current branch: $current_branch_final"
    echo "Latest commits:"
    git log --oneline -5
    
    echo "=== SUCCESS: Branch switch complete ==="
    echo "Backup branch: $backup_branch"
    echo "Current branch: $current_branch_final"
    
else
    echo "❌ Feature branch 'feature/process-view-refactor-1' not found on remote"
    echo "Available remote branches:"
    git branch -r | grep -v HEAD
    exit 1
fi

echo "=== Backup and Pull Complete ==="
