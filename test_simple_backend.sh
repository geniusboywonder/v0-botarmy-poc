#!/bin/bash
cd "/Users/neill/Documents/AI Code/Projects/v0-botarmy-poc"

echo "🧪 Testing Backend Startup with main_simple.py"
echo "=" * 50

# Set test mode for safe testing
export AGENT_TEST_MODE=true

echo "Environment:"
echo "  AGENT_TEST_MODE: $AGENT_TEST_MODE"
echo "  Current directory: $(pwd)"

# Test that we can import and start the simple backend
echo "Testing Python import..."
python3 -c "
import sys
sys.path.insert(0, '.')
sys.path.insert(0, './backend')
from backend import main_simple
print('✅ main_simple.py imported successfully')
"

if [ $? -eq 0 ]; then
    echo "✅ Backend import test PASSED"
else
    echo "❌ Backend import test FAILED"
    exit 1
fi

echo "🎉 Ready to test backend functionality!"
