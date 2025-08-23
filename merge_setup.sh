#!/bin/bash

# BotArmy HITL Branch Merge Script
echo "=== BotArmy HITL Branch Merge Setup ==="

cd "/Users/neill/Documents/AI Code/Projects/v0-botarmy-poc"

# Check current status
echo "Current branch:"
git branch --show-current

echo -e "\nGit status:"
git status --short

echo -e "\nFetching latest remote changes..."
git fetch origin

echo -e "\nAvailable remote branches:"
git branch -r | grep -E "(hitl|human-in-the-loop)"

echo -e "\nCreating merge branch..."
git checkout -b merge/human-in-the-loop

echo -e "\nAttempting to merge origin/feature/human-in-the-loop..."
git merge origin/feature/human-in-the-loop --no-commit --no-ff

echo -e "\nMerge status:"
git status --short

echo "=== Merge preparation complete. Check status before proceeding ==="
