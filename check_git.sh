#!/bin/bash

# Test git access and repository state
cd "/Users/neill/Documents/AI Code/Projects/v0-botarmy-poc"

echo "=== Git Repository Analysis ==="
echo "Current directory: $(pwd)"
echo "Current branch: $(git branch --show-current)"
echo -e "\nLocal branches:"
git branch

echo -e "\nRemote branches:"
git branch -r

echo -e "\nLatest commits on main:"
git log --oneline -5

echo -e "\nChecking for HITL branch..."
git ls-remote origin | grep -E "(hitl|human-in-the-loop)"

echo -e "\nRepository status:"
git status
