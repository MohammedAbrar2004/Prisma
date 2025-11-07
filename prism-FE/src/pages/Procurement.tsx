import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { TrendingDown, Leaf, MapPin } from "lucide-react";

const procurementData = [
  {
    material: "Steel Rods (TMT)",
    supplier: "Tata Steel",
    orderDate: "Jun 15, 2025",
    cost: "₹45 L",
    co2: 120,
    savings: true,
  },
  {
    material: "Cement (Grade 53)",
    supplier: "UltraTech",
    orderDate: "Jun 10, 2025",
    cost: "₹32 L",
    co2: 85,
    savings: false,
  },
  {
    material: "Copper Wire",
    supplier: "Hindalco",
    orderDate: "Jul 5, 2025",
    cost: "₹28 L",
    co2: 65,
    savings: true,
  },
  {
    material: "Insulators",
    supplier: "Aditya Birla",
    orderDate: "Jul 12, 2025",
    cost: "₹18 L",
    co2: 45,
    savings: false,
  },
];

const Procurement = () => {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-foreground">Procurement Planner</h1>
        <p className="text-muted-foreground mt-2">Optimized supplier recommendations and order schedule</p>
      </div>

      {/* Key Insights */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">Total Cost Savings</CardTitle>
            <TrendingDown className="h-4 w-4 text-success" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-foreground">₹8.5 L</div>
            <p className="text-xs text-success mt-1">12% below market average</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">CO₂ Reduction</CardTitle>
            <Leaf className="h-4 w-4 text-success" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-foreground">315 tons</div>
            <p className="text-xs text-success mt-1">18% lower emissions</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">Optimized Routes</CardTitle>
            <MapPin className="h-4 w-4 text-primary" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-foreground">4</div>
            <p className="text-xs text-muted-foreground mt-1">Consolidated deliveries</p>
          </CardContent>
        </Card>
      </div>

      {/* Procurement Table */}
      <Card>
        <CardHeader>
          <CardTitle>Recommended Procurement Schedule</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Material</TableHead>
                <TableHead>Supplier</TableHead>
                <TableHead>Order Date</TableHead>
                <TableHead className="text-right">Cost</TableHead>
                <TableHead className="text-right">CO₂ (tons)</TableHead>
                <TableHead>Status</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {procurementData.map((row, index) => (
                <TableRow key={index}>
                  <TableCell className="font-medium">{row.material}</TableCell>
                  <TableCell>{row.supplier}</TableCell>
                  <TableCell>{row.orderDate}</TableCell>
                  <TableCell className="text-right font-medium">{row.cost}</TableCell>
                  <TableCell className="text-right">{row.co2}</TableCell>
                  <TableCell>
                    {row.savings ? (
                      <Badge className="gap-1">
                        <TrendingDown className="h-3 w-3" />
                        Best price
                      </Badge>
                    ) : (
                      <Badge variant="secondary">Standard</Badge>
                    )}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
          <div className="mt-4 flex justify-end gap-3">
            <Button variant="secondary">Export Schedule</Button>
            <Button>Approve Orders</Button>
          </div>
        </CardContent>
      </Card>

      {/* Route Visualization Placeholder */}
      <Card>
        <CardHeader>
          <CardTitle>Delivery Route Optimization</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="h-64 bg-muted rounded-lg flex items-center justify-center">
            <div className="text-center space-y-2">
              <MapPin className="h-12 w-12 text-muted-foreground mx-auto" />
              <p className="text-muted-foreground">Route map visualization</p>
              <p className="text-sm text-muted-foreground">Optimized for cost and emissions</p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default Procurement;
