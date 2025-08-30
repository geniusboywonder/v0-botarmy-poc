#!/bin/bash

# BotArmy Application Killer
# Kills all processes related to the BotArmy application

echo "🔴 Killing BotArmy Application..."
echo "=================================="

# Function to kill processes by pattern and report
kill_by_pattern() {
    local pattern="$1"
    local description="$2"
    
    pids=$(pgrep -f "$pattern")
    if [ ! -z "$pids" ]; then
        echo "🔍 Found $description processes: $pids"
        kill -TERM $pids 2>/dev/null
        sleep 2
        
        # Force kill if still running
        remaining_pids=$(pgrep -f "$pattern")
        if [ ! -z "$remaining_pids" ]; then
            echo "💀 Force killing stubborn $description processes: $remaining_pids"
            kill -KILL $remaining_pids 2>/dev/null
        fi
        echo "✅ $description processes terminated"
    else
        echo "✅ No $description processes found"
    fi
}

# Function to kill by port
kill_by_port() {
    local port="$1"
    local description="$2"
    
    pids=$(lsof -ti:$port)
    if [ ! -z "$pids" ]; then
        echo "🔍 Found processes on port $port ($description): $pids"
        kill -TERM $pids 2>/dev/null
        sleep 2
        
        # Force kill if still running
        remaining_pids=$(lsof -ti:$port)
        if [ ! -z "$remaining_pids" ]; then
            echo "💀 Force killing processes on port $port: $remaining_pids"
            kill -KILL $remaining_pids 2>/dev/null
        fi
        echo "✅ Port $port ($description) cleared"
    else
        echo "✅ Port $port ($description) is free"
    fi
}

# Kill by process patterns
kill_by_pattern "npm.*replit:dev" "npm replit:dev"
kill_by_pattern "npm.*run.*dev" "npm run dev"
kill_by_pattern "next.*dev" "Next.js dev server"
kill_by_pattern "python3.*main.py" "Python backend"
kill_by_pattern "uvicorn.*main:app" "Uvicorn server"
kill_by_pattern "concurrently.*npm" "Concurrently process"

# Kill by ports
kill_by_port 3000 "Frontend (default)"
kill_by_port 3001 "Frontend (alternate)"
kill_by_port 8000 "Backend API"

# Additional cleanup
echo ""
echo "🧹 Additional Cleanup..."
echo "========================"

# Kill any remaining node processes related to the project
project_path="/Users/neill/Documents/AI Code/Projects/v0-botarmy-poc"
node_pids=$(pgrep -f "node.*$project_path")
if [ ! -z "$node_pids" ]; then
    echo "🔍 Found remaining Node.js processes in project: $node_pids"
    kill -TERM $node_pids 2>/dev/null
    sleep 2
    remaining_node_pids=$(pgrep -f "node.*$project_path")
    if [ ! -z "$remaining_node_pids" ]; then
        echo "💀 Force killing remaining Node.js processes: $remaining_node_pids"
        kill -KILL $remaining_node_pids 2>/dev/null
    fi
    echo "✅ Node.js processes cleaned up"
else
    echo "✅ No remaining Node.js processes found"
fi

# Kill any Python processes in the backend directory
python_pids=$(pgrep -f "python.*$project_path/backend")
if [ ! -z "$python_pids" ]; then
    echo "🔍 Found remaining Python processes in backend: $python_pids"
    kill -TERM $python_pids 2>/dev/null
    sleep 2
    remaining_python_pids=$(pgrep -f "python.*$project_path/backend")
    if [ ! -z "$remaining_python_pids" ]; then
        echo "💀 Force killing remaining Python processes: $remaining_python_pids"
        kill -KILL $remaining_python_pids 2>/dev/null
    fi
    echo "✅ Python processes cleaned up"
else
    echo "✅ No remaining Python processes found"
fi

echo ""
echo "🔍 Final Status Check..."
echo "========================"

# Check if ports are truly free
for port in 3000 3001 8000; do
    if lsof -ti:$port > /dev/null 2>&1; then
        echo "⚠️  Port $port is still in use!"
    else
        echo "✅ Port $port is free"
    fi
done

# Check for any remaining processes
remaining_processes=$(ps aux | grep -E "(npm.*replit|next.*dev|python3.*main|uvicorn)" | grep -v grep | wc -l)
if [ "$remaining_processes" -gt 0 ]; then
    echo "⚠️  Some processes may still be running:"
    ps aux | grep -E "(npm.*replit|next.*dev|python3.*main|uvicorn)" | grep -v grep
else
    echo "✅ No remaining BotArmy processes found"
fi

echo ""
echo "🎉 BotArmy Application Termination Complete!"
echo "============================================="
echo "You can now safely restart the application with:"
echo "cd /Users/neill/Documents/AI\ Code/Projects/v0-botarmy-poc && npm run replit:dev"
echo ""
