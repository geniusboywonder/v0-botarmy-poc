#!/bin/bash

# Fix Push Rejection Script
# Handles the "fetch first" error after secret removal

echo "🔄 Fix Push Rejection Script"
echo "============================"

cd "/Users/neill/Documents/AI Code/Projects/v0-botarmy-poc"

echo "📍 Current directory: $(pwd)"
echo ""

echo "1. 🔍 Checking current status..."
git status --short
echo ""

echo "2. 📥 Fetching latest changes from remote..."
git fetch origin

echo ""
echo "3. 📊 Comparing local and remote branches..."
echo "   Local commits ahead of remote:"
git log --oneline origin/main..main --no-merges | head -5
echo ""
echo "   Remote commits ahead of local:"
git log --oneline main..origin/main --no-merges | head -5
echo ""

echo "4. 🎯 RESOLUTION OPTIONS:"
echo "   A) Force push (overwrites remote with your local history)"
echo "   B) Pull and merge (safer, preserves remote changes)"
echo ""

read -p "Choose option (A/B): " OPTION

case $OPTION in
    A|a)
        echo ""
        echo "5A. 🚀 Force pushing to remote..."
        echo "    This will overwrite the remote repository with your local history."
        read -p "Are you sure? (y/N): " CONFIRM
        
        if [[ $CONFIRM =~ ^[Yy]$ ]]; then
            git push --force-with-lease origin main
            if [ $? -eq 0 ]; then
                echo "   ✅ Force push successful!"
            else
                echo "   ❌ Force push failed. Check error above."
            fi
        else
            echo "   ⏸️ Force push cancelled."
        fi
        ;;
        
    B|b)
        echo ""
        echo "5B. 🔄 Pulling and merging remote changes..."
        git pull origin main --allow-unrelated-histories
        
        if [ $? -eq 0 ]; then
            echo "   ✅ Pull successful!"
            echo ""
            echo "6. 📤 Pushing merged changes..."
            git push origin main
            
            if [ $? -eq 0 ]; then
                echo "   ✅ Push successful!"
            else
                echo "   ❌ Push failed. Check error above."
            fi
        else
            echo "   ❌ Pull failed. You may have merge conflicts to resolve."
            echo "   Run: git status"
        fi
        ;;
        
    *)
        echo "❌ Invalid option selected"
        exit 1
        ;;
esac

echo ""
echo "🎉 Push issue resolution completed!"
echo "📊 Final status:"
git status
echo ""
git log --oneline -3