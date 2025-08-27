"use client"

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Label } from "@/components/ui/label"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Switch } from "@/components/ui/switch"
import { Checkbox } from "@/components/ui/checkbox"
import { UploadCloud } from "lucide-react"

const mockArtifactsToGenerate = [
    { id: 'srs', label: 'System Requirements Specification' },
    { id: 'use_case', label: 'Use Case Diagrams' },
    { id: 'risk_analysis', label: 'Risk Analysis Report' },
]

export function StageConfig() {
  return (
    <Card>
        <CardHeader>
            <CardTitle>Stage Configuration</CardTitle>
            <CardDescription>
                Customize the settings and agent behavior for this stage.
            </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
            {/* Agent Role Configuration */}
            <div className="space-y-2">
                <Label htmlFor="agent-role" className="text-base">Agent Role Configuration</Label>
                <p className="text-sm text-muted-foreground">Upload a .md file to define the agent's role, goals, and constraints for this stage.</p>
                <div className="flex w-full max-w-sm items-center space-x-2">
                    <Input id="agent-role" type="file" accept=".md" />
                    <Button type="submit">
                        <UploadCloud className="w-4 h-4 mr-2" />
                        Upload
                    </Button>
                </div>
            </div>

            {/* Artifact Selection */}
            <div className="space-y-2">
                <Label className="text-base">Artifact Generation</Label>
                <p className="text-sm text-muted-foreground">Select which artifacts should be generated in this stage.</p>
                <div className="space-y-2 pt-2">
                    {mockArtifactsToGenerate.map(artifact => (
                        <div key={artifact.id} className="flex items-center space-x-2">
                            <Checkbox id={artifact.id} defaultChecked />
                            <label
                                htmlFor={artifact.id}
                                className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                            >
                                {artifact.label}
                            </label>
                        </div>
                    ))}
                </div>
            </div>

            {/* Stage-specific settings */}
            <div className="space-y-2">
                <Label className="text-base">Stage Settings</Label>
                 <p className="text-sm text-muted-foreground">Enable or disable specific behaviors for this stage.</p>
                <div className="flex items-center space-x-2 pt-2">
                    <Switch id="auto-approve" />
                    <Label htmlFor="auto-approve">Auto-approve all tasks in this stage</Label>
                </div>
                 <div className="flex items-center space-x-2 pt-2">
                    <Switch id="strict-mode" defaultChecked />
                    <Label htmlFor="strict-mode">Enable strict mode (agent must follow instructions precisely)</Label>
                </div>
            </div>

             <div className="pt-4 flex justify-end">
                <Button>Save Configuration</Button>
            </div>
        </CardContent>
    </Card>
  )
}
