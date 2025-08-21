#!/bin/bash

# Git Remote Recovery Script for v0-botarmy-poc
# This script fixes the repository after git-filter-repo removed remotes

echo "🔧 Git Remote Recovery Script"
echo "=============================="

# Navigate to project directory
cd "/Users/neill/Documents/AI Code/Projects/v0-botarmy-poc"

echo "📍 Current directory: $(pwd)"
echo ""

# Check current git status
echo "1. Checking current git status..."
git status --short
echo ""

# Check if any remotes exist
echo "2. Checking current remotes..."
git remote -v
echo ""

# Check current branch
echo "3. Current branch:"
git branch --show-current
echo ""

# We need to add the GitHub remote back
# First, let's check what the original remote URL might have been
echo "4. 🔍 MANUAL INPUT REQUIRED:"
echo "   What is your GitHub repository URL?"
echo "   Examples:"
echo "   - https://github.com/yourusername/v0-botarmy-poc.git"
echo "   - git@github.com:yourusername/v0-botarmy-poc.git"
echo ""
read -p "Enter your GitHub repository URL: " REPO_URL

if [ -z "$REPO_URL" ]; then
    echo "❌ No repository URL provided. Exiting."
    exit 1
fi

# Add the remote origin back
echo "5. Adding remote origin..."
git remote add origin "$REPO_URL"

# Verify the remote was added
echo "6. Verifying remote configuration..."
git remote -v
echo ""

# Check if we can fetch from the remote
echo "7. Testing connection to remote..."
if git ls-remote origin > /dev/null 2>&1; then
    echo "✅ Successfully connected to remote repository"
    
    # Fetch the latest changes
    echo "8. Fetching latest changes from remote..."
    git fetch origin
    
    # Check what branches exist on remote
    echo "9. Remote branches:"
    git branch -r
    echo ""
    
    # Set up tracking for main branch
    echo "10. Setting up branch tracking..."
    git branch --set-upstream-to=origin/main main
    
    # Check for any differences between local and remote
    echo "11. Checking for differences with remote..."
    git log --oneline main..origin/main --no-merges | head -10
    echo ""
    git log --oneline origin/main..main --no-merges | head -10
    echo ""
    
    echo "12. 🎯 Ready to push! Choose an option:"
    echo "    a) Force push (overwrites remote history with your local history)"
    echo "    b) Merge remote changes first (safer, but may create merge commits)"
    echo "    c) Exit and handle manually"
    echo ""
    read -p "Choose option (a/b/c): " PUSH_OPTION
    
    case $PUSH_OPTION in
        a)
            echo "🚀 Force pushing to remote..."
            git push --force-with-lease origin main
            echo "✅ Force push completed!"
            ;;
        b)
            echo "🔄 Pulling and merging remote changes..."
            git pull origin main --allow-unrelated-histories
            echo "🚀 Pushing merged changes..."
            git push origin main
            echo "✅ Merge and push completed!"
            ;;
        c)
            echo "⏸️  Stopping here. Your remote is configured."
            echo "    You can now manually handle the push as needed."
            ;;
        *)
            echo "❌ Invalid option. Remote is configured but not pushed."
            ;;
    esac
    
else
    echo "❌ Could not connect to remote repository"
    echo "   Please check:"
    echo "   - Repository URL is correct"
    echo "   - You have access permissions"
    echo "   - Repository exists on GitHub"
    exit 1
fi

echo ""
echo "🎉 Git remote recovery completed!"
echo "📊 Final status:"
git status
echo ""
git remote -v
