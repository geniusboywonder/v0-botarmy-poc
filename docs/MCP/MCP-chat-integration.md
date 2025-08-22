# Chat Integration - Real-time Agent Communication

**Part of:** MCP-Based Role-Constrained Agent Orchestration  
**Focus:** Frontend WebSocket implementation and real-time streaming

---

## Real-Time Chat Architecture

The chat interface provides transparent, real-time visibility into agent work, allowing users to collaborate naturally with the AI orchestration system.

### WebSocket Communication Layer

```typescript
// WebSocket client for real-time agent communication
class AgentOrchestrationClient {
    private ws: WebSocket | null = null;
    private reconnectAttempts = 0;
    private maxReconnectAttempts = 5;
    private sessionId: string;
    
    constructor(private onMessage: (message: AgentMessage) => void) {
        this.sessionId = this.generateSessionId();
    }
    
    connect(wsUrl: string): Promise<void> {
        return new Promise((resolve, reject) => {
            this.ws = new WebSocket(`${wsUrl}?session=${this.sessionId}`);
            
            this.ws.onopen = () => {
                console.log('Connected to agent orchestration');
                this.reconnectAttempts = 0;
                resolve();
            };
            
            this.ws.onmessage = (event) => {
                try {
                    const message: AgentMessage = JSON.parse(event.data);
                    this.handleMessage(message);
                } catch (error) {
                    console.error('Failed to parse message:', error);
                }
            };
            
            this.ws.onclose = (event) => {
                console.log('WebSocket closed:', event.code);
                if (!event.wasClean && this.reconnectAttempts < this.maxReconnectAttempts) {
                    this.attemptReconnect(wsUrl);
                }
            };
            
            this.ws.onerror = (error) => {
                console.error('WebSocket error:', error);
                reject(error);
            };
        });
    }
    
    private handleMessage(message: AgentMessage) {
        switch (message.type) {
            case 'workflow_started':
                this.handleWorkflowStarted(message);
                break;
            case 'agent_started':
                this.handleAgentStarted(message);
                break;
            case 'agent_progress':
                this.handleAgentProgress(message);
                break;
            case 'agent_completed':
                this.handleAgentCompleted(message);
                break;
            case 'approval_required':
                this.handleApprovalRequired(message);
                break;
            case 'workflow_completed':
                this.handleWorkflowCompleted(message);
                break;
            case 'error':
                this.handleError(message);
                break;
            default:
                console.log('Unknown message type:', message.type);
        }
        
        // Pass to parent component
        this.onMessage(message);
    }
    
    sendUserMessage(content: string, attachments?: File[]): void {
        if (!this.ws || this.ws.readyState !== WebSocket.OPEN) {
            throw new Error('WebSocket not connected');
        }
        
        const message: UserMessage = {
            type: 'user_input',
            sessionId: this.sessionId,
            content,
            attachments: attachments ? attachments.map(f => ({
                name: f.name,
                size: f.size,
                type: f.type
            })) : [],
            timestamp: new Date().toISOString()
        };
        
        this.ws.send(JSON.stringify(message));
        
        // Handle file uploads separately if present
        if (attachments && attachments.length > 0) {
            this.uploadFiles(attachments);
        }
    }
    
    sendApproval(approvalId: string, approved: boolean, feedback?: string): void {
        if (!this.ws || this.ws.readyState !== WebSocket.OPEN) {
            throw new Error('WebSocket not connected');
        }
        
        const message: ApprovalMessage = {
            type: 'approval_response',
            sessionId: this.sessionId,
            approvalId,
            approved,
            feedback,
            timestamp: new Date().toISOString()
        };
        
        this.ws.send(JSON.stringify(message));
    }
    
    private async uploadFiles(files: File[]): Promise<void> {
        const formData = new FormData();
        formData.append('sessionId', this.sessionId);
        
        files.forEach((file, index) => {
            formData.append(`file_${index}`, file);
        });
        
        try {
            const response = await fetch('/api/upload', {
                method: 'POST',
                body: formData
            });
            
            if (!response.ok) {
                throw new Error(`Upload failed: ${response.statusText}`);
            }
            
            const result = await response.json();
            console.log('Files uploaded successfully:', result);
        } catch (error) {
            console.error('File upload failed:', error);
            this.onMessage({
                type: 'error',
                sessionId: this.sessionId,
                error: 'File upload failed',
                timestamp: new Date().toISOString()
            });
        }
    }
    
    private attemptReconnect(wsUrl: string): void {
        this.reconnectAttempts++;
        const delay = Math.min(1000 * Math.pow(2, this.reconnectAttempts), 30000);
        
        console.log(`Attempting to reconnect in ${delay}ms (attempt ${this.reconnectAttempts})`);
        
        setTimeout(() => {
            this.connect(wsUrl).catch(error => {
                console.error('Reconnection failed:', error);
            });
        }, delay);
    }
    
    private generateSessionId(): string {
        return `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    }
    
    disconnect(): void {
        if (this.ws) {
            this.ws.close(1000, 'Client disconnect');
            this.ws = null;
        }
    }
}
```

### Message Type Definitions

```typescript
interface AgentMessage {
    type: 'workflow_started' | 'agent_started' | 'agent_progress' | 'agent_completed' | 
          'approval_required' | 'workflow_completed' | 'error';
    sessionId: string;
    timestamp: string;
    [key: string]: any;
}

interface WorkflowStartedMessage extends AgentMessage {
    type: 'workflow_started';
    workflowId: string;
    workflowName: string;
    estimatedDuration: number;
    agents: Array<{
        role: string;
        position: number;
        estimatedTime: number;
    }>;
}

interface AgentStartedMessage extends AgentMessage {
    type: 'agent_started';
    agentRole: string;
    agentName: string;
    position: number;
    totalAgents: number;
    estimatedCompletionTime: string;
    inputs: Record<string, any>;
}

interface AgentProgressMessage extends AgentMessage {
    type: 'agent_progress';
    agentRole: string;
    progress: number; // 0-1
    currentTask: string;
    partialOutput?: string;
    thinkingProcess?: string;
}

interface AgentCompletedMessage extends AgentMessage {
    type: 'agent_completed';
    agentRole: string;
    duration: number;
    outputs: Record<string, any>;
    qualityScore?: number;
    nextAgent?: string;
}

interface ApprovalRequiredMessage extends AgentMessage {
    type: 'approval_required';
    approvalId: string;
    title: string;
    description: string;
    agentOutputs: Record<string, any>;
    requiredBy: string;
    timeoutMinutes?: number;
}

interface WorkflowCompletedMessage extends AgentMessage {
    type: 'workflow_completed';
    workflowId: string;
    totalDuration: number;
    finalOutputs: Record<string, any>;
    qualityScore: number;
    costBreakdown: Record<string, number>;
}

interface ErrorMessage extends AgentMessage {
    type: 'error';
    error: string;
    details?: Record<string, any>;
    agentRole?: string;
    recoverable: boolean;
    suggestedActions?: string[];
}

interface UserMessage {
    type: 'user_input';
    sessionId: string;
    content: string;
    attachments: Array<{
        name: string;
        size: number;
        type: string;
    }>;
    timestamp: string;
}

interface ApprovalMessage {
    type: 'approval_response';
    sessionId: string;
    approvalId: string;
    approved: boolean;
    feedback?: string;
    timestamp: string;
}
```

---

## React Chat Interface Components

### Main Chat Container

```tsx
import React, { useState, useEffect, useRef } from 'react';
import { AgentOrchestrationClient } from './AgentOrchestrationClient';
import { MessageList } from './MessageList';
import { MessageInput } from './MessageInput';
import { WorkflowProgress } from './WorkflowProgress';
import { ApprovalGate } from './ApprovalGate';

interface ChatContainerProps {
    wsUrl: string;
    onError?: (error: string) => void;
}

export const ChatContainer: React.FC<ChatContainerProps> = ({ wsUrl, onError }) => {
    const [messages, setMessages] = useState<AgentMessage[]>([]);
    const [currentWorkflow, setCurrentWorkflow] = useState<WorkflowState | null>(null);
    const [pendingApproval, setPendingApproval] = useState<ApprovalRequiredMessage | null>(null);
    const [isConnected, setIsConnected] = useState(false);
    const [isLoading, setIsLoading] = useState(false);
    
    const clientRef = useRef<AgentOrchestrationClient | null>(null);
    
    useEffect(() => {
        const client = new AgentOrchestrationClient(handleMessage);
        clientRef.current = client;
        
        client.connect(wsUrl)
            .then(() => setIsConnected(true))
            .catch(error => {
                console.error('Connection failed:', error);
                onError?.('Failed to connect to agent orchestration service');
            });
        
        return () => {
            client.disconnect();
        };
    }, [wsUrl]);
    
    const handleMessage = (message: AgentMessage) => {
        setMessages(prev => [...prev, message]);
        
        switch (message.type) {
            case 'workflow_started':
                const workflowMsg = message as WorkflowStartedMessage;
                setCurrentWorkflow({
                    id: workflowMsg.workflowId,
                    name: workflowMsg.workflowName,
                    agents: workflowMsg.agents,
                    currentAgentIndex: 0,
                    startTime: new Date(workflowMsg.timestamp)
                });
                setIsLoading(true);
                break;
                
            case 'agent_started':
                const agentStartMsg = message as AgentStartedMessage;
                setCurrentWorkflow(prev => prev ? {
                    ...prev,
                    currentAgentIndex: agentStartMsg.position - 1
                } : null);
                break;
                
            case 'agent_completed':
                // Progress to next agent
                setCurrentWorkflow(prev => prev ? {
                    ...prev,
                    currentAgentIndex: prev.currentAgentIndex + 1
                } : null);
                break;
                
            case 'approval_required':
                setPendingApproval(message as ApprovalRequiredMessage);
                setIsLoading(false);
                break;
                
            case 'workflow_completed':
                setCurrentWorkflow(null);
                setPendingApproval(null);
                setIsLoading(false);
                break;
                
            case 'error':
                setIsLoading(false);
                onError?.(message.error);
                break;
        }
    };
    
    const sendMessage = (content: string, attachments?: File[]) => {
        if (!clientRef.current || !isConnected) {
            onError?.('Not connected to service');
            return;
        }
        
        try {
            clientRef.current.sendUserMessage(content, attachments);
            
            // Add user message to display
            const userMessage: AgentMessage = {
                type: 'user_input' as any,
                sessionId: clientRef.current.sessionId,
                content,
                attachments: attachments?.map(f => ({ name: f.name, size: f.size, type: f.type })) || [],
                timestamp: new Date().toISOString()
            };
            setMessages(prev => [...prev, userMessage]);
            
        } catch (error) {
            console.error('Failed to send message:', error);
            onError?.('Failed to send message');
        }
    };
    
    const handleApproval = (approved: boolean, feedback?: string) => {
        if (!clientRef.current || !pendingApproval) return;
        
        clientRef.current.sendApproval(pendingApproval.approvalId, approved, feedback);
        setPendingApproval(null);
        setIsLoading(true);
    };
    
    return (
        <div className="flex flex-col h-screen max-w-4xl mx-auto">
            <div className="flex-1 flex flex-col min-h-0">
                
                {/* Workflow Progress Header */}
                {currentWorkflow && (
                    <WorkflowProgress 
                        workflow={currentWorkflow}
                        className="border-b bg-slate-50 p-4"
                    />
                )}
                
                {/* Connection Status */}
                <div className={`px-4 py-2 text-sm ${isConnected ? 'bg-green-50 text-green-700' : 'bg-red-50 text-red-700'}`}>
                    {isConnected ? '🟢 Connected to Agent Orchestration' : '🔴 Disconnected'}
                </div>
                
                {/* Message List */}
                <MessageList 
                    messages={messages}
                    isLoading={isLoading}
                    className="flex-1 overflow-y-auto p-4"
                />
                
                {/* Approval Gate */}
                {pendingApproval && (
                    <ApprovalGate
                        approval={pendingApproval}
                        onApprove={(feedback) => handleApproval(true, feedback)}
                        onReject={(feedback) => handleApproval(false, feedback)}
                        className="border-t bg-blue-50 p-4"
                    />
                )}
            </div>
            
            {/* Message Input */}
            <MessageInput
                onSendMessage={sendMessage}
                disabled={!isConnected || pendingApproval !== null}
                placeholder={pendingApproval ? "Waiting for approval..." : "Describe what you want to build or analyze..."}
                className="border-t"
            />
        </div>
    );
};

interface WorkflowState {
    id: string;
    name: string;
    agents: Array<{ role: string; position: number; estimatedTime: number }>;
    currentAgentIndex: number;
    startTime: Date;
}
```

### Workflow Progress Component

```tsx
import React from 'react';
import { Progress } from '@/components/ui/progress';
import { Badge } from '@/components/ui/badge';

interface WorkflowProgressProps {
    workflow: WorkflowState;
    className?: string;
}

export const WorkflowProgress: React.FC<WorkflowProgressProps> = ({ workflow, className }) => {
    const totalAgents = workflow.agents.length;
    const currentProgress = ((workflow.currentAgentIndex + 1) / totalAgents) * 100;
    
    const formatAgentName = (role: string) => {
        return role.split('_').map(word => 
            word.charAt(0).toUpperCase() + word.slice(1)
        ).join(' ');
    };
    
    const getAgentStatus = (index: number) => {
        if (index < workflow.currentAgentIndex) return 'completed';
        if (index === workflow.currentAgentIndex) return 'active';
        return 'pending';
    };
    
    const getStatusColor = (status: string) => {
        switch (status) {
            case 'completed': return 'bg-green-500 text-white';
            case 'active': return 'bg-blue-500 text-white';
            case 'pending': return 'bg-gray-200 text-gray-600';
            default: return 'bg-gray-200 text-gray-600';
        }
    };
    
    const getStatusIcon = (status: string) => {
        switch (status) {
            case 'completed': return '✅';
            case 'active': return '🔄';
            case 'pending': return '⏳';
            default: return '⏳';
        }
    };
    
    return (
        <div className={className}>
            <div className="mb-4">
                <div className="flex justify-between items-center mb-2">
                    <h3 className="text-lg font-semibold">{workflow.name}</h3>
                    <Badge variant="outline">
                        {workflow.currentAgentIndex + 1} / {totalAgents} agents
                    </Badge>
                </div>
                
                <Progress value={currentProgress} className="h-2" />
                
                <div className="text-sm text-gray-600 mt-1">
                    {Math.round(currentProgress)}% complete
                </div>
            </div>
            
            <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
                {workflow.agents.map((agent, index) => {
                    const status = getAgentStatus(index);
                    return (
                        <div
                            key={agent.role}
                            className={`p-3 rounded-lg border text-center ${
                                status === 'active' ? 'border-blue-500 bg-blue-50' :
                                status === 'completed' ? 'border-green-500 bg-green-50' :
                                'border-gray-200 bg-gray-50'
                            }`}
                        >
                            <div className="text-lg mb-1">
                                {getStatusIcon(status)}
                            </div>
                            <div className="font-medium text-sm">
                                {formatAgentName(agent.role)}
                            </div>
                            <div className="text-xs text-gray-500 mt-1">
                                ~{agent.estimatedTime}min
                            </div>
                        </div>
                    );
                })}
            </div>
        </div>
    );
};
```

### Message List Component

```tsx
import React, { useEffect, useRef } from 'react';
import { AgentMessage } from './types';
import { MessageBubble } from './MessageBubble';
import { LoadingIndicator } from './LoadingIndicator';

interface MessageListProps {
    messages: AgentMessage[];
    isLoading: boolean;
    className?: string;
}

export const MessageList: React.FC<MessageListProps> = ({ messages, isLoading, className }) => {
    const scrollRef = useRef<HTMLDivElement>(null);
    
    useEffect(() => {
        // Auto-scroll to bottom when new messages arrive
        if (scrollRef.current) {
            scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
        }
    }, [messages]);
    
    return (
        <div ref={scrollRef} className={`space-y-4 ${className}`}>
            {messages.map((message, index) => (
                <MessageBubble 
                    key={`${message.sessionId}-${index}`}
                    message={message}
                />
            ))}
            
            {isLoading && (
                <LoadingIndicator message="Agent is working..." />
            )}
        </div>
    );
};
```

### Message Bubble Component

```tsx
import React from 'react';
import { AgentMessage } from './types';
import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';

interface MessageBubbleProps {
    message: AgentMessage;
}

export const MessageBubble: React.FC<MessageBubbleProps> = ({ message }) => {
    const formatTimestamp = (timestamp: string) => {
        return new Date(timestamp).toLocaleTimeString([], { 
            hour: '2-digit', 
            minute: '2-digit' 
        });
    };
    
    const renderMessageContent = () => {
        switch (message.type) {
            case 'user_input':
                return (
                    <div className="ml-auto max-w-lg">
                        <Card className="p-4 bg-blue-500 text-white">
                            <div className="whitespace-pre-wrap">{(message as any).content}</div>
                            {(message as any).attachments?.length > 0 && (
                                <div className="mt-2 space-y-1">
                                    {(message as any).attachments.map((file: any, index: number) => (
                                        <div key={index} className="text-xs bg-blue-400 px-2 py-1 rounded">
                                            📎 {file.name} ({(file.size / 1024).toFixed(1)} KB)
                                        </div>
                                    ))}
                                </div>
                            )}
                        </Card>
                        <div className="text-xs text-gray-500 mt-1 text-right">
                            {formatTimestamp(message.timestamp)}
                        </div>
                    </div>
                );
                
            case 'workflow_started':
                const workflowMsg = message as WorkflowStartedMessage;
                return (
                    <Card className="p-4 bg-green-50 border-green-200">
                        <div className="flex items-center gap-2 mb-2">
                            <span className="text-lg">🚀</span>
                            <h4 className="font-semibold">Workflow Started</h4>
                        </div>
                        <div className="text-sm text-gray-600">
                            <div><strong>Workflow:</strong> {workflowMsg.workflowName}</div>
                            <div><strong>Agents:</strong> {workflowMsg.agents.map(a => a.role).join(' → ')}</div>
                            <div><strong>Estimated Duration:</strong> {workflowMsg.estimatedDuration} minutes</div>
                        </div>
                    </Card>
                );
                
            case 'agent_started':
                const agentStartMsg = message as AgentStartedMessage;
                return (
                    <Card className="p-4 bg-blue-50 border-blue-200">
                        <div className="flex items-center gap-2 mb-2">
                            <span className="text-lg">🤖</span>
                            <h4 className="font-semibold">{agentStartMsg.agentName} Started</h4>
                            <Badge variant="outline">{agentStartMsg.position}/{agentStartMsg.totalAgents}</Badge>
                        </div>
                        <div className="text-sm text-gray-600">
                            Working on your request...
                        </div>
                    </Card>
                );
                
            case 'agent_progress':
                const progressMsg = message as AgentProgressMessage;
                return (
                    <Card className="p-4 bg-yellow-50 border-yellow-200">
                        <div className="flex items-center gap-2 mb-2">
                            <span className="text-lg">⚙️</span>
                            <h4 className="font-semibold">{progressMsg.agentRole} Progress</h4>
                        </div>
                        <div className="space-y-2">
                            <Progress value={progressMsg.progress * 100} className="h-2" />
                            <div className="text-sm text-gray-600">
                                <div><strong>Current Task:</strong> {progressMsg.currentTask}</div>
                                {progressMsg.thinkingProcess && (
                                    <div className="mt-2 p-2 bg-gray-100 rounded text-xs">
                                        <strong>Thinking:</strong> {progressMsg.thinkingProcess}
                                    </div>
                                )}
                            </div>
                        </div>
                    </Card>
                );
                
            case 'agent_completed':
                const completedMsg = message as AgentCompletedMessage;
                return (
                    <Card className="p-4 bg-green-50 border-green-200">
                        <div className="flex items-center gap-2 mb-2">
                            <span className="text-lg">✅</span>
                            <h4 className="font-semibold">{completedMsg.agentRole} Completed</h4>
                            {completedMsg.qualityScore && (
                                <Badge variant="outline">
                                    Quality: {(completedMsg.qualityScore * 100).toFixed(0)}%
                                </Badge>
                            )}
                        </div>
                        <div className="space-y-2">
                            <div className="text-sm text-gray-600">
                                Completed in {Math.round(completedMsg.duration / 1000)}s
                            </div>
                            {Object.entries(completedMsg.outputs).map(([key, value]) => (
                                <div key={key} className="p-3 bg-white rounded border">
                                    <h5 className="font-medium text-sm mb-1">{key}</h5>
                                    <div className="text-sm text-gray-700 whitespace-pre-wrap">
                                        {typeof value === 'string' ? value : JSON.stringify(value, null, 2)}
                                    </div>
                                </div>
                            ))}
                            {completedMsg.nextAgent && (
                                <div className="text-sm text-blue-600">
                                    ➡️ Passing to {completedMsg.nextAgent}...
                                </div>
                            )}
                        </div>
                    </Card>
                );
                
            case 'error':
                const errorMsg = message as ErrorMessage;
                return (
                    <Card className="p-4 bg-red-50 border-red-200">
                        <div className="flex items-center gap-2 mb-2">
                            <span className="text-lg">❌</span>
                            <h4 className="font-semibold">Error</h4>
                            {errorMsg.agentRole && (
                                <Badge variant="destructive">{errorMsg.agentRole}</Badge>
                            )}
                        </div>
                        <div className="space-y-2">
                            <div className="text-sm text-red-700">{errorMsg.error}</div>
                            {errorMsg.recoverable && (
                                <div className="text-sm text-green-700">
                                    ✅ This error is recoverable. The system will attempt to continue.
                                </div>
                            )}
                            {errorMsg.suggestedActions && (
                                <div className="text-sm">
                                    <strong>Suggested Actions:</strong>
                                    <ul className="list-disc list-inside mt-1">
                                        {errorMsg.suggestedActions.map((action, index) => (
                                            <li key={index}>{action}</li>
                                        ))}
                                    </ul>
                                </div>
                            )}
                        </div>
                    </Card>
                );
                
            default:
                return (
                    <Card className="p-4 bg-gray-50 border-gray-200">
                        <div className="text-sm text-gray-600">
                            {JSON.stringify(message, null, 2)}
                        </div>
                    </Card>
                );
        }
    };
    
    return (
        <div className="max-w-full">
            {renderMessageContent()}
        </div>
    );
};
```

---

## Backend WebSocket Handler

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import Dict, Set
import json
import asyncio
import logging

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.session_workflows: Dict[str, str] = {}
        
    async def connect(self, websocket: WebSocket, session_id: str):
        await websocket.accept()
        self.active_connections[session_id] = websocket
        logging.info(f"Client {session_id} connected")
        
    def disconnect(self, session_id: str):
        if session_id in self.active_connections:
            del self.active_connections[session_id]
        if session_id in self.session_workflows:
            del self.session_workflows[session_id]
        logging.info(f"Client {session_id} disconnected")
        
    async def send_message(self, session_id: str, message: dict):
        if session_id in self.active_connections:
            try:
                await self.active_connections[session_id].send_text(json.dumps(message))
            except Exception as e:
                logging.error(f"Failed to send message to {session_id}: {e}")
                self.disconnect(session_id)
                
    async def broadcast_workflow_update(self, workflow_id: str, message: dict):
        """Broadcast update to all sessions following this workflow"""
        disconnected_sessions = []
        
        for session_id, ws in self.active_connections.items():
            if self.session_workflows.get(session_id) == workflow_id:
                try:
                    await ws.send_text(json.dumps(message))
                except Exception as e:
                    logging.error(f"Failed to broadcast to {session_id}: {e}")
                    disconnected_sessions.append(session_id)
        
        # Clean up disconnected sessions
        for session_id in disconnected_sessions:
            self.disconnect(session_id)

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, session: str):
    await manager.connect(websocket, session)
    
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            await handle_websocket_message(session, message)
            
    except WebSocketDisconnect:
        manager.disconnect(session)
    except Exception as e:
        logging.error(f"WebSocket error for session {session}: {e}")
        manager.disconnect(session)

async def handle_websocket_message(session_id: str, message: dict):
    """Handle incoming WebSocket messages"""
    message_type = message.get("type")
    
    if message_type == "user_input":
        await handle_user_input(session_id, message)
    elif message_type == "approval_response":
        await handle_approval_response(session_id, message)
    else:
        logging.warning(f"Unknown message type: {message_type}")

async def handle_user_input(session_id: str, message: dict):
    """Process user input and start workflow"""
    try:
        user_content = message.get("content", "")
        attachments = message.get("attachments", [])
        
        # Start workflow orchestration
        workflow_id = await orchestration_engine.start_workflow(
            session_id=session_id,
            user_input=user_content,
            attachments=attachments
        )
        
        # Track workflow for this session
        manager.session_workflows[session_id] = workflow_id
        
    except Exception as e:
        await manager.send_message(session_id, {
            "type": "error",
            "sessionId": session_id,
            "error": f"Failed to process input: {str(e)}",
            "timestamp": datetime.now().isoformat(),
            "recoverable": False
        })

async def handle_approval_response(session_id: str, message: dict):
    """Handle user approval response"""
    try:
        approval_id = message.get("approvalId")
        approved = message.get("approved", False)
        feedback = message.get("feedback", "")
        
        await orchestration_engine.handle_approval(
            approval_id=approval_id,
            approved=approved,
            feedback=feedback,
            session_id=session_id
        )
        
    except Exception as e:
        await manager.send_message(session_id, {
            "type": "error",
            "sessionId": session_id,
            "error": f"Failed to process approval: {str(e)}",
            "timestamp": datetime.now().isoformat(),
            "recoverable": True
        })

# Workflow event streaming
class WorkflowEventStreamer:
    def __init__(self, connection_manager: ConnectionManager):
        self.connection_manager = connection_manager
        
    async def stream_workflow_started(self, session_id: str, workflow_data: dict):
        """Stream workflow started event"""
        await self.connection_manager.send_message(session_id, {
            "type": "workflow_started",
            "sessionId": session_id,
            "workflowId": workflow_data["workflow_id"],
            "workflowName": workflow_data["name"],
            "estimatedDuration": workflow_data["estimated_duration"],
            "agents": workflow_data["agents"],
            "timestamp": datetime.now().isoformat()
        })
    
    async def stream_agent_started(self, session_id: str, agent_data: dict):
        """Stream agent started event"""
        await self.connection_manager.send_message(session_id, {
            "type": "agent_started",
            "sessionId": session_id,
            "agentRole": agent_data["role"],
            "agentName": agent_data["name"],
            "position": agent_data["position"],
            "totalAgents": agent_data["total_agents"],
            "estimatedCompletionTime": agent_data["estimated_completion"],
            "inputs": agent_data["inputs"],
            "timestamp": datetime.now().isoformat()
        })
    
    async def stream_agent_progress(self, session_id: str, progress_data: dict):
        """Stream agent progress updates"""
        await self.connection_manager.send_message(session_id, {
            "type": "agent_progress",
            "sessionId": session_id,
            "agentRole": progress_data["role"],
            "progress": progress_data["progress"],
            "currentTask": progress_data["current_task"],
            "partialOutput": progress_data.get("partial_output"),
            "thinkingProcess": progress_data.get("thinking_process"),
            "timestamp": datetime.now().isoformat()
        })
    
    async def stream_agent_completed(self, session_id: str, completion_data: dict):
        """Stream agent completion event"""
        await self.connection_manager.send_message(session_id, {
            "type": "agent_completed",
            "sessionId": session_id,
            "agentRole": completion_data["role"],
            "duration": completion_data["duration"],
            "outputs": completion_data["outputs"],
            "qualityScore": completion_data.get("quality_score"),
            "nextAgent": completion_data.get("next_agent"),
            "timestamp": datetime.now().isoformat()
        })
    
    async def stream_approval_required(self, session_id: str, approval_data: dict):
        """Stream approval gate event"""
        await self.connection_manager.send_message(session_id, {
            "type": "approval_required",
            "sessionId": session_id,
            "approvalId": approval_data["approval_id"],
            "title": approval_data["title"],
            "description": approval_data["description"],
            "agentOutputs": approval_data["agent_outputs"],
            "requiredBy": approval_data["required_by"],
            "timeoutMinutes": approval_data.get("timeout_minutes"),
            "timestamp": datetime.now().isoformat()
        })
    
    async def stream_workflow_completed(self, session_id: str, completion_data: dict):
        """Stream workflow completion event"""
        await self.connection_manager.send_message(session_id, {
            "type": "workflow_completed",
            "sessionId": session_id,
            "workflowId": completion_data["workflow_id"],
            "totalDuration": completion_data["total_duration"],
            "finalOutputs": completion_data["final_outputs"],
            "qualityScore": completion_data["quality_score"],
            "costBreakdown": completion_data["cost_breakdown"],
            "timestamp": datetime.now().isoformat()
        })

event_streamer = WorkflowEventStreamer(manager)

---

## File Upload Handling

```python
from fastapi import FastAPI, UploadFile, File, Form
from typing import List
import aiofiles
import os
import uuid

@app.post("/api/upload")
async def upload_files(
    session_id: str = Form(...),
    files: List[UploadFile] = File(...)
):
    """Handle file uploads for chat sessions"""
    try:
        uploaded_files = []
        upload_dir = f"uploads/{session_id}"
        
        # Create session upload directory
        os.makedirs(upload_dir, exist_ok=True)
        
        for file in files:
            # Generate unique filename
            file_id = str(uuid.uuid4())
            file_extension = os.path.splitext(file.filename)[1]
            safe_filename = f"{file_id}{file_extension}"
            file_path = os.path.join(upload_dir, safe_filename)
            
            # Save file
            async with aiofiles.open(file_path, 'wb') as f:
                content = await file.read()
                await f.write(content)
            
            # Process file based on type
            processed_content = await process_uploaded_file(file_path, file.content_type)
            
            uploaded_files.append({
                "file_id": file_id,
                "original_name": file.filename,
                "file_path": file_path,
                "content_type": file.content_type,
                "size": len(content),
                "processed_content": processed_content
            })
        
        # Notify session about uploaded files
        await manager.send_message(session_id, {
            "type": "files_uploaded",
            "sessionId": session_id,
            "files": uploaded_files,
            "timestamp": datetime.now().isoformat()
        })
        
        return {"status": "success", "files": uploaded_files}
        
    except Exception as e:
        logging.error(f"File upload failed for session {session_id}: {e}")
        return {"status": "error", "message": str(e)}

async def process_uploaded_file(file_path: str, content_type: str) -> dict:
    """Process uploaded files based on content type"""
    
    if content_type.startswith('text/'):
        # Text files - read content
        async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
            content = await f.read()
            return {
                "type": "text",
                "content": content,
                "preview": content[:500] + ("..." if len(content) > 500 else "")
            }
    
    elif content_type == 'application/pdf':
        # PDF files - extract text
        import PyPDF2
        with open(file_path, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            text_content = ""
            for page in pdf_reader.pages:
                text_content += page.extract_text() + "\n"
            
            return {
                "type": "pdf",
                "content": text_content,
                "pages": len(pdf_reader.pages),
                "preview": text_content[:500] + ("..." if len(text_content) > 500 else "")
            }
    
    elif content_type.startswith('image/'):
        # Image files - basic metadata
        from PIL import Image
        with Image.open(file_path) as img:
            return {
                "type": "image",
                "dimensions": img.size,
                "format": img.format,
                "mode": img.mode,
                "file_path": file_path  # For vision model processing
            }
    
    elif content_type in ['application/json', 'application/xml']:
        # Structured data files
        async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
            content = await f.read()
            return {
                "type": "structured_data",
                "content": content,
                "format": content_type,
                "preview": content[:500] + ("..." if len(content) > 500 else "")
            }
    
    else:
        # Unknown file type
        return {
            "type": "binary",
            "message": "Binary file uploaded - content not processed",
            "file_path": file_path
        }
```

---

## Message Input Component

```tsx
import React, { useState, useRef } from 'react';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Card } from '@/components/ui/card';
import { X, Upload, Send } from 'lucide-react';

interface MessageInputProps {
    onSendMessage: (content: string, attachments?: File[]) => void;
    disabled?: boolean;
    placeholder?: string;
    className?: string;
}

export const MessageInput: React.FC<MessageInputProps> = ({
    onSendMessage,
    disabled = false,
    placeholder = "Type your message...",
    className
}) => {
    const [message, setMessage] = useState('');
    const [attachments, setAttachments] = useState<File[]>([]);
    const [dragOver, setDragOver] = useState(false);
    const fileInputRef = useRef<HTMLInputElement>(null);
    const textareaRef = useRef<HTMLTextAreaElement>(null);
    
    const handleSend = () => {
        if (message.trim() || attachments.length > 0) {
            onSendMessage(message.trim(), attachments);
            setMessage('');
            setAttachments([]);
        }
    };
    
    const handleKeyPress = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    };
    
    const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
        const files = Array.from(e.target.files || []);
        setAttachments(prev => [...prev, ...files]);
    };
    
    const handleDragOver = (e: React.DragEvent) => {
        e.preventDefault();
        setDragOver(true);
    };
    
    const handleDragLeave = (e: React.DragEvent) => {
        e.preventDefault();
        setDragOver(false);
    };
    
    const handleDrop = (e: React.DragEvent) => {
        e.preventDefault();
        setDragOver(false);
        
        const files = Array.from(e.dataTransfer.files);
        setAttachments(prev => [...prev, ...files]);
    };
    
    const removeAttachment = (index: number) => {
        setAttachments(prev => prev.filter((_, i) => i !== index));
    };
    
    const formatFileSize = (bytes: number) => {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    };
    
    // Auto-resize textarea
    React.useEffect(() => {
        if (textareaRef.current) {
            textareaRef.current.style.height = 'auto';
            textareaRef.current.style.height = textareaRef.current.scrollHeight + 'px';
        }
    }, [message]);
    
    return (
        <div className={className}>
            <Card className={`p-4 ${dragOver ? 'border-blue-500 bg-blue-50' : ''}`}>
                
                {/* File Attachments */}
                {attachments.length > 0 && (
                    <div className="mb-3 space-y-2">
                        <div className="text-sm font-medium text-gray-700">
                            Attachments ({attachments.length})
                        </div>
                        <div className="space-y-1">
                            {attachments.map((file, index) => (
                                <div key={index} className="flex items-center justify-between bg-gray-100 p-2 rounded">
                                    <div className="flex items-center gap-2">
                                        <span className="text-sm">📎</span>
                                        <span className="text-sm font-medium">{file.name}</span>
                                        <span className="text-xs text-gray-500">
                                            ({formatFileSize(file.size)})
                                        </span>
                                    </div>
                                    <Button
                                        size="sm"
                                        variant="ghost"
                                        onClick={() => removeAttachment(index)}
                                        className="h-6 w-6 p-0"
                                    >
                                        <X className="h-3 w-3" />
                                    </Button>
                                </div>
                            ))}
                        </div>
                    </div>
                )}
                
                {/* Message Input */}
                <div 
                    className="relative"
                    onDragOver={handleDragOver}
                    onDragLeave={handleDragLeave}
                    onDrop={handleDrop}
                >
                    <Textarea
                        ref={textareaRef}
                        value={message}
                        onChange={(e) => setMessage(e.target.value)}
                        onKeyPress={handleKeyPress}
                        placeholder={placeholder}
                        disabled={disabled}
                        className="min-h-[60px] max-h-[200px] resize-none pr-20"
                        rows={1}
                    />
                    
                    {/* Action Buttons */}
                    <div className="absolute bottom-2 right-2 flex gap-1">
                        <input
                            ref={fileInputRef}
                            type="file"
                            multiple
                            onChange={handleFileSelect}
                            className="hidden"
                            accept=".txt,.pdf,.doc,.docx,.csv,.json,.png,.jpg,.jpeg,.gif"
                        />
                        
                        <Button
                            size="sm"
                            variant="ghost"
                            onClick={() => fileInputRef.current?.click()}
                            disabled={disabled}
                            className="h-8 w-8 p-0"
                        >
                            <Upload className="h-4 w-4" />
                        </Button>
                        
                        <Button
                            size="sm"
                            onClick={handleSend}
                            disabled={disabled || (!message.trim() && attachments.length === 0)}
                            className="h-8 w-8 p-0"
                        >
                            <Send className="h-4 w-4" />
                        </Button>
                    </div>
                </div>
                
                {/* Drag Overlay */}
                {dragOver && (
                    <div className="absolute inset-0 bg-blue-100 bg-opacity-90 flex items-center justify-center rounded border-2 border-dashed border-blue-500">
                        <div className="text-center">
                            <Upload className="h-8 w-8 mx-auto mb-2 text-blue-500" />
                            <div className="text-blue-700 font-medium">Drop files here</div>
                        </div>
                    </div>
                )}
            </Card>
            
            {/* Input Hints */}
            <div className="mt-2 text-xs text-gray-500 px-1">
                Press Enter to send • Shift+Enter for new line • Drag & drop files to attach
            </div>
        </div>
    );
};
```

---

## Approval Gate Component

```tsx
import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { Textarea } from '@/components/ui/textarea';
import { Badge } from '@/components/ui/badge';
import { CheckCircle, XCircle, Clock } from 'lucide-react';

interface ApprovalGateProps {
    approval: ApprovalRequiredMessage;
    onApprove: (feedback?: string) => void;
    onReject: (feedback?: string) => void;
    className?: string;
}

export const ApprovalGate: React.FC<ApprovalGateProps> = ({
    approval,
    onApprove,
    onReject,
    className
}) => {
    const [feedback, setFeedback] = useState('');
    const [showFeedback, setShowFeedback] = useState(false);
    
    const handleApprove = () => {
        onApprove(feedback.trim() || undefined);
        setFeedback('');
        setShowFeedback(false);
    };
    
    const handleReject = () => {
        onReject(feedback.trim() || undefined);
        setFeedback('');
        setShowFeedback(false);
    };
    
    const formatTimeRemaining = (timeoutMinutes?: number) => {
        if (!timeoutMinutes) return null;
        
        const now = new Date();
        const approvalTime = new Date(approval.timestamp);
        const timeoutTime = new Date(approvalTime.getTime() + timeoutMinutes * 60000);
        const remaining = timeoutTime.getTime() - now.getTime();
        
        if (remaining <= 0) return "Expired";
        
        const minutes = Math.floor(remaining / 60000);
        const seconds = Math.floor((remaining % 60000) / 1000);
        
        return `${minutes}:${seconds.toString().padStart(2, '0')}`;
    };
    
    return (
        <Card className={`${className} border-blue-500 bg-blue-50`}>
            <div className="p-4">
                
                {/* Header */}
                <div className="flex items-center justify-between mb-3">
                    <div className="flex items-center gap-2">
                        <Clock className="h-5 w-5 text-blue-600" />
                        <h3 className="font-semibold text-blue-900">{approval.title}</h3>
                        <Badge variant="outline" className="bg-white">
                            Approval Required
                        </Badge>
                    </div>
                    
                    {approval.timeoutMinutes && (
                        <div className="text-sm text-blue-700">
                            Time remaining: {formatTimeRemaining(approval.timeoutMinutes)}
                        </div>
                    )}
                </div>
                
                {/* Description */}
                <div className="mb-4">
                    <p className="text-blue-800 mb-3">{approval.description}</p>
                    
                    {/* Agent Outputs */}
                    <div className="space-y-2">
                        <h4 className="font-medium text-blue-900">Agent Results to Review:</h4>
                        {Object.entries(approval.agentOutputs).map(([key, value]) => (
                            <Card key={key} className="p-3 bg-white border">
                                <h5 className="font-medium text-sm mb-1 text-gray-700">
                                    {key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                                </h5>
                                <div className="text-sm text-gray-600 whitespace-pre-wrap max-h-32 overflow-y-auto">
                                    {typeof value === 'string' ? value : JSON.stringify(value, null, 2)}
                                </div>
                            </Card>
                        ))}
                    </div>
                </div>
                
                {/* Feedback Section */}
                {showFeedback && (
                    <div className="mb-4">
                        <label className="block text-sm font-medium text-blue-900 mb-2">
                            Feedback (optional)
                        </label>
                        <Textarea
                            value={feedback}
                            onChange={(e) => setFeedback(e.target.value)}
                            placeholder="Provide feedback or suggestions for improvements..."
                            className="bg-white"
                            rows={3}
                        />
                    </div>
                )}
                
                {/* Action Buttons */}
                <div className="flex gap-2">
                    <Button
                        onClick={handleApprove}
                        className="bg-green-600 hover:bg-green-700 text-white"
                    >
                        <CheckCircle className="h-4 w-4 mr-1" />
                        Approve & Continue
                    </Button>
                    
                    <Button
                        onClick={handleReject}
                        variant="destructive"
                    >
                        <XCircle className="h-4 w-4 mr-1" />
                        Reject & Revise
                    </Button>
                    
                    {!showFeedback && (
                        <Button
                            onClick={() => setShowFeedback(true)}
                            variant="outline"
                            className="bg-white"
                        >
                            Add Feedback
                        </Button>
                    )}
                </div>
                
                {/* Required By Info */}
                <div className="mt-3 text-xs text-blue-600">
                    Approval required by: {approval.requiredBy}
                </div>
            </div>
        </Card>
    );
};
```

---

## Performance Optimizations

### Message Virtualization for Large Conversations

```tsx
import React from 'react';
import { FixedSizeList as List } from 'react-window';

interface VirtualizedMessageListProps {
    messages: AgentMessage[];
    height: number;
    itemHeight: number;
}

export const VirtualizedMessageList: React.FC<VirtualizedMessageListProps> = ({
    messages,
    height,
    itemHeight
}) => {
    const Row = ({ index, style }: { index: number; style: React.CSSProperties }) => (
        <div style={style}>
            <MessageBubble message={messages[index]} />
        </div>
    );
    
    return (
        <List
            height={height}
            itemCount={messages.length}
            itemSize={itemHeight}
            overscanCount={5}
        >
            {Row}
        </List>
    );
};
```

### WebSocket Connection Recovery

```typescript
class RobustWebSocketClient extends AgentOrchestrationClient {
    private heartbeatInterval: NodeJS.Timeout | null = null;
    private lastPongReceived = Date.now();
    
    connect(wsUrl: string): Promise<void> {
        return super.connect(wsUrl).then(() => {
            this.startHeartbeat();
        });
    }
    
    private startHeartbeat() {
        this.heartbeatInterval = setInterval(() => {
            if (this.ws && this.ws.readyState === WebSocket.OPEN) {
                this.ws.send(JSON.stringify({ type: 'ping' }));
                
                // Check if we've received a pong recently
                if (Date.now() - this.lastPongReceived > 30000) {
                    console.warn('WebSocket appears to be stale, reconnecting...');
                    this.ws.close();
                }
            }
        }, 10000);
    }
    
    protected handleMessage(message: AgentMessage) {
        if (message.type === 'pong') {
            this.lastPongReceived = Date.now();
            return;
        }
        
        super.handleMessage(message);
    }
    
    disconnect() {
        if (this.heartbeatInterval) {
            clearInterval(this.heartbeatInterval);
            this.heartbeatInterval = null;
        }
        super.disconnect();
    }
}
```

This comprehensive chat integration provides a robust, real-time interface for users to interact with the MCP-based agent orchestration system, with full support for file uploads, approval gates, and seamless WebSocket communication.