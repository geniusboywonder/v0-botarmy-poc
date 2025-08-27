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

// Removed the mockArtifacts constant. The component will now rely on the artifacts prop.

export function ArtifactsList({ artifacts = [] }: { artifacts?: Artifact[] }) {
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
