"use client"

import React from 'react';

export const TypingIndicator = () => {
  return (
    <div className="flex items-center space-x-1">
      <div
        className="w-2 h-2 bg-primary rounded-full animate-bounce"
        style={{ animationDelay: '0ms', animationDuration: '1s' }}
      />
      <div
        className="w-2 h-2 bg-primary rounded-full animate-bounce"
        style={{ animationDelay: '150ms', animationDuration: '1s' }}
      />
      <div
        className="w-2 h-2 bg-primary rounded-full animate-bounce"
        style={{ animationDelay: '300ms', animationDuration: '1s' }}
      />
    </div>
  );
};
