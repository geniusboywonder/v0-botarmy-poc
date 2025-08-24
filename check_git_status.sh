#!/bin/bash

# Git Status Check Script
echo "=== BotArmy Git Status Check ==="
echo "Date: $(date)"
echo "Working Directory: $(pwd)"
echo

echo "=== Current Branch ==="
git branch --show-current
echo

echo "=== Git Status ==="
git status --porcelain
echo

echo "=== Recent Commits (Last 5) ==="
git log --oneline -5
echo

echo "=== Remote Branches ==="
git branch -r
echo

echo "=== Local Branches ==="
git branch
echo

echo "=== Uncommitted Changes Check ==="
if [ -z "$(git status --porcelain)" ]; then
    echo "✅ Working directory is clean"
else
    echo "⚠️ Uncommitted changes detected:"
    git status --short
fi
echo

echo "=== Status Check Complete ==="
