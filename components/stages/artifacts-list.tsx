"use client"

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { FileText, Download, Share2 } from "lucide-react"
import type { Artifact } from "@/lib/types"

const mockArtifacts: Artifact[] = [
  { id: 'art-001', name: 'Project Plan v1.2.docx', type: 'document', status: 'done', lastModified: '2025-08-26 10:00' },
  { id: 'art-002', name: 'SRS Document v1.0.pdf', type: 'document', status: 'done', lastModified: '2025-08-26 14:30' },
  { id: 'art-003', name: 'Use Case Diagrams.png', type: 'image', status: 'wip', lastModified: '2025-08-27 09:15' },
  { id: 'art-004', name: 'Risk Analysis.xlsx', type: 'spreadsheet', status: 'queued', lastModified: '2025-08-27 11:00' },
]

export function ArtifactsList({ artifacts = mockArtifacts }: { artifacts?: Artifact[] }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Artifacts</CardTitle>
        <CardDescription>
            A list of all artifacts generated in this stage.
        </CardDescription>
      </CardHeader>
      <CardContent>
        {artifacts && artifacts.length > 0 ? (
            <Table>
            <TableHeader>
                <TableRow>
                <TableHead>Name</TableHead>
                <TableHead>Type</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Last Modified</TableHead>
                <TableHead className="text-right">Actions</TableHead>
                </TableRow>
            </TableHeader>
            <TableBody>
                {artifacts.map((artifact) => (
                <TableRow key={artifact.id}>
                    <TableCell className="font-medium flex items-center gap-2">
                        <FileText className="w-4 h-4" />
                        {artifact.name}
                    </TableCell>
                    <TableCell>{artifact.type}</TableCell>
                    <TableCell>
                        <Badge variant={artifact.status === 'done' ? 'default' : 'outline'}>
                            {artifact.status}
                        </Badge>
                    </TableCell>
                    <TableCell>{artifact.lastModified}</TableCell>
                    <TableCell className="text-right">
                        <Button variant="ghost" size="icon">
                            <Download className="h-4 w-4" />
                        </Button>
                        <Button variant="ghost" size="icon">
                            <Share2 className="h-4 w-4" />
                        </Button>
                    </TableCell>
                </TableRow>
                ))}
            </TableBody>
            </Table>
        ) : (
            <div className="text-center text-muted-foreground py-8">
                <p>No artifacts for this stage yet.</p>
            </div>
        )}
      </CardContent>
    </Card>
  )
}
