"use client"

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from "recharts"
import { CheckCircle, Loader, PauseCircle, XCircle } from "lucide-react"

const mockStats = {
    totalTasks: 32,
    statusBreakdown: [
        { name: 'Done', value: 18, color: '#22c55e' },
        { name: 'In Progress', value: 5, color: '#3b82f6' },
        { name: 'Queued', value: 7, color: '#6b7280' },
        { name: 'Error', value: 2, color: '#ef4444' },
    ],
    performance: {
        avgTaskCompletion: '12.5m',
        successRate: '93.75%',
        tokensUsed: '1.2M'
    }
}

export function GlobalStatistics() {
  return (
    <Card>
        <CardHeader>
            <CardTitle>Global Statistics</CardTitle>
            <CardDescription>
                An overview of all tasks and system performance.
            </CardDescription>
        </CardHeader>
        <CardContent>
            <div className="grid md:grid-cols-2 gap-8">
                {/* Task Status Breakdown */}
                <div className="space-y-4">
                    <h3 className="text-lg font-semibold">Task Status</h3>
                    <div className="grid grid-cols-2 gap-4">
                        <Card>
                            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                                <CardTitle className="text-sm font-medium">Done</CardTitle>
                                <CheckCircle className="h-4 w-4 text-green-500" />
                            </CardHeader>
                            <CardContent>
                                <div className="text-2xl font-bold">{mockStats.statusBreakdown.find(s => s.name === 'Done')?.value}</div>
                            </CardContent>
                        </Card>
                         <Card>
                            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                                <CardTitle className="text-sm font-medium">In Progress</CardTitle>
                                <Loader className="h-4 w-4 text-blue-500 animate-spin" />
                            </CardHeader>
                            <CardContent>
                                <div className="text-2xl font-bold">{mockStats.statusBreakdown.find(s => s.name === 'In Progress')?.value}</div>
                            </CardContent>
                        </Card>
                         <Card>
                            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                                <CardTitle className="text-sm font-medium">Queued</CardTitle>
                                <PauseCircle className="h-4 w-4 text-gray-500" />
                            </CardHeader>
                            <CardContent>
                                <div className="text-2xl font-bold">{mockStats.statusBreakdown.find(s => s.name === 'Queued')?.value}</div>
                            </CardContent>
                        </Card>
                         <Card>
                            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                                <CardTitle className="text-sm font-medium">Error</CardTitle>
                                <XCircle className="h-4 w-4 text-red-500" />
                            </CardHeader>
                            <CardContent>
                                <div className="text-2xl font-bold">{mockStats.statusBreakdown.find(s => s.name === 'Error')?.value}</div>
                            </CardContent>
                        </Card>
                    </div>
                </div>
                {/* Pie Chart */}
                <div className="flex flex-col items-center">
                     <h3 className="text-lg font-semibold mb-4">Task Distribution</h3>
                    <div style={{ width: '100%', height: 200 }}>
                        <ResponsiveContainer>
                            <PieChart>
                                <Pie
                                    data={mockStats.statusBreakdown}
                                    cx="50%"
                                    cy="50%"
                                    labelLine={false}
                                    outerRadius={80}
                                    fill="#8884d8"
                                    dataKey="value"
                                >
                                    {mockStats.statusBreakdown.map((entry, index) => (
                                        <Cell key={`cell-${index}`} fill={entry.color} />
                                    ))}
                                </Pie>
                                <Tooltip />
                                <Legend />
                            </PieChart>
                        </ResponsiveContainer>
                    </div>
                </div>
            </div>
        </CardContent>
    </Card>
  )
}
