# Replit Secrets Configuration for BotArmy

**IMPORTANT:** Copy these exact values into your Replit Secrets tab (🔐 icon)

## 🔑 **Required API Keys**

```bash
# OpenAI API Key (from your .env file)
OPENAI_API_KEY=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

# Google/Gemini API Key (from your .env file)
GOOGLE_API_KEY=AIzaSyB_FH53-q9yE13t7Nav0_tSq2I9GbhBLN4
GEMINI_KEY_KEY=AIzaSyB_FH53-q9yE13t7Nav0_tSq2I9GbhBLN4
```

## ⚙️ **Environment Settings**

```bash
# Replit environment indicator
REPLIT=1

# Logging and debug
DEBUG=true
LOG_LEVEL=INFO

# Safety brake settings (keep these for stability)
AGENT_TEST_MODE=true
ROLE_TEST_MODE=false
TEST_MODE=true
ENABLE_HITL=false
AUTO_ACTION=approve
```

## 🌐 **URL Configuration (Auto-detected)**

The startup script will auto-detect these, but you can override if needed:

```bash
# Backend URLs (will be auto-detected from REPL_SLUG and REPL_OWNER)
BACKEND_URL=https://your-repl-name.your-username.repl.co
NEXT_PUBLIC_BACKEND_URL=https://your-repl-name.your-username.repl.co
WEBSOCKET_URL=wss://your-repl-name.your-username.repl.co/api/ws
NEXT_PUBLIC_WEBSOCKET_URL=wss://your-repl-name.your-username.repl.co/api/ws
```

## 📋 **Step-by-Step Setup**

1. **Open your Replit project**
2. **Click the Secrets tab** (🔐 icon in the left sidebar)  
3. **Add each variable** by clicking "New Secret":
   - Key: `OPENAI_API_KEY`
   - Value: `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`
4. **Continue adding all required secrets** from the sections above
5. **Click "Run"** to test the configuration

## ✅ **Verification Commands**

After setting up secrets, test in the Replit console:

```bash
# Test environment variables
python -c "import os; print('REPLIT:', os.getenv('REPLIT')); print('OPENAI_API_KEY:', 'SET' if os.getenv('OPENAI_API_KEY') else 'MISSING')"

# Test backend startup
python start_replit.py

# Test imports
python -c "from backend.main import app; print('Backend imports OK')"
```

## 🚨 **Common Issues**

- **"Missing API keys"**: Make sure OPENAI_API_KEY is set in Secrets (not just uploaded as .env file)
- **"Import errors"**: The new requirements-replit.txt should fix ControlFlow/Prefect issues
- **"WebSocket connection failed"**: Check that port 8000→80 mapping is working in .replit

## 🎯 **Success Indicators**

You'll know it's working when:
- ✅ Replit console shows "Backend starting... (Ctrl+C to stop)"
- ✅ No import errors in the startup logs  
- ✅ Configuration tab loads without errors
- ✅ WebSocket shows "Connected" status in frontend

---

**Next Steps:** After setting up Secrets, click **Run** in Replit to test the fixed configuration.