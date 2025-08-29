"use client"

import { ThemeProvider } from "@/components/theme-provider"
import { ErrorBoundary } from "@/components/error-boundary"
import { WebSocketProvider } from "@/lib/context/websocket-provider"
import type React from "react"

export function ClientProvider({ children }: { children: React.ReactNode }) {
  return (
    <div className="dark">
      <ThemeProvider
        attribute="class"
        defaultTheme="dark"
        enableSystem={false}
        forcedTheme="dark"
        disableTransitionOnChange
      >
        <ErrorBoundary>
          <WebSocketProvider>
            {children}
          </WebSocketProvider>
        </ErrorBoundary>
      </ThemeProvider>
    </div>
  )
}
