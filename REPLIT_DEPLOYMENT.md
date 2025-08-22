# BotArmy Replit Deployment Guide

🤖 **BotArmy POC - Complete deployment guide for Replit platform**

---

## 🎯 **Quick Start (5 minutes)**

### **Step 1: Import to Replit**
1. Go to [replit.com](https://replit.com)
2. Click **"Import from GitHub"**
3. Enter repository URL: `https://github.com/geniusboywonder/v0-botarmy-poc.git`
4. Make the repl **private** (requires Replit Core plan)
5. Click **"Import"**

### **Step 2: Configure Environment**
1. Click **"Secrets"** tab in Replit
2. Add your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   GOOGLE_AI_API_KEY=your_google_api_key_here
   ```

### **Step 3: Start the Application**
1. Click the **"Run"** button in Replit
2. Wait for dependencies to install (2-3 minutes first time)
3. Backend will start on port 8000
4. Open the **"Webview"** tab to see the frontend

---

## 🚀 **Full Deployment Process**

### **Prerequisites**
- **Replit Core Plan** ($25/month) - Required for private repos and full features
- **API Keys** for OpenAI, Anthropic, or Google AI
- **GitHub account** with repository access

### **Environment Setup**

#### **Required Environment Variables**
Add these to your Replit **Secrets** tab:

```bash
# Essential
REPLIT=1
OPENAI_API_KEY=your_openai_api_key_here

# Optional but recommended
ANTHROPIC_API_KEY=your_anthropic_api_key_here
GOOGLE_AI_API_KEY=your_google_api_key_here
LOG_LEVEL=INFO
DEBUG=true
```

#### **Automatic Configuration**
Replit will automatically:
- Detect Python 3.13 and Node.js 20
- Install dependencies from `requirements.txt`
- Configure ports (8000 for backend, 3000 for frontend)
- Set up the development environment

---

## 🔧 **Architecture on Replit**

### **File Structure**
```
├── .replit                 # Replit configuration
├── replit.nix             # Nix environment setup
├── requirements.txt       # Python dependencies (full functionality)
├── package.json           # Node.js dependencies
├── start_replit.py        # Replit startup script
├── backend/
│   ├── main.py            # FastAPI backend (Replit-optimized)
│   └── runtime_env.py     # Environment detection
└── app/                   # Next.js frontend
```

### **Key Differences from Vercel**
| Feature | Vercel | Replit |
|---------|--------|--------|
| **Python Version** | 3.12 only | Any version (we use 3.13) |
| **Size Limits** | 250MB | No limits |
| **Long-running Processes** | No | Yes (perfect for agents) |
| **ControlFlow/Prefect** | Not supported | Fully supported |
| **WebSocket Support** | Limited | Full support |
| **Development Environment** | External | Built-in IDE |

---

## 📦 **Dependencies & Features**

### **Python Dependencies (Full Support)**
```txt
# Core Framework
fastapi==0.116.1
uvicorn[standard]==0.24.0
websockets==12.0

# Agent Orchestration (NOW SUPPORTED!)
prefect>=3.0.0,<4.0.0
controlflow>=0.11.0

# LLM Integration
openai>=1.0.0
anthropic>=0.8.0
google-generativeai==0.5.4

# All other dependencies without restrictions
```

### **Available Features**
- ✅ **Full agent orchestration** with ControlFlow
- ✅ **Real-time WebSocket communication**
- ✅ **Long-running agent processes**
- ✅ **All LLM providers** (OpenAI, Anthropic, Google)
- ✅ **File uploads and artifacts**
- ✅ **Human-in-the-loop workflows**
- ✅ **Built-in database** (Replit DB)
- ✅ **AI-powered development** (Replit Agent)

---

## 🛠 **Development Workflow**

### **Local Development in Replit**
1. **Edit code** directly in Replit's browser IDE
2. **Use Replit Agent** for AI-assisted coding
3. **Real-time collaboration** with team members
4. **Instant preview** with live reload
5. **Built-in terminal** for debugging

### **Replit-Specific Commands**
```bash
# Install dependencies
pip install -r requirements.txt
npm install

# Start backend only
cd backend && python main.py

# Start frontend only
npm run dev

# Start both (for development)
npm run replit:dev
```

### **Using Replit Agent for Development**
- Press **Ctrl+I** or click the **Agent** tab
- Ask for help with coding tasks:
  - "Fix the WebSocket connection issue"
  - "Add a new agent type for code review"
  - "Optimize the ControlFlow workflow"

---

## 🚢 **Deployment Options**

### **Development Deployment (Included)**
- **Free with Core plan**
- Accessible via `https://your-repl-name.username.replit.dev`
- Perfect for testing and development

### **Production Deployment**

#### **Option 1: Autoscale Deployment** (Recommended)
```bash
Cost: $1/month base + usage
Features:
- Automatic scaling
- Custom domain support
- 99.9% uptime
- Perfect for variable traffic
```

#### **Option 2: Reserved VM Deployment**
```bash
Cost: $20/month minimum
Features:
- Dedicated resources
- Predictable costs
- Always-on availability
- Better for consistent high traffic
```

### **Setting up Production Deployment**
1. Click **"Deploy"** in Replit
2. Choose **"Autoscale"** or **"Reserved VM"**
3. Configure custom domain (optional)
4. Set production environment variables
5. Deploy with one click

---

## 🔍 **Troubleshooting**

### **Common Issues & Solutions**

#### **Dependencies Installation Failed**
```bash
# Check Python version
python --version  # Should be 3.13+

# Reinstall requirements
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

#### **WebSocket Connection Issues**
```bash
# Check if backend is running
curl http://localhost:8000/health

# Verify WebSocket endpoint
curl -i -N -H "Connection: Upgrade" \
  -H "Upgrade: websocket" \
  http://localhost:8000/api/ws
```

#### **ControlFlow Import Errors**
```bash
# Check if ControlFlow installed correctly
python -c "import controlflow; print(controlflow.__version__)"

# If failed, install specific version
pip install controlflow==0.11.0 --force-reinstall
```

### **Performance Optimization**

#### **For Development**
- Use **"Boost"** feature for faster performance
- Enable **"Always On"** to avoid cold starts
- Monitor resource usage in Replit dashboard

#### **For Production**
- Use **Reserved VM** for consistent performance
- Enable **autoscaling** for traffic spikes
- Monitor costs in billing dashboard

---

## 📊 **Monitoring & Logs**

### **Built-in Monitoring**
- **Console logs** in Replit terminal
- **Resource usage** in dashboard
- **Real-time metrics** for deployments
- **Error tracking** in deployment logs

### **Custom Monitoring**
```python
# Add to your backend/main.py
import logging

# Configure enhanced logging for Replit
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Monitor agent performance
@app.middleware("http")
async def log_requests(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(f"{request.method} {request.url} - {response.status_code} - {process_time:.3f}s")
    return response
```

---

## 💡 **Pro Tips**

### **Development Best Practices**
1. **Use Replit Agent** for faster coding and debugging
2. **Enable real-time collaboration** for team development
3. **Test WebSocket connections** regularly
4. **Monitor resource usage** to optimize costs
5. **Use environment variables** for all sensitive data

### **Cost Optimization**
1. **Start with Autoscale deployment** (pay-per-use)
2. **Monitor usage patterns** before upgrading to Reserved VM
3. **Use Replit's built-in database** instead of external services
4. **Optimize agent workflows** to reduce LLM API costs

### **Security Best Practices**
1. **Keep repositories private** (required for API keys)
2. **Use Replit Secrets** for all sensitive data
3. **Regularly rotate API keys**
4. **Monitor access logs** in production

---

## 🎯 **Next Steps**

### **After Successful Deployment**
1. **Test all agent workflows** end-to-end
2. **Configure production monitoring** and alerts
3. **Set up custom domain** for production deployment
4. **Document your specific configuration** for team members
5. **Plan scaling strategy** based on usage patterns

### **Advanced Features to Explore**
- **Replit Database** integration for persistent storage
- **Multi-agent collaboration** patterns
- **Custom LLM model** integration
- **Advanced human-in-the-loop** workflows
- **Integration with external APIs** and services

---

## 📞 **Support**

### **Getting Help**
- **Replit Community**: [ask.replit.com](https://ask.replit.com)
- **Documentation**: [docs.replit.com](https://docs.replit.com)
- **BotArmy Issues**: GitHub repository issues
- **Direct Support**: Replit Core plan includes support

### **Useful Resources**
- [Replit Python Guide](https://docs.replit.com/programming-ide/configuring-repl)
- [Replit Deployment Docs](https://docs.replit.com/deployments)
- [FastAPI on Replit Tutorial](https://docs.replit.com/tutorials/python/build-basic-web-app-fastapi)
- [ControlFlow Documentation](https://controlflow.ai/welcome/what-is-controlflow)

---

## ✅ **Success Checklist**

- [ ] Repository imported to Replit successfully
- [ ] API keys configured in Secrets
- [ ] Dependencies installed without errors
- [ ] Backend starts and responds to /health endpoint
- [ ] Frontend loads and connects to backend
- [ ] WebSocket connection working
- [ ] Agent workflows execute successfully
- [ ] Production deployment configured (if needed)
- [ ] Monitoring and logging set up
- [ ] Team access configured (if applicable)

**🎉 Your BotArmy POC is now running on Replit with full functionality!**