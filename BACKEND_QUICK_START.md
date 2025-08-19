# Backend Quick Start Guide

## SIMPLE START (Recommended for testing)

1. **Navigate to project root:**
   ```bash
   cd /Users/neill/Documents/AI\ Code/Projects/v0-botarmy-poc
   ```

2. **Install minimal Python dependencies:**
   ```bash
   pip install -r backend/requirements_minimal.txt
   ```

3. **Set OpenAI API Key (Optional for testing):**
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

4. **Start the simplified backend server:**
   ```bash
   python backend/main_simple.py
   ```

5. **Verify backend is running:**
   - Open http://localhost:8000 in browser
   - Should see: `{"message": "BotArmy Backend v2 is running"}`

## FULL VERSION (If simple version works)

1. **Install full dependencies:**
   ```bash
   pip install -r backend/requirements.txt
   ```

2. **Start full backend:**
   ```bash
   python backend/main.py
   ```

## Test the Connection

1. Start frontend: `pnpm dev` (in separate terminal)
2. Open http://localhost:3000
3. Click "Test Backend" button - should show success message
4. Click "Test OpenAI" button - will test API key if set

## Common Issues

- **"Connection failed"**: Backend not running on port 8000
- **"OpenAI API key not found"**: Set OPENAI_API_KEY environment variable
- **Import errors**: Run `pip install -r backend/requirements.txt`
