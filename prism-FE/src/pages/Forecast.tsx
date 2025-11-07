import { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Area, AreaChart, Legend, Line, ComposedChart, Bar } from "recharts";
import {
  Download,
  FileText,
  TrendingUp,
  Sparkles,
  CheckCircle2,
  AlertCircle,
  Clock,
  Zap,
  BarChart3,
  Package,
  ArrowUpRight,
  ArrowDownRight,
  Minus,
  Filter,
  RefreshCw,
  ChevronDown,
  Calendar,
  Search,
  MoreVertical,
  Grid3x3,
  List,
  ChevronLeft,
  ChevronRight,
  ArrowUpDown,
  Home,
  Activity,
  DollarSign,
  Percent,
  X,
  Maximize2,
  Minimize2,
  Eye,
  Settings,
  Layers,
  Target,
  Info,
  ChevronUp,
  PanelLeftClose,
  PanelLeftOpen
} from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { toast } from "@/components/ui/sonner";
import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator,
} from "@/components/ui/breadcrumb";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Input } from "@/components/ui/input";
import { Separator } from "@/components/ui/separator";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Skeleton } from "@/components/ui/skeleton";
import { ToggleGroup, ToggleGroupItem } from "@/components/ui/toggle-group";

// Enhanced data with comparison and trends
const demandData = [
  { month: "Jun", forecast: 1900, actual: 1850, lastYear: 1650 },
  { month: "Jul", forecast: 2100, actual: 2050, lastYear: 1800 },
  { month: "Aug", forecast: 2300, actual: null, lastYear: 1950 },
  { month: "Sep", forecast: 2200, actual: null, lastYear: 2100 },
  { month: "Oct", forecast: 2400, actual: null, lastYear: 2200 },
  { month: "Nov", forecast: 2600, actual: null, lastYear: 2350 },
];

// Expanded forecast table with more enterprise data
const forecastTableData = [
  {
    id: 1,
    material: "Steel Rods (TMT)",
    category: "Structural",
    month: "Jun 2025",
    demand: 450,
    unit: "MT",
    confidence: 92,
    value: 2250000,
    supplier: "Tata Steel",
    leadTime: 14,
    status: "high-priority",
    note: "High priority"
  },
  {
    id: 2,
    material: "Cement (Grade 53)",
    category: "Construction",
    month: "Jun 2025",
    demand: 1200,
    unit: "MT",
    confidence: 94,
    value: 4800000,
    supplier: "UltraTech",
    leadTime: 7,
    status: "normal",
    note: ""
  },
  {
    id: 3,
    material: "Copper Wire",
    category: "Electrical",
    month: "Jul 2025",
    demand: 350,
    unit: "KM",
    confidence: 88,
    value: 1750000,
    supplier: "Hindalco",
    leadTime: 21,
    status: "risk",
    note: "Supplier delay risk"
  },
  {
    id: 4,
    material: "Insulators",
    category: "Electrical",
    month: "Jul 2025",
    demand: 800,
    unit: "Units",
    confidence: 91,
    value: 1600000,
    supplier: "NGK Insulators",
    leadTime: 10,
    status: "normal",
    note: ""
  },
  {
    id: 5,
    material: "Transformers",
    category: "Equipment",
    month: "Aug 2025",
    demand: 12,
    unit: "Units",
    confidence: 85,
    value: 3600000,
    supplier: "ABB India",
    leadTime: 45,
    status: "long-lead",
    note: "Long lead time"
  },
  {
    id: 6,
    material: "Circuit Breakers",
    category: "Equipment",
    month: "Aug 2025",
    demand: 85,
    unit: "Units",
    confidence: 90,
    value: 2550000,
    supplier: "Siemens",
    leadTime: 28,
    status: "normal",
    note: ""
  },
  {
    id: 7,
    material: "Aluminum Conductors",
    category: "Electrical",
    month: "Sep 2025",
    demand: 520,
    unit: "KM",
    confidence: 89,
    value: 2080000,
    supplier: "Vedanta",
    leadTime: 18,
    status: "normal",
    note: ""
  },
  {
    id: 8,
    material: "Concrete Poles",
    category: "Structural",
    month: "Sep 2025",
    demand: 340,
    unit: "Units",
    confidence: 93,
    value: 1700000,
    supplier: "L&T Construction",
    leadTime: 12,
    status: "normal",
    note: ""
  },
];

const Forecast = () => {
  const [animateIn, setAnimateIn] = useState(false);
  const [isExporting, setIsExporting] = useState(false);
  const [chartAnimated, setChartAnimated] = useState(false);
  const [viewMode, setViewMode] = useState<"table" | "cards">("table");
  const [dateRange, setDateRange] = useState("6months");
  const [categoryFilter, setCategoryFilter] = useState("all");
  const [searchQuery, setSearchQuery] = useState("");
  const [sortColumn, setSortColumn] = useState<string | null>(null);
  const [sortDirection, setSortDirection] = useState<"asc" | "desc">("asc");
  const [currentPage, setCurrentPage] = useState(1);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const itemsPerPage = 5;

  useEffect(() => {
    const timer = setTimeout(() => setAnimateIn(true), 100);
    const chartTimer = setTimeout(() => setChartAnimated(true), 500);
    return () => {
      clearTimeout(timer);
      clearTimeout(chartTimer);
    };
  }, []);

  const handleExport = (type: 'csv' | 'pdf' | 'excel') => {
    setIsExporting(true);
    setTimeout(() => {
      setIsExporting(false);
      toast.success(`Export successful!`, {
        description: `Your ${type.toUpperCase()} file is ready to download`,
      });
    }, 1500);
  };

  const handleRefresh = () => {
    setIsRefreshing(true);
    setTimeout(() => {
      setIsRefreshing(false);
      toast.success("Data refreshed", {
        description: `Updated at ${new Date().toLocaleTimeString()}`,
      });
    }, 1000);
  };

  // Filter and sort data
  const filteredData = forecastTableData
    .filter(item => {
      const matchesCategory = categoryFilter === "all" || item.category === categoryFilter;
      const matchesSearch = searchQuery === "" ||
        item.material.toLowerCase().includes(searchQuery.toLowerCase()) ||
        item.supplier.toLowerCase().includes(searchQuery.toLowerCase());
      return matchesCategory && matchesSearch;
    })
    .sort((a, b) => {
      if (!sortColumn) return 0;
      const aVal = a[sortColumn as keyof typeof a];
      const bVal = b[sortColumn as keyof typeof b];
      const modifier = sortDirection === "asc" ? 1 : -1;
      return aVal > bVal ? modifier : -modifier;
    });

  const totalPages = Math.ceil(filteredData.length / itemsPerPage);
  const paginatedData = filteredData.slice(
    (currentPage - 1) * itemsPerPage,
    currentPage * itemsPerPage
  );

  const handleSort = (column: string) => {
    if (sortColumn === column) {
      setSortDirection(sortDirection === "asc" ? "desc" : "asc");
    } else {
      setSortColumn(column);
      setSortDirection("asc");
    }
  };

  // Calculate KPIs
  const totalValue = forecastTableData.reduce((sum, item) => sum + item.value, 0);
  const avgConfidence = Math.round(
    forecastTableData.reduce((sum, item) => sum + item.confidence, 0) / forecastTableData.length
  );
  const highPriorityCount = forecastTableData.filter(item => item.status === "high-priority").length;
  const riskCount = forecastTableData.filter(item => item.status === "risk").length;

  return (
    <div className="min-h-screen bg-background">
      {/* Enterprise Sticky Toolbar */}
      <div className="sticky top-0 z-40 bg-card border-b border-border shadow-sm">
        <div className="max-w-[1600px] mx-auto px-6 lg:px-8">
          {/* Breadcrumbs */}
          <div className="py-3 border-b border-border/50">
            <Breadcrumb>
              <BreadcrumbList>
                <BreadcrumbItem>
                  <BreadcrumbLink href="/dashboard" className="flex items-center gap-1.5 text-sm">
                    <Home className="h-3.5 w-3.5" />
                    Dashboard
                  </BreadcrumbLink>
                </BreadcrumbItem>
                <BreadcrumbSeparator />
                <BreadcrumbItem>
                  <BreadcrumbLink href="/forecast" className="text-sm">Analytics</BreadcrumbLink>
                </BreadcrumbItem>
                <BreadcrumbSeparator />
                <BreadcrumbItem>
                  <BreadcrumbPage className="text-sm font-medium">Demand Forecast</BreadcrumbPage>
                </BreadcrumbItem>
              </BreadcrumbList>
            </Breadcrumb>
          </div>

          {/* Toolbar Actions */}
          <div className="py-4 flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-3">
                <div className="h-10 w-10 rounded-lg bg-primary/10 flex items-center justify-center">
                  <BarChart3 className="h-5 w-5 text-primary" />
                </div>
                <div>
                  <h1 className="text-xl font-semibold text-foreground">Demand Forecast</h1>
                  <p className="text-xs text-muted-foreground">
                    Last updated: {new Date().toLocaleTimeString()} • {filteredData.length} materials
                  </p>
                </div>
              </div>
            </div>

            <div className="flex flex-wrap items-center gap-3">
              {/* Date Range Selector */}
              <Select value={dateRange} onValueChange={setDateRange}>
                <SelectTrigger className="w-[140px] h-9 text-sm">
                  <Calendar className="h-4 w-4 mr-2" />
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="3months">3 Months</SelectItem>
                  <SelectItem value="6months">6 Months</SelectItem>
                  <SelectItem value="12months">12 Months</SelectItem>
                  <SelectItem value="custom">Custom Range</SelectItem>
                </SelectContent>
              </Select>

              {/* Category Filter */}
              <Select value={categoryFilter} onValueChange={setCategoryFilter}>
                <SelectTrigger className="w-[140px] h-9 text-sm">
                  <Filter className="h-4 w-4 mr-2" />
                  <SelectValue placeholder="Category" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Categories</SelectItem>
                  <SelectItem value="Structural">Structural</SelectItem>
                  <SelectItem value="Electrical">Electrical</SelectItem>
                  <SelectItem value="Equipment">Equipment</SelectItem>
                  <SelectItem value="Construction">Construction</SelectItem>
                </SelectContent>
              </Select>

              {/* Refresh Button */}
              <Button
                variant="outline"
                size="sm"
                className="h-9 gap-2"
                onClick={handleRefresh}
                disabled={isRefreshing}
              >
                <RefreshCw className={`h-4 w-4 ${isRefreshing ? 'animate-spin' : ''}`} />
                Refresh
              </Button>

              {/* Export Dropdown */}
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="outline" size="sm" className="h-9 gap-2">
                    <Download className="h-4 w-4" />
                    Export
                    <ChevronDown className="h-3.5 w-3.5" />
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end" className="w-48">
                  <DropdownMenuLabel>Export Format</DropdownMenuLabel>
                  <DropdownMenuSeparator />
                  <DropdownMenuItem onClick={() => handleExport('csv')}>
                    <FileText className="h-4 w-4 mr-2" />
                    Export as CSV
                  </DropdownMenuItem>
                  <DropdownMenuItem onClick={() => handleExport('excel')}>
                    <FileText className="h-4 w-4 mr-2" />
                    Export as Excel
                  </DropdownMenuItem>
                  <DropdownMenuItem onClick={() => handleExport('pdf')}>
                    <Download className="h-4 w-4 mr-2" />
                    Export as PDF
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>

              {/* More Actions */}
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="ghost" size="sm" className="h-9 w-9 p-0">
                    <MoreVertical className="h-4 w-4" />
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end">
                  <DropdownMenuItem>
                    <Activity className="h-4 w-4 mr-2" />
                    View Analytics
                  </DropdownMenuItem>
                  <DropdownMenuItem>
                    <Sparkles className="h-4 w-4 mr-2" />
                    Refine Forecast
                  </DropdownMenuItem>
                  <DropdownMenuSeparator />
                  <DropdownMenuItem>
                    <AlertCircle className="h-4 w-4 mr-2" />
                    Report Issue
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content Area with Max Width */}
      <div className="max-w-[1600px] mx-auto px-6 lg:px-8 py-8 space-y-8">

        {/* KPI Metrics Bar */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <Card className="border-l-4 border-l-primary">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div className="space-y-1">
                  <p className="text-sm font-medium text-muted-foreground">Total Forecast Value</p>
                  <p className="text-2xl font-bold text-foreground">
                    ₹{(totalValue / 1000000).toFixed(1)}M
                  </p>
                  <p className="text-xs text-green-600 dark:text-green-400 flex items-center gap-1">
                    <ArrowUpRight className="h-3 w-3" />
                    +12.5% vs last period
                  </p>
                </div>
                <div className="h-12 w-12 rounded-full bg-primary/10 flex items-center justify-center">
                  <DollarSign className="h-6 w-6 text-primary" />
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="border-l-4 border-l-green-500">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div className="space-y-1">
                  <p className="text-sm font-medium text-muted-foreground">Avg. Confidence</p>
                  <p className="text-2xl font-bold text-foreground">{avgConfidence}%</p>
                  <p className="text-xs text-muted-foreground">Across all materials</p>
                </div>
                <div className="h-12 w-12 rounded-full bg-green-500/10 flex items-center justify-center">
                  <Percent className="h-6 w-6 text-green-600 dark:text-green-400" />
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="border-l-4 border-l-orange-500">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div className="space-y-1">
                  <p className="text-sm font-medium text-muted-foreground">High Priority</p>
                  <p className="text-2xl font-bold text-foreground">{highPriorityCount}</p>
                  <p className="text-xs text-muted-foreground">Requires attention</p>
                </div>
                <div className="h-12 w-12 rounded-full bg-orange-500/10 flex items-center justify-center">
                  <AlertCircle className="h-6 w-6 text-orange-600 dark:text-orange-400" />
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="border-l-4 border-l-yellow-500">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div className="space-y-1">
                  <p className="text-sm font-medium text-muted-foreground">At Risk</p>
                  <p className="text-2xl font-bold text-foreground">{riskCount}</p>
                  <p className="text-xs text-muted-foreground">Potential delays</p>
                </div>
                <div className="h-12 w-12 rounded-full bg-yellow-500/10 flex items-center justify-center">
                  <Clock className="h-6 w-6 text-yellow-600 dark:text-yellow-400" />
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Chart Section with Tabs */}
        <Tabs defaultValue="trend" className="space-y-4">
          <div className="flex items-center justify-between">
            <TabsList>
              <TabsTrigger value="trend" className="gap-2">
                <TrendingUp className="h-4 w-4" />
                Trend Analysis
              </TabsTrigger>
              <TabsTrigger value="comparison" className="gap-2">
                <BarChart3 className="h-4 w-4" />
                Comparison View
              </TabsTrigger>
            </TabsList>
          </div>

          <TabsContent value="trend" className="space-y-4">
            <Card>
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div>
                    <CardTitle className="text-lg font-semibold">Demand Forecast Trend</CardTitle>
                    <p className="text-sm text-muted-foreground mt-1">
                      6-month projection with historical comparison
                    </p>
                  </div>
                  <Badge variant="outline" className="gap-1">
                    <TrendingUp className="h-3 w-3 text-green-500" />
                    +18% growth
                  </Badge>
                </div>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={400}>
                  <ComposedChart data={demandData}>
                    <defs>
                      <linearGradient id="forecastGradient" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="hsl(var(--primary))" stopOpacity={0.3}/>
                        <stop offset="95%" stopColor="hsl(var(--primary))" stopOpacity={0}/>
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" opacity={0.3} vertical={false} />
                    <XAxis
                      dataKey="month"
                      stroke="hsl(var(--muted-foreground))"
                      style={{ fontSize: '12px', fontWeight: 500 }}
                      axisLine={{ stroke: 'hsl(var(--border))' }}
                      tickLine={{ stroke: 'hsl(var(--border))' }}
                    />
                    <YAxis
                      stroke="hsl(var(--muted-foreground))"
                      style={{ fontSize: '12px', fontWeight: 500 }}
                      axisLine={{ stroke: 'hsl(var(--border))' }}
                      tickLine={{ stroke: 'hsl(var(--border))' }}
                      label={{ value: 'Units', angle: -90, position: 'insideLeft', style: { fontSize: '12px', fill: 'hsl(var(--muted-foreground))' } }}
                    />
                    <Tooltip
                      contentStyle={{
                        backgroundColor: "hsl(var(--card))",
                        border: "1px solid hsl(var(--border))",
                        borderRadius: "8px",
                        boxShadow: "0 4px 12px rgba(0,0,0,0.1)",
                        padding: "12px"
                      }}
                      labelStyle={{ fontWeight: 600, marginBottom: '8px', fontSize: '14px' }}
                    />
                    <Legend
                      wrapperStyle={{ paddingTop: '20px' }}
                      iconType="circle"
                    />
                    <Area
                      type="monotone"
                      dataKey="forecast"
                      stroke="hsl(var(--primary))"
                      strokeWidth={2.5}
                      fill="url(#forecastGradient)"
                      name="Forecast"
                      animationDuration={1500}
                    />
                    <Line
                      type="monotone"
                      dataKey="actual"
                      stroke="hsl(142 50% 45%)"
                      strokeWidth={2.5}
                      name="Actual"
                      dot={{ fill: "hsl(142 50% 45%)", r: 4 }}
                      connectNulls={false}
                    />
                    <Line
                      type="monotone"
                      dataKey="lastYear"
                      stroke="hsl(var(--muted-foreground))"
                      strokeWidth={2}
                      strokeDasharray="5 5"
                      name="Last Year"
                      dot={false}
                    />
                  </ComposedChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="comparison" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle className="text-lg font-semibold">Year-over-Year Comparison</CardTitle>
                <p className="text-sm text-muted-foreground mt-1">
                  Current forecast vs. last year actual demand
                </p>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={400}>
                  <ComposedChart data={demandData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" opacity={0.3} vertical={false} />
                    <XAxis
                      dataKey="month"
                      stroke="hsl(var(--muted-foreground))"
                      style={{ fontSize: '12px', fontWeight: 500 }}
                    />
                    <YAxis
                      stroke="hsl(var(--muted-foreground))"
                      style={{ fontSize: '12px', fontWeight: 500 }}
                      label={{ value: 'Units', angle: -90, position: 'insideLeft', style: { fontSize: '12px' } }}
                    />
                    <Tooltip
                      contentStyle={{
                        backgroundColor: "hsl(var(--card))",
                        border: "1px solid hsl(var(--border))",
                        borderRadius: "8px",
                        boxShadow: "0 4px 12px rgba(0,0,0,0.1)"
                      }}
                    />
                    <Legend />
                    <Bar dataKey="forecast" fill="hsl(var(--primary))" name="2025 Forecast" radius={[4, 4, 0, 0]} />
                    <Bar dataKey="lastYear" fill="hsl(var(--muted-foreground))" name="2024 Actual" radius={[4, 4, 0, 0]} opacity={0.6} />
                  </ComposedChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>

        {/* Data Table Section */}
        <Card>
          <CardHeader>
            <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
              <div>
                <CardTitle className="text-lg font-semibold">Material Forecast Details</CardTitle>
                <p className="text-sm text-muted-foreground mt-1">
                  Comprehensive breakdown of all forecasted materials
                </p>
              </div>

              <div className="flex items-center gap-3">
                {/* Search */}
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                  <Input
                    placeholder="Search materials..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="pl-9 w-[200px] h-9 text-sm"
                  />
                </div>

                {/* View Toggle */}
                <ToggleGroup type="single" value={viewMode} onValueChange={(value) => value && setViewMode(value as "table" | "cards")}>
                  <ToggleGroupItem value="table" aria-label="Table view" className="h-9 w-9 p-0">
                    <List className="h-4 w-4" />
                  </ToggleGroupItem>
                  <ToggleGroupItem value="cards" aria-label="Card view" className="h-9 w-9 p-0">
                    <Grid3x3 className="h-4 w-4" />
                  </ToggleGroupItem>
                </ToggleGroup>
              </div>
            </div>
          </CardHeader>
          <CardContent>
            {viewMode === "table" ? (
              <div className="space-y-4">
                <div className="rounded-md border">
                  <Table>
                    <TableHeader>
                      <TableRow className="bg-muted/50">
                        <TableHead className="w-[250px]">
                          <Button
                            variant="ghost"
                            size="sm"
                            className="h-8 gap-1 hover:bg-transparent p-0 font-semibold"
                            onClick={() => handleSort('material')}
                          >
                            Material
                            <ArrowUpDown className="h-3.5 w-3.5" />
                          </Button>
                        </TableHead>
                        <TableHead>
                          <Button
                            variant="ghost"
                            size="sm"
                            className="h-8 gap-1 hover:bg-transparent p-0 font-semibold"
                            onClick={() => handleSort('category')}
                          >
                            Category
                            <ArrowUpDown className="h-3.5 w-3.5" />
                          </Button>
                        </TableHead>
                        <TableHead>Month</TableHead>
                        <TableHead className="text-right">
                          <Button
                            variant="ghost"
                            size="sm"
                            className="h-8 gap-1 hover:bg-transparent p-0 font-semibold ml-auto"
                            onClick={() => handleSort('demand')}
                          >
                            Demand
                            <ArrowUpDown className="h-3.5 w-3.5" />
                          </Button>
                        </TableHead>
                        <TableHead className="text-right">
                          <Button
                            variant="ghost"
                            size="sm"
                            className="h-8 gap-1 hover:bg-transparent p-0 font-semibold ml-auto"
                            onClick={() => handleSort('confidence')}
                          >
                            Confidence
                            <ArrowUpDown className="h-3.5 w-3.5" />
                          </Button>
                        </TableHead>
                        <TableHead className="text-right">Value</TableHead>
                        <TableHead>Supplier</TableHead>
                        <TableHead className="text-right">Lead Time</TableHead>
                        <TableHead>Status</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {paginatedData.length === 0 ? (
                        <TableRow>
                          <TableCell colSpan={9} className="h-32 text-center">
                            <div className="flex flex-col items-center justify-center gap-2">
                              <Package className="h-8 w-8 text-muted-foreground" />
                              <p className="text-sm text-muted-foreground">No materials found</p>
                              <p className="text-xs text-muted-foreground">Try adjusting your filters</p>
                            </div>
                          </TableCell>
                        </TableRow>
                      ) : (
                        paginatedData.map((row) => {
                          const getStatusBadge = () => {
                            switch (row.status) {
                              case 'high-priority':
                                return (
                                  <Badge className="bg-orange-500/10 text-orange-700 dark:text-orange-300 border-orange-300 dark:border-orange-700 text-xs">
                                    High Priority
                                  </Badge>
                                );
                              case 'risk':
                                return (
                                  <Badge className="bg-yellow-500/10 text-yellow-700 dark:text-yellow-300 border-yellow-300 dark:border-yellow-700 text-xs gap-1">
                                    <AlertCircle className="h-3 w-3" />
                                    At Risk
                                  </Badge>
                                );
                              case 'long-lead':
                                return (
                                  <Badge className="bg-blue-500/10 text-blue-700 dark:text-blue-300 border-blue-300 dark:border-blue-700 text-xs gap-1">
                                    <Clock className="h-3 w-3" />
                                    Long Lead
                                  </Badge>
                                );
                              default:
                                return (
                                  <Badge variant="outline" className="text-xs">
                                    Normal
                                  </Badge>
                                );
                            }
                          };

                          return (
                            <TableRow key={row.id} className="hover:bg-muted/50 transition-colors">
                              <TableCell className="font-medium">
                                <div className="flex items-center gap-2">
                                  <Package className="h-4 w-4 text-muted-foreground" />
                                  {row.material}
                                </div>
                              </TableCell>
                              <TableCell>
                                <Badge variant="outline" className="text-xs">
                                  {row.category}
                                </Badge>
                              </TableCell>
                              <TableCell className="text-sm text-muted-foreground">{row.month}</TableCell>
                              <TableCell className="text-right font-medium">
                                {row.demand.toLocaleString()} {row.unit}
                              </TableCell>
                              <TableCell className="text-right">
                                <div className="flex items-center justify-end gap-2">
                                  <div className="h-2 w-16 bg-muted rounded-full overflow-hidden">
                                    <div
                                      className={`h-full ${row.confidence >= 90 ? 'bg-green-500' : 'bg-yellow-500'}`}
                                      style={{ width: `${row.confidence}%` }}
                                    ></div>
                                  </div>
                                  <span className="text-sm font-medium">{row.confidence}%</span>
                                </div>
                              </TableCell>
                              <TableCell className="text-right font-medium">
                                ₹{(row.value / 1000000).toFixed(2)}M
                              </TableCell>
                              <TableCell className="text-sm text-muted-foreground">{row.supplier}</TableCell>
                              <TableCell className="text-right text-sm">
                                <Badge variant="secondary" className="text-xs">
                                  {row.leadTime} days
                                </Badge>
                              </TableCell>
                              <TableCell>{getStatusBadge()}</TableCell>
                            </TableRow>
                          );
                        })
                      )}
                    </TableBody>
                  </Table>
                </div>

                {/* Pagination */}
                {totalPages > 1 && (
                  <div className="flex items-center justify-between">
                    <p className="text-sm text-muted-foreground">
                      Showing {((currentPage - 1) * itemsPerPage) + 1} to {Math.min(currentPage * itemsPerPage, filteredData.length)} of {filteredData.length} materials
                    </p>
                    <div className="flex items-center gap-2">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => setCurrentPage(p => Math.max(1, p - 1))}
                        disabled={currentPage === 1}
                        className="h-8 w-8 p-0"
                      >
                        <ChevronLeft className="h-4 w-4" />
                      </Button>
                      <div className="flex items-center gap-1">
                        {Array.from({ length: totalPages }, (_, i) => i + 1).map((page) => (
                          <Button
                            key={page}
                            variant={currentPage === page ? "default" : "outline"}
                            size="sm"
                            onClick={() => setCurrentPage(page)}
                            className="h-8 w-8 p-0"
                          >
                            {page}
                          </Button>
                        ))}
                      </div>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => setCurrentPage(p => Math.min(totalPages, p + 1))}
                        disabled={currentPage === totalPages}
                        className="h-8 w-8 p-0"
                      >
                        <ChevronRight className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                )}
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {paginatedData.map((row) => (
                  <Card key={row.id} className="hover:shadow-md transition-all duration-300">
                    <CardContent className="p-6">
                      <div className="space-y-4">
                        <div className="flex items-start justify-between">
                          <div className="flex items-center gap-3">
                            <div className="h-10 w-10 rounded-lg bg-primary/10 flex items-center justify-center">
                              <Package className="h-5 w-5 text-primary" />
                            </div>
                            <div>
                              <h4 className="font-semibold text-foreground">{row.material}</h4>
                              <p className="text-xs text-muted-foreground">{row.category}</p>
                            </div>
                          </div>
                          <Badge variant="outline" className="text-xs">{row.month}</Badge>
                        </div>

                        <Separator />

                        <div className="grid grid-cols-2 gap-4">
                          <div>
                            <p className="text-xs text-muted-foreground mb-1">Demand</p>
                            <p className="text-lg font-bold">{row.demand.toLocaleString()} {row.unit}</p>
                          </div>
                          <div>
                            <p className="text-xs text-muted-foreground mb-1">Value</p>
                            <p className="text-lg font-bold">₹{(row.value / 1000000).toFixed(1)}M</p>
                          </div>
                          <div>
                            <p className="text-xs text-muted-foreground mb-1">Confidence</p>
                            <div className="flex items-center gap-2">
                              <div className="h-2 flex-1 bg-muted rounded-full overflow-hidden">
                                <div
                                  className={`h-full ${row.confidence >= 90 ? 'bg-green-500' : 'bg-yellow-500'}`}
                                  style={{ width: `${row.confidence}%` }}
                                ></div>
                              </div>
                              <span className="text-sm font-medium">{row.confidence}%</span>
                            </div>
                          </div>
                          <div>
                            <p className="text-xs text-muted-foreground mb-1">Lead Time</p>
                            <p className="text-sm font-medium">{row.leadTime} days</p>
                          </div>
                        </div>

                        <div className="flex items-center justify-between pt-2">
                          <p className="text-xs text-muted-foreground">{row.supplier}</p>
                          {row.status === 'high-priority' && (
                            <Badge className="bg-orange-500/10 text-orange-700 text-xs">High Priority</Badge>
                          )}
                          {row.status === 'risk' && (
                            <Badge className="bg-yellow-500/10 text-yellow-700 text-xs">At Risk</Badge>
                          )}
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Forecast;
