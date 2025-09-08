## Development Commands

## Code Standards

**IMPORTANT**: Always read and follow `docs/CODEPROTOCOL.md` before making any code changes. This file contains the complete development workflow, quality standards, and enforcement rules that must be followed for every task.
Read and follow the front-end style guide in docs/STYLEGUIDE.md before making any front-end changes.

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
- **LLM Service**: Multi-provider abstraction with rate limiting
- **Workflow Engine**: ControlFlow-based agent orchestration
- **Status Broadcasting**: Real-time agent status updates

### Frontend State Management

- **Agent Store**: Agent status and workflow state
- **Conversation Store**: Chat interface messages
- **Log Store**: System logs and debugging information
- **WebSocket Service**: Global WebSocket connection management

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

### Agent Development

- Extend BaseAgent for new agent types
- Implement proper status broadcasting
- Use ControlFlow for workflow orchestration
- Follow existing agent patterns in `backend/agents/`

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
3. Register agent in workflow orchestration
4. Update frontend components for status display
5. Test agent functionality in isolation

### Frontend Feature Development

1. Create components following shadcn/ui patterns
2. Implement proper TypeScript interfaces
3. Add to appropriate Zustand store if state needed
4. Test component functionality
5. Update routing in app/ directory

### WebSocket Communication

- Use websocketService for all WebSocket operations
- Follow existing message protocols in agui/protocol.py
- Implement proper connection management and error handling
- Test WebSocket functionality with backend integration

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
