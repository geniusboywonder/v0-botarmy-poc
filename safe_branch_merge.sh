#!/bin/bash

# Safe Branch Merge Script for BotArmy Integration
echo "🚀 BotArmy Safe Branch Merge - Phase 2"
echo "========================================"
echo "Date: $(date)"
echo

# Step 1: Check current status
echo "📊 Step 1: Checking current git status..."
echo "Current branch: $(git branch --show-current)"
echo "Current commit: $(git log -1 --oneline)"
echo

# Check for uncommitted changes
if [ ! -z "$(git status --porcelain)" ]; then
    echo "⚠️ WARNING: Uncommitted changes detected!"
    echo "Please commit or stash changes before proceeding."
    git status --short
    exit 1
fi

echo "✅ Working directory is clean"
echo

# Step 2: Fetch latest changes from remote
echo "📡 Step 2: Fetching latest remote changes..."
git fetch origin

if [ $? -ne 0 ]; then
    echo "❌ Failed to fetch remote changes"
    exit 1
fi

echo "✅ Remote changes fetched successfully"
echo

# Step 3: Switch to main branch
echo "🔄 Step 3: Switching to main branch..."
git checkout main

if [ $? -ne 0 ]; then
    echo "❌ Failed to checkout main branch"
    echo "Attempting to checkout origin/main..."
    git checkout -b main origin/main
    if [ $? -ne 0 ]; then
        echo "❌ Could not access main branch"
        exit 1
    fi
fi

echo "✅ Now on main branch: $(git branch --show-current)"
echo "Main branch commit: $(git log -1 --oneline)"
echo

# Step 4: Create integration branch
INTEGRATION_BRANCH="integration/enhanced-hitl-final"
echo "🌿 Step 4: Creating integration branch: $INTEGRATION_BRANCH"

# Delete existing integration branch if it exists
git branch -D "$INTEGRATION_BRANCH" 2>/dev/null && echo "🗑️ Removed existing integration branch"

# Create new integration branch from main
git checkout -b "$INTEGRATION_BRANCH"

if [ $? -ne 0 ]; then
    echo "❌ Failed to create integration branch"
    exit 1
fi

echo "✅ Integration branch created: $(git branch --show-current)"
echo

# Step 5: Merge Jules' work
echo "🔀 Step 5: Merging Jules' enhanced HITL work..."
echo "Source branch: feature/enhanced-hitl-integration-final"
echo "Target branch: $INTEGRATION_BRANCH"
echo

# Attempt merge
git merge feature/enhanced-hitl-integration-final --no-edit

MERGE_RESULT=$?

if [ $MERGE_RESULT -eq 0 ]; then
    echo "✅ Merge completed successfully!"
    echo "New commit: $(git log -1 --oneline)"
    echo
    echo "📊 Merge Summary:"
    echo "Files changed: $(git diff --name-only HEAD~1 | wc -l)"
    echo "Recent commits:"
    git log --oneline -5
    echo
    echo "🎉 PHASE 2 STEP 1 COMPLETE: Integration branch created and merged"
    echo
    echo "Next steps:"
    echo "1. Validate merge results"
    echo "2. Check for missing dependencies" 
    echo "3. Test integration branch functionality"
    
else
    echo "⚠️ Merge conflicts detected or merge failed"
    echo "Merge result code: $MERGE_RESULT"
    echo
    echo "📋 Conflict Resolution Required:"
    echo "Run 'git status' to see conflicts"
    echo "Resolve conflicts manually"
    echo "Then run 'git add .' and 'git commit'"
    echo
    echo "Or to abort merge: 'git merge --abort'"
fi

echo
echo "🔍 Current Status:"
echo "Branch: $(git branch --show-current)"
echo "Status: $(git status --porcelain | wc -l) files with changes"

if [ -z "$(git status --porcelain)" ]; then
    echo "✅ Working directory clean - merge successful"
else
    echo "⚠️ Changes detected - may need conflict resolution"
    git status --short
fi
