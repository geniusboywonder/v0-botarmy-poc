"use client"

import type React from "react"
import { Sidebar } from "./sidebar"

interface MainLayoutProps {
  children: React.ReactNode
}

export function MainLayout({ children }: MainLayoutProps) {
  return (
    <div className="min-h-screen bg-background flex">
      <Sidebar activeView="" onViewChange={() => {}} />
      <main className="flex-1 overflow-auto">{children}</main>
    </div>
  )
}
