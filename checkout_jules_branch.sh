#!/bin/bash
cd "/Users/neill/Documents/AI Code/Projects/v0-botarmy-poc"

echo "Starting branch checkout process..."
echo "Current directory: $(pwd)"

echo "Fetching all remote branches..."
git fetch --all 2>&1

echo "Current branch before checkout:"
git branch --show-current

echo "Checking out Jules' branch..."
git checkout feature/enhanced-hitl-integration-final 2>&1

echo "Current branch after checkout:"
git branch --show-current

echo "Latest 5 commits on this branch:"
git log --oneline -5

echo "Checkout process complete!"
