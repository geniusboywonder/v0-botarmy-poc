#!/bin/bash

# Secret Removal and Push Fix Script
# Removes OpenAI API key from git history and enables successful push

echo "🔐 Secret Removal and Push Fix Script"
echo "====================================="

cd "/Users/neill/Documents/AI Code/Projects/v0-botarmy-poc"

echo "📍 Current directory: $(pwd)"
echo ""

echo "1. 🔍 Analyzing the secret detection..."
echo "   GitHub detected an OpenAI API key in:"
echo "   - Commit: 0f097d8182beb3505c734f325cac9f87d8feac6e"
echo "   - File: startapp.txt:2"
echo ""

echo "2. 🕵️ Checking if startapp.txt exists in current working directory..."
if [ -f "startapp.txt" ]; then
    echo "   ✅ Found startapp.txt in working directory"
    echo "   Content preview:"
    head -5 startapp.txt
else
    echo "   ❌ startapp.txt not found in working directory"
    echo "   It may only exist in git history"
fi
echo ""

echo "3. 🧹 SOLUTION OPTIONS:"
echo "   A) Remove file from git history completely (safest)"
echo "   B) Add file to .gitignore and remove from tracking"
echo "   C) Allow the secret on GitHub (not recommended)"
echo ""

read -p "Choose option (A/B/C): " OPTION

case $OPTION in
    A|a)
        echo ""
        echo "4A. 🗑️ Removing startapp.txt from entire git history..."
        
        # Use git filter-branch to remove the file from all commits
        git filter-branch --force --index-filter \
            'git rm --cached --ignore-unmatch startapp.txt' \
            --prune-empty --tag-name-filter cat -- --all
        
        # Alternative using BFG if filter-branch fails
        if [ $? -ne 0 ]; then
            echo "   Filter-branch failed, trying git-filter-repo..."
            git filter-repo --path startapp.txt --invert-paths --force
        fi
        
        echo "   ✅ File removed from git history"
        ;;
        
    B|b)
        echo ""
        echo "4B. 🙈 Adding startapp.txt to .gitignore and removing from tracking..."
        
        # Add to .gitignore if not already there
        if ! grep -q "startapp.txt" .gitignore 2>/dev/null; then
            echo "startapp.txt" >> .gitignore
            echo "   ✅ Added startapp.txt to .gitignore"
        else
            echo "   ✅ startapp.txt already in .gitignore"
        fi
        
        # Remove from git tracking if it exists
        git rm --cached startapp.txt 2>/dev/null || echo "   File not currently tracked"
        
        # Commit the .gitignore change
        git add .gitignore
        git commit -m "Add startapp.txt to .gitignore to hide secrets"
        
        echo "   ⚠️  WARNING: File still exists in git history!"
        echo "   The secret is still in previous commits."
        echo "   For complete security, choose option A instead."
        ;;
        
    C|c)
        echo ""
        echo "4C. ⚠️ Allowing secret on GitHub (NOT RECOMMENDED)..."
        echo "   You can manually allow this secret using the GitHub link:"
        echo "   https://github.com/geniusboywonder/v0-botarmy-poc/security/secret-scanning/unblock-secret/31bHkZGDLXLCcoNN7F348wjvvT8"
        echo ""
        echo "   🚨 WARNING: This exposes your API key publicly!"
        echo "   Only do this if the key is already invalid/rotated."
        exit 0
        ;;
        
    *)
        echo "❌ Invalid option selected"
        exit 1
        ;;
esac

echo ""
echo "5. 🧹 Cleaning up filter-branch references..."
# Clean up refs created by filter-branch
git for-each-ref --format='delete %(refname)' refs/original | git update-ref --stdin
git reflog expire --expire=now --all
git gc --prune=now

echo ""
echo "6. 📤 Attempting to push to remote..."
git push --force-with-lease origin main

if [ $? -eq 0 ]; then
    echo "   ✅ Push successful!"
    echo ""
    echo "🎉 Secret removal and push completed!"
    echo "📊 Final status:"
    git status
    git remote -v
else
    echo "   ❌ Push failed. Check the error message above."
    echo ""
    echo "🔍 Troubleshooting:"
    echo "   - If secrets still detected, the file may exist in other commits"
    echo "   - Try running the script again with option A"
    echo "   - Check for other files containing secrets"
fi

echo ""
echo "📋 Next Steps:"
echo "1. Rotate any exposed API keys for security"
echo "2. Update your .env file with new keys"
echo "3. Verify the repository is working: git pull origin main"