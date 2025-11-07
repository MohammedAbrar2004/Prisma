import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from "recharts";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { AlertCircle, TrendingUp, Package } from "lucide-react";
import { Progress } from "@/components/ui/progress";

const stockData = [
  { material: "Steel Rods", current: 450, forecasted: 650 },
  { material: "Cement", current: 1200, forecasted: 1400 },
  { material: "Copper Wire", current: 280, forecasted: 350 },
  { material: "Insulators", current: 650, forecasted: 800 },
  { material: "Transformers", current: 8, forecasted: 12 },
];

const alerts = [
  {
    material: "Steel Rods (TMT)",
    status: "Low Stock",
    currentQty: 450,
    required: 650,
    reorderDate: "May 26, 2025",
    severity: "high",
  },
  {
    material: "Transformers",
    status: "Critical",
    currentQty: 8,
    required: 12,
    reorderDate: "May 20, 2025",
    severity: "critical",
  },
  {
    material: "Copper Wire",
    status: "Monitor",
    currentQty: 280,
    required: 350,
    reorderDate: "Jun 5, 2025",
    severity: "medium",
  },
];

const Inventory = () => {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-foreground">Inventory Management</h1>
        <p className="text-muted-foreground mt-2">Real-time stock levels and reorder recommendations</p>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">Items in Stock</CardTitle>
            <Package className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-foreground">2,588</div>
            <p className="text-xs text-muted-foreground mt-1">Across 5 material types</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">Low Stock Alerts</CardTitle>
            <AlertCircle className="h-4 w-4 text-warning" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-foreground">3</div>
            <p className="text-xs text-warning mt-1">Requires immediate attention</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">Stock Utilization</CardTitle>
            <TrendingUp className="h-4 w-4 text-success" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-foreground">78%</div>
            <Progress value={78} className="mt-2" />
          </CardContent>
        </Card>
      </div>

      {/* Stock vs Forecasted Chart */}
      <Card>
        <CardHeader>
          <CardTitle>Current Stock vs Forecasted Usage</CardTitle>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={stockData}>
              <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
              <XAxis dataKey="material" stroke="hsl(var(--muted-foreground))" />
              <YAxis stroke="hsl(var(--muted-foreground))" />
              <Tooltip
                contentStyle={{
                  backgroundColor: "hsl(var(--card))",
                  border: "1px solid hsl(var(--border))",
                  borderRadius: "var(--radius)"
                }}
              />
              <Legend />
              <Bar dataKey="current" fill="hsl(var(--primary))" name="Current Stock" />
              <Bar dataKey="forecasted" fill="hsl(var(--chart-3))" name="Forecasted Need" />
            </BarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      {/* Reorder Alerts Table */}
      <Card>
        <CardHeader>
          <CardTitle>Reorder Recommendations</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Material</TableHead>
                <TableHead>Status</TableHead>
                <TableHead className="text-right">Current Qty</TableHead>
                <TableHead className="text-right">Required</TableHead>
                <TableHead>Reorder By</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {alerts.map((alert, index) => (
                <TableRow key={index}>
                  <TableCell className="font-medium">{alert.material}</TableCell>
                  <TableCell>
                    <Badge
                      variant={
                        alert.severity === "critical"
                          ? "destructive"
                          : alert.severity === "high"
                          ? "default"
                          : "secondary"
                      }
                      className="gap-1"
                    >
                      {alert.severity === "critical" || alert.severity === "high" ? (
                        <AlertCircle className="h-3 w-3" />
                      ) : null}
                      {alert.status}
                    </Badge>
                  </TableCell>
                  <TableCell className="text-right">{alert.currentQty}</TableCell>
                  <TableCell className="text-right">{alert.required}</TableCell>
                  <TableCell className="font-medium text-foreground">{alert.reorderDate}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  );
};

export default Inventory;
