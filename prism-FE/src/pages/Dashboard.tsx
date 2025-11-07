import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from "recharts";
import { TrendingUp, Package, AlertCircle, CheckCircle, Upload, FileText, MessageSquare } from "lucide-react";
import { useNavigate } from "react-router-dom";

const forecastData = [
  { month: "Jan", forecast: 1200, actual: 1150 },
  { month: "Feb", forecast: 1350, actual: 1400 },
  { month: "Mar", forecast: 1500, actual: 1480 },
  { month: "Apr", forecast: 1650, actual: 1620 },
  { month: "May", forecast: 1800, actual: 1750 },
  { month: "Jun", forecast: 1900, actual: null },
];

const notifications = [
  { id: 1, message: "Material consumption up by 6% this quarter", type: "info" },
  { id: 2, message: "Steel rods expected to run out by May 26", type: "warning" },
  { id: 3, message: "Forecast accuracy improved to 94.2%", type: "success" },
];

const Dashboard = () => {
  const navigate = useNavigate();

  return (
    <div className="space-y-6">
      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">Current Stock Levels</CardTitle>
            <Package className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-foreground">87%</div>
            <p className="text-xs text-success mt-1">+2.5% from last month</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">Forecast Accuracy</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-foreground">94.2%</div>
            <p className="text-xs text-success mt-1">+1.8% improvement</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">Active Projects</CardTitle>
            <CheckCircle className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-foreground">12</div>
            <p className="text-xs text-muted-foreground mt-1">3 starting next month</p>
          </CardContent>
        </Card>
      </div>

      {/* Quick Actions */}
      <Card>
        <CardHeader>
          <CardTitle>Quick Actions</CardTitle>
        </CardHeader>
        <CardContent className="flex flex-wrap gap-3">
          <Button onClick={() => navigate("/upload")} className="gap-2">
            <Upload className="h-4 w-4" />
            Upload Data
          </Button>
          <Button onClick={() => navigate("/forecast")} variant="secondary" className="gap-2">
            <TrendingUp className="h-4 w-4" />
            Quick Forecast
          </Button>
          <Button onClick={() => navigate("/reports")} variant="secondary" className="gap-2">
            <FileText className="h-4 w-4" />
            View Reports
          </Button>
          <Button onClick={() => navigate("/assistant")} variant="secondary" className="gap-2">
            <MessageSquare className="h-4 w-4" />
            AI Assistant
          </Button>
        </CardContent>
      </Card>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Forecast Chart */}
        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle>Forecast vs Actual Demand</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={forecastData}>
                <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                <XAxis dataKey="month" stroke="hsl(var(--muted-foreground))" />
                <YAxis stroke="hsl(var(--muted-foreground))" />
                <Tooltip 
                  contentStyle={{ 
                    backgroundColor: "hsl(var(--card))",
                    border: "1px solid hsl(var(--border))",
                    borderRadius: "var(--radius)"
                  }}
                />
                <Legend />
                <Line
                  type="monotone"
                  dataKey="forecast"
                  stroke="hsl(var(--primary))"
                  strokeWidth={2}
                  dot={{ fill: "hsl(var(--primary))" }}
                />
                <Line
                  type="monotone"
                  dataKey="actual"
                  stroke="hsl(var(--success))"
                  strokeWidth={2}
                  dot={{ fill: "hsl(var(--success))" }}
                />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Notifications Panel */}
        <Card>
          <CardHeader>
            <CardTitle>Notifications</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {notifications.map((notification) => (
              <div key={notification.id} className="flex items-start space-x-3 p-3 rounded-lg bg-muted border border-border">
                {notification.type === "warning" && (
                  <AlertCircle className="h-5 w-5 text-warning flex-shrink-0 mt-0.5" />
                )}
                {notification.type === "success" && (
                  <CheckCircle className="h-5 w-5 text-success flex-shrink-0 mt-0.5" />
                )}
                {notification.type === "info" && (
                  <TrendingUp className="h-5 w-5 text-foreground flex-shrink-0 mt-0.5" />
                )}
                <p className="text-sm text-foreground">{notification.message}</p>
              </div>
            ))}
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Dashboard;
