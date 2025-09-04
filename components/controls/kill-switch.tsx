"use client";

import React from 'react';
import { Button } from '@/components/ui/button';
import { Pause, Play, Square } from 'lucide-react';
import { useAgentStore } from '@/lib/stores/agent-store';

interface KillSwitchControlsProps {
  agentName: string;
}

export const KillSwitchControls: React.FC<KillSwitchControlsProps> = ({ agentName }) => {
  const { pauseAgent, resumeAgent, resetAgent, agents } = useAgentStore();
  const agent = agents.find(a => a.name === agentName);

  const handlePause = () => {
    if (agent && agent.status !== 'paused') {
      pauseAgent(agentName);
    }
  };

  const handleResume = () => {
    if (agent && agent.status === 'paused') {
      resumeAgent(agentName);
    }
  };

  const handleReset = () => {
    resetAgent(agentName);
  };

  return (
    <div className="flex items-center gap-2">
      {agent?.status !== 'paused' ? (
        <Button
          variant="outline"
          size="sm"
          onClick={handlePause}
          title="Pause agent execution"
        >
          <Pause className="w-3 h-3 mr-1" />
          Pause
        </Button>
      ) : (
        <Button
          variant="outline"
          size="sm"
          onClick={handleResume}
          title="Resume agent execution"
        >
          <Play className="w-3 h-3 mr-1" />
          Resume
        </Button>
      )}

      <Button
        variant="destructive"
        size="sm"
        onClick={handleReset}
        title="Stop and reset agent"
      >
        <Square className="w-3 h-3 mr-1" />
        Stop
      </Button>
    </div>
  );
};
