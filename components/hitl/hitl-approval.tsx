import React from 'react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

interface HITLModifyDialogProps {
  onModify: (feedback: string) => void;
}

const HITLModifyDialog: React.FC<HITLModifyDialogProps> = ({ onModify }) => {
  const [feedback, setFeedback] = React.useState('');

  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button variant="outline">Modify</Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Modify and Respond</DialogTitle>
          <DialogDescription>
            Provide feedback or new instructions to the agent.
          </DialogDescription>
        </DialogHeader>
        <div className="grid gap-4 py-4">
          <div className="grid grid-cols-4 items-center gap-4">
            <Label htmlFor="feedback" className="text-right">
              Feedback
            </Label>
            <Input
              id="feedback"
              value={feedback}
              onChange={(e) => setFeedback(e.target.value)}
              className="col-span-3"
            />
          </div>
        </div>
        <DialogFooter>
          <Button type="submit" onClick={() => onModify(feedback)}>Send Feedback</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
};


interface HITLApprovalProps {
  agentName: string;
  decision: string;
  context: any;
  priority: 'low' | 'medium' | 'high' | 'urgent';
  onApprove: () => void;
  onReject: () => void;
  onModify: (feedback: string) => void;
}

export const HITLApprovalComponent: React.FC<HITLApprovalProps> = ({
  agentName,
  decision,
  context,
  priority,
  onApprove,
  onReject,
  onModify
}) => {
  return (
    <div className="border-l-4 border-amber-500 bg-amber-50 p-4 rounded-lg">
      <div className="flex items-center justify-between mb-3">
        <Badge variant="outline" className="bg-amber-100 text-amber-800">
          🤖 {agentName} Needs Approval
        </Badge>
        <Badge variant={priority === 'urgent' ? 'destructive' : 'secondary'}>
          {priority.toUpperCase()}
        </Badge>
      </div>

      <div className="mb-4">
        <h4 className="font-semibold mb-2">Decision Required:</h4>
        <p className="text-sm">{decision}</p>
        {context && (
          <details className="mt-2">
            <summary className="cursor-pointer text-sm text-muted-foreground">
              View Context
            </summary>
            <pre className="text-xs bg-muted p-2 rounded mt-2">
              {JSON.stringify(context, null, 2)}
            </pre>
          </details>
        )}
      </div>

      <div className="flex gap-2">
        <Button onClick={onApprove} className="bg-green-600 hover:bg-green-700">
          ✓ Approve
        </Button>
        <Button onClick={onReject} variant="destructive">
          ✗ Reject
        </Button>
        <HITLModifyDialog onModify={onModify} />
      </div>
    </div>
  );
};
