# BotArmy POC - AI Multi-Agent System

A proof-of-concept multi-agent system that orchestrates AI agents through the Software Development Life Cycle (SDLC) to automatically generate functional web applications.

## 🚀 Quick Start

### Prerequisites
- **Python 3.11** (REQUIRED - ControlFlow doesn't work with 3.12+)
- **Node.js 18+** 
- **OpenAI API Key**

⚠️ **Important**: ControlFlow requires exactly Python 3.11. Python 3.12+ will not work.

### 1. Clone and Setup
```bash
git clone https://github.com/geniusboywonder/v0-botarmy-poc.git
cd v0-botarmy-poc

# Run the automated setup script
chmod +x setup.sh
./setup.sh
```

### 2. Configure Environment
```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your OpenAI API key
nano .env
```

### 3. Start the Application

**Terminal 1 - Backend:**
```bash
source venv/bin/activate
cd backend
python main.py
```

**Terminal 2 - Frontend:**
```bash
pnpm dev
# or: npm run dev / yarn dev
```

**Access:** http://localhost:3000

## 🔧 Manual Setup (if automated setup fails)

### Backend Setup
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r backend/requirements.txt
```

### Frontend Setup
```bash
# Install dependencies
pnpm install  # or npm install

# Build check
pnpm build
```

## 🎯 Features

- **Real-time Chat Interface** - Interact with AI agents through a clean chat UI
- **5 Specialized Agents** - Analyst, Architect, Developer, Tester, Deployer
- **WebSocket Communication** - Live updates and agent status
- **Agent Orchestration** - ControlFlow-powered workflow management
- **Modern UI** - Next.js with shadcn/ui components

## 🔍 Troubleshooting

### Python 3.11 Installation

**ControlFlow requires Python 3.11 specifically**. If you have Python 3.12+ or 3.10-, you need to install 3.11:

**macOS:**
```bash
# Install Python 3.11 via Homebrew
brew install python@3.11

# Or use our helper script
./install-python311-macos.sh
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-dev
```

**CentOS/RHEL:**
```bash
sudo dnf install python3.11 python3.11-pip
```

### Backend Issues

**ControlFlow Import Error:**
```bash
# Check Python version (MUST be 3.11)
python3 --version
python3.11 --version

# Remove old virtual environment
rm -rf venv

# Create new venv with Python 3.11
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install "prefect>=2.14.0,<3.0.0"
pip install "controlflow==0.8.0"
```

**OpenAI API Issues:**
```bash
# Test OpenAI connection
python3 -c "import openai; print('OpenAI installed successfully')"

# Check API key
echo $OPENAI_API_KEY
```

### Frontend Issues

**Module Not Found:**
```bash
# Clear Next.js cache
rm -rf .next
pnpm build

# Check all components exist
ls components/chat/
ls components/ui/
```

**Build Errors:**
```bash
# Check TypeScript issues
pnpm build 2>&1 | grep -i error
```

## 📁 Project Structure

```
├── app/                    # Next.js pages
├── backend/               # FastAPI backend
│   ├── main.py           # Main server file
│   ├── workflow.py       # Agent workflow
│   ├── agents/          # Agent implementations
│   └── requirements.txt  # Python dependencies
├── components/           # React components
│   ├── chat/            # Chat interface
│   └── ui/              # UI components
├── lib/                 # Utilities and stores
└── docs/               # Documentation
```

## 🧪 Testing

### Backend Test
```bash
# Test backend connection
curl http://localhost:8000

# Test WebSocket
wscat -c ws://localhost:8000/ws
```

### Frontend Test
```bash
# Access the app
open http://localhost:3000

# Test agent chat
# Enter: "Create a simple todo app"
```

## 🔑 Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key | `sk-...` |
| `BACKEND_URL` | Backend URL | `http://localhost:8000` |
| `WEBSOCKET_URL` | WebSocket URL | `ws://localhost:8000/ws` |

## 📋 Dependencies

### Backend
- FastAPI 0.104.1
- ControlFlow 0.8.0
- OpenAI 1.0.0+
- Uvicorn 0.24.0
- WebSockets 12.0

### Frontend  
- Next.js 15.2.4
- React 19
- TypeScript 5
- Tailwind CSS 4.1.9
- shadcn/ui components

## 🐛 Known Issues

1. **ControlFlow Dependency** - Experimental library, may have compatibility issues
2. **WebSocket Reliability** - Basic implementation, needs reconnection logic
3. **Error Handling** - Limited error boundaries in place
4. **Rate Limiting** - Basic OpenAI rate limiting implemented

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This is a proof-of-concept project. See LICENSE file for details.

## 🆘 Support

If you encounter issues:

1. Check this README's troubleshooting section
2. Verify all prerequisites are installed
3. Check the console for error messages
4. Open an issue with:
   - Your OS and versions
   - Full error messages
   - Steps to reproduce

---

**Status:** POC Phase - Active Development  
**Last Updated:** August 2025  
**Version:** 0.1.0