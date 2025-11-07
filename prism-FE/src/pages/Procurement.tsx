import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Sheet, SheetContent, SheetHeader, SheetTitle, SheetTrigger } from "@/components/ui/sheet";
import { TrendingDown, Leaf, Menu, Filter, Calendar, DollarSign, Package, X } from "lucide-react";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";

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
  const [filterOpen, setFilterOpen] = useState(false);
  const [dateRange, setDateRange] = useState("all");
  const [supplierFilter, setSupplierFilter] = useState("all");
  const [statusFilter, setStatusFilter] = useState("all");

  return (
    <div className="space-y-6">
      {/* Header with Slide-in Menu Trigger */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-foreground">Procurement Planner</h1>
          <p className="text-muted-foreground mt-2">Optimized supplier recommendations and order schedule</p>
        </div>

        {/* Slide-in Menu Trigger */}
        <Sheet open={filterOpen} onOpenChange={setFilterOpen}>
          <SheetTrigger asChild>
            <Button variant="outline" className="gap-2">
              <Menu className="h-4 w-4" />
              Filters & Options
            </Button>
          </SheetTrigger>
          <SheetContent side="left" className="w-80 overflow-y-auto">
            <SheetHeader>
              <SheetTitle className="flex items-center gap-2">
                <Filter className="h-5 w-5" />
                Filters & Settings
              </SheetTitle>
            </SheetHeader>

            <div className="mt-6 space-y-6">
              {/* Date Range Filter */}
              <div className="space-y-2">
                <Label htmlFor="date-range" className="flex items-center gap-2">
                  <Calendar className="h-4 w-4" />
                  Date Range
                </Label>
                <Select value={dateRange} onValueChange={setDateRange}>
                  <SelectTrigger id="date-range">
                    <SelectValue placeholder="Select date range" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All Time</SelectItem>
                    <SelectItem value="today">Today</SelectItem>
                    <SelectItem value="week">This Week</SelectItem>
                    <SelectItem value="month">This Month</SelectItem>
                    <SelectItem value="quarter">This Quarter</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              {/* Supplier Filter */}
              <div className="space-y-2">
                <Label htmlFor="supplier" className="flex items-center gap-2">
                  <Package className="h-4 w-4" />
                  Supplier
                </Label>
                <Select value={supplierFilter} onValueChange={setSupplierFilter}>
                  <SelectTrigger id="supplier">
                    <SelectValue placeholder="Select supplier" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All Suppliers</SelectItem>
                    <SelectItem value="tata">Tata Steel</SelectItem>
                    <SelectItem value="ultratech">UltraTech</SelectItem>
                    <SelectItem value="hindalco">Hindalco</SelectItem>
                    <SelectItem value="aditya">Aditya Birla</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              {/* Status Filter */}
              <div className="space-y-2">
                <Label htmlFor="status" className="flex items-center gap-2">
                  <TrendingDown className="h-4 w-4" />
                  Status
                </Label>
                <Select value={statusFilter} onValueChange={setStatusFilter}>
                  <SelectTrigger id="status">
                    <SelectValue placeholder="Select status" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All Status</SelectItem>
                    <SelectItem value="best-price">Best Price</SelectItem>
                    <SelectItem value="standard">Standard</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              {/* Cost Range */}
              <div className="space-y-2">
                <Label htmlFor="cost-min" className="flex items-center gap-2">
                  <DollarSign className="h-4 w-4" />
                  Cost Range (₹ Lakhs)
                </Label>
                <div className="grid grid-cols-2 gap-2">
                  <Input id="cost-min" type="number" placeholder="Min" />
                  <Input id="cost-max" type="number" placeholder="Max" />
                </div>
              </div>

              {/* Action Buttons */}
              <div className="pt-4 space-y-2">
                <Button className="w-full" onClick={() => setFilterOpen(false)}>
                  Apply Filters
                </Button>
                <Button
                  variant="outline"
                  className="w-full"
                  onClick={() => {
                    setDateRange("all");
                    setSupplierFilter("all");
                    setStatusFilter("all");
                  }}
                >
                  Reset Filters
                </Button>
              </div>
            </div>
          </SheetContent>
        </Sheet>
      </div>

      {/* Key Insights - Removed "Optimized Routes" card */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
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
    </div>
  );
};

export default Procurement;
