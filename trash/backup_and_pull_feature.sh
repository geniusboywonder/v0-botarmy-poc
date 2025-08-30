#!/bin/bash

echo "=== BotArmy Main Branch Backup & Feature Branch Pull ==="
echo "Date: $(date)"
echo

# Change to project directory
cd /Users/neill/Documents/AI\ Code/Projects/v0-botarmy-poc

echo "=== Step 1: Check Current Git Status ==="
./check_git_status.sh

echo "=== Step 2: Stash Any Uncommitted Changes ==="
if [ ! -z "$(git status --porcelain)" ]; then
    echo "Stashing uncommitted changes..."
    git stash push -m "Auto-stash before branch switch - $(date)"
else
    echo "✅ No changes to stash - working directory clean"
fi

echo "=== Step 3: Create Backup Branch ==="
current_branch=$(git branch --show-current)
backup_branch="backup-${current_branch}-$(date +%Y%m%d-%H%M%S)"
echo "Creating backup branch: $backup_branch"
git checkout -b "$backup_branch"
git checkout "$current_branch"
echo "✅ Backup branch created: $backup_branch"

echo "=== Step 4: Fetch Remote Changes ==="
git fetch origin

echo "=== Step 5: Check if Feature Branch Exists Remotely ==="
if git show-ref --verify --quiet refs/remotes/origin/feature/process-view-refactor-1; then
    echo "✅ Feature branch exists on remote"
    
    echo "=== Step 6: Pull Feature Branch ==="
    git checkout -b feature/process-view-refactor-1 origin/feature/process-view-refactor-1 || \
    git checkout feature/process-view-refactor-1 && git pull origin feature/process-view-refactor-1
    
    echo "✅ Successfully switched to feature branch"
    
    echo "=== Step 7: Verify Branch Switch ==="
    current_branch_after=$(git branch --show-current)
    echo "Current branch: $current_branch_after"
    git log --oneline -3
    
else
    echo "❌ Feature branch 'feature/process-view-refactor-1' not found on remote"
    echo "Available remote branches:"
    git branch -r
    exit 1
fi

echo "=== Backup and Branch Pull Complete ==="
