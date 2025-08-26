#!/bin/bash

# Simple git status check after merge attempt
cd "/Users/neill/Documents/AI Code/Projects/v0-botarmy-poc"

echo "=== Git Status Check ==="
echo "Current branch:"
git branch --show-current

echo -e "\nRepository status:"
git status

echo -e "\nStaged changes (if any):"
git diff --cached --name-only

echo -e "\nConflicts (if any):"
git diff --name-only --diff-filter=U

echo -e "\nRecent commits:"
git log --oneline -5
