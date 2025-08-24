# BotArmy POC - Dynamic AI Agent Orchestration Platform

A proof-of-concept multi-agent system that orchestrates specialized AI agents through dynamic workflows to automatically generate functional web applications. Features real-time human-in-the-loop collaboration, multi-LLM provider support, and extensible agent architectures.

## 🎯 Overview

BotArmy demonstrates sophisticated AI agent orchestration beyond traditional SDLC workflows. The platform supports dynamic team assembly, multi-domain problem solving (software development, marketing campaigns, technical support), and seamless human-AI collaboration through an intuitive chat interface.

**Key Capabilities:**
- **Dynamic Agent Teams** - Configure specialized agents for any domain
- **Human-in-the-Loop Control** - Real-time oversight with pause/resume workflows
- **Multi-LLM Support** - OpenAI, Anthropic Claude, Google Gemini integration
- **Real-time Collaboration** - WebSocket-powered agent communication
- **Extensible Architecture** - Plugin-based system for custom workflows

## 🛠 Environment Requirements

### **Current Environment Configuration**
The project is optimized for modern development environments with the latest stable versions:

| Component | Version | Notes |
|-----------|---------|-------|
| **Python** | **3.13.x** | Latest stable release with all new features |
| **Node.js** | **20.x LTS** | Long-term support version for stability |
| **Next.js** | **15.2.4** | Current stable with React 19 support |
| **React** | **19.x** | Latest stable release |
| **TypeScript** | **5.x** | Full type safety implementation |

### **Python Dependencies (Production)**
```bash
# Core Framework
fastapi==0.116.1
uvicorn[standard]==0.24.0
websockets==12.0

# Agent Orchestration
prefect>=3.0.0,<4.0.0
controlflow>=0.11.0

# Multi-LLM Support
openai>=1.0.0
anthropic>=0.8.0
google-generativeai==0.5.4

# Data & Validation
pydantic>=2.11.7,<3.0.0
python-dotenv>=1.0.0
```

### **Frontend Dependencies**
```bash
# Core Framework
next@15.2.4
react@19.x
react-dom@19.x
typescript@5.x

# UI Framework
tailwindcss@4.1.9
@radix-ui/*@latest
lucide-react@0.454.0
```

## 🚀 Quick Start

### **Prerequisites Check**
```bash
# Verify versions
python --version      # Should show 3.13.x (or 3.12+ is fine)
node --version         # Should show 20.x.x
npm --version          # Should show 10.x.x
```

### **1. Environment Setup**

**Install Latest Versions:**
```bash
# Python 3.13 (recommended) or 3.12+
# macOS: brew install python@3.13
# Ubuntu: sudo apt install python3.13 python3.13-venv

# Node.js 20 LTS
# Using nvm: nvm install 20 && nvm use 20
```

**Clone and Initialize:**
```bash
git clone https://github.com/geniusboywonder/v0-botarmy-poc.git
cd v0-botarmy-poc

# Create Python virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Verify Python version in venv
python --version  # Should show 3.13.x or 3.12+
```

### **2. Dependency Installation**

**Backend Dependencies:**
```bash
# Install Python packages (ensure venv is activated)
pip install --upgrade pip
pip install -r requirements.txt

# Verify critical packages
python -c "import controlflow, fastapi, openai; print('✅ Core packages installed')"
```

**Frontend Dependencies:**
```bash
# Install Node.js packages
npm install

# Handle any peer dependency warnings (normal with latest versions)
npm install --force  # if peer dependency warnings occur
```

### **3. Configuration**

**Environment Variables:**
```bash
# Copy environment template
cp .env.example .env

# Edit .env and configure:
nano .env
```

**Required Environment Variables:**
```bash
# LLM API Keys (at least one required)
OPENAI_API_KEY=sk-your-openai-key-here
ANTHROPIC_API_KEY=ant_your-anthropic-key
GOOGLE_GENAI_API_KEY=your-google-ai-key

# Application Configuration
BACKEND_URL=http://localhost:8000
WEBSOCKET_URL=ws://localhost:8000/ws
DEBUG=true
ENVIRONMENT=development
```

### **4. Development Startup**

**Option A: Concurrent Development (Recommended)**
```bash
# Single command starts both frontend and backend
npm run replit:dev
```

**Option B: Separate Terminals**

*Terminal 1 - Backend:*
```bash
source venv/bin/activate
cd backend
python main.py
```

*Terminal 2 - Frontend:*
```bash
npm run dev
```

**Access Application:** http://localhost:3000

## 📁 Project Structure

```
v0-botarmy-poc/
├── README.md                    # This file
├── package.json                 # Frontend dependencies & scripts
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment template
├── .replit                      # Replit deployment config
├──
├── app/                         # Next.js App Router
│   ├── layout.tsx              # Root layout component
│   ├── page.tsx                # Dashboard/home page
│   ├── globals.css             # Global styles
│   ├── analytics/              # Analytics dashboard page
│   ├── artifacts/              # Artifacts management page
│   ├── logs/                   # System logs page
│   ├── settings/               # Configuration page
│   └── tasks/                  # Task management page
│
├── backend/                     # FastAPI Backend
│   ├── main.py                 # Main FastAPI application
│   ├── workflow.py             # Agent workflow orchestration
│   ├── config.py               # Application configuration
│   ├── connection_manager.py   # WebSocket connection handling
│   ├── agent_status_broadcaster.py  # Real-time status updates
│   ├── rate_limiter.py         # LLM API rate limiting
│   ├── runtime_env.py          # Environment detection (Replit/local)
│   ├──
│   ├── agents/                 # AI Agent Implementations
│   │   ├── base_agent.py       # Base agent class
│   │   ├── analyst_agent.py    # Requirements analysis agent
│   │   ├── architect_agent.py  # System architecture agent
│   │   ├── developer_agent.py  # Code development agent
│   │   ├── tester_agent.py     # Testing and QA agent
│   │   └── deployer_agent.py   # Deployment agent
│   │
│   ├── agui/                   # Agent GUI Protocol
│   │   ├── protocol.py         # AG-UI message protocol
│   │   └── message_protocol.py # Enhanced messaging
│   │
│   └── services/               # Service Layer
│       └── llm_service.py      # Multi-LLM provider service
│
├── components/                  # React UI Components
│   ├── ui/                     # shadcn/ui base components
│   ├── agent-status-card.tsx   # Agent status display
│   ├── chat/                   # Chat interface components
│   ├── dashboard/              # Dashboard-specific components
│   └── layout/                 # Layout components
│
├── lib/                        # Frontend Utilities
│   ├── stores/                 # Zustand state management
│   │   ├── agent-store.ts      # Agent state management
│   │   ├── log-store.ts        # Log management
│   │   └── conversation-store.ts # Chat conversation state
│   ├── websocket/              # WebSocket client
│   │   └── websocket-service.ts # WebSocket communication
│   ├── utils.ts                # Utility functions
│   └── types.ts                # TypeScript definitions
│
├── hooks/                      # Custom React Hooks
│   ├── use-websocket.ts        # WebSocket connection hook
│   ├── use-performance-metrics.ts # Performance monitoring
│   └── use-system-health.ts    # System health monitoring
│
├── api/                        # API Route Handlers (Next.js)
│   └── index.py                # Python API endpoints
│
├── scripts/                    # Utility Scripts
│   ├── start_replit.py         # Replit startup automation
│   ├── start_backend.py        # Backend startup script
│   └── test_websocket_replit.py # WebSocket testing
│
├── docs/                       # Documentation
│   ├── botarmy-plan-v3.md      # V3 development plan
│   ├── botarmy-progress-v3.md  # Development progress tracking
│   ├── BIG-PLAN Final Architecture # Major architecture decisions
│   └── [various analysis documents]
│
├── artifacts/                  # Generated Artifacts (runtime)
├── venv/                       # Python virtual environment
└── .next/                      # Next.js build cache
```

## 🔧 Core Features

### **1. Dynamic Agent Orchestration**
- **Role-based Agents:** Analyst, Architect, Developer, Tester, Deployer
- **Workflow Flexibility:** Sequential, parallel, and custom orchestration patterns
- **Human Oversight:** Pause/resume workflows with approval gates
- **Multi-domain Support:** Beyond SDLC to marketing, support, research

### **2. Real-time Human-AI Collaboration**
- **Chat Interface:** Natural language interaction with agent teams
- **Live Status Updates:** Real-time agent progress and task completion
- **Approval Workflows:** Human-in-the-loop decision points
- **Progress Tracking:** Visual indicators for workflow stages

### **3. Multi-LLM Provider Support**
- **Primary Providers:** OpenAI GPT-4, Anthropic Claude, Google Gemini
- **Intelligent Routing:** Automatic model selection based on task complexity
- **Rate Limiting:** Built-in API usage management and cost control
- **Fallback Logic:** Automatic provider switching on failures

### **4. Advanced WebSocket Communication**
- **Real-time Messaging:** Live agent-to-agent and human-agent communication
- **Status Broadcasting:** Agent progress and system health updates
- **Message Batching:** Performance optimization for high-volume scenarios
- **Auto-Reconnection:** Robust connection handling with exponential backoff

### **5. Extensible Architecture**
- **Plugin System:** Custom agent types and workflow patterns
- **Configuration-driven:** YAML/JSON-based agent and workflow definitions
- **Multi-framework Support:** ControlFlow + Prefect orchestration options
- **Community Integration:** Template sharing and collaborative development

## 🧪 Usage Examples

### **Basic Software Development Workflow**
```bash
# Start the application
npm run replit:dev

# In the chat interface, enter:
"Create a simple todo application with React and FastAPI backend"

# Watch as agents collaborate:
# 1. Analyst → Analyzes requirements
# 2. Architect → Designs system architecture
# 3. Developer → Implements core features
# 4. Tester → Creates test plans
# 5. Deployer → Prepares deployment strategy
```

### **Marketing Campaign Generation**
```bash
# Configure marketing team (via settings or chat):
"Create a marketing campaign for a new productivity app targeting remote workers"

# Agents adapt their roles:
# 1. Research Agent → Market analysis
# 2. Strategy Agent → Campaign strategy
# 3. Creative Agent → Asset creation
# 4. Analytics Agent → Success metrics
# 5. Launch Agent → Go-to-market plan
```

### **Human-in-the-Loop Workflow**
```bash
# Pause workflow for human review:
User: "Pause after requirements analysis for my review"

# Agent pauses and requests approval:
Agent: "Requirements analysis complete. Please review and approve to continue..."

# Human provides feedback:
User: "Add mobile app requirement and continue"

# Workflow resumes with updated context
```

## 🔍 Troubleshooting

### **Environment Issues**

**Python Version Flexibility:**
```bash
# Check Python version - 3.12+ or 3.13 both work great
python --version  # Should show 3.12.x or 3.13.x

# If using older Python, upgrade:
# macOS: brew install python@3.13
# Ubuntu: sudo apt install python3.13 python3.13-venv
```

**Node.js Compatibility:**
```bash
# Check Node.js version
node --version  # Should show 20.x.x

# If wrong version (using nvm):
nvm install 20
nvm use 20
nvm alias default 20
```

**React 19 Dependencies:**
```bash
# Handle peer dependency warnings (normal with latest versions):
npm install --force
# or
npm install --legacy-peer-deps
```

### **Runtime Issues**

**ControlFlow/Prefect:**
```bash
# Verify compatible versions:
pip show prefect controlflow

# Update to latest stable versions:
pip install --upgrade "prefect>=3.0.0" "controlflow>=0.11.0"
```

**WebSocket Connection Issues:**
```bash
# Test WebSocket connectivity:
python test_websocket_replit.py

# Check backend logs:
cd backend && python main.py  # Look for WebSocket errors

# Test with browser dev tools:
# Open browser console at http://localhost:3000
# Check for WebSocket connection errors
```

**LLM API Issues:**
```bash
# Test API keys:
python -c "
import openai, os
client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
print('✅ OpenAI API key valid')
"

# Check rate limits in logs:
grep -i "rate limit" backend/logs/*
```

**Import/Dependency Errors:**
```bash
# Test all imports:
python test_imports.py

# Reinstall problematic packages:
pip install --force-reinstall [package-name]
```

### **Development Issues**

**Next.js Build Issues:**
```bash
# Clear build cache:
rm -rf .next
npm run build

# Check TypeScript errors:
npx tsc --noEmit
```

**Component Issues:**
```bash
# Verify component structure:
ls -la components/ui/
ls -la components/chat/

# Reinstall shadcn/ui components:
npx shadcn-ui@latest add [component-name]
```

**WebSocket Development Testing:**
```bash
# Test WebSocket manually:
wscat -c ws://localhost:8000/ws

# Check connection manager:
curl http://localhost:8000/health
```

## 🚧 Development Status

### **✅ Completed Features**
- [x] Core agent orchestration with ControlFlow
- [x] Multi-LLM provider integration (OpenAI, Anthropic, Gemini)
- [x] Real-time WebSocket communication
- [x] Human-in-the-loop workflow controls
- [x] Next.js 15 + React 19 frontend
- [x] Replit deployment compatibility
- [x] Agent status broadcasting and progress tracking

### **🔄 In Progress**
- [ ] Enhanced error boundaries and recovery
- [ ] Performance optimization and metrics
- [ ] Advanced workflow customization
- [ ] Community template marketplace

### **📋 Planned Enhancements**
- [ ] Multi-user collaboration
- [ ] Advanced analytics dashboard
- [ ] Plugin system for custom agents
- [ ] Mobile-responsive interface improvements

## 🎯 Deployment

### **Development (Local)**
```bash
# Standard development setup
npm run replit:dev
# Access: http://localhost:3000
```

### **Production (Replit)**
```bash
# Replit automatically detects and runs:
# Backend: python backend/main.py (via .replit config)
# Frontend: npm run start
# Full-stack: npm run replit:start
```

**Replit Configuration:**
The `.replit` file configures the deployment with:
- Python 3.12+ runtime (supports 3.13)
- Node.js 20 runtime
- Automatic port forwarding (3000 for frontend, 8000 for backend)
- Google Cloud Run deployment target

### **Alternative Platforms**
- **Railway:** Full-stack deployment with Docker support
- **Render:** Separate frontend/backend deployment
- **Fly.io:** Global edge deployment with containers
- **DigitalOcean App Platform:** Simple deployment with managed services

## 📊 Performance Characteristics

### **Typical Resource Usage**
- **Memory:** ~200-500MB for typical workflows
- **CPU:** Low baseline, spikes during LLM inference
- **Network:** WebSocket persistent connections + LLM API calls
- **Storage:** Minimal (logs, artifacts, configuration)

### **Scalability Notes**
- **Concurrent Users:** 10-100 (depending on LLM usage)
- **Agent Workflows:** 5-50 simultaneous processes
- **Message Throughput:** 100+ messages/second via WebSocket
- **LLM Rate Limits:** Configurable per provider

## 🤝 Contributing

### **Development Setup**
1. Fork the repository
2. Follow environment setup above
3. Create feature branch: `git checkout -b feature/your-feature`
4. Make changes and test thoroughly
5. Submit pull request with clear description

### **Code Standards**
- **Python:** Black formatting, type hints, docstrings
- **TypeScript:** Strict mode, proper typing, ESLint
- **Components:** Functional components with hooks
- **Testing:** Comprehensive tests for core functionality

## 📄 License

This project is a proof-of-concept for AI agent orchestration research and development.

## 🆘 Support

### **Getting Help**
1. **Check troubleshooting section** above for common issues
2. **Review logs** in browser console and backend terminal
3. **Verify environment** matches requirements (Python 3.12+, Node.js 20)
4. **Open GitHub issue** with full error details and reproduction steps

### **Issue Reporting**
Include in your issue report:
- Operating system and version
- Python version: `python --version`
- Node.js version: `node --version`
- Full error messages and stack traces
- Steps to reproduce the problem
- Expected vs actual behavior

---

**Project Status:** Active Development - Proof of Concept
**Last Updated:** August 23, 2025
**Version:** 0.2.0 - Human-in-the-Loop Integration
**Next Release:** Enhanced Multi-Domain Agent Support

---

## 📚 Additional Resources

- **[Development Plan v3](docs/botarmy-plan-v3.md)** - Detailed development roadmap
- **[Architecture Documentation](docs/BIG-PLAN Final Architecture)** - System architecture decisions
- **[Progress Tracking](docs/botarmy-progress-v3.md)** - Feature implementation status
- **[Strategic Analysis](docs/BotArmyStrategicAnalysis.md)** - Market positioning and competitive analysis

**For technical questions, architecture discussions, or contribution opportunities, please open a GitHub issue or discussion.**