#!/bin/bash
cd "/Users/neill/Documents/AI Code/Projects/v0-botarmy-poc"

echo "=== Fetching all remote branches ==="
git fetch --all

echo -e "\n=== Looking for Jules' branch ==="
git branch -r | grep -E "(enhanced-hitl|hitl-integration)"

echo -e "\n=== Current branch ==="
git branch --show-current

echo -e "\n=== Checking out Jules' branch ==="
git checkout feature/enhanced-hitl-integration-final

echo -e "\n=== Branch switched successfully ==="
git branch --show-current

echo -e "\n=== Latest commits on this branch ==="
git log --oneline -5
