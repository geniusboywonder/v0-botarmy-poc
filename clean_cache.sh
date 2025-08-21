#!/bin/bash

# Clean up Python cache files to avoid import issues
echo "🧹 Cleaning Python cache files..."

find /Users/neill/Documents/AI\ Code/Projects/v0-botarmy-poc -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
find /Users/neill/Documents/AI\ Code/Projects/v0-botarmy-poc -name "*.pyc" -delete 2>/dev/null || true

echo "✅ Cache cleaned!"
echo ""
echo "🚀 Now try starting the backend:"
echo "   source venv/bin/activate"
echo "   python start_backend.py"
