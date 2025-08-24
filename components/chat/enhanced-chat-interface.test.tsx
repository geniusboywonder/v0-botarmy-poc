import { render, screen, fireEvent, act } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { EnhancedChatInterface } from './enhanced-chat-interface';
import { useLogStore } from '@/lib/stores/log-store';
import { useAgentStore } from '@/lib/stores/agent-store';
import { websocketService } from '@/lib/websocket/websocket-service';

// Mock the external dependencies
vi.mock('@/lib/stores/log-store');
vi.mock('@/lib/stores/agent-store');
vi.mock('@/lib/websocket/websocket-service');

describe('EnhancedChatInterface', () => {
  const mockAddLog = vi.fn();
  const mockStartProject = vi.fn();

  beforeEach(() => {
    // Reset mocks before each test
    vi.clearAllMocks();

    // Setup mock return values for the hooks and service
    (useLogStore as any).mockReturnValue({
      logs: [
        { id: '1', agent: 'System', level: 'info', message: 'Welcome!', timestamp: new Date() },
        { id: '2', agent: 'User', level: 'info', message: 'Test prompt', timestamp: new Date() },
      ],
      addLog: mockAddLog,
    });

    (useAgentStore as any).mockReturnValue({
      agents: [],
    });

    (websocketService as any).startProject = mockStartProject;
    (websocketService as any).getConnectionStatus = vi.fn().mockReturnValue({ connected: true });
  });

  it('should render the chat logs from the log store', () => {
    // Arrange
    render(<EnhancedChatInterface />);

    // Assert
    expect(screen.getByText('Welcome!')).toBeInTheDocument();
    expect(screen.getByText('Test prompt')).toBeInTheDocument();
  });

  it('should allow the user to type in the input', async () => {
    // Arrange
    render(<EnhancedChatInterface />);
    const input = screen.getByPlaceholderText(/e.g., Create a Python script/i);

    // Act
    await act(async () => {
        fireEvent.change(input, { target: { value: 'This is a new message.' } });
    });

    // Assert
    expect(input).toHaveValue('This is a new message.');
  });

  it('should call websocketService.startProject and addLog when sending a valid message', async () => {
    // Arrange
    render(<EnhancedChatInterface />);
    const input = screen.getByPlaceholderText(/e.g., Create a Python script/i);
    const sendButton = screen.getByRole('button', { name: /Send/i });
    const message = 'This is a valid test message.';

    // Act
    await act(async () => {
        fireEvent.change(input, { target: { value: message } });
    });

    // Ensure the button is enabled before clicking
    expect(sendButton).not.toBeDisabled();

    await act(async () => {
        fireEvent.click(sendButton);
    });

    // Assert
    // Check that the user's message was added to the log
    expect(mockAddLog).toHaveBeenCalledWith(expect.objectContaining({
        agent: 'User',
        message: message,
    }));

    // Check that the "initializing" message was added
    expect(mockAddLog).toHaveBeenCalledWith(expect.objectContaining({
        agent: 'System',
        message: 'Initializing agents...',
    }));

    // Check that the websocket service was called
    expect(mockStartProject).toHaveBeenCalledWith(message);
  });

  it('should disable the send button for short messages', async () => {
    // Arrange
    render(<EnhancedChatInterface />);
    const input = screen.getByPlaceholderText(/e.g., Create a Python script/i);
    const sendButton = screen.getByRole('button', { name: /Send/i });

    // Act
    await act(async () => {
        fireEvent.change(input, { target: { value: 'short' } });
    });

    // Assert
    expect(sendButton).toBeDisabled();
  });

  it('should disable the send button when disconnected', async () => {
    // Arrange
    (websocketService as any).getConnectionStatus = vi.fn().mockReturnValue({ connected: false });
    render(<EnhancedChatInterface />);
    const input = screen.getByPlaceholderText(/Connect to server to send messages/i);
    const sendButton = screen.getByRole('button', { name: /Send/i });

    // Act
    await act(async () => {
        fireEvent.change(input, { target: { value: 'This is a valid test message.' } });
    });

    // Assert
    expect(sendButton).toBeDisabled();
    expect(input).toBeDisabled();
  });
});
