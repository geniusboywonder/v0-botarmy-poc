#!/bin/bash
cd "/Users/neill/Documents/AI Code/Projects/v0-botarmy-poc"

echo "=== CURRENT GIT STATUS ==="
echo "Current branch:"
cat .git/HEAD

echo ""
echo "Current commit:"
if [[ -f ".git/refs/heads/feature/production-polish-tasks" ]]; then
    echo "Feature branch commit: $(cat .git/refs/heads/feature/production-polish-tasks)"
fi

if [[ -f ".git/refs/heads/main" ]]; then
    echo "Main branch commit: $(cat .git/refs/heads/main)"
fi

if [[ -f ".git/refs/remotes/origin/main" ]]; then
    echo "Origin main commit: $(cat .git/refs/remotes/origin/main)"
fi

echo ""
echo "=== CHECKING FOR UNCOMMITTED CHANGES ==="
# This is a simple check - in practice you'd use git status
echo "Recent file modifications:"
find . -name "*.ts" -o -name "*.tsx" -o -name "*.py" -o -name "*.md" -newer .git/refs/heads/feature/production-polish-tasks | head -10
