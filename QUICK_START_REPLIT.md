# BotArmy POC - Quick Start Guide (Replit)

🤖 **Get BotArmy running on Replit in 5 minutes**

---

## 🚀 **Immediate Setup Steps**

### **1. Import to Replit (2 minutes)**
```bash
1. Go to replit.com
2. Click "Import from GitHub"
3. Enter: https://github.com/geniusboywonder/v0-botarmy-poc.git
4. Make private (requires Replit Core $25/mo)
5. Click "Import"
```

### **2. Configure API Keys (1 minute)**
```bash
In Replit "Secrets" tab, add:
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here  # Optional
GOOGLE_AI_API_KEY=your_key_here  # Optional
```

### **3. Start Application (2 minutes)**
```bash
1. Click "Run" button
2. Wait for dependency installation
3. Backend starts on port 8000
4. Open "Webview" for frontend
```

---

## ✅ **What's Different from Vercel**

| Issue | Vercel Problem | Replit Solution |
|-------|----------------|-----------------|
| **Python 3.13** | ❌ Not supported | ✅ **Fully supported** |
| **ControlFlow** | ❌ Size limits | ✅ **No limits** |
| **Long Agents** | ❌ 60s timeout | ✅ **No timeout** |
| **WebSockets** | ❌ Limited | ✅ **Full support** |
| **Development** | ❌ External IDE | ✅ **Built-in IDE** |

---

## 🔧 **Key Changes Made**

### **Requirements Updated**
```txt
# OLD (Vercel-limited)
# Minimal dependencies only

# NEW (Replit-full)
prefect>=3.0.0,<4.0.0      # ✅ Now included
controlflow>=0.11.0        # ✅ Now included  
openai>=1.0.0             # ✅ Now included
anthropic>=0.8.0          # ✅ Now included
```

### **Backend Configuration**
```python
# OLD: Vercel detection
IS_VERCEL = os.getenv('VERCEL') == '1'

# NEW: Replit detection  
IS_REPLIT = os.getenv('REPLIT') == '1'

# OLD: Limited features in Vercel
features = {"full_workflow": not IS_VERCEL}

# NEW: Full features in Replit
features = {"full_workflow": True}
```

### **Files Added**
- `.replit` - Replit configuration
- `replit.nix` - Environment setup  
- `REPLIT_DEPLOYMENT.md` - Complete guide
- `.env.replit` - Environment template
- `start_replit.py` - Startup script

### **Files Removed**
- `vercel.json` → `vercel.json.removed`
- `VERCEL_DEPLOYMENT.md` → `VERCEL_DEPLOYMENT.md.removed`
- `requirements-vercel.txt` → `requirements-vercel.txt.removed`

---

## 🎯 **Immediate Benefits**

### **Development Experience**
- ✅ **No version downgrades** needed (keep Python 3.13)
- ✅ **No dependency restrictions** (install anything)
- ✅ **Built-in AI coding** assistant (Replit Agent)
- ✅ **Real-time collaboration** for team development
- ✅ **One-click deployment** without configuration

### **Technical Capabilities**
- ✅ **Full agent orchestration** with ControlFlow
- ✅ **Real WebSocket support** for real-time features
- ✅ **Long-running processes** for complex agents
- ✅ **File upload support** without size limits
- ✅ **Built-in database** (Replit DB) if needed

---

## 🚨 **Next Actions Required**

### **Immediate (Today)**
1. **Test the import** to Replit
2. **Verify all features** work without restrictions
3. **Fix any remaining WebSocket issues** Jules is working on
4. **Test agent workflows** end-to-end

### **Short-term (This Week)**
1. **Set up production deployment** if needed
2. **Configure custom domain** (optional)
3. **Test with real LLM integrations**
4. **Document any Replit-specific issues**

---

## 📊 **Cost Comparison**

| Platform | **Base Cost** | **Full Features** | **Restrictions** |
|----------|---------------|-------------------|------------------|
| **Vercel** | $20/mo | ❌ Limited | Size, timeout, versions |
| **Replit** | $25/mo | ✅ **Complete** | None for development |
| **Railway** | $5/mo | ✅ Complete | Docker complexity |

**Replit offers the best balance of features, simplicity, and cost for BotArmy development.**

---

## 🤔 **Questions for You**

1. **API Keys**: Do you have OpenAI/Anthropic keys ready?
2. **Replit Plan**: Are you okay with $25/mo for Core plan?
3. **Team Access**: Do you need to share with other developers?
4. **Production**: Will you need production deployment immediately?

---

## 📋 **Success Validation**

After import, verify these work:
- [ ] Backend starts without errors
- [ ] Frontend loads and connects
- [ ] WebSocket connection established  
- [ ] Health check returns "replit" environment
- [ ] No dependency installation errors
- [ ] All Python 3.13 features working

**🎉 If all checks pass, your Replit migration is complete!**

---

**The main advantage: Your current environment (Python 3.13, all dependencies) will work perfectly on Replit without any changes, while gaining access to full agent orchestration capabilities that were blocked on Vercel.**