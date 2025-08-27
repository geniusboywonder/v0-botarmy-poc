"use client"

import type React from "react"
import { Sidebar } from "./sidebar"
import { Header } from "./layout/header"
import { ConsoleLoggerProvider } from "./console-logger-provider"

interface MainLayoutProps {
  children: React.ReactNode
}

export function MainLayout({ children }: MainLayoutProps) {
  return (
    <ConsoleLoggerProvider>
      <div className="min-h-screen bg-background flex flex-col">
        <Header />
        <div className="flex flex-1">
          <Sidebar activeView="" onViewChange={() => {}} />
          <main className="flex-1 overflow-auto">{children}</main>
        </div>
      </div>
    </ConsoleLoggerProvider>
  )
}