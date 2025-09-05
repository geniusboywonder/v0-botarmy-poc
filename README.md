# BotArmy POC - Dynamic AI Agent Orchestration Platform

A proof-of-concept multi-agent system that orchestrates specialized AI agents through dynamic workflows to automatically generate functional web applications. Features real-time human-in-the-loop collaboration, multi-LLM provider support, and extensible agent architectures.

## 🎯 Overview

BotArmy demonstrates sophisticated AI agent orchestration beyond traditional SDLC workflows. The platform supports dynamic team assembly, multi-domain problem solving (software development, marketing campaigns, technical support), and seamless human-AI collaboration through an intuitive chat interface.

**Key Capabilities:**

- **Dynamic Agent Teams** - Configure specialized agents for any domain
- **Human-in-the-Loop Control** - Real-time oversight with pause/resume workflows  
- **Multi-LLM Support** - OpenAI, Anthropic Claude, Google Gemini integration
- **Real-time Collaboration** - WebSocket-powered agent communication
- **🆕 CopilotKit Integration** - Advanced AI chat interface with embedded workflows
- **Extensible Architecture** - Plugin-based system for custom workflows

## 🛠 Environment Requirements

### **Current Environment Configuration**

The project is optimized for modern development environments with the latest stable versions:

| Component | Version | Notes |
|-----------|---------|-------|
| **Python** | **3.13.5** | Latest stable release with all new features |
| **Node.js** | **22.17.1** | Latest LTS release for optimal performance |
| **npm** | **11.5.2** | Latest stable package manager |
| **Next.js** | **15.5.2** | Current stable with React 19 support |
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
next@15.5.2
react@19.x
react-dom@19.x
typescript@5.x

# UI Framework & Styling
tailwindcss@3.4.17
postcss@8.5.6
autoprefixer@10.4.21
@radix-ui/*@latest
lucide-react@0.454.0

# AI Integration & Chat
@copilotkit/react-core@1.10.3
@copilotkit/react-ui@1.10.3
@copilotkit/react-textarea@1.10.3
@copilotkit/runtime@1.10.3

# State Management & Utilities
zustand@latest
clsx@2.1.1
tailwind-merge@2.5.5
```

## 🚀 Quick Start

### **Prerequisites Check**

```bash
# Verify versions
python --version      # Should show 3.13.5 (or 3.13.x)+ is fine)
node --version         # Should show 20.x.x  
npm --version          # Should show 10.x.x
```

### **1. Environment Setup**

**Install Latest Versions:**

```bash
# Python 3.13.5 (recommended) or 3.13.x+
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
python --version  # Should show 3.13.5 or 3.13.x+
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

**Access Application:** <http://localhost:3000>

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
├── app/api/                    # API Route Handlers (Next.js)
│   └── copilotkit/             # CopilotKit SSE endpoint
│       └── route.ts            # Server-sent events bridge
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
- **🆕 Recursion Protection:** Advanced workflow stability with circular reference prevention

### **2. Real-time Human-AI Collaboration**  

- **CopilotKit Chat Interface:** Advanced AI chat with embedded workflows and real-time agent integration
- **WebSocket Bridge:** Seamless communication between frontend CopilotKit and backend agent system  
- **Live Status Updates:** Real-time agent progress and task completion
- **Approval Workflows:** Human-in-the-loop decision points
- **Progress Tracking:** Visual indicators for workflow stages

### **3. Multi-LLM Provider Support**

- **Primary Providers:** OpenAI GPT-4, Anthropic Claude, Google Gemini
- **Intelligent Routing:** Automatic model selection based on task complexity
- **🆕 Connection Pooling:** HTTP connection optimization for improved performance
- **Enhanced Rate Limiting:** Multi-level API usage management and cost control
- **Fallback Logic:** Automatic provider switching on failures
- **🆕 Health Monitoring:** Real-time provider status and performance metrics

### **4. Enhanced Human-in-the-Loop Interface (v2.5)**

- **🎯 Agent Filtering with Visual Highlights**: Teal highlights indicate filtered agents with clear visual state
- **🔄 Auto-HITL Display**: Automatically shows HITL prompts when switching between agents with pending requests
- **🚨 Comprehensive Alert System**: Real-time HITL alerts bar combining system and agent-specific notifications
- **🖱️ Improved Event Handling**: Fixed expand/collapse conflicts with proper event target detection
- **📱 Responsive HITL Components**: Mobile-optimized interface with minimal and full rendering modes
- **🧭 Smart Navigation**: Direct navigation to HITL requests from alerts and agent status displays

### **5. Advanced WebSocket Communication**

- **Real-time Messaging:** Live agent-to-agent and human-agent communication
- **Status Broadcasting:** Agent progress and system health updates
- **Message Batching:** Performance optimization for high-volume scenarios
- **Auto-Reconnection:** Robust connection handling with exponential backoff

### **6. Enterprise Security & Validation**

- **🆕 YAML Schema Validation:** Comprehensive input validation with JSON Schema
- **🆕 Input Sanitization:** Multi-layer security against injection attacks
- **🆕 File Upload Security:** Advanced validation with malicious content detection
- **🆕 Rate Limiting:** Multi-dimensional abuse prevention (IP, user, global limits)
- **🆕 Security Pattern Detection:** Real-time threat identification and blocking

### **7. Extensible Architecture**

- **Plugin System:** Custom agent types and workflow patterns
- **Configuration-driven:** YAML/JSON-based agent and workflow definitions
- **Multi-framework Support:** ControlFlow + Prefect orchestration options
- **Community Integration:** Template sharing and collaborative development
- **🆕 Performance Monitoring:** Real-time metrics and optimization insights

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

## 🛡️ Security & Performance Features

### **Enterprise-Grade Security**

The platform implements multiple layers of security protection:

**Input Validation & Sanitization:**
```bash
# YAML files are validated against comprehensive JSON Schema
# Automatic detection of malicious patterns:
# - Prompt injection attempts
# - Command injection patterns  
# - SQL injection attempts
# - XSS attack vectors
# - Path traversal attempts
```

**Rate Limiting & Abuse Prevention:**
```bash
# Multi-level protection:
# - Per-IP: 10 uploads/hour
# - Per-user: 50 uploads/hour  
# - Global: 1000 uploads/hour
# - Automatic cleanup and monitoring
```

**File Upload Security:**
```bash
# Comprehensive file validation:
# - Size limits (1MB default)
# - MIME type verification
# - Content pattern detection
# - YAML bomb prevention (depth limits)
# - Real-time security scanning
```

### **Performance Optimizations**

**HTTP Connection Pooling:**
```bash
# Optimized LLM API communication:
# - Connection reuse across providers
# - Keep-alive optimization (5 min)
# - DNS caching enabled
# - Configurable limits (10 per provider)
# - Real-time pool statistics
```

**Intelligent Provider Management:**
```bash
# Enhanced LLM service features:
# - Health monitoring for all providers
# - Performance metrics tracking
# - Automatic provider fallback
# - Response time optimization
# - Cost tracking and optimization
```

**Workflow Stability:**
```bash
# Advanced workflow protection:
# - Circular reference prevention
# - Parameter serialization safety
# - Automatic error recovery
# - Memory leak prevention
# - Resource cleanup automation
```

### **Monitoring & Observability**

**Real-time Metrics:**
- Connection pool utilization
- Provider response times and success rates
- Security threat detection and blocking
- Rate limiting effectiveness
- System resource utilization

**Health Checks:**
```bash
# Comprehensive system monitoring:
GET /api/status    # System health overview
GET /api/health    # Detailed health check with services
GET /api/config    # Current system configuration
```

## 🔌 API Endpoints

The BotArmy backend provides a comprehensive REST API for system management, monitoring, and interaction. All endpoints are accessible when the backend is running on `http://localhost:8000`.

### **Core System Endpoints**

| Method | Endpoint | Description | Browser Access |
|--------|----------|-------------|---------------|
| `GET` | `/` | Root endpoint with system information and features | `http://localhost:8000/` |
| `GET` | `/health` | Basic health check with environment info | `http://localhost:8000/health` |
| `GET` | `/api/health` | Detailed health check with all services status | `http://localhost:8000/api/health` |

### **Configuration Management**

| Method | Endpoint | Description | Browser Access |
|--------|----------|-------------|---------------|
| `GET` | `/api/config` | Get current system configuration (agents, system settings) | `http://localhost:8000/api/config` |
| `POST` | `/api/config` | Update system configuration (requires JSON body) | API only |
| `POST` | `/api/config/refresh` | Refresh configuration cache from .env file | API only |

### **System Status & Monitoring**

| Method | Endpoint | Description | Browser Access |
|--------|----------|-------------|---------------|
| `GET` | `/api/status` | Enhanced system status with metrics and active workflows | `http://localhost:8000/api/status` |

### **File Upload & Rate Limiting**

| Method | Endpoint | Description | Browser Access |
|--------|----------|-------------|---------------|
| `POST` | `/api/uploads/validate` | Validate file uploads and check rate limits | API only |
| `GET` | `/api/uploads/rate-limit/{identifier}` | Check rate limit status for specific identifier | `http://localhost:8000/api/uploads/rate-limit/test` |
| `GET` | `/api/uploads/metrics` | Global upload metrics and statistics | `http://localhost:8000/api/uploads/metrics` |

### **Interactive Session Management**

| Method | Endpoint | Description | Browser Access |
|--------|----------|-------------|---------------|
| `GET` | `/api/interactive/sessions` | List all active interactive sessions | `http://localhost:8000/api/interactive/sessions` |
| `GET` | `/api/interactive/sessions/{session_id}/status` | Get specific session status | `http://localhost:8000/api/interactive/sessions/test-session/status` |
| `POST` | `/api/interactive/sessions/{session_id}/answers` | Submit answers for interactive questions | API only |
| `POST` | `/api/interactive/sessions/{session_id}/cancel` | Cancel an active interactive session | API only |

### **Performance Monitoring & Analytics**

| Method | Endpoint | Description | Browser Access |
|--------|----------|-------------|---------------|
| `GET` | `/api/performance/metrics/realtime` | Real-time performance metrics | `http://localhost:8000/api/performance/metrics/realtime` |
| `GET` | `/api/performance/summary?hours={N}` | Performance summary for specified time period | `http://localhost:8000/api/performance/summary?hours=24` |
| `GET` | `/api/performance/agents` | Agent performance metrics and statistics | `http://localhost:8000/api/performance/agents` |
| `GET` | `/api/performance/workflows/{workflow_id}` | Detailed metrics for specific workflow | API only |
| `GET` | `/api/performance/connections` | Connection diagnostics and WebSocket status | `http://localhost:8000/api/performance/connections` |
| `GET` | `/api/performance/dashboard` | Comprehensive dashboard data (all metrics) | `http://localhost:8000/api/performance/dashboard` |
| `POST` | `/api/performance/cleanup?hours={N}` | Clean up old performance data | API only |

### **CopilotKit Integration Endpoints**

| Method | Endpoint | Description | Browser Access |
|--------|----------|-------------|---------------|
| `POST` | `/api/copilotkit` | CopilotKit Server-Sent Events bridge to WebSocket backend | CopilotKit integration |

### **WebSocket Endpoints**

| Type | Endpoint | Description | Usage |
|------|----------|-------------|-------|
| `WS` | `/api/ws` | Main WebSocket connection for real-time communication | Frontend integration |
| `WS` | `/ws/interactive/{session_id}` | Interactive workflow WebSocket connection | Interactive sessions |

### **Quick API Testing**

Start the backend and test these endpoints in your browser:

```bash
# 1. Start the backend
cd backend && python main.py

# 2. Test key endpoints in browser:
# System Information
open http://localhost:8000/

# System Health & Status  
open http://localhost:8000/api/status

# Performance Dashboard (comprehensive metrics)
open http://localhost:8000/api/performance/dashboard

# Configuration View
open http://localhost:8000/api/config

# Upload Metrics
open http://localhost:8000/api/uploads/metrics
```

### **API Response Examples**

**System Status (`/api/status`):**
```json
{
  "active_workflows": 2,
  "environment": "development",
  "features_available": {
    "full_workflow": true,
    "websockets": true,
    "rate_limiting": true,
    "multi_llm": true,
    "upload_rate_limiting": true,
    "yaml_validation": true,
    "connection_pooling": true
  },
  "upload_metrics": { /* upload statistics */ },
  "llm_status": { /* LLM provider health */ }
}
```

**Performance Dashboard (`/api/performance/dashboard`):**
```json
{
  "dashboard_generated_at": "2025-01-15T10:30:00Z",
  "realtime_metrics": { /* current system metrics */ },
  "summary_1h": { /* last hour performance */ },
  "summary_24h": { /* last day performance */ },
  "connection_diagnostics": { /* WebSocket health */ },
  "agent_performance": { /* per-agent statistics */ },
  "llm_metrics": { /* LLM provider performance */ },
  "upload_metrics": { /* file upload statistics */ },
  "system_info": {
    "uptime_seconds": 3600,
    "monitoring_active": true,
    "active_workflows_count": 2
  }
}
```

**Interactive Sessions (`/api/interactive/sessions`):**
```json
{
  "sessions": [
    {
      "session_id": "session-123",
      "status": "waiting_for_answer",
      "current_question": { /* question details */ },
      "created_at": "2025-01-15T10:00:00Z"
    }
  ],
  "total_count": 1
}
```

## 🔍 Troubleshooting

### **Environment Issues**

**Python Version Flexibility:**

```bash
# Check Python version - 3.13.5+ or 3.13 both work great
python --version  # Should show 3.13.5.x or 3.13.x

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

# CopilotKit integration is fully compatible with React 19
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

# Install optional aiohttp for connection pooling:
pip install aiohttp>=3.8.0
```

**Security & Performance Issues:**

```bash
# Test workflow recursion fix:
python test_workflow_recursion.py

# Check security validation:
curl -X POST http://localhost:8000/api/validate-upload \
  -H "Content-Type: application/json" \
  -d '{"filename":"test.yaml","content":"test: value"}'

# Monitor connection pool status:
curl http://localhost:8000/api/status | jq '.connection_pool_stats'

# Check rate limiting status:
curl http://localhost:8000/api/status | jq '.rate_limiting'

# Verify LLM provider health:
curl http://localhost:8000/api/status | jq '.llm_providers'
```

**Workflow Recursion Issues:**

```bash
# If you encounter "maximum recursion depth exceeded":
# 1. Check that Prefect flows have persist_result=False
# 2. Verify AgentStatusBroadcaster serialization safety
# 3. Test with: python test_workflow_recursion.py
# 4. Monitor logs for circular reference warnings
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

### **✅ Read docs/PLAN.md to understand the plan and next steps**

### **✅ Read docs/PROGRESS.md to understand progress made**

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

- Python 3.13.5+ runtime (supports 3.13)
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
3. **Verify environment** matches requirements (Python 3.13.5+, Node.js 20)
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

## 🆕 Recent Updates

### **HITL Interface Enhancements v2.5 (2025-09-05)**

**🎯 Human-in-the-Loop Interface Improvements:**
- **Enhanced Agent Filtering**: Teal visual highlights for filtered agents with smart navigation to pending HITL requests
- **Auto-HITL Display**: Automatically shows HITL prompts when switching between agents with active requests
- **Comprehensive Alert System**: New HITL alerts bar combining system alerts and agent-specific notifications
- **Improved Event Handling**: Fixed expand/collapse conflicts in artifact summaries with proper event target detection
- **Responsive Components**: Mobile-optimized HITL interface with dual rendering modes (minimal/full)
- **Real-time Navigation**: Direct navigation to HITL requests from alerts and status indicators

**🔧 Technical Improvements:**
- **Component Architecture**: New `HITLAlertsBar` and enhanced `HITLApproval` components with flexible rendering
- **Event Management**: Advanced event handling with `stopPropagation()` and `closest()` target detection
- **State Management**: Enhanced Zustand store integration for HITL state synchronization
- **Type Safety**: Improved TypeScript interfaces across all HITL-related components

**📁 New Components Added:**
- `components/hitl/hitl-alerts-bar.tsx` - Comprehensive HITL alert management system
- `components/ui/alert.tsx` - Standard shadcn/ui Alert component with accessibility features
- Enhanced HITL integration across chat, header, and process summary components

### **CopilotKit Integration (2025-09-03)**

The project has been successfully integrated with CopilotKit for advanced AI chat capabilities:

**✅ What's New:**
- **CopilotKit React Components**: Full integration with @copilotkit/react-core, react-ui, react-textarea, and runtime packages
- **Server-Sent Events Bridge**: Seamless communication between CopilotKit frontend and WebSocket backend
- **React 19 Compatibility**: All hydration issues resolved, clean rendering with latest React version
- **Enhanced Chat Interface**: Embedded AI workflows with real-time agent communication

**🔧 Technical Implementation:**
- **Frontend Configuration**: CopilotKit provider with `publicApiKey` authentication
- **API Bridge**: `/api/copilotkit` endpoint handling SSE streams from WebSocket messages
- **Component Updates**: Enhanced chat interfaces with CopilotKit integration
- **Error Handling**: Robust error boundaries and fallback mechanisms

**📋 Migration Status:**
- ✅ Dependencies installed and configured
- ✅ React 19 hydration issues resolved  
- ✅ CopilotKit provider properly configured
- ✅ WebSocket bridge operational
- ✅ All integration tests passing
- ✅ Documentation updated

**📚 Documentation:**
- Complete migration details in `docs/MIGRATION_COPILOTKIT.md`
- Updated project instructions in `CLAUDE.md`
- Updated dependency specifications in this README

---

**Project Status:** Active Development - Proof of Concept  
**Last Updated:** September 5, 2025  
**Version:** 2.5.0 - HITL Interface & User Experience Enhancements  
**Previous:** 0.3.0 - CopilotKit Integration Complete  
**Next Release:** Enhanced Multi-Domain Agent Support with Advanced HITL Workflows

---

## 📚 Additional Resources

- **[Development Plan v3](docs/PLAN.md)** - Detailed development roadmap
- **[Progress Tracking](docs/PROGRESS.md)** - Feature implementation status  
- **[API Endpoints Documentation](docs/API_ENDPOINTS.md)** - Complete REST API reference with examples

**For technical questions, architecture discussions, or contribution opportunities, please open a GitHub issue or discussion.**
