"use client"

import { useState } from "react"
import { MainLayout } from "@/components/main-layout"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Badge } from "@/components/ui/badge"
import { FileText, Code, Download, Upload, Folder, FolderOpen, ChevronRight, ChevronDown } from "lucide-react"

interface FileNode {
  name: string
  type: "file" | "folder"
  size?: string
  modified?: string
  children?: FileNode[]
  expanded?: boolean
}

const mockArtifacts = {
  requirements: [
    {
      name: "requirements/",
      type: "folder" as const,
      expanded: true,
      children: [
        { name: "product_requirements.md", type: "file" as const, size: "12.4 KB", modified: "2 hours ago" },
        { name: "technical_specs.md", type: "file" as const, size: "8.7 KB", modified: "3 hours ago" },
        { name: "user_stories.json", type: "file" as const, size: "5.2 KB", modified: "4 hours ago" },
      ],
    },
  ],
  design: [
    {
      name: "design/",
      type: "folder" as const,
      expanded: true,
      children: [
        { name: "wireframes.figma", type: "file" as const, size: "24.1 KB", modified: "1 hour ago" },
        { name: "ui_components.tsx", type: "file" as const, size: "15.3 KB", modified: "2 hours ago" },
        { name: "style_guide.css", type: "file" as const, size: "7.8 KB", modified: "3 hours ago" },
      ],
    },
  ],
  development: [
    {
      name: "source_code/",
      type: "folder" as const,
      expanded: true,
      children: [
        { name: "main.py", type: "file" as const, size: "18.5 KB", modified: "30 mins ago" },
        { name: "utils.py", type: "file" as const, size: "9.2 KB", modified: "45 mins ago" },
        { name: "config.json", type: "file" as const, size: "2.1 KB", modified: "1 hour ago" },
      ],
    },
    {
      name: "docs/",
      type: "folder" as const,
      expanded: false,
      children: [
        { name: "readme.md", type: "file" as const, size: "4.3 KB", modified: "2 hours ago" },
        { name: "api_docs.md", type: "file" as const, size: "11.7 KB", modified: "3 hours ago" },
      ],
    },
  ],
  testing: [
    {
      name: "tests/",
      type: "folder" as const,
      expanded: true,
      children: [
        { name: "test_main.py", type: "file" as const, size: "6.4 KB", modified: "1 hour ago" },
        { name: "test_utils.py", type: "file" as const, size: "4.1 KB", modified: "2 hours ago" },
        { name: "coverage_report.html", type: "file" as const, size: "45.2 KB", modified: "3 hours ago" },
      ],
    },
  ],
}

function FileTreeNode({ node, level = 0 }: { node: FileNode; level?: number }) {
  const [expanded, setExpanded] = useState(node.expanded || false)

  const handleToggle = () => {
    if (node.type === "folder") {
      setExpanded(!expanded)
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
            <span className="text-xs text-muted-foreground">{node.size}</span>
            <Button size="sm" variant="ghost" className="h-6 w-6 p-0">
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

export default function ArtifactsPage() {
  const [activeTab, setActiveTab] = useState("development")

  const getTabCount = (artifacts: FileNode[]) => {
    return artifacts.reduce((count, node) => {
      if (node.type === "folder" && node.children) {
        return count + node.children.length
      }
      return count + 1
    }, 0)
  }

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

        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-lg">Artifact Repository</CardTitle>
          </CardHeader>
          <CardContent>
            <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
              <TabsList className="grid w-full grid-cols-4">
                <TabsTrigger value="requirements" className="gap-2">
                  Requirements
                  <Badge variant="secondary" className="ml-1">
                    {getTabCount(mockArtifacts.requirements)}
                  </Badge>
                </TabsTrigger>
                <TabsTrigger value="design" className="gap-2">
                  Design
                  <Badge variant="secondary" className="ml-1">
                    {getTabCount(mockArtifacts.design)}
                  </Badge>
                </TabsTrigger>
                <TabsTrigger value="development" className="gap-2">
                  Development
                  <Badge variant="secondary" className="ml-1">
                    {getTabCount(mockArtifacts.development)}
                  </Badge>
                </TabsTrigger>
                <TabsTrigger value="testing" className="gap-2">
                  Testing
                  <Badge variant="secondary" className="ml-1">
                    {getTabCount(mockArtifacts.testing)}
                  </Badge>
                </TabsTrigger>
              </TabsList>

              <div className="mt-6 min-h-[400px]">
                <TabsContent value="requirements" className="mt-0">
                  <div className="space-y-2">
                    {mockArtifacts.requirements.map((node, index) => (
                      <FileTreeNode key={index} node={node} />
                    ))}
                  </div>
                </TabsContent>

                <TabsContent value="design" className="mt-0">
                  <div className="space-y-2">
                    {mockArtifacts.design.map((node, index) => (
                      <FileTreeNode key={index} node={node} />
                    ))}
                  </div>
                </TabsContent>

                <TabsContent value="development" className="mt-0">
                  <div className="space-y-2">
                    {mockArtifacts.development.map((node, index) => (
                      <FileTreeNode key={index} node={node} />
                    ))}
                  </div>
                </TabsContent>

                <TabsContent value="testing" className="mt-0">
                  <div className="space-y-2">
                    {mockArtifacts.testing.map((node, index) => (
                      <FileTreeNode key={index} node={node} />
                    ))}
                  </div>
                </TabsContent>
              </div>
            </Tabs>
          </CardContent>
        </Card>
      </div>
    </MainLayout>
  )
}
