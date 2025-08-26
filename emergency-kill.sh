#!/bin/bash

# EMERGENCY KILL - Simple and fast
echo "🚨 EMERGENCY KILL - BotArmy Application"
echo "======================================="

# Kill everything related to the project
pkill -9 -f "npm.*replit"
pkill -9 -f "npm.*dev"  
pkill -9 -f "next.*dev"
pkill -9 -f "python3.*main"
pkill -9 -f "uvicorn"
pkill -9 -f "concurrently"

# Kill by ports - force kill immediately
lsof -ti:3000 | xargs -r kill -9
lsof -ti:3001 | xargs -r kill -9  
lsof -ti:8000 | xargs -r kill -9

echo "💀 All processes killed forcefully!"
echo "✅ Ports 3000, 3001, 8000 cleared!"
echo ""
echo "Safe to restart with: npm run replit:dev"
