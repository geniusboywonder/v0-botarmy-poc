# BotArmy Environment Setup Instructions

## Required Environment Variables

Create a `.env` file in the project root with:

```bash
# OpenAI API Configuration
OPENAI_API_KEY=your-openai-api-key-here

# Gemini API Configuration  
GEMINI_KEY_KEY=your-gemini-api-key-here

# Backend Configuration
BACKEND_HOST=localhost
BACKEND_PORT=8000
BACKEND_URL=http://localhost:8000

# WebSocket Configuration
WEBSOCKET_URL=ws://localhost:8000/api/ws
NEXT_PUBLIC_WEBSOCKET_URL=ws://localhost:8000/api/ws

# Safety Settings (for testing without API costs)
TEST_MODE=true
AGENT_TEST_MODE=true
ENABLE_HITL=true
AUTO_ACTION=none
```

## Getting API Keys

1. **OpenAI**: Visit https://platform.openai.com/api-keys
2. **Gemini**: Visit https://makersuite.google.com/app/apikey

## Testing Without API Keys

The system works in TEST_MODE without real API keys:
- Set `TEST_MODE=true` (default)
- Set `AGENT_TEST_MODE=true` (default) 
- Agents return mock responses instead of calling LLMs
- No API costs incurred during testing
