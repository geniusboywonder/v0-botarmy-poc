import { render, screen, fireEvent, act } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { Sidebar } from './sidebar';

// Mock the next/navigation module
vi.mock('next/navigation', () => ({
  usePathname: vi.fn(),
}));

// Mock the SystemHealthDashboard component as it's a complex child component
vi.mock('./system-health-dashboard', () => ({
  SystemHealthDashboard: () => <div data-testid="system-health-dashboard-mock" />,
}));

const mockOnViewChange = vi.fn();

describe('Sidebar Component', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render all navigation items', () => {
    // Arrange
    const { usePathname } = require('next/navigation');
    usePathname.mockReturnValue('/');
    render(<Sidebar activeView="dashboard" onViewChange={mockOnViewChange} />);

    // Assert
    expect(screen.getByText('Dashboard')).toBeInTheDocument();
    expect(screen.getByText('Tasks')).toBeInTheDocument();
    expect(screen.getByText('Logs')).toBeInTheDocument();
    expect(screen.getByText('Artifacts')).toBeInTheDocument();
    expect(screen.getByText('Analytics')).toBeInTheDocument();
    expect(screen.getByText('Settings')).toBeInTheDocument();
  });

  it('should highlight the active link based on the current pathname', () => {
    // Arrange
    const { usePathname } = require('next/navigation');
    usePathname.mockReturnValue('/logs');
    render(<Sidebar activeView="logs" onViewChange={mockOnViewChange} />);

    // Act
    const logsLink = screen.getByRole('link', { name: /Logs/i });
    const dashboardLink = screen.getByRole('link', { name: /Dashboard/i });

    // Assert
    // The active link should have a different variant, which results in different classes.
    // We check for the 'secondary' variant class which is applied when active.
    // Note: This relies on the implementation detail of how `variant` is translated to classes.
    // A more robust way is to check `aria-current` if it were used.
    expect(logsLink.querySelector('button')).toHaveClass(/secondary/);
    expect(dashboardLink.querySelector('button')).not.toHaveClass(/secondary/);
  });

  it('should call onViewChange when a navigation item is clicked', async () => {
    // Arrange
    const { usePathname } = require('next/navigation');
    usePathname.mockReturnValue('/');
    render(<Sidebar activeView="dashboard" onViewChange={mockOnViewChange} />);
    const tasksLink = screen.getByRole('link', { name: /Tasks/i });

    // Act
    await act(async () => {
      fireEvent.click(tasksLink);
    });

    // Assert
    expect(mockOnViewChange).toHaveBeenCalledWith('tasks');
  });

  it('should collapse and expand when the chevron button is clicked', async () => {
    // Arrange
    const { usePathname } = require('next/navigation');
    usePathname.mockReturnValue('/');
    render(<Sidebar activeView="dashboard" onViewChange={mockOnViewChange} />);

    // Check initial state (expanded)
    expect(screen.getByText('BotArmy')).toBeInTheDocument();

    // Act: Collapse the sidebar
    const collapseButton = screen.getByRole('button', { name: /chevron-left/i });
    await act(async () => {
        fireEvent.click(collapseButton);
    });

    // Assert: Sidebar is collapsed
    expect(screen.queryByText('BotArmy')).not.toBeInTheDocument();
    expect(screen.getByRole('button', { name: /chevron-right/i })).toBeInTheDocument();

    // Act: Expand the sidebar
    const expandButton = screen.getByRole('button', { name: /chevron-right/i });
    await act(async () => {
        fireEvent.click(expandButton);
    });

    // Assert: Sidebar is expanded again
    expect(screen.getByText('BotArmy')).toBeInTheDocument();
  });
});
