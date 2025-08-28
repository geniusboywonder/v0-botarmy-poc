#!/bin/bash
# Git operations for test framework merge

cd /Users/neill/Documents/AI\ Code/Projects/v0-botarmy-poc

echo "Current working directory: $(pwd)"
echo "Current branch: $(cat .git/HEAD)"

# Check if we can switch to main
if [ -f ".git/refs/heads/main" ]; then
    echo "Main branch exists, switching..."
    echo "ref: refs/heads/main" > .git/HEAD
    echo "Switched to main branch"
    echo "New branch: $(cat .git/HEAD)"
else
    echo "Main branch not found"
    ls -la .git/refs/heads/
fi