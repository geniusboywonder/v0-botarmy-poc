#!/bin/bash

# Script to check git status and merge remote branch
echo "=== BotArmy Git Status and Merge Script ==="

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

echo "=== All Local Branches ==="
git branch
echo ""

echo "=== All Remote Branches ==="
git branch -r
echo ""

echo "=== Fetching latest from remote ==="
git fetch origin
echo ""

echo "=== Available Branches After Fetch ==="
git branch -a
echo ""

echo "=== Checking if feature/enhanced-hitl-integration branch exists locally ==="
if git branch --list feature/enhanced-hitl-integration | grep -q feature/enhanced-hitl-integration; then
    echo "Local feature/enhanced-hitl-integration branch exists"

    # Switch to the local feature branch
    echo