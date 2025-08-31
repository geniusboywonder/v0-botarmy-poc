#!/bin/bash
# Fixes frontmatter in all Claude Code agent files by adding name and description
# Compatible with macOS default bash (3.x)

AGENTS_DIR="/Users/neill/.claude/agents"

# List of files and descriptions
files=(
  "README.md"
  "studio-operations/infrastructure-maintainer.md"
  "studio-operations/finance-tracker.md"
  "studio-operations/support-responder.md"
  "studio-operations/analytics-reporter.md"
  "studio-operations/legal-compliance-checker.md"
  "design/visual-storyteller.md"
  "design/ux-researcher.md"
  "design/brand-guardian.md"
  "design/ui-designer.md"
  "design/whimsy-injector.md"
  "bonus/studio-coach.md"
  "bonus/joker.md"
  "project-management/experiment-tracker.md"
  "project-management/project-shipper.md"
  "project-management/studio-producer.md"
  "product/trend-researcher.md"
  "product/feedback-synthesizer.md"
  "product/sprint-prioritizer.md"
  "testing/tool-evaluator.md"
  "testing/api-tester.md"
  "testing/performance-benchmarker.md"
  "testing/test-results-analyzer.md"
  "testing/workflow-optimizer.md"
  "marketing/tiktok-strategist.md"
  "marketing/reddit-community-builder.md"
  "marketing/content-creator.md"
  "marketing/growth-hacker.md"
  "marketing/twitter-engager.md"
  "marketing/app-store-optimizer.md"
  "marketing/instagram-curator.md"
  "engineering/mobile-app-builder.md"
  "engineering/backend-architect.md"
  "engineering/test-writer-fixer.md"
  "engineering/rapid-prototyper.md"
  "engineering/ai-engineer.md"
  "engineering/devops-automator.md"
  "engineering/frontend-developer.md"
)

descriptions=(
  "Overview of Claude Code agents"
  "Maintains and optimizes studio infrastructure"
  "Tracks and manages studio financial data"
  "Handles customer support queries efficiently"
  "Generates and reports analytics insights"
  "Ensures compliance with legal standards"
  "Crafts compelling visual narratives"
  "Conducts user experience research and analysis"
  "Maintains and enforces brand consistency"
  "Designs intuitive user interfaces"
  "Adds creative and playful design elements"
  "Provides guidance and coaching for studio teams"
  "Injects humor and engagement into content"
  "Tracks and manages project experiments"
  "Ensures timely project delivery"
  "Oversees studio project production"
  "Researches market and user trends"
  "Synthesizes user feedback for product improvements"
  "Prioritizes tasks for product sprints"
  "Evaluates and selects testing tools"
  "Tests and validates API functionality"
  "Benchmarks system performance"
  "Analyzes test results for insights"
  "Optimizes testing workflows"
  "Develops TikTok content and growth strategies"
  "Builds and manages Reddit communities"
  "Creates high-quality content for multiple platforms"
  "Implements rapid user and revenue growth strategies"
  "Drives engagement and follower growth on Twitter"
  "Optimizes app store listings for visibility"
  "Specializes in visual content strategy and Instagram growth"
  "Builds and maintains mobile applications"
  "Designs scalable backend systems"
  "Writes and fixes automated tests"
  "Creates rapid prototypes for testing"
  "Develops AI-driven features and models"
  "Automates DevOps processes"
  "Builds responsive frontend interfaces"
)

echo "Fixing frontmatter for agent files in $AGENTS_DIR..."
echo "----------------------------------------------------"

# Process each file
for i in "${!files[@]}"; do
  file="${files[$i]}"
  desc="${descriptions[$i]}"
  full_path="$AGENTS_DIR/$file"
  
  if [ -f "$full_path" ]; then
    # Derive name from filename (convert to title case)
    name=$(basename "$file" .md | sed 's/-/ /g' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) tolower(substr($i,2))}1')
    
    # Remove existing frontmatter (between first and second ---, if present)
    if grep -q "^---$" "$full_path"; then
      sed -i '' '/^---$/,/^---$/d' "$full_path"
    fi
    
    # Prepend new frontmatter
    echo -e "---\nname: $name\ndescription: $desc\n---\n\n$(cat "$full_path")" > "$full_path.tmp" && mv "$full_path.tmp" "$full_path"
    echo "Updated $full_path with name and description"
  else
    echo "File not found: $full_path"
  fi
done

echo "Fix complete. Run check-agent-frontmatter.sh to verify."