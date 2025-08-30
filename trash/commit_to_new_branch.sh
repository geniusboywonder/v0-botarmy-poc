#!/bin/bash

# Script to commit all changes to a new branch and push to remote
# Usage: ./commit_to_new_branch.sh <new-branch-name>

# Check if a branch name was provided
if [ -z "$1" ]; then
    echo "Error: Please provide a new branch name."
    echo "Usage: $0 <new-branch-name>"
    exit 1
fi

NEW_BRANCH="$1"

# Stage all changes (modified, deleted, untracked)
git add .

# Verify staged changes
echo "Staged changes:"
git status

# Create and switch to new branch
git checkout -b "$NEW_BRANCH"

# Commit changes
git commit -m "Add all changes from feature/enhanced-hitl-integration-final to $NEW_BRANCH"

# Push to remote
git push origin "$NEW_BRANCH"

# Switch back to original branch
git checkout feature/enhanced-hitl-integration-final

# Notify user
echo "Changes committed to $NEW_BRANCH and pushed to origin/$NEW_BRANCH."
echo "Back on feature/enhanced-hitl-integration-final."