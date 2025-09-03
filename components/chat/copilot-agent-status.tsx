"use client";

import { useAgentStore } from "@/lib/stores/agent-store";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Bot, ClipboardCheck, DraftingCompass, Construction, TestTube2, Rocket } from "lucide-react";
import { getStatusBadgeClasses, getAgentBadgeClasses } from "@/lib/utils/badge-utils";
import { cn } from "@/lib/utils";

const getAgentIcon = (agentName: string) => {
  const agentLower = agentName.toLowerCase();
  if (agentLower.includes('analyst')) return <ClipboardCheck className="w-4 h-4" />;
  if (agentLower.includes('architect')) return <DraftingCompass className="w-4 h-4" />;
  if (agentLower.includes('developer')) return <Construction className="w-4 h-4" />;
  if (agentLower.includes('tester')) return <TestTube2 className="w-4 h-4" />;
  if (agentLower.includes('deployer')) return <Rocket className="w-4 h-4" />;
  return <Bot className="w-4 h-4" />;
};

export const CopilotAgentStatus = () => {
  const { agents } = useAgentStore();

  if (agents.length === 0) {
    return (
        <Card>
            <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                <Bot className="w-5 h-5" />
                <span>Agent Status</span>
                </CardTitle>
            </CardHeader>
            <CardContent>
                <p className="text-muted-foreground">No agents active.</p>
            </CardContent>
        </Card>
    );
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center space-x-2">
          <Bot className="w-5 h-5" />
          <span>Agent Status</span>
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {agents.map((agent) => (
            <div key={agent.name} className="flex items-start justify-between">
              <div className="flex items-start space-x-3">
                <div className={cn("p-2 rounded-full", getAgentBadgeClasses(agent.name))}>
                  {getAgentIcon(agent.name)}
                </div>
                <div>
                  <div className="font-semibold">{agent.name}</div>
                  <div className="text-sm text-muted-foreground">{agent.task}</div>
                </div>
              </div>
              <Badge variant="muted" size="sm" className={getStatusBadgeClasses(agent.status)}>
                {agent.status}
              </Badge>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
};
