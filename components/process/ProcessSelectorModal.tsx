"use client"

import { useState, ChangeEvent } from "react"
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
  DialogFooter,
} from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Label } from "@/components/ui/label"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"

interface ProcessSelectorModalProps {
  isOpen: boolean;
  onOpenChange: (isOpen: boolean) => void;
  onStartProcess: (process: string | File) => void;
}

const predefinedProcesses = [
  { id: "sdlc", name: "Software Development Lifecycle" },
  { id: "marketing_campaign", name: "Marketing Campaign" },
  { id: "research_project", name: "Research Project" },
];

export function ProcessSelectorModal({ isOpen, onOpenChange, onStartProcess }: ProcessSelectorModalProps) {
  const [selectedProcess, setSelectedProcess] = useState<string | null>(null);
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);

  const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      setUploadedFile(event.target.files[0]);
      setSelectedProcess(null); // Clear dropdown selection if file is uploaded
    }
  };

  const handleStartProcess = () => {
    if (uploadedFile) {
      onStartProcess(uploadedFile);
    } else if (selectedProcess) {
      onStartProcess(selectedProcess);
    }
    onOpenChange(false); // Close modal after starting
  };

  const isStartButtonDisabled = !selectedProcess && !uploadedFile;

  return (
    <Dialog open={isOpen} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Start a New Process</DialogTitle>
          <DialogDescription>
            Select a predefined process template or upload your own YAML configuration file.
          </DialogDescription>
        </DialogHeader>
        <div className="grid gap-4 py-4">
          <div className="grid w-full items-center gap-1.5">
            <Label htmlFor="process-template">Select a Template</Label>
            <Select onValueChange={setSelectedProcess} value={selectedProcess || ""} disabled={!!uploadedFile}>
              <SelectTrigger id="process-template">
                <SelectValue placeholder="Choose a process..." />
              </SelectTrigger>
              <SelectContent>
                {predefinedProcesses.map((process) => (
                  <SelectItem key={process.id} value={process.id}>
                    {process.name}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
          <div className="flex items-center justify-center">
            <span className="text-sm text-muted-foreground">OR</span>
          </div>
          <div className="grid w-full max-w-sm items-center gap-1.5">
            <Label htmlFor="custom-process">Upload a Custom Process</Label>
            <Input id="custom-process" type="file" accept=".yaml,.yml" onChange={handleFileChange} />
          </div>
        </div>
        <DialogFooter>
          <Button variant="outline" onClick={() => onOpenChange(false)}>Cancel</Button>
          <Button onClick={handleStartProcess} disabled={isStartButtonDisabled}>
            Start Process
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
