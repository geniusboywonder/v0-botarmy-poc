#!/bin/bash

echo "=== BotArmy Frontend Testing Script ==="
echo "Date: $(date)"

cd "/Users/neill/Documents/AI Code/Projects/v0-botarmy-poc"

echo "=== Checking Node.js Environment ==="
echo "Node.js version: $(node --version)"
echo "npm version: $(npm --version)"

echo ""
echo "=== Installing/Updating Dependencies ==="
echo "Running npm install to ensure all dependencies are up to date..."
npm install

echo ""
echo "=== Starting Frontend Server (Next.js) ==="
echo "Command: npm run dev"
echo "Expected: Server should start on http://localhost:3000"
echo "Expected: Should show the refactored process-based dashboard"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the frontend server
npm run dev
