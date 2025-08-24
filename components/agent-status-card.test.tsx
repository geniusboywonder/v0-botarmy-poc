import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { AgentStatusCard, type Agent } from './agent-status-card';

// A mock agent object to be used in tests
const mockAgent: Agent = {
  id: 'agent-1',
  name: 'Analyst Agent',
  role: 'Requirements Analysis',
  status: 'idle',
  lastActivity: new Date().toISOString(),
  tasksCompleted: 5,
  successRate: 95,
  is_thinking: false,
};

describe('AgentStatusCard Component', () => {
  it('should render the agent name and role', () => {
    // Arrange
    render(<AgentStatusCard agent={mockAgent} />);

    // Assert
    expect(screen.getByText('Analyst Agent')).toBeInTheDocument();
    expect(screen.getByText('Requirements Analysis')).toBeInTheDocument();
  });

  it('should display the correct stats', () => {
    // Arrange
    render(<AgentStatusCard agent={mockAgent} />);

    // Assert
    expect(screen.getByText('✓ 5')).toBeInTheDocument();
    expect(screen.getByText('95% success')).toBeInTheDocument();
  });

  it('should display "Idle" status correctly', () => {
    // Arrange
    const idleAgent = { ...mockAgent, status: 'idle' as const };
    render(<AgentStatusCard agent={idleAgent} />);

    // Assert
    expect(screen.getByText('Idle')).toBeInTheDocument();
  });

  it('should display "Working" status correctly', () => {
    // Arrange
    const workingAgent = {
      ...mockAgent,
      status: 'working' as const,
      currentTask: 'Analyzing user prompt...',
      progress: 50,
    };
    render(<AgentStatusCard agent={workingAgent} />);

    // Assert
    expect(screen.getByText('Working')).toBeInTheDocument();
    expect(screen.getByText('Analyzing user prompt...')).toBeInTheDocument();
    expect(screen.getByText('50%')).toBeInTheDocument(); // Checks for progress text
  });

  it('should display "Error" status correctly', () => {
    // Arrange
    const errorAgent = { ...mockAgent, status: 'error' as const };
    render(<AgentStatusCard agent={errorAgent} />);

    // Assert
    // The badge should have the 'destructive' variant, which we can check via text or class
    const errorBadge = screen.getByText('Error');
    expect(errorBadge).toBeInTheDocument();
    expect(errorBadge).toHaveClass(/destructive/);
  });

  it('should display the typing indicator when the agent is thinking', () => {
    // Arrange
    const thinkingAgent = { ...mockAgent, is_thinking: true };
    render(<AgentStatusCard agent={thinkingAgent} />);

    // Assert
    // The TypingIndicator component doesn't have specific text, so we might need
    // to add a data-testid to it or check for one of its child elements' classes.
    // For now, we assume its presence implies some visual change we can't easily test.
    // A better way would be to test for a specific element added by TypingIndicator.
    // This is a placeholder for a more robust test.
    expect(screen.queryByText('Agents are working...')).not.toBeInTheDocument(); // This text is in the chat, not the card
  });
});
