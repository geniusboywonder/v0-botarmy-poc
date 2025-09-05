import React, { useState, useRef, useEffect } from 'react';
import { Send, Loader2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { cn } from '@/lib/utils';

interface ChatInputProps {
  onSend: (message: string) => void;
  isLoading: boolean;
  hasActiveHITL: boolean;
  placeholder?: string;
  disabled?: boolean;
  maxLength?: number;
}

const ChatInput: React.FC<ChatInputProps> = ({
  onSend,
  isLoading,
  hasActiveHITL,
  placeholder = "Type a message...",
  disabled = false,
  maxLength = 1000
}) => {
  const [message, setMessage] = useState('');
  const inputRef = useRef<HTMLInputElement>(null);

  // Focus input when component mounts
  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (message.trim() && !isLoading && !disabled) {
      onSend(message.trim());
      setMessage('');
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const isDisabled = disabled || isLoading || hasActiveHITL;
  const canSend = message.trim().length > 0 && !isDisabled;

  const getPlaceholder = () => {
    if (hasActiveHITL) {
      return "Please respond to the HITL request first...";
    }
    if (isLoading) {
      return "Agent is responding...";
    }
    return placeholder;
  };

  return (
    <div className="border-t bg-background p-4">
      <form onSubmit={handleSubmit} className="flex items-center space-x-2">
        <div className="flex-1 relative">
          <Input
            ref={inputRef}
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder={getPlaceholder()}
            disabled={isDisabled}
            maxLength={maxLength}
            className={cn(
              "pr-12",
              isDisabled && "opacity-50 cursor-not-allowed",
              hasActiveHITL && "ring-2 ring-amber-500/50"
            )}
          />
          {/* Character Counter */}
          {maxLength && (
            <div className="absolute inset-y-0 right-2 flex items-center">
              <span className={cn(
                "text-xs text-muted-foreground",
                message.length > maxLength * 0.9 ? "text-destructive" : 
                message.length > maxLength * 0.7 ? "text-amber-500" : "text-muted-foreground"
              )}>
                {message.length}/{maxLength}
              </span>
            </div>
          )}
        </div>
        
        <Button
          type="submit"
          disabled={!canSend}
          size="sm"
          className={cn(
            "px-4 py-2 h-10",
            hasActiveHITL && "bg-amber-500 hover:bg-amber-600",
            !hasActiveHITL && "bg-primary hover:bg-primary/90"
          )}
        >
          {isLoading ? (
            <Loader2 className="w-4 h-4 animate-spin" />
          ) : (
            <Send className="w-4 h-4" />
          )}
        </Button>
      </form>
      
      {/* HITL Warning */}
      {hasActiveHITL && (
        <div className="mt-2 text-xs text-amber-600 flex items-center">
          <div className="w-2 h-2 bg-amber-500 rounded-full mr-2 animate-pulse" />
          Human approval required before continuing
        </div>
      )}
    </div>
  );
};

export default ChatInput;
