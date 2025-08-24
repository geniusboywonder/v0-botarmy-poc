#!/bin/bash

# Script to fetch and merge the remote enhanced-hitl-integration-final branch
echo "=== BotArmy Enhanced HITL Integration Merge Script ==="

# Change to project directory
cd "/Users/neill/Documents/AI Code/Projects/v0-botarmy-poc" || exit 1

echo "Current directory: $(pwd)"
echo ""

echo "=== Current Git Status ==="
git status
echo ""

echo "=== Current Branch ==="
git branch --show-current
echo ""

echo "=== Fetching latest from remote ==="
git fetch origin
echo ""

echo "=== Available Remote Branches ==="
git branch -r | grep enhanced-hitl
echo ""

echo "=== Checking if local feature/enhanced-hitl-integration branch exists ==="
if git branch --list feature/enhanced-hitl-integration | grep -q feature/enhanced-hitl-integration; then
    echo "Local feature/enhanced-hitl-integration branch exists - switching to it"
    git checkout feature/enhanced-hitl-integration
else
    echo "Creating local feature/enhanced-hitl-integration branch"
    git checkout -b feature/enhanced-hitl-integration
fi
echo ""

echo "=== Merging remote feature/enhanced-hitl-integration-final into local branch ==="
git merge origin/feature/enhanced-hitl-integration-final
echo ""

echo "=== Merge Status ==="
git status
echo ""

echo "=== Updated ClaudeProgress.md Preview ==="
if [ -f "ClaudeProgress.md" ]; then
    echo "First 50 lines of updated ClaudeProgress.md:"
    head -50 ClaudeProgress.md
else
    echo "ClaudeProgress.md not found after merge"
fi

echo ""
echo "=== Merge Complete - Ready for Code Review ==="
