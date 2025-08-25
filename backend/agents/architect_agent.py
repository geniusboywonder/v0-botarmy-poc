"""
Architect Agent with proper logging, safety limits, and improved fallback responses.
Combines safety features with enhanced architecture recommendations.
"""
import asyncio
import logging
import os

from backend.runtime_env import get_controlflow, get_prefect, IS_REPLIT

cf = get_controlflow()
prefect = get_prefect()

logger = logging.getLogger(__name__)

# Safety counter to prevent infinite loops
_architect_call_count = 0
MAX_LLM_CALLS = 1

ARCHITECT_SYSTEM_PROMPT = """
You are a master AI software architect. Your goal is to take a requirements
document and produce a high-level technical architecture specification.

The specification should include:
1. **Technology Stack:** A list of recommended technologies (e.g., Frontend Framework, Backend Language, Database).
2. **System Components:** A breakdown of the major components of the system (e.g., API Server, Database, Caching Layer, Frontend App).
3. **Data Model:** A simple representation of the core data entities and their relationships.
4. **API Endpoints:** A list of key API endpoints, including the HTTP method, path, and a brief description.
5. **Security Considerations:** Basic security requirements

Produce the output in Markdown format. Be concise and clear.
"""

def should_be_interactive() -> bool:
    """Determine if the architect task should request human approval"""
    hitl_enabled = os.getenv("ENABLE_HITL", "true").lower() == "true"
    auto_action = os.getenv("AUTO_ACTION", "none").lower()
    return hitl_enabled and auto_action == "none" and not IS_REPLIT

@cf.task(interactive=should_be_interactive())
async def run_architect_task(requirements_document: str) -> str:
    """
    Architect Agent task with proper logging, safety limits, and enhanced fallback responses.
    """
    global _architect_call_count

    # Get appropriate logger
    if IS_REPLIT:
        current_logger = logger
        current_logger.info(f"🏗️ Starting Architect Agent (Replit mode)")
    else:
        try:
            current_logger = prefect.get_run_logger()
        except:
            current_logger = logger
        current_logger.info(f"🏗️ Starting Architect Agent (Development mode)")

    # Log the input
    input_preview = requirements_document[:200] + "..." if len(requirements_document) > 200 else requirements_document
    current_logger.info(f"📝 INPUT RECEIVED: '{input_preview}'")
    current_logger.info(f"📊 Agent call count: {_architect_call_count}/{MAX_LLM_CALLS}")

    # Safety check - prevent infinite loops
    if _architect_call_count >= MAX_LLM_CALLS:
        current_logger.warning(f"🚨 SAFETY LIMIT REACHED: Architect has made {_architect_call_count} LLM calls. Returning enhanced fallback.")
        return f"""# Technical Architecture - Enhanced Fallback Response

## System Overview
⚠️ **Safety Limit Active**: This agent has reached its maximum LLM call limit ({MAX_LLM_CALLS} calls) to prevent infinite loops.

## Recommended Architecture
Based on requirements: "{requirements_document[:150]}..."

### Technology Stack
- **Frontend:** React/Next.js with TypeScript
- **Backend:** Python FastAPI with async support
- **Database:** PostgreSQL for structured data
- **Caching:** Redis for session management
- **Deployment:** Railway + Replit for development

### System Components
1. **Frontend Application** - User interface and client-side logic
2. **REST API Server** - Business logic and data processing
3. **Database Layer** - Data persistence and queries
4. **Authentication Service** - User management and security
5. **WebSocket Service** - Real-time communication

### Data Model
- Core entities based on requirements analysis
- Relational structure with proper normalization
- API-first design for frontend integration

### Key API Endpoints
- GET/POST /api/auth/* - Authentication endpoints
- GET/POST /api/data/* - Core data operations
- WebSocket /ws - Real-time communication

### Security Considerations
- Input validation and sanitization
- Authentication and authorization
- CORS configuration for frontend
- Rate limiting for API protection

## Status
✅ Enhanced fallback architecture provided
🔄 Ready to hand off to Developer Agent

---
*Safety limit: {_architect_call_count}/{MAX_LLM_CALLS} calls made*"""

    # Increment call counter
    _architect_call_count += 1
    current_logger.info(f"🚀 Making LLM call #{_architect_call_count}")

    # Create and execute the architect agent
    current_logger.info("🤖 Creating BaseAgent with system prompt...")
    
    try:
        from backend.agents.base_agent import BaseAgent
        architect_agent = BaseAgent(ARCHITECT_SYSTEM_PROMPT)
        current_logger.info("📡 Calling LLM for architecture design...")
        architecture_doc = await architect_agent.execute(
            user_prompt=f"Create technical architecture for:\n{requirements_document}", 
            context=""
        )

        # Log the output (truncated for readability)
        output_preview = architecture_doc[:200] + "..." if len(architecture_doc) > 200 else architecture_doc
        current_logger.info(f"✅ LLM RESPONSE RECEIVED (preview): {output_preview}")
        current_logger.info(f"📏 Full response length: {len(architecture_doc)} characters")
        current_logger.info("🎯 Architect Agent completed successfully")
        
        return architecture_doc
        
    except Exception as e:
        error_msg = f"Architect Agent error: {str(e)}"
        current_logger.error(f"❌ LLM CALL FAILED: {error_msg}")
        
        return f"""# Technical Architecture - Error Recovery

## Issue
⚠️ Automated architecture design failed: {str(e)}

## Enhanced Fallback Architecture
Based on requirements: "{requirements_document[:100]}..."

### Recommended Technology Stack
- **Frontend:** React/Next.js with TypeScript and Tailwind CSS
- **Backend:** Python FastAPI with async support
- **Database:** PostgreSQL for relational data
- **Real-time:** WebSockets for live updates
- **Deployment:** Railway + Replit development environment

### System Components
1. **Frontend Application** - Modern React-based UI
2. **REST API Server** - FastAPI backend service
3. **Database Layer** - PostgreSQL with proper indexing
4. **Authentication Service** - JWT-based user management
5. **WebSocket Handler** - Real-time communication layer

### Core Data Entities
- User management and profiles
- Application-specific data models
- Audit trails and logging
- Configuration and settings

### Essential API Endpoints
- `POST /api/auth/login` - User authentication
- `GET /api/data/list` - Data retrieval
- `POST /api/data/create` - Data creation
- `WebSocket /ws` - Real-time updates

### Security & Performance
- Input validation with Pydantic models
- Rate limiting and CORS configuration  
- Database connection pooling
- Error handling and logging

## Next Steps
- Manual architecture review recommended
- Technical team consultation advised
- Consider specific requirements for optimization

---
*Error: {str(e)}*"""

def reset_architect_call_count():
    """Reset the call counter (for testing)"""
    global _architect_call_count
    _architect_call_count = 0
    logger.info(f"🔄 Architect call counter reset to 0")

def get_architect_call_count():
    """Get current call count"""
    return _architect_call_count