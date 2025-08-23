"use client"

import { useAgentStore } from "@/lib/stores/agent-store"
import { AgentStatusCard, AgentStatusCardSkeleton } from "./agent-status-card"

export function AgentGrid() {
  const agents = useAgentStore((state) => state.agents)
  const isInitialized = useAgentStore((state) => state.isInitialized)

  if (!isInitialized) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {[...Array(6)].map((_, i) => (
          <AgentStatusCardSkeleton key={i} />
        ))}
      </div>
    )
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {agents.map((agent) => (
        <AgentStatusCard key={agent.id} agent={agent} />
      ))}
    </div>
  )
}
