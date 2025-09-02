import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { RequirementsGatheringInterface } from './requirements-gathering-interface';
import { useInteractiveSessionStore } from '@/lib/stores/interactive-session-store';
import { useWebSocket } from '@/hooks/use-websocket';

// Mock the hooks
vi.mock('@/lib/stores/interactive-session-store');
vi.mock('@/hooks/use-websocket');

const mockSendRequirementAnswers = vi.fn();
const mockClearSession = vi.fn();
const mockUpdateAnswer = vi.fn();

describe('RequirementsGatheringInterface', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    (useWebSocket as vi.Mock).mockReturnValue({
      sendRequirementAnswers: mockSendRequirementAnswers,
    });
  });

  it('should not render if there are no questions', () => {
    (useInteractiveSessionStore as vi.Mock).mockReturnValue({
      questions: [],
      answers: {},
      updateAnswer: mockUpdateAnswer,
      clearSession: mockClearSession,
    });
    const { container } = render(<RequirementsGatheringInterface />);
    expect(container.firstChild).toBeNull();
  });

  it('should render questions and inputs', () => {
    (useInteractiveSessionStore as vi.Mock).mockReturnValue({
      questions: [{ id: '1', text: 'Question 1?' }],
      answers: {},
      updateAnswer: mockUpdateAnswer,
      clearSession: mockClearSession,
    });
    render(<RequirementsGatheringInterface />);
    expect(screen.getByText('Question 1?')).not.toBeNull();
    expect(screen.getByPlaceholderText('Your answer...')).not.toBeNull();
  });

  it('should call updateAnswer on input change', () => {
    (useInteractiveSessionStore as vi.Mock).mockReturnValue({
      questions: [{ id: '1', text: 'Question 1?' }],
      answers: { '1': '' },
      updateAnswer: mockUpdateAnswer,
      clearSession: mockClearSession,
    });
    render(<RequirementsGatheringInterface />);
    const input = screen.getByPlaceholderText('Your answer...');
    fireEvent.change(input, { target: { value: 'My answer' } });
    expect(mockUpdateAnswer).toHaveBeenCalledWith('1', 'My answer');
  });

  it('should call sendRequirementAnswers and clearSession on submit', () => {
    const answers = { '1': 'My answer' };
    (useInteractiveSessionStore as vi.Mock).mockReturnValue({
      questions: [{ id: '1', text: 'Question 1?' }],
      answers: answers,
      updateAnswer: mockUpdateAnswer,
      clearSession: mockClearSession,
    });
    render(<RequirementsGatheringInterface />);
    const submitButton = screen.getByText('Submit Answers');
    fireEvent.click(submitButton);
    expect(mockSendRequirementAnswers).toHaveBeenCalledWith(answers);
    expect(mockClearSession).toHaveBeenCalled();
  });
});
