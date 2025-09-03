"use client";

import { CopilotChat, CopilotMessage as Message } from "@copilotkit/react-ui";
import { useCopilotReadable } from "@copilotkit/react-core";
import "@copilotkit/react-ui/styles.css";
import {
  Bot,
  User,
  CheckCircle,
  ClipboardCheck,
  DraftingCompass,
  Construction,
  TestTube2,
  Rocket,
  ChevronsRightLeft
} from "lucide-react";
import { cn } from "@/lib/utils";
import { useAgentStore } from "@/lib/stores/agent-store";
import { useChatModeStore } from "@/lib/stores/chat-mode-store";
import { useState, useRef, useCallback } from "react";
import { CopilotAgentStatus } from "./copilot-agent-status";

interface CustomCopilotMessage extends Message {
  agent?: string;
}

// Multi-Corner Resizable Hook
const useMultiResizable = (initialWidth = 800, initialHeight = 600) => {
  const getInitialDimensions = () => {
    if (typeof window === 'undefined') return { width: initialWidth, height: initialHeight, x: 0, y: 0 };
    const isMobile = window.innerWidth < 768;
    return {
      width: isMobile ? window.innerWidth - 40 : initialWidth,
      height: isMobile ? window.innerHeight - 120 : initialHeight,
      x: 0,
      y: 0
    };
  };

  const [dimensions, setDimensions] = useState(getInitialDimensions);
  const [isResizable, setIsResizable] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);

  const createResizeHandler = useCallback((corner: 'nw' | 'ne' | 'sw' | 'se') => {
    return (e: React.MouseEvent) => {
      e.preventDefault();
      e.stopPropagation();

      const startX = e.clientX;
      const startY = e.clientY;
      const startWidth = dimensions.width;
      const startHeight = dimensions.height;
      const startPosX = dimensions.x;
      const startPosY = dimensions.y;

      const handleMouseMove = (moveEvent: MouseEvent) => {
        moveEvent.preventDefault();

        const deltaX = moveEvent.clientX - startX;
        const deltaY = moveEvent.clientY - startY;

        let newWidth = startWidth;
        let newHeight = startHeight;
        let newX = startPosX;
        let newY = startPosY;

        if (corner === 'nw') {
          newWidth = startWidth - deltaX;
          newHeight = startHeight - deltaY;
          newX = startPosX + deltaX;
          newY = startPosY + deltaY;
        } else if (corner === 'ne') {
          newWidth = startWidth + deltaX;
          newHeight = startHeight - deltaY;
          newY = startPosY + deltaY;
        } else if (corner === 'sw') {
          newWidth = startWidth - deltaX;
          newHeight = startHeight + deltaY;
          newX = startPosX + deltaX;
        } else if (corner === 'se') {
          newWidth = startWidth + deltaX;
          newHeight = startHeight + deltaY;
        }

        const maxWidth = Math.min(window.innerWidth - 40, 1200);
        const maxHeight = Math.min(window.innerHeight - 120, 800);
        const minWidth = 400;
        const minHeight = 400;

        newWidth = Math.max(minWidth, Math.min(newWidth, maxWidth));
        newHeight = Math.max(minHeight, Math.min(newHeight, maxHeight));

        requestAnimationFrame(() => {
          setDimensions({ width: newWidth, height: newHeight, x: newX, y: newY });
        });
      };

      const handleMouseUp = () => {
        document.removeEventListener("mousemove", handleMouseMove);
        document.removeEventListener("mouseup", handleMouseUp);
      };

      document.addEventListener("mousemove", handleMouseMove);
      document.addEventListener("mouseup", handleMouseUp);
    };
  }, [dimensions]);

  return {
    dimensions,
    containerRef,
    createResizeHandler,
    isResizable,
    setIsResizable
  };
};


// Role-based Icon Mapping
const getRoleIcon = (agent: string = '') => {
  const agentLower = agent.toLowerCase();
  if (agentLower.includes('analyst')) return <ClipboardCheck className="w-4 h-4" />;
  if (agentLower.includes('architect')) return <DraftingCompass className="w-4 h-4" />;
  if (agentLower.includes('developer')) return <Construction className="w-4 h-4" />;
  if (agentLower.includes('tester')) return <TestTube2 className="w-4 h-4" />;
  if (agentLower.includes('deployer')) return <Rocket className="w-4 h-4" />;

  if (agent === 'User') return <User className="w-4 h-4" />;
  if (agent === 'System') return <CheckCircle className="w-4 h-4" />;
  return <Bot className="w-4 h-4" />;
};

const getMessageIcon = (message: CustomCopilotMessage) => {
  if (message.role === "user") return <User className="w-4 h-4 text-user" />;
  if (message.agent === "System") return <CheckCircle className="w-4 h-4 text-system" />;
  return getRoleIcon(message.agent || '');
};

const getMessageSeverityColor = (message: CustomCopilotMessage) => {
  if (message.role === "user") return 'bg-user/10 border-user/20 text-user';
  if (message.agent === "System") return 'bg-system/10 border-system/20 text-system';
  return 'bg-secondary border-border text-foreground';
};

const CopilotChatMessage = ({ message }: { message: CustomCopilotMessage }) => {
  return (
    <div className={cn("p-4 rounded-lg border", getMessageSeverityColor(message))}>
      <div className="flex items-start space-x-3">
        <div className="mt-1">
          {getMessageIcon(message)}
        </div>
        <div className="flex-1">
          <div className="font-semibold">
            {message.agent || message.role}
          </div>
          <div className="prose prose-sm text-foreground/80">
            {message.content}
          </div>
        </div>
      </div>
    </div>
  );
};

const CustomCopilotChat = () => {
  const { agents } = useAgentStore();
  const { mode } = useChatModeStore();
  const {
    dimensions,
    containerRef,
    createResizeHandler,
    isResizable,
    setIsResizable
  } = useMultiResizable();

  useCopilotReadable({
    description: "The current status of all AI agents.",
    value: agents,
  });

  useCopilotReadable({
    description: "The current mode of the chat.",
    value: mode,
  });

  return (
    <div
      ref={containerRef}
      style={isResizable ? {
        width: `${dimensions.width}px`,
        height: `${dimensions.height}px`,
        transform: `translate(${dimensions.x}px, ${dimensions.y}px)`,
      } : {}}
      className={cn(
        "fixed bottom-4 right-4 z-50 transition-all duration-300",
        isResizable && "border-2 border-primary/50 shadow-2xl rounded-lg bg-background"
      )}
    >
      <div className="flex h-full">
        <div className="w-1/2 h-full">
          <CopilotChat
            instructions="Help the user manage their project. The current agent statuses are available. The current chat mode is also available."
            defaultOpen={true}
            labels={{
              title: "BotArmy Assistant",
              initial: "Hello! How can I help you today?",
            }}
            messageRenderer={CopilotChatMessage as React.FC<{message: Message}>}
          />
        </div>
        <div className="w-1/2 h-full p-4 overflow-y-auto">
          <CopilotAgentStatus />
        </div>
      </div>

      <button
        onClick={() => setIsResizable(!isResizable)}
        className="absolute top-2 right-2 p-1 rounded-full bg-background hover:bg-muted transition-colors"
        title={isResizable ? "Dock chat" : "Undock and resize chat"}
      >
        <ChevronsRightLeft className="w-4 h-4" />
      </button>

      {isResizable && (
        <>
          <div onMouseDown={createResizeHandler('nw')} className="absolute -top-1 -left-1 w-4 h-4 cursor-nw-resize" />
          <div onMouseDown={createResizeHandler('ne')} className="absolute -top-1 -right-1 w-4 h-4 cursor-ne-resize" />
          <div onMouseDown={createResizeHandler('sw')} className="absolute -bottom-1 -left-1 w-4 h-4 cursor-sw-resize" />
          <div onMouseDown={createResizeHandler('se')} className="absolute -bottom-1 -right-1 w-4 h-4 cursor-se-resize" />
        </>
      )}
    </div>
  );
};

export default CustomCopilotChat;
