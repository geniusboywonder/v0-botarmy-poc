# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Important

- ASK FOR CLARIFICATION If you are uncertain of any of thing within the document.
- ALL instructions within this document MUST BE FOLLOWED, these are not optional unless explicitly stated.
- DO NOT edit more code than you have to.
- DO NOT WASTE TOKENS, be succinct and concise.
- Follow the code protocol in docs/CODEPROTOCOL.md.
- Follow the front-end style guide in docs/STYLEGUIDE.md.

## Development Commands

### Frontend (Next.js)

```bash
npm run dev           # Start development server (localhost:3000)
npm run build         # Build for production
npm run start         # Start production server
npm run lint          # Run ESLint
npm run test          # Run Vitest tests
npm run test:ui       # Run Vitest with UI
```

### Backend (FastAPI)

```bash
# Activate Python environment first
source venv/bin/activate
cd backend && python main.py  # Start backend server (localhost:8000)
```

### Full-stack Development

```bash
npm run replit:dev    # Start both frontend and backend concurrently
npm run kill          # Kill running processes
npm run restart       # Kill and restart both services
```

### Testing

```bash
npm test              # Run frontend tests with Vitest
python -m pytest backend/tests/  # Run backend tests
```

## Architecture Overview

### Core Technology Stack

- **Frontend**: Next.js 15 with React 19, TypeScript, Tailwind CSS
- **Backend**: FastAPI with Python 3.13+, WebSocket support
- **AI Orchestration**: ControlFlow + Prefect for agent workflows
- **LLM Providers**: OpenAI, Anthropic Claude, Google Gemini
- **State Management**: Zustand stores for frontend state
- **Real-time Communication**: WebSocket with connection management
- **UI Components**: Radix UI with shadcn/ui

### Project Structure

```
├── app/              # Next.js App Router pages
├── backend/          # FastAPI backend with agent orchestration
├── components/       # React components (shadcn/ui based)
├── lib/              # Frontend utilities and stores
├── hooks/            # Custom React hooks
└── docs/             # Documentation and plans
```

### Key Backend Architecture

- **Agent System**: Role-based agents (Analyst, Architect, Developer, Tester, Deployer)
- **WebSocket Management**: EnhancedConnectionManager for real-time communication
- **LLM Service**: Multi-provider abstraction with connection pooling and enhanced rate limiting
- **Workflow Engine**: ControlFlow-based agent orchestration with recursion protection
- **Status Broadcasting**: Real-time agent status updates with serialization safety
- **Security Layer**: Input sanitization, YAML validation, and rate limiting
- **Performance Monitoring**: Real-time metrics and health monitoring

### Frontend State Management

- **Agent Store**: Agent status and workflow state
- **Conversation Store**: Chat interface messages
- **Log Store**: System logs and debugging information
- **WebSocket Service**: Global WebSocket connection management

### Environment Settings & Configuration

- **Settings Page**: `/settings` route provides UI for configuring environment variables
- **Workflow Configuration**: Enhanced 10-step workflow settings are fully configurable
- **API Integration**: `GET/POST /api/env-settings` endpoints handle configuration persistence
- **Real-time Updates**: Settings changes trigger backend configuration refresh

## Environment Setup Requirements

### Required Versions

- Python 3.13+ (virtual environment required)
- Node.js 20+ LTS
- npm 10+

### Environment Variables

```bash
# Copy from template
cp .env.example .env

# Required API keys (at least one)
OPENAI_API_KEY=sk-your-key
ANTHROPIC_API_KEY=ant_your-key
GOOGLE_GENAI_API_KEY=your-key

# Application URLs
BACKEND_URL=http://localhost:8000
WEBSOCKET_URL=ws://localhost:8000/ws
```

## Development Patterns

### Component Architecture

- Use functional components with hooks
- Implement proper TypeScript typing
- Follow existing shadcn/ui patterns for new components
- Maintain consistent import structure with `@/` paths

### Backend Development

- Follow FastAPI async patterns
- Use Pydantic models for data validation
- Implement proper error handling with ErrorHandler
- Maintain WebSocket connection stability
- **NEW**: Use InputSanitizer for all user input validation
- **NEW**: Implement connection pooling for LLM providers
- **NEW**: Add rate limiting to prevent abuse
- **NEW**: Include security pattern detection

### Agent Development

- Extend BaseAgent for new agent types
- Implement proper status broadcasting with serialization safety
- Use ControlFlow for workflow orchestration with recursion protection
- Follow existing agent patterns in `backend/agents/`
- **NEW**: Use GenericAgentExecutor for enhanced security
- **NEW**: Implement proper parameter serialization for Prefect workflows

### Security Development Patterns

- **Input Validation**: Always use comprehensive input sanitization
- **File Upload Security**: Validate file size, type, and content
- **Rate Limiting**: Implement multi-level rate limiting (IP, user, global)
- **YAML Validation**: Use JSON Schema validation for configuration files
- **Circular Reference Prevention**: Use serialization-safe wrappers for complex objects

## Code Standards

**IMPORTANT**: Always read and follow `docs/CODEPROTOCOL.md` before making any code changes. This file contains the complete development workflow, quality standards, and enforcement rules that must be followed for every task.

## Testing Strategy

### Frontend Testing

- Vitest for unit testing with jsdom environment
- React Testing Library for component testing
- Global test setup in `vitest.setup.ts`

### Backend Testing  

- pytest for Python backend testing
- Async test support with pytest-asyncio
- Test configurations in backend/conftest.py

## Common Development Workflows

### Adding New Agents

1. Create agent class in `backend/agents/`
2. Extend BaseAgent with required methods
3. **NEW**: Implement input sanitization using InputSanitizer
4. **NEW**: Add serialization safety for workflow parameters
5. Register agent in workflow orchestration
6. Update frontend components for status display
7. Test agent functionality in isolation
8. **NEW**: Add security tests for input validation

### Frontend Feature Development

1. Create components following shadcn/ui patterns
2. Implement proper TypeScript interfaces
3. Add to appropriate Zustand store if state needed
4. **NEW**: Add client-side validation for file uploads
5. Test component functionality
6. Update routing in app/ directory
7. **NEW**: Test security features and rate limiting

### WebSocket Communication

- Use websocketService for all WebSocket operations
- Follow existing message protocols in agui/protocol.py
- Implement proper connection management and error handling
- **NEW**: Use serialization-safe wrappers for complex objects
- Test WebSocket functionality with backend integration

### Security Implementation Workflow

1. **Input Validation**: Always validate and sanitize user input
2. **Schema Validation**: Use JSON Schema for configuration files
3. **Rate Limiting**: Implement appropriate rate limits for endpoints
4. **Security Testing**: Add tests for malicious input patterns
5. **Monitoring**: Add logging for security events
6. **Documentation**: Document security considerations

### Performance Optimization Workflow

1. **Connection Pooling**: Use HTTP connection pooling for external APIs
2. **Metrics Collection**: Add performance monitoring
3. **Health Checks**: Implement provider health monitoring
4. **Resource Cleanup**: Ensure proper resource management
5. **Performance Testing**: Add benchmarking tests
6. **Optimization**: Monitor and optimize based on metrics

### Workflow Stability Implementation

1. **Parameter Serialization**: Use `persist_result=False, validate_parameters=False`
2. **Circular Reference Prevention**: Use serialization-safe wrappers
3. **Error Recovery**: Implement graceful error handling
4. **Resource Management**: Ensure proper cleanup
5. **Testing**: Add recursion prevention tests
6. **Monitoring**: Log workflow execution issues

## Code Standards

- Max 300 lines per file
- Single responsibility for components and functions
- Domain boundaries must be respected
- Type safety is mandatory - no any types
- Error handling must include recovery mechanisms
- State updates must be atomic and predictable
- Performance considerations must be documented
- Accessibility must be built-in, not added later

## Visual Development & Testing

### Quick Visual Check

**IMMEDIATELY after implementing any front-end change:**

1. **Identify what changed** - Review the modified components/pages
2. **Navigate to affected pages** - Use `mcp__puppeteer__puppeteer_navigate` to visit each changed view
4. **Validate feature implementation** - Ensure the change fulfills the user's specific request
5. **Check acceptance criteria** - Review any provided context files or requirements
6. **Capture evidence** - Take full page screenshot at desktop viewport (1440px) of each changed view
7. **Check for errors** - Use `mcp__puppeteer__puppeteer_evaluate` to check console messages ⚠️

This verification ensures changes meet design standards and user requirements.

### Puppeteer MCP Integration

#### Essential Commands for UI Testing

```javascript
// Navigation & Screenshots
mcp__puppeteer__puppeteer_navigate({url}); // Navigate to page
mcp__puppeteer__puppeteer_screenshot({name, width, height}); // Capture visual evidence

// Interaction Testing
mcp__puppeteer__puppeteer_click({selector}); // Test clicks
mcp__puppeteer__puppeteer_fill({selector, value}); // Test input
mcp__puppeteer__puppeteer_hover({selector}); // Test hover states
mcp__puppeteer__puppeteer_select({selector, value}); // Test select elements

// Validation
mcp__puppeteer__puppeteer_evaluate({script}); // Execute JavaScript and check for errors
```

### Design Compliance Checklist

When implementing UI features, verify:

- [ ] **Visual Hierarchy**: Clear focus flow, appropriate spacing
- [ ] **Consistency**: Uses design tokens, follows patterns
- [ ] **Responsiveness**: Works on mobile (375px), tablet (768px), desktop (1440px)
- [ ] **Accessibility**: Keyboard navigable, proper contrast, semantic HTML
- [ ] **Performance**: Fast load times, smooth animations (150-300ms)
- [ ] **Error Handling**: Clear error states, helpful messages
- [ ] **Polish**: Micro-interactions, loading states, empty states

## When to Use Automated Visual Testing

### Use Quick Visual Check for

- Every front-end change, no matter how small
- After implementing new components or features
- When modifying existing UI elements
- After fixing visual bugs
- Before committing UI changes

### Skip Visual Testing for

- Backend-only changes (API, database)
- Configuration file updates
- Documentation changes
- Test file modifications
- Non-visual utility functions

### Feature Implementation Guidelines

- **CRITICAL**: Make MINIMAL CHANGES to existing patterns and structures
- **CRITICAL**: Preserve existing naming conventions and file organization
- Follow project's established architecture and component patterns
- Use existing utility functions and avoid duplicating functionality

## Task Cost and Usage Information Retrieval

- IMPERATIVE: ANY time the user mentions "task stats", "get task stats", "last task stats", or similar variations, IMMEDIATELY use the automated task stats script without question.

### Task Stats Script Usage

**Primary Command**: `bash "## Task Cost and Usage Information Retrieval

- IMPERATIVE: ANY time the user mentions "task stats", "get task stats", "last task stats", or similar variations, IMMEDIATELY use the automated task stats script without question.

### Task Stats Script Usage

**Primary Command**: `bash "/Users/neill/Documents/AI Code/Projects/v0-botarmy-poc/.claude/functions/task/task_stats.sh"`

**Script Options:**

- `bash .claude/functions/task/task_stats.sh` - Auto-detects and analyzes most recent Task session
- `bash .claude/functions/task/task_stats.sh session_id.jsonl` - Analyzes specific session file

### IMPORTANT RULES

- Execute the task_stats.sh script immediately when task stats are requested
- The script auto-detects the most recent Task session or accepts a specific session file/.claude/functions/task/task_stats.sh"`

**Script Options:**

- `bash .claude/functions/task/task_stats.sh` - Auto-detects and analyzes most recent Task session
- `bash .claude/functions/task/task_stats.sh session_id.jsonl` - Analyzes specific session file

### IMPORTANT RULES

- Execute the task_stats.sh script immediately when task stats are requested
- The script auto-detects the most recent Task session or accepts a specific session file
