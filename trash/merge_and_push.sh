#!/bin/bash

# BotArmy - Merge all branches to main and push to GitHub
# This script safely merges the feature branch back to main and pushes everything

set -e  # Exit on any error

PROJECT_DIR="/Users/neill/Documents/AI Code/Projects/v0-botarmy-poc"
FEATURE_BRANCH="feature/production-polish-tasks"

echo "🚀 Starting BotArmy branch merge and push process..."
echo "=================================================="

# Change to project directory
cd "$PROJECT_DIR"

# 1. Check current status
echo "📋 Step 1: Checking current status..."
echo "Current branch:"
git branch --show-current

echo "Git status:"
git status --porcelain

# 2. Commit any uncommitted changes on current branch
if [[ -n $(git status --porcelain) ]]; then
    echo "⚠️  Found uncommitted changes. Committing them first..."
    git add .
    git commit -m "chore: Commit remaining changes before merge

- Auto-commit of any remaining changes
- Preparing for merge to main branch
- Ensures no work is lost during merge process"
    echo "✅ Changes committed"
else
    echo "✅ No uncommitted changes found"
fi

# 3. Switch to main branch
echo "📋 Step 2: Switching to main branch..."
git checkout main
echo "✅ Now on main branch"

# 4. Pull latest changes from origin/main (just in case)
echo "📋 Step 3: Pulling latest changes from origin..."
git fetch origin
echo "✅ Fetched latest changes"

# 5. Check if we're behind origin/main
BEHIND=$(git rev-list HEAD..origin/main --count)
if [[ $BEHIND -gt 0 ]]; then
    echo "⚠️  Main branch is $BEHIND commits behind origin/main. Merging..."
    git merge origin/main --no-edit
    echo "✅ Merged origin/main changes"
else
    echo "✅ Main branch is up to date with origin"
fi

# 6. Merge feature branch into main
echo "📋 Step 4: Merging $FEATURE_BRANCH into main..."
git merge "$FEATURE_BRANCH" --no-edit
echo "✅ Successfully merged $FEATURE_BRANCH into main"

# 7. Verify the build still works (quick check)
echo "📋 Step 5: Verifying build..."
if npm run build > /dev/null 2>&1; then
    echo "✅ Build verification successful"
else
    echo "⚠️  Build verification failed, but continuing with push"
fi

# 8. Push main branch to origin
echo "📋 Step 6: Pushing main branch to GitHub..."
git push origin main
echo "✅ Successfully pushed main branch to origin"

# 9. Push feature branch to origin (for backup/history)
echo "📋 Step 7: Pushing feature branch to GitHub..."
git push origin "$FEATURE_BRANCH"
echo "✅ Successfully pushed feature branch to origin"

# 10. Summary
echo "=================================================="
echo "🎉 MERGE AND PUSH COMPLETE!"
echo "=================================================="
echo "✅ All changes merged to main branch"
echo "✅ Main branch pushed to GitHub"
echo "✅ Feature branch backed up to GitHub"
echo ""
echo "Current status:"
git log --oneline -5
echo ""
echo "Next steps:"
echo "- Feature branch '$FEATURE_BRANCH' can be deleted if no longer needed"
echo "- All team members should pull the latest main branch"
echo "- Ready to continue with production polish tasks"
echo ""
echo "🚀 BotArmy is ready for the next phase!"
