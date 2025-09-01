"use client"

import * as React from "react"
import * as TabsPrimitive from "@radix-ui/react-tabs"

import { cn } from "@/lib/utils"

function Tabs({
  className,
  ...props
}: React.ComponentProps<typeof TabsPrimitive.Root>) {
  return (
    <TabsPrimitive.Root
      data-slot="tabs"
      className={cn("flex flex-col gap-2", className)}
      {...props}
    />
  )
}

function TabsList({
  className,
  ...props
}: React.ComponentProps<typeof TabsPrimitive.List>) {
  return (
    <TabsPrimitive.List
      data-slot="tabs-list"
      className={cn(
        "inline-flex h-auto w-fit items-end justify-start border-b border-border bg-transparent",
        className
      )}
      {...props}
    />
  )
}

function TabsTrigger({
  className,
  ...props
}: React.ComponentProps<typeof TabsPrimitive.Trigger>) {
  return (
    <TabsPrimitive.Trigger
      data-slot="tabs-trigger"
      className={cn(
        // Base styling
        "inline-flex items-center justify-center gap-2 px-4 py-2.5 text-sm font-medium transition-all duration-200",
        "whitespace-nowrap border-t border-l border-r border-transparent bg-transparent",
        "rounded-t-lg -mb-px relative",
        // Inactive state
        "text-muted-foreground hover:text-foreground hover:bg-muted/50",
        // Active state
        "data-[state=active]:text-foreground data-[state=active]:bg-background",
        "data-[state=active]:border-border data-[state=active]:border-b-background",
        "data-[state=active]:shadow-sm",
        // Focus states
        "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary/20",
        "focus-visible:border-primary/50",
        // Disabled state
        "disabled:pointer-events-none disabled:opacity-50",
        // Icon sizing
        "[&_svg]:pointer-events-none [&_svg]:shrink-0 [&_svg:not([class*='size-'])]:size-4",
        className
      )}
      {...props}
    />
  )
}

function TabsContent({
  className,
  ...props
}: React.ComponentProps<typeof TabsPrimitive.Content>) {
  return (
    <TabsPrimitive.Content
      data-slot="tabs-content"
      className={cn(
        "flex-1 outline-none border border-border border-t-0 rounded-b-lg rounded-tr-lg bg-background p-4",
        className
      )}
      {...props}
    />
  )
}

export { Tabs, TabsList, TabsTrigger, TabsContent }
