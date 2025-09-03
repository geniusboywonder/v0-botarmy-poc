"use client"

import React, { useState, useEffect } from "react"
import { MainLayout } from "@/components/main-layout"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Badge } from "@/components/ui/badge"
import { Switch } from "@/components/ui/switch"
import { 
  Save, 
  RefreshCw, 
  Eye, 
  EyeOff, 
  AlertTriangle,
  CheckCircle,
  Settings as SettingsIcon,
  Key,
  Server,
  Globe,
  Zap,
  TestTube
} from "lucide-react"
import { cn } from "@/lib/utils"

interface EnvVariable {
  key: string
  value: string | boolean | number
  description: string
  category: string
  isSecret?: boolean
  required?: boolean
  type: "string" | "boolean" | "number"
}

// Fetch environment variables from API
const fetchEnvVariables = async (): Promise<EnvVariable[]> => {
  try {
    const response = await fetch('/api/env-settings')
    const data = await response.json()
    
    if (data.success) {
      // Map API response to our EnvVariable format
      return data.variables.map((variable: any) => ({
        ...variable,
        category: variable.category || "Testing Configuration", // Default category
        required: false,
        isSecret: false
      }))
    } else {
      console.error('Failed to fetch environment variables:', data.error)
      return getDefaultEnvVariables()
    }
  } catch (error) {
    console.error('Error fetching environment variables:', error)
    return getDefaultEnvVariables()
  }
}

const getDefaultEnvVariables = (): EnvVariable[] => [
  // Fallback default values if API fails
  {
    key: "AGENT_TEST_MODE",
    value: true,
    description: "Enable agent test mode to return static confirmations",
    category: "Testing Configuration",
    required: false,
    type: "boolean"
  },
  {
    key: "ROLE_TEST_MODE",
    value: false,
    description: "Enable role test mode for LLM role confirmation",
    category: "Testing Configuration",
    required: false,
    type: "boolean"
  },
  {
    key: "TEST_MODE",
    value: true,
    description: "Enable overall test mode for mock LLM responses",
    category: "Testing Configuration",
    required: false,
    type: "boolean"
  },
  {
    key: "ENABLE_HITL",
    value: false,
    description: "Enable Human-in-the-Loop functionality",
    category: "Testing Configuration",
    required: false,
    type: "boolean"
  },
  {
    key: "AUTO_ACTION",
    value: "approve",
    description: "Default auto action (approve/reject)",
    category: "Testing Configuration",
    required: false,
    type: "string"
  },
  // Enhanced 10-step Workflow Configuration
  {
    key: "WORKFLOW_REQUIREMENTS_GATHERING_ENABLED",
    value: true,
    description: "Enable interactive requirements gathering in workflows",
    category: "Workflow Configuration",
    required: false,
    type: "boolean"
  },
  {
    key: "WORKFLOW_REQUIREMENTS_MAX_QUESTIONS",
    value: 5,
    description: "Maximum number of requirements gathering questions",
    category: "Workflow Configuration",
    required: false,
    type: "number"
  },
  {
    key: "WORKFLOW_REQUIREMENTS_TIMEOUT_MINUTES",
    value: 10,
    description: "Timeout for requirements gathering (minutes)",
    category: "Workflow Configuration",
    required: false,
    type: "number"
  },
  {
    key: "WORKFLOW_REQUIREMENTS_AUTO_PROCEED",
    value: true,
    description: "Automatically proceed when requirements gathering times out",
    category: "Workflow Configuration",
    required: false,
    type: "boolean"
  },
  {
    key: "WORKFLOW_HITL_ANALYZE_REQUIRED",
    value: true,
    description: "Require human approval at Analyze stage",
    category: "Workflow Configuration",
    required: false,
    type: "boolean"
  },
  {
    key: "WORKFLOW_HITL_ANALYZE_TIMEOUT_MINUTES",
    value: 30,
    description: "Timeout for Analyze stage approval (minutes)",
    category: "Workflow Configuration",
    required: false,
    type: "number"
  },
  {
    key: "WORKFLOW_HITL_DESIGN_REQUIRED",
    value: false,
    description: "Require human approval at Design stage",
    category: "Workflow Configuration",
    required: false,
    type: "boolean"
  },
  {
    key: "WORKFLOW_HITL_DESIGN_TIMEOUT_MINUTES",
    value: 30,
    description: "Timeout for Design stage approval (minutes)",
    category: "Workflow Configuration",
    required: false,
    type: "number"
  },
  {
    key: "WORKFLOW_ARTIFACT_AUTO_PLACEHOLDERS",
    value: true,
    description: "Automatically create artifact placeholders",
    category: "Workflow Configuration",
    required: false,
    type: "boolean"
  },
  {
    key: "WORKFLOW_ARTIFACT_UI_INTEGRATION",
    value: true,
    description: "Enable UI integration for artifact scaffolding",
    category: "Workflow Configuration",
    required: false,
    type: "boolean"
  }
]

const getCategoryIcon = (category: string) => {
  switch (category) {
    case "LLM Configuration": return <Key className="w-4 h-4 text-primary" />
    case "Backend Configuration": return <Server className="w-4 h-4 text-analyst" />
    case "WebSocket Configuration": return <Zap className="w-4 h-4 text-amber" />
    case "Frontend Configuration": return <Globe className="w-4 h-4 text-tester" />
    case "Development Settings": return <SettingsIcon className="w-4 h-4 text-muted-foreground" />
    case "Testing Configuration": return <TestTube className="w-4 h-4 text-developer" />
    case "Workflow Configuration": return <RefreshCw className="w-4 h-4 text-architect" />
    default: return <SettingsIcon className="w-4 h-4 text-muted-foreground" />
  }
}

const getCategoryColor = (category: string) => {
  switch (category) {
    case "LLM Configuration": return "bg-primary/10 text-primary border-primary/20"
    case "Backend Configuration": return "bg-analyst/10 text-analyst border-analyst/20"
    case "WebSocket Configuration": return "bg-amber/10 text-amber border-amber/20"
    case "Frontend Configuration": return "bg-tester/10 text-tester border-tester/20"
    case "Development Settings": return "bg-muted/10 text-muted-foreground border-muted/20"
    case "Testing Configuration": return "bg-developer/10 text-developer border-developer/20"
    case "Workflow Configuration": return "bg-architect/10 text-architect border-architect/20"
    default: return "bg-muted/10 text-muted-foreground border-muted/20"
  }
}

export default function SettingsPage() {
  const [envVariables, setEnvVariables] = useState<EnvVariable[]>([])
  const [visibleSecrets, setVisibleSecrets] = useState<string[]>([])
  const [hasChanges, setHasChanges] = useState(false)
  const [isSaving, setIsSaving] = useState(false)
  const [saveStatus, setSaveStatus] = useState<"idle" | "success" | "error">("idle")
  const [isClient, setIsClient] = useState(false)

  useEffect(() => {
    setIsClient(true)
    // Load real environment variables from the API
    const loadEnvVariables = async () => {
      const variables = await fetchEnvVariables()
      setEnvVariables(variables)
    }
    loadEnvVariables()
  }, [])

  // Group variables by category for 3-column layout
  const allVariables = envVariables.reduce((acc, variable) => {
    if (!acc[variable.category]) {
      acc[variable.category] = []
    }
    acc[variable.category].push(variable)
    return acc
  }, {} as Record<string, EnvVariable[]>)

  const categories = Object.keys(allVariables)

  const toggleSecretVisibility = (key: string) => {
    setVisibleSecrets(prev =>
      prev.includes(key)
        ? prev.filter(k => k !== key)
        : [...prev, key]
    )
  }

  const updateEnvVariable = (key: string, newValue: string | boolean) => {
    setEnvVariables(prev =>
      prev.map(env =>
        env.key === key ? { ...env, value: newValue } : env
      )
    )
    setHasChanges(true)
    setSaveStatus("idle")
  }

  const handleSave = async () => {
    setIsSaving(true)
    setSaveStatus("idle")
    
    try {
      const response = await fetch('/api/env-settings', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          variables: envVariables
        }),
      })
      
      const data = await response.json()
      
      if (data.success) {
        console.log("Environment variables saved successfully")
        
        // Refresh backend configuration cache
        try {
          const refreshResponse = await fetch('/api/config-refresh', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
          })
          
          if (refreshResponse.ok) {
            console.log("Backend configuration cache refreshed")
          } else {
            console.warn("Failed to refresh backend configuration cache")
          }
        } catch (refreshError) {
          console.warn("Could not refresh backend configuration cache:", refreshError)
        }
        
        setSaveStatus("success")
        setHasChanges(false)
      } else {
        console.error("Failed to save:", data.error)
        setSaveStatus("error")
      }
    } catch (error) {
      console.error("Failed to save:", error)
      setSaveStatus("error")
    } finally {
      setIsSaving(false)
    }
  }

  const handleReset = async () => {
    const variables = await fetchEnvVariables()
    setEnvVariables(variables)
    setHasChanges(false)
    setSaveStatus("idle")
  }

  if (!isClient) {
    return (
      <MainLayout>
        <div className="p-6">
          <div className="animate-pulse">Loading...</div>
        </div>
      </MainLayout>
    )
  }

  return (
    <MainLayout>
      <div className="p-6 space-y-8">
        {/* Page Header */}
        <div className="space-y-2">
          <h1 className="text-3xl font-bold tracking-tight text-foreground">Environment Settings</h1>
          <p className="text-lg text-muted-foreground">
            Configure environment variables and application settings for the BotArmy platform.
          </p>
        </div>

        {/* Save Actions */}
        <Card className="border-dashed border-teal/20 bg-teal/10">
          <CardContent className="pt-6">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                {saveStatus === "success" && (
                  <div className="flex items-center space-x-2 text-tester">
                    <CheckCircle className="w-4 h-4" />
                    <span className="text-sm font-medium">Settings saved successfully</span>
                  </div>
                )}
                {saveStatus === "error" && (
                  <div className="flex items-center space-x-2 text-destructive">
                    <AlertTriangle className="w-4 h-4" />
                    <span className="text-sm font-medium">Failed to save settings</span>
                  </div>
                )}
                {hasChanges && saveStatus === "idle" && (
                  <div className="flex items-center space-x-2 text-amber">
                    <AlertTriangle className="w-4 h-4" />
                    <span className="text-sm font-medium">You have unsaved changes</span>
                  </div>
                )}
              </div>
              <div className="flex items-center space-x-2">
                <Button 
                  variant="outline" 
                  onClick={handleReset}
                  disabled={isSaving || !hasChanges}
                >
                  <RefreshCw className="w-4 h-4 mr-2" />
                  Reset
                </Button>
                <Button 
                  onClick={handleSave}
                  disabled={isSaving || !hasChanges}
                  className={cn(
                    "bg-teal text-background hover:bg-teal/90 shadow-sm",
                    hasChanges && "ring-2 ring-teal/30 ring-offset-1"
                  )}
                >
                  {isSaving ? (
                    <RefreshCw className="w-4 h-4 mr-2 animate-spin" />
                  ) : (
                    <Save className="w-4 h-4 mr-2" />
                  )}
                  {isSaving ? "Saving..." : "Save Changes"}
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Environment Variables Section */}
        <div className="space-y-4">
          <div className="border-t border-border pt-8">
            <h2 className="text-xl font-semibold text-foreground mb-6">Configuration Categories</h2>
          </div>
          <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-8">
            {categories.map((category) => (
              <Card key={category} className="shadow-sm">
                <CardHeader>
                <div className="flex items-center space-x-3">
                  {getCategoryIcon(category)}
                  <div>
                    <CardTitle className="text-base">{category}</CardTitle>
                    <CardDescription>
                      {allVariables[category].length} variables
                    </CardDescription>
                  </div>
                </div>
                <Badge variant="outline" className={cn("w-fit", getCategoryColor(category))}>
                  {category.replace(" Configuration", "").replace(" Settings", "")}
                </Badge>
              </CardHeader>
              <CardContent className="space-y-4">
                {allVariables[category].map((env) => (
                  <div key={env.key} className="space-y-2">
                    <div className="flex items-center justify-between">
                      <Label htmlFor={env.key} className="text-xs font-semibold flex items-center space-x-2">
                        <span>{env.key}</span>
                      </Label>
                      {env.isSecret && (
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => toggleSecretVisibility(env.key)}
                          className="h-6 px-2"
                        >
                          {visibleSecrets.includes(env.key) ? (
                            <EyeOff className="w-3 h-3" />
                          ) : (
                            <Eye className="w-3 h-3" />
                          )}
                        </Button>
                      )}
                    </div>
                    <p className="text-xs text-muted-foreground">{env.description}</p>
                    
                    {env.type === "boolean" ? (
                      <div className="flex items-center space-x-2">
                        <Switch
                          id={env.key}
                          checked={env.value as boolean}
                          onCheckedChange={(checked) => updateEnvVariable(env.key, checked)}
                        />
                        <Label htmlFor={env.key} className="text-sm">
                          {env.value ? "Enabled" : "Disabled"}
                        </Label>
                      </div>
                    ) : env.type === "number" ? (
                      <Input
                        id={env.key}
                        type="number"
                        value={env.value as number}
                        onChange={(e) => updateEnvVariable(env.key, parseInt(e.target.value) || 0)}
                        className={cn(
                          "font-mono text-xs",
                          env.required && !env.value && "border-destructive focus:border-destructive"
                        )}
                        placeholder={env.required ? "Required" : "Optional"}
                      />
                    ) : (
                      <Input
                        id={env.key}
                        type={env.isSecret && !visibleSecrets.includes(env.key) ? "password" : "text"}
                        value={env.value as string}
                        onChange={(e) => updateEnvVariable(env.key, e.target.value)}
                        className={cn(
                          "font-mono text-xs",
                          env.required && !env.value && "border-destructive focus:border-destructive"
                        )}
                        placeholder={env.required ? "Required" : "Optional"}
                      />
                    )}
                  </div>
                ))}
              </CardContent>
            </Card>
            ))}
          </div>
        </div>
      </div>
    </MainLayout>
  )
}
