# Manual Backup & Branch Switch Instructions

## Current Status
- We're on the `main` branch  
- Need to backup current state and switch to `feature/process-view-refactor-1`
- The backup script `backup_and_pull.sh` is ready to execute

## Option 1: Run the Automated Script (Recommended)

Open Terminal and run these commands:

```bash
cd "/Users/neill/Documents/AI Code/Projects/v0-botarmy-poc"
chmod +x backup_and_pull.sh
./backup_and_pull.sh
```

## Option 2: Manual Step-by-Step (if script fails)

```bash
# 1. Navigate to project
cd "/Users/neill/Documents/AI Code/Projects/v0-botarmy-poc"

# 2. Check current status
git status
git branch --show-current

# 3. Stash any uncommitted changes
git stash push -m "Auto-stash before process-refactor review - $(date)"

# 4. Create backup branch
git checkout -b "backup-main-$(date +%Y%m%d-%H%M%S)"
git checkout main

# 5. Fetch remote changes  
git fetch origin --prune

# 6. Check if feature branch exists
git branch -r | grep process-view-refactor

# 7. Switch to feature branch
git checkout -b feature/process-view-refactor-1 origin/feature/process-view-refactor-1

# 8. Verify success
git branch --show-current
git log --oneline -3
```

## Expected Result
- Current branch should be: `feature/process-view-refactor-1`
- Should see recent commits from Jules showing the process view refactor

## After Success
Report back with:
1. Current branch name
2. Last 3 commit messages
3. Any errors encountered

Then I'll proceed with testing the refactored code.
