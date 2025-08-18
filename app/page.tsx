import { MainLayout } from "@/components/main-layout"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Zap, Settings } from "lucide-react"

export default function HomePage() {
  return (
    <MainLayout>
      <div className="p-6">
        {/* Page Header */}
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-2xl font-bold text-foreground">Dashboard</h1>
            <p className="text-muted-foreground">Monitor your AI agent orchestration system</p>
          </div>
          <Button variant="outline" size="sm">
            <Settings className="w-4 h-4 mr-2" />
            Settings
          </Button>
        </div>

        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {/* Welcome Card */}
          <Card className="md:col-span-2 lg:col-span-3">
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Zap className="w-5 h-5 text-primary" />
                <span>Welcome to BotArmy</span>
              </CardTitle>
              <CardDescription>Multi-agent AI orchestration system for autonomous product generation</CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground mb-4">
                BotArmy orchestrates 6 specialized AI agents through the Software Development Life Cycle (SDLC) to
                automatically generate functional web product POCs. Monitor agent status, track tasks, and manage the
                entire development workflow from this dashboard.
              </p>
              <div className="flex space-x-3">
                <Button className="bg-primary hover:bg-primary/90">Start New Project</Button>
                <Button variant="outline">View Documentation</Button>
              </div>
            </CardContent>
          </Card>

          {/* Agent Status Cards */}
          {[
            { name: "Analyst", status: "Active", description: "Requirements analysis" },
            { name: "Architect", status: "Idle", description: "System design" },
            { name: "Developer", status: "Active", description: "Code generation" },
            { name: "Tester", status: "Idle", description: "Quality assurance" },
            { name: "Deployer", status: "Idle", description: "Deployment management" },
            { name: "Monitor", status: "Active", description: "System monitoring" },
          ].map((agent) => (
            <Card key={agent.name}>
              <CardHeader className="pb-3">
                <div className="flex items-center justify-between">
                  <CardTitle className="text-base">{agent.name}</CardTitle>
                  <Badge
                    variant={agent.status === "Active" ? "default" : "secondary"}
                    className={agent.status === "Active" ? "bg-primary" : ""}
                  >
                    {agent.status}
                  </Badge>
                </div>
                <CardDescription>{agent.description}</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="flex items-center space-x-2 text-sm text-muted-foreground">
                  <div className={`w-2 h-2 rounded-full ${agent.status === "Active" ? "bg-primary" : "bg-muted"}`} />
                  <span>{agent.status === "Active" ? "Processing tasks" : "Waiting for tasks"}</span>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </MainLayout>
  )
}
