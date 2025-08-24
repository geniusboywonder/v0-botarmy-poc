#!/bin/bash

# Create Backup Script for BotArmy Integration
echo "=== BotArmy State Backup Script ==="
echo "Date: $(date)"
echo

# Create backup directory with timestamp
BACKUP_DIR="backups/pre-merge-$(date +%Y%m%d_%H%M%S)"
echo "Creating backup directory: $BACKUP_DIR"
mkdir -p "$BACKUP_DIR"

echo "=== Step 1: Git State Backup ==="
# Save current git state
echo "Current branch: $(git branch --show-current)" > "$BACKUP_DIR/git-state.txt"
echo "Git status:" >> "$BACKUP_DIR/git-state.txt"
git status >> "$BACKUP_DIR/git-state.txt"
echo "" >> "$BACKUP_DIR/git-state.txt"
echo "Recent commits:" >> "$BACKUP_DIR/git-state.txt"
git log --oneline -10 >> "$BACKUP_DIR/git-state.txt"

# Create branch backup
echo "Creating branch backup..."
git branch -a > "$BACKUP_DIR/all-branches.txt"
git log --all --graph --decorate --oneline -20 > "$BACKUP_DIR/git-history.txt"

echo "=== Step 2: Key Configuration Backup ==="
# Backup critical configuration files
cp .env "$BACKUP_DIR/.env.backup" 2>/dev/null || echo "No .env file found"
cp .env.local "$BACKUP_DIR/.env.local.backup" 2>/dev/null || echo "No .env.local file found"
cp .env.replit "$BACKUP_DIR/.env.replit.backup" 2>/dev/null || echo "No .env.replit file found"
cp package.json "$BACKUP_DIR/package.json.backup"
cp requirements.txt "$BACKUP_DIR/requirements.txt.backup" 2>/dev/null || echo "No requirements.txt found"

echo "=== Step 3: Current State Documentation ==="
# Document current working state
echo "=== Current Working State Documentation ===" > "$BACKUP_DIR/current-state.md"
echo "Date: $(date)" >> "$BACKUP_DIR/current-state.md"
echo "Branch: $(git branch --show-current)" >> "$BACKUP_DIR/current-state.md"
echo "Last Commit: $(git log -1 --oneline)" >> "$BACKUP_DIR/current-state.md"
echo "" >> "$BACKUP_DIR/current-state.md"

echo "## Project Structure" >> "$BACKUP_DIR/current-state.md"
tree -L 2 -I 'node_modules|__pycache__|.git|.next|venv' >> "$BACKUP_DIR/current-state.md" 2>/dev/null || ls -la >> "$BACKUP_DIR/current-state.md"

echo "## Key Files Present" >> "$BACKUP_DIR/current-state.md"
echo "- Backend main.py: $(test -f backend/main.py && echo "✅ Present" || echo "❌ Missing")" >> "$BACKUP_DIR/current-state.md"
echo "- Frontend page.tsx: $(test -f app/page.tsx && echo "✅ Present" || echo "❌ Missing")" >> "$BACKUP_DIR/current-state.md"
echo "- Package.json: $(test -f package.json && echo "✅ Present" || echo "❌ Missing")" >> "$BACKUP_DIR/current-state.md"
echo "- WebSocket service: $(test -f lib/websocket/websocket-service.ts && echo "✅ Present" || echo "❌ Missing")" >> "$BACKUP_DIR/current-state.md"

echo "=== Step 4: Create Rollback Instructions ==="
cat > "$BACKUP_DIR/ROLLBACK_INSTRUCTIONS.md" << 'EOF'
# Rollback Instructions

## To Rollback to Pre-Merge State:

### 1. Reset to Current Branch State
```bash
# If currently on a different branch, switch back
git checkout feature/enhanced-hitl-integration-final

# Reset any uncommitted changes
git reset --hard HEAD
git clean -fd
```

### 2. Restore Configuration Files
```bash
# Restore environment files if needed
cp backups/pre-merge-TIMESTAMP/.env.backup .env
cp backups/pre-merge-TIMESTAMP/.env.local.backup .env.local
cp backups/pre-merge-TIMESTAMP/.env.replit.backup .env.replit
```

### 3. Verify Rollback Success
```bash
# Check branch
git branch --show-current

# Check status
git status

# Check last commit matches backup
git log -1 --oneline
```

### 4. Test Functionality
- Start backend: `python backend/main.py`
- Start frontend: `npm run dev`
- Test WebSocket connection
- Verify basic functionality

## Emergency Contact
If rollback fails, check the backup files in this directory and restore manually.
EOF

echo "=== Backup Complete ==="
echo "Backup location: $BACKUP_DIR"
echo "✅ Git state saved"
echo "✅ Configuration files backed up"
echo "✅ Current state documented"
echo "✅ Rollback instructions created"
echo ""
echo "To rollback: Follow instructions in $BACKUP_DIR/ROLLBACK_INSTRUCTIONS.md"
