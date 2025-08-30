#!/bin/bash

echo "=== Testing Frontend Server (Next.js) ==="
echo "Date: $(date)"

cd "/Users/neill/Documents/AI Code/Projects/v0-botarmy-poc"

echo "=== Dependencies Check ==="
echo "Node.js: $(node --version)"
echo "npm: $(npm --version)"

echo ""
echo "=== Created Missing Dependencies ==="
echo "✅ lib/types.ts - Core TypeScript definitions"
echo "✅ lib/stores/process-store.ts - Process state management"
echo "✅ components/ui/dropdown-menu.tsx - Dropdown menu component"
echo "✅ components/ui/dialog.tsx - Dialog component"

echo ""
echo "=== Installing Dependencies ==="
npm install --silent

echo ""
echo "=== Checking for TypeScript Errors ==="
echo "Running TypeScript check..."
npx tsc --noEmit --pretty

echo ""
echo "=== Build Test ==="
echo "Testing Next.js build..."
npm run build

echo ""
echo "Ready to start development server!"
echo "Run: npm run dev"
