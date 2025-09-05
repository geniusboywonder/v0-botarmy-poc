import { 
  Bot, 
  User, 
  Search, 
  Building2, 
  Code, 
  TestTube, 
  Rocket, 
  Activity,
  type LucideIcon 
} from 'lucide-react';

export interface AgentDefinition {
  name: string;
  description: string;
  role: string;
  icon: LucideIcon;
  color: string;
  capabilities: string[];
  status: 'idle' | 'busy' | 'error' | 'offline';
}

export const AGENT_DEFINITIONS: AgentDefinition[] = [
  {
    name: 'Analyst',
    description: 'Requirements analysis agent',
    role: 'analyst',
    icon: Search,
    color: 'text-blue-600',
    capabilities: ['requirements_gathering', 'stakeholder_analysis', 'business_analysis'],
    status: 'idle'
  },
  {
    name: 'Architect',
    description: 'System design agent',
    role: 'architect',
    icon: Building2,
    color: 'text-purple-600',
    capabilities: ['system_design', 'architecture_planning', 'technical_specifications'],
    status: 'idle'
  },
  {
    name: 'Developer',
    description: 'Code generation agent',
    role: 'developer',
    icon: Code,
    color: 'text-green-600',
    capabilities: ['code_generation', 'implementation', 'debugging'],
    status: 'idle'
  },
  {
    name: 'Tester',
    description: 'Quality assurance agent',
    role: 'tester',
    icon: TestTube,
    color: 'text-orange-600',
    capabilities: ['quality_assurance', 'testing', 'validation'],
    status: 'idle'
  },
  {
    name: 'Deployer',
    description: 'Deployment management agent',
    role: 'deployer',
    icon: Rocket,
    color: 'text-red-600',
    capabilities: ['deployment', 'infrastructure', 'monitoring'],
    status: 'idle'
  },
  {
    name: 'Monitor',
    description: 'System monitoring agent',
    role: 'monitor',
    icon: Activity,
    color: 'text-cyan-600',
    capabilities: ['monitoring', 'performance_analysis', 'alerting'],
    status: 'idle'
  }
];

// Helper function to get agent by name
export const getAgentByName = (name: string): AgentDefinition | undefined => {
  return AGENT_DEFINITIONS.find(agent => agent.name === name);
};

// Helper function to get agents by role
export const getAgentsByRole = (role: string): AgentDefinition[] => {
  return AGENT_DEFINITIONS.filter(agent => agent.role === role);
};
