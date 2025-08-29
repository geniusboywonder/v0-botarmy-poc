#!/bin/bash
# Pre-Test Framework Merge Backup Script
# Created: 2025-08-25
# Purpose: Complete backup before merging test framework branch

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="BACKUPS/pre_test_merge_$TIMESTAMP"

echo "🔄 Creating backup: $BACKUP_DIR"

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Backup critical directories and files (excluding git, node_modules, venv)
echo "📁 Backing up application directories..."
cp -R app/ "$BACKUP_DIR/app/"
cp -R backend/ "$BACKUP_DIR/backend/"
cp -R api/ "$BACKUP_DIR/api/"
cp -R components/ "$BACKUP_DIR/components/"
cp -R lib/ "$BACKUP_DIR/lib/"
cp -R hooks/ "$BACKUP_DIR/hooks/"
cp -R styles/ "$BACKUP_DIR/styles/"
cp -R public/ "$BACKUP_DIR/public/"
cp -R tests/ "$BACKUP_DIR/tests/"
cp -R docs/ "$BACKUP_DIR/docs/"

# Backup configuration files
echo "⚙️ Backing up configuration files..."
cp package.json "$BACKUP_DIR/"
cp package-lock.json "$BACKUP_DIR/"
cp tsconfig.json "$BACKUP_DIR/"
cp next.config.mjs "$BACKUP_DIR/"
cp postcss.config.mjs "$BACKUP_DIR/"
cp components.json "$BACKUP_DIR/"
cp requirements*.txt "$BACKUP_DIR/"
cp README.md "$BACKUP_DIR/"
cp .env.example "$BACKUP_DIR/"
cp .gitignore "$BACKUP_DIR/"
cp .replit "$BACKUP_DIR/"

# Backup current branch info
echo "🔀 Recording git state..."
git branch > "$BACKUP_DIR/git_branches.txt"
git status > "$BACKUP_DIR/git_status.txt"
git log --oneline -10 > "$BACKUP_DIR/git_recent_commits.txt"

# Create restore instructions
cat > "$BACKUP_DIR/RESTORE_INSTRUCTIONS.md" << EOF
# Restore Instructions

## To restore this backup:

1. **Stop all servers** (frontend and backend)
2. **Copy files back** to project root:
   \`\`\`bash
   cp -R BACKUPS/pre_test_merge_$TIMESTAMP/* ./
   \`\`\`
3. **Reinstall dependencies**:
   \`\`\`bash
   npm install
   pip install -r requirements.txt
   \`\`\`
4. **Restart servers** and verify functionality

## Backup created from branch:
$(git branch --show-current)

## Backup timestamp:
$TIMESTAMP

## Files included:
- All application source code
- Configuration files  
- Documentation
- Current git state info
- Test directory contents

## NOT included:
- node_modules/ (reinstall with npm install)
- venv/ (recreate virtual environment)
- .git/ (git repository intact)
- Environment files (.env* - for security)
EOF

echo "✅ Backup completed: $BACKUP_DIR"
echo "📋 Backup includes all source code, configs, and git state"
echo "🚫 Excluded: node_modules, venv, .git, env files"