"use client"

import { useState } from "react"
import { MainLayout } from "@/components/main-layout"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Badge } from "@/components/ui/badge"
import { FileText, Code, Download, Upload, Folder, FolderOpen, ChevronRight, ChevronDown } from "lucide-react"
import { useArtifactStore, ArtifactNode } from "@/lib/stores/artifact-store"
import { Switch } from "@/components/ui/switch"
import { Label } from "@/components/ui/label"

// The mockArtifacts object is now removed.

function formatBytes(bytes: number, decimals = 2) {
  if (bytes === 0) return "0 Bytes"
  const k = 1024
  const dm = decimals < 0 ? 0 : decimals
  const sizes = ["Bytes", "KB", "MB", "GB", "TB"]
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + " " + sizes[i]
}

function FileTreeNode({ node, level = 0 }: { node: ArtifactNode; level?: number }) {
  const [expanded, setExpanded] = useState(node.type === "folder" ? level < 1 : false)

  const handleToggle = () => {
    if (node.type === "folder") {
      setExpanded(!expanded)
    }
  }

  const handleDownload = (e: React.MouseEvent) => {
    e.stopPropagation() // Prevent the row click from toggling folder state
    if (node.type === "file" && node.path) {
      const backendUrl = "http://localhost:8000"
      // The path from the backend includes the "artifacts/" prefix, which we need to remove for the download URL.
      const relativePath = node.path.startsWith("artifacts/") ? node.path.substring("artifacts/".length) : node.path
      const downloadUrl = `${backendUrl}/artifacts/download/${relativePath}`
      window.open(downloadUrl, "_blank")
    }
  }

  return (
    <div className="select-none">
      <div
        className={`flex items-center gap-2 py-1 px-2 hover:bg-muted/50 rounded cursor-pointer group ${
          level > 0 ? "ml-4" : ""
        }`}
        onClick={handleToggle}
      >
        {node.type === "folder" ? (
          <>
            {expanded ? (
              <ChevronDown className="h-4 w-4 text-muted-foreground" />
            ) : (
              <ChevronRight className="h-4 w-4 text-muted-foreground" />
            )}
            {expanded ? <FolderOpen className="h-4 w-4 text-primary" /> : <Folder className="h-4 w-4 text-primary" />}
          </>
        ) : (
          <>
            <div className="w-4" />
            {node.name.endsWith(".py") ? (
              <Code className="h-4 w-4 text-green-500" />
            ) : (
              <FileText className="h-4 w-4 text-blue-500" />
            )}
          </>
        )}

        <span className="flex-1 text-sm font-medium">{node.name}</span>

        {node.type === "file" && (
          <div className="flex items-center gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
            <span className="text-xs text-muted-foreground">{node.size ? formatBytes(node.size) : ""}</span>
            <Button size="sm" variant="ghost" className="h-6 w-6 p-0" onClick={handleDownload}>
              <Download className="h-3 w-3" />
            </Button>
          </div>
        )}
      </div>

      {node.type === "folder" && expanded && node.children && (
        <div className="ml-2">
          {node.children.map((child, index) => (
            <FileTreeNode key={index} node={child} level={level + 1} />
          ))}
        </div>
      )}
    </div>
  )
}

const artifactChecklistData = {
  requirements: [
    { id: "reqs-doc", label: "Requirements Document", critical: true },
    { id: "use-cases", label: "Use Cases", critical: false },
  ],
  design: [
    { id: "arch-diagram", label: "Architecture Diagram", critical: true },
    { id: "design-model", label: "Design Models", critical: false },
  ],
  development: [
    { id: "source-code", label: "Source Code", critical: true },
    { id: "code-docs", label: "Code Documentation", critical: false },
  ],
  testing: [
    { id: "test-plan", label: "Test Plan", critical: true },
    { id: "test-cases", label: "Test Cases", critical: false },
    { id: "test-scripts", label: "Test Scripts", critical: false },
  ],
  deployment: [
    { id: "deploy-scripts", label: "Deployment Scripts", critical: true },
    { id: "config-files", label: "Configuration Files", critical: false },
  ],
  maintenance: [
    { id: "monitoring-reports", label: "Monitoring Reports", critical: false },
    { id: "logs", label: "Logs", critical: false },
  ],
};

export default function ArtifactsPage() {
  const [activeTab, setActiveTab] = useState("development")
  const artifacts = useArtifactStore((state) => state.artifacts)
  const [checklist, setChecklist] = useState(() => {
    const initialState = {};
    Object.values(artifactChecklistData).forEach(phase => {
      phase.forEach(item => {
        initialState[item.id] = true; // Default all to checked
      });
    });
    return initialState;
  });

  const handleChecklistChange = (itemId: string, isChecked: boolean, isCritical: boolean) => {
    if (isCritical && !isChecked) {
      // Prevent unchecking critical items for now
      return;
    }
    setChecklist(prev => ({ ...prev, [itemId]: isChecked }));
    websocketService.sendArtifactPreference(itemId, isChecked);
  };

  const getTabCount = (artifacts: ArtifactNode[] | undefined) => {
    if (!artifacts) return 0
    return artifacts.reduce((count, node) => {
      if (node.type === "folder" && node.children) {
        return count + node.children.length
      }
      return count + 1
    }, 0)
  }

  const tabs = [
    { value: "requirements", label: "Requirements" },
    { value: "design", label: "Design" },
    { value: "development", label: "Development" },
    { value: "testing", label: "Testing" },
    { value: "deployment", label: "Deployment" },
    { value: "maintenance", label: "Maintenance" },
  ]

  return (
    <MainLayout>
      <div className="p-6">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-2xl font-bold text-foreground">Artifacts</h1>
            <p className="text-muted-foreground">Generated files and documentation from the SDLC process</p>
          </div>
          <Button size="sm">
            <Upload className="h-4 w-4 mr-2" />
            Upload Files
          </Button>
        </div>

        <Card className="mb-6">
          <CardHeader>
            <CardTitle>Artifact Generation Checklist</CardTitle>
            <p className="text-sm text-muted-foreground">
              Toggle which artifacts the agents should produce or skip. Critical artifacts cannot be skipped.
            </p>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {Object.entries(artifactChecklistData).map(([phase, items]) => (
                <div key={phase}>
                  <h4 className="font-semibold mb-2 capitalize">{phase}</h4>
                  <div className="space-y-2">
                    {items.map(item => (
                      <div key={item.id} className="flex items-center justify-between p-2 border rounded-md">
                        <Label htmlFor={item.id} className="flex-1 cursor-pointer">
                          {item.label} {item.critical && <span className="text-red-500">*</span>}
                        </Label>
                        <Switch
                          id={item.id}
                          checked={checklist[item.id]}
                          onCheckedChange={(isChecked) => handleChecklistChange(item.id, isChecked, item.critical)}
                          disabled={item.critical}
                        />
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-lg">Artifact Repository</CardTitle>
          </CardHeader>
          <CardContent>
            <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
              <TabsList className="grid w-full grid-cols-6">
                {tabs.map((tab) => (
                  <TabsTrigger key={tab.value} value={tab.value} className="gap-2">
                    {tab.label}
                    <Badge variant="secondary" className="ml-1">
                      {getTabCount(artifacts[tab.value])}
                    </Badge>
                  </TabsTrigger>
                ))}
              </TabsList>

              <div className="mt-6 min-h-[400px]">
                {tabs.map((tab) => (
                  <TabsContent key={tab.value} value={tab.value} className="mt-0">
                    <div className="space-y-2">
                      {(artifacts[tab.value] || []).map((node, index) => (
                        <FileTreeNode key={index} node={node} />
                      ))}
                    </div>
                  </TabsContent>
                ))}
              </div>
            </Tabs>
          </CardContent>
        </Card>
      </div>
    </MainLayout>
  )
}
