# BotArmy API Endpoints Documentation

**Version:** 3.0.0  
**Last Updated:** September 3, 2025  
**Base URL:** `http://localhost:8000` (Development)

This document provides comprehensive documentation for all REST API endpoints available in the BotArmy backend.

---

## 📊 Overview

The BotArmy backend provides a RESTful API for:
- System health monitoring and configuration
- Performance metrics and analytics
- Interactive session management
- File upload validation and rate limiting
- Real-time WebSocket communication

All endpoints return JSON responses unless otherwise specified.

---

## 🔌 Core System Endpoints

### `GET /`
**Description:** Root endpoint with system information and available features  
**Response:** System status, version, environment, and feature flags  
**Browser Access:** `http://localhost:8000/`

**Example Response:**
```json
{
  "message": "BotArmy Backend is running",
  "version": "3.0.0",
  "environment": "Development",
  "features": {
    "full_workflow": true,
    "controlflow": true,
    "prefect": true,
    "websockets": true,
    "llm_integration": true,
    "rate_limiting": true,
    "multi_llm": true,
    "hitl": true
  },
  "runtime_info": { /* environment details */ }
}
```

### `GET /health`
**Description:** Basic health check with environment information  
**Response:** Simple health status and environment type  
**Browser Access:** `http://localhost:8000/health`

**Example Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-09-03T10:30:00Z",
  "environment": "development",
  "port": "8000"
}
```

### `GET /api/health`
**Description:** Detailed health check with all services status  
**Response:** Comprehensive health information including service availability  
**Browser Access:** `http://localhost:8000/api/health`

**Example Response:**
```json
{
  "status": "healthy",
  "environment": "development",
  "timestamp": "2025-09-03T10:30:00Z",
  "version": "1.0.0",
  "services": {
    "websocket": "available",
    "llm_providers": ["openai", "google"],
    "test_mode": false
  }
}
```

---

## ⚙️ Configuration Management

### `GET /api/config`
**Description:** Get current system configuration including agents and system settings  
**Response:** Complete system configuration object  
**Browser Access:** `http://localhost:8000/api/config`

**Example Response:**
```json
{
  "system": {
    "max_agents": 5,
    "agent_timeout": 300,
    "debug": true,
    "log_level": "INFO",
    "websocket_heartbeat_interval": 30,
    "interactive_timeout_minutes": 5,
    "max_questions_per_session": 10,
    "auto_proceed_on_timeout": false,
    "max_concurrent_workflows": 5,
    "max_retry_attempts": 3
  },
  "agents": { /* agent configurations */ },
  "environment": { /* environment info */ }
}
```

### `POST /api/config`
**Description:** Update system configuration  
**Method:** POST  
**Content-Type:** application/json  
**Body:** Configuration update object  

**Example Request:**
```json
{
  "system": {
    "max_agents": 10,
    "agent_timeout": 600
  }
}
```

**Example Response:**
```json
{
  "status": "success",
  "message": "Updated: max_agents, agent_timeout",
  "updated_fields": ["max_agents", "agent_timeout"]
}
```

### `POST /api/config/refresh`
**Description:** Refresh configuration cache from .env file  
**Method:** POST  
**Response:** Refresh confirmation with timestamp

**Example Response:**
```json
{
  "status": "success",
  "message": "Configuration cache refreshed from .env file",
  "timestamp": "2025-09-03T10:30:00Z"
}
```

---

## 📈 System Status & Monitoring

### `GET /api/status`
**Description:** Enhanced system status with metrics and active workflows  
**Response:** Comprehensive system status including performance metrics  
**Browser Access:** `http://localhost:8000/api/status`

**Example Response:**
```json
{
  "active_workflows": 2,
  "environment": "development",
  "features_available": {
    "full_workflow": true,
    "websockets": true,
    "artifacts": true,
    "controlflow": true,
    "rate_limiting": true,
    "multi_llm": true,
    "hitl": true,
    "upload_rate_limiting": true,
    "yaml_validation": true,
    "connection_pooling": true
  },
  "upload_metrics": {
    "total_uploads": 150,
    "failed_uploads": 5,
    "rate_limited_requests": 12
  },
  "llm_status": {
    "openai": "healthy",
    "google": "healthy",
    "anthropic": "unavailable"
  }
}
```

---

## 📁 File Upload & Rate Limiting

### `POST /api/uploads/validate`
**Description:** Validate file uploads and check rate limits  
**Method:** POST  
**Content-Type:** application/json  
**Response:** Validation result and rate limit status

**Example Response:**
```json
{
  "status": "allowed",
  "message": "Upload allowed within rate limits",
  "rate_limit_info": {
    "remaining_uploads": 8,
    "reset_time": "2025-09-03T11:00:00Z"
  }
}
```

### `GET /api/uploads/rate-limit/{identifier}`
**Description:** Check rate limit status for specific identifier (IP, user, etc.)  
**Parameters:** `identifier` - IP address or user identifier  
**Browser Access:** `http://localhost:8000/api/uploads/rate-limit/192.168.1.1`

**Example Response:**
```json
{
  "identifier": "192.168.1.1",
  "current_count": 2,
  "limit": 10,
  "remaining": 8,
  "reset_time": "2025-09-03T11:00:00Z",
  "blocked": false
}
```

### `GET /api/uploads/metrics`
**Description:** Global upload metrics and statistics  
**Response:** Comprehensive upload statistics and performance metrics  
**Browser Access:** `http://localhost:8000/api/uploads/metrics`

**Example Response:**
```json
{
  "upload_metrics": {
    "total_uploads_today": 450,
    "successful_uploads": 425,
    "failed_uploads": 25,
    "rate_limited_requests": 15,
    "average_upload_size": "1.2MB",
    "top_blocked_ips": ["192.168.1.100", "10.0.0.50"]
  },
  "llm_metrics": {
    "total_requests": 1250,
    "average_response_time": "2.3s",
    "provider_distribution": {
      "openai": 60,
      "google": 30,
      "anthropic": 10
    }
  },
  "timestamp": "2025-09-03T10:30:00Z"
}
```

---

## 🔄 Interactive Session Management

### `GET /api/interactive/sessions`
**Description:** List all active interactive sessions  
**Response:** Array of active interactive sessions with their status  
**Browser Access:** `http://localhost:8000/api/interactive/sessions`

**Example Response:**
```json
{
  "sessions": [
    {
      "session_id": "session-abc123",
      "status": "waiting_for_answer",
      "current_question": {
        "question_id": "q1",
        "text": "What is the primary goal of your application?",
        "type": "text"
      },
      "created_at": "2025-09-03T10:00:00Z",
      "workflow_config": "interactive_sdlc"
    },
    {
      "session_id": "session-def456",
      "status": "processing",
      "current_stage": "architect",
      "created_at": "2025-09-03T09:45:00Z"
    }
  ],
  "total_count": 2
}
```

### `GET /api/interactive/sessions/{session_id}/status`
**Description:** Get specific session status and current state  
**Parameters:** `session_id` - Unique session identifier  
**Browser Access:** `http://localhost:8000/api/interactive/sessions/session-abc123/status`

**Example Response:**
```json
{
  "session_id": "session-abc123",
  "status": "waiting_for_answer",
  "current_question": {
    "question_id": "q2",
    "text": "What specific features should the application include?",
    "type": "multi_choice",
    "options": ["User Authentication", "Data Export", "Real-time Updates", "Mobile Support"]
  },
  "questions_answered": 1,
  "total_questions": 5,
  "workflow_progress": 20,
  "timeout_at": "2025-09-03T10:35:00Z",
  "created_at": "2025-09-03T10:00:00Z"
}
```

### `POST /api/interactive/sessions/{session_id}/answers`
**Description:** Submit answers for interactive questions  
**Method:** POST  
**Content-Type:** application/json  
**Parameters:** `session_id` - Session identifier

**Example Request:**
```json
{
  "question_id": "q2",
  "answer": "User Authentication, Real-time Updates"
}
```

**Example Response:**
```json
{
  "status": "success",
  "message": "Answer submitted successfully",
  "session_status": {
    "session_id": "session-abc123",
    "questions_answered": 2,
    "next_question": {
      "question_id": "q3",
      "text": "What is your target user base size?"
    }
  }
}
```

### `POST /api/interactive/sessions/{session_id}/cancel`
**Description:** Cancel an active interactive session  
**Method:** POST  
**Parameters:** `session_id` - Session identifier

**Example Response:**
```json
{
  "status": "success",
  "message": "Interactive session cancelled"
}
```

---

## 📊 Performance Monitoring & Analytics

### `GET /api/performance/metrics/realtime`
**Description:** Real-time performance metrics  
**Response:** Current system performance indicators  
**Browser Access:** `http://localhost:8000/api/performance/metrics/realtime`

**Example Response:**
```json
{
  "timestamp": "2025-09-03T10:30:00Z",
  "system": {
    "cpu_usage": 15.5,
    "memory_usage": 245.7,
    "active_connections": 12,
    "uptime_seconds": 86400
  },
  "workflows": {
    "active_count": 3,
    "completed_today": 45,
    "failed_today": 2,
    "average_duration": "8.5min"
  },
  "agents": {
    "analyst": {"active": true, "tasks_completed": 15},
    "architect": {"active": false, "tasks_completed": 12},
    "developer": {"active": true, "tasks_completed": 8}
  }
}
```

### `GET /api/performance/summary?hours={N}`
**Description:** Performance summary for specified time period  
**Parameters:** `hours` - Time period in hours (1-168)  
**Browser Access:** `http://localhost:8000/api/performance/summary?hours=24`

**Example Response:**
```json
{
  "time_period": "24 hours",
  "summary": {
    "total_workflows": 125,
    "successful_workflows": 118,
    "failed_workflows": 7,
    "success_rate": 94.4,
    "average_duration": "6.8min",
    "peak_concurrent": 15
  },
  "agent_performance": {
    "analyst": {"completion_rate": 98.5, "avg_duration": "45s"},
    "architect": {"completion_rate": 96.2, "avg_duration": "2.1min"},
    "developer": {"completion_rate": 89.5, "avg_duration": "4.2min"}
  },
  "llm_usage": {
    "total_requests": 2450,
    "provider_breakdown": {
      "openai": {"requests": 1470, "avg_latency": "1.8s"},
      "google": {"requests": 735, "avg_latency": "2.1s"},
      "anthropic": {"requests": 245, "avg_latency": "1.5s"}
    }
  }
}
```

### `GET /api/performance/agents`
**Description:** Agent performance metrics and statistics  
**Response:** Per-agent performance data and historical trends  
**Browser Access:** `http://localhost:8000/api/performance/agents`

**Example Response:**
```json
{
  "agents": {
    "analyst": {
      "total_tasks": 150,
      "completed_tasks": 148,
      "failed_tasks": 2,
      "success_rate": 98.7,
      "average_duration": "42s",
      "current_status": "idle"
    },
    "architect": {
      "total_tasks": 120,
      "completed_tasks": 115,
      "failed_tasks": 5,
      "success_rate": 95.8,
      "average_duration": "2.3min",
      "current_status": "working"
    },
    "developer": {
      "total_tasks": 95,
      "completed_tasks": 85,
      "failed_tasks": 10,
      "success_rate": 89.5,
      "average_duration": "5.1min",
      "current_status": "working"
    }
  },
  "timestamp": "2025-09-03T10:30:00Z"
}
```

### `GET /api/performance/workflows/{workflow_id}`
**Description:** Detailed metrics for specific workflow  
**Parameters:** `workflow_id` - Unique workflow identifier  
**Response:** Comprehensive workflow execution details

**Example Response:**
```json
{
  "workflow_id": "wf-abc123",
  "config_name": "sdlc",
  "session_id": "session-def456",
  "status": "completed",
  "start_time": "2025-09-03T10:00:00Z",
  "end_time": "2025-09-03T10:08:30Z",
  "duration": "8.5min",
  "agents_used": ["analyst", "architect", "developer", "tester"],
  "artifacts_created": 15,
  "error_message": null,
  "is_completed": true,
  "stage_breakdown": {
    "analysis": {"duration": "45s", "status": "completed"},
    "architecture": {"duration": "2.1min", "status": "completed"},
    "development": {"duration": "4.5min", "status": "completed"},
    "testing": {"duration": "1.4min", "status": "completed"}
  }
}
```

### `GET /api/performance/connections`
**Description:** Connection diagnostics and WebSocket status  
**Response:** WebSocket connection health and client diagnostics  
**Browser Access:** `http://localhost:8000/api/performance/connections`

**Example Response:**
```json
{
  "system_diagnostics": {
    "total_connections": 12,
    "active_connections": 10,
    "disconnected_clients": 2,
    "average_connection_age": "15min",
    "messages_sent_today": 5420,
    "messages_received_today": 3680
  },
  "connection_health": {
    "healthy_connections": 10,
    "unhealthy_connections": 0,
    "reconnection_rate": 0.02,
    "heartbeat_success_rate": 99.8
  },
  "performance_metrics": {
    "average_message_latency": "12ms",
    "peak_concurrent_connections": 25,
    "bandwidth_usage": "1.2MB/hour"
  }
}
```

### `GET /api/performance/dashboard`
**Description:** Comprehensive dashboard data with all key metrics  
**Response:** Complete system overview for dashboard display  
**Browser Access:** `http://localhost:8000/api/performance/dashboard`

**Example Response:**
```json
{
  "dashboard_generated_at": "2025-09-03T10:30:00Z",
  "realtime_metrics": { /* real-time system data */ },
  "summary_1h": { /* last hour performance */ },
  "summary_24h": { /* last 24 hours performance */ },
  "connection_diagnostics": { /* WebSocket health */ },
  "agent_performance": { /* per-agent statistics */ },
  "llm_metrics": { /* LLM provider performance */ },
  "upload_metrics": { /* file upload statistics */ },
  "system_info": {
    "uptime_seconds": 86400,
    "monitoring_active": true,
    "active_workflows_count": 3
  }
}
```

### `POST /api/performance/cleanup?hours={N}`
**Description:** Clean up old performance data  
**Method:** POST  
**Parameters:** `hours` - Age threshold for cleanup (1-8760)

**Example Response:**
```json
{
  "status": "success",
  "message": "Cleaned up metrics older than 24 hours",
  "cleaned_at": "2025-09-03T10:30:00Z"
}
```

---

## 🔌 WebSocket Endpoints

### `WS /api/ws`
**Description:** Main WebSocket connection for real-time communication  
**Protocol:** WebSocket  
**Usage:** Frontend integration for real-time updates

**Connection URL:** `ws://localhost:8000/api/ws`

**Message Types:**
- `heartbeat_response` - Client heartbeat response
- `ping` - Connection test
- `user_command` - User commands (ping, test_openai, chat_message, etc.)
- `agent_command` - Agent control commands (pause_agent, resume_agent)
- `artifacts_get_all` - Request all artifacts

### `WS /ws/interactive/{session_id}`
**Description:** Interactive workflow WebSocket connection  
**Protocol:** WebSocket  
**Parameters:** `session_id` - Session identifier  
**Usage:** Interactive session communication

**Connection URL:** `ws://localhost:8000/ws/interactive/session-abc123`

---

## 🧪 Quick Testing Commands

### Start Backend
```bash
cd backend && python main.py
```

### Test Core Endpoints
```bash
# System Information
curl http://localhost:8000/ | jq

# System Status
curl http://localhost:8000/api/status | jq

# Configuration
curl http://localhost:8000/api/config | jq

# Performance Dashboard
curl http://localhost:8000/api/performance/dashboard | jq
```

### Test Interactive Sessions
```bash
# List active sessions
curl http://localhost:8000/api/interactive/sessions | jq

# Submit answer (example)
curl -X POST http://localhost:8000/api/interactive/sessions/session-123/answers \
  -H "Content-Type: application/json" \
  -d '{"question_id": "q1", "answer": "Web application"}'
```

### Test Performance Monitoring
```bash
# Real-time metrics
curl http://localhost:8000/api/performance/metrics/realtime | jq

# 24-hour summary
curl http://localhost:8000/api/performance/summary?hours=24 | jq

# Agent performance
curl http://localhost:8000/api/performance/agents | jq
```

---

## 🔧 Error Responses

All API endpoints use consistent error response format:

### 400 Bad Request
```json
{
  "detail": "Invalid request parameters or missing required fields"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 429 Too Many Requests
```json
{
  "detail": "Rate limit exceeded. Please try again later."
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error message"
}
```

---

## 📚 Integration Examples

### Frontend WebSocket Integration
```typescript
const ws = new WebSocket('ws://localhost:8000/api/ws');

ws.onmessage = (event) => {
  const message = JSON.parse(event.data);
  console.log('Received:', message);
};

// Send ping
ws.send(JSON.stringify({
  type: 'user_command',
  data: { command: 'ping' },
  session_id: 'my-session'
}));
```

### Performance Monitoring Integration
```typescript
const fetchDashboardData = async () => {
  const response = await fetch('/api/performance/dashboard');
  const data = await response.json();
  return data;
};
```

### Interactive Session Management
```typescript
const submitAnswer = async (sessionId: string, questionId: string, answer: string) => {
  const response = await fetch(`/api/interactive/sessions/${sessionId}/answers`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question_id: questionId, answer })
  });
  return await response.json();
};
```

---

## ⚙️ Environment Settings & Configuration

### `GET /api/env-settings`
**Description:** Retrieve editable environment variables and workflow configuration  
**Frontend Route:** Available at `/settings` page  
**Response:** List of configurable environment variables with categories

**Example Response:**
```json
{
  "success": true,
  "variables": [
    {
      "key": "WORKFLOW_REQUIREMENTS_GATHERING_ENABLED",
      "value": true,
      "description": "Enable interactive requirements gathering in workflows",
      "category": "Workflow Configuration",
      "type": "boolean"
    },
    {
      "key": "WORKFLOW_REQUIREMENTS_MAX_QUESTIONS",
      "value": 5,
      "description": "Maximum number of requirements gathering questions",
      "category": "Workflow Configuration", 
      "type": "number"
    },
    {
      "key": "AGENT_TEST_MODE",
      "value": true,
      "description": "Enable agent test mode to return static confirmations",
      "category": "Testing Configuration",
      "type": "boolean"
    }
  ]
}
```

### `POST /api/env-settings`
**Description:** Update environment variables and workflow configuration  
**Method:** POST  
**Content-Type:** application/json  
**Response:** Update success status

**Example Request:**
```json
{
  "variables": [
    {
      "key": "WORKFLOW_REQUIREMENTS_GATHERING_ENABLED",
      "value": true,
      "type": "boolean"
    },
    {
      "key": "WORKFLOW_REQUIREMENTS_MAX_QUESTIONS", 
      "value": 3,
      "type": "number"
    }
  ]
}
```

**Example Response:**
```json
{
  "success": true,
  "message": "Environment variables updated successfully"
}
```

### `POST /api/config-refresh`
**Description:** Refresh backend configuration cache after environment updates  
**Method:** POST  
**Content-Type:** application/json  
**Response:** Cache refresh status

**Example Response:**
```json
{
  "status": "success",
  "message": "Configuration cache refreshed successfully"
}
```

## 🔧 Enhanced 10-Step Workflow Configuration

The following environment variables control the enhanced 10-step workflow behavior:

### Requirements Gathering Configuration
- `WORKFLOW_REQUIREMENTS_GATHERING_ENABLED` - Enable/disable interactive requirements collection
- `WORKFLOW_REQUIREMENTS_MAX_QUESTIONS` - Maximum questions to ask (default: 5)
- `WORKFLOW_REQUIREMENTS_TIMEOUT_MINUTES` - Timeout for user responses (default: 10) 
- `WORKFLOW_REQUIREMENTS_AUTO_PROCEED` - Auto-proceed on timeout (default: true)

### Human-in-the-Loop (HITL) Checkpoints
- `WORKFLOW_HITL_ANALYZE_REQUIRED` - Require approval at Analyze stage (default: true)
- `WORKFLOW_HITL_ANALYZE_TIMEOUT_MINUTES` - Analyze stage timeout (default: 30)
- `WORKFLOW_HITL_DESIGN_REQUIRED` - Require approval at Design stage (default: false)
- `WORKFLOW_HITL_DESIGN_TIMEOUT_MINUTES` - Design stage timeout (default: 30)

### Artifact Scaffolding
- `WORKFLOW_ARTIFACT_AUTO_PLACEHOLDERS` - Auto-create placeholders (default: true)
- `WORKFLOW_ARTIFACT_UI_INTEGRATION` - Enable UI integration (default: true)

**UI Access:** All workflow configuration items are editable via the Settings page at `/settings`

---

**Documentation Version:** 3.0.0  
**Last Updated:** September 3, 2025  
**Maintainer:** BotArmy Development Team