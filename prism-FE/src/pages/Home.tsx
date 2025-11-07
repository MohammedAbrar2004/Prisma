import { useState, useEffect } from "react";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import {
  TrendingUp,
  Package,
  AlertCircle,
  Upload,
  FileText,
  MessageSquare,
  ArrowUpRight,
  Activity,
  BarChart3,
  Sparkles,
  ChevronRight,
  Calendar,
  DollarSign,
  ShoppingCart,
  Zap,
  Target,
  Clock
} from "lucide-react";
import { useNavigate } from "react-router-dom";
import GradientCard from "@/components/GradientCard";
import GradientButton from "@/components/GradientButton";

const forecastData = [
  { month: "Jan", forecast: 1200, actual: 1150 },
  { month: "Feb", forecast: 1350, actual: 1400 },
  { month: "Mar", forecast: 1500, actual: 1480 },
  { month: "Apr", forecast: 1650, actual: 1620 },
  { month: "May", forecast: 1800, actual: 1750 },
  { month: "Jun", forecast: 1900, actual: 1850 },
];

const trendData = [
  { day: "Mon", value: 85 },
  { day: "Tue", value: 92 },
  { day: "Wed", value: 78 },
  { day: "Thu", value: 95 },
  { day: "Fri", value: 88 },
  { day: "Sat", value: 82 },
  { day: "Sun", value: 90 },
];

const kpiData = [
  { label: "Total Value", value: "$2.4M", change: "+12.5%", trend: "up", icon: DollarSign, color: "teal" },
  { label: "Active Orders", value: "342", change: "+8.2%", trend: "up", icon: ShoppingCart, color: "purple" },
  { label: "Forecast Accuracy", value: "94.2%", change: "+1.8%", trend: "up", icon: Target, color: "green" },
  { label: "Stock Level", value: "87%", change: "+2.5%", trend: "up", icon: Package, color: "teal" },
];

const recentActivity = [
  { id: 1, action: "Forecast generated", item: "Q2 2025 Materials", time: "10 min ago", icon: BarChart3 },
  { id: 2, action: "Data uploaded", item: "March consumption data", time: "1h ago", icon: Upload },
  { id: 3, action: "Report exported", item: "Inventory summary", time: "3h ago", icon: FileText },
  { id: 4, action: "AI analysis completed", item: "Demand patterns", time: "5h ago", icon: Sparkles },
];

const alerts = [
  { id: 1, message: "Material consumption up 6%", type: "info", icon: AlertCircle, color: "blue" },
  { id: 2, message: "Steel rods low stock alert", type: "warning", icon: Package, color: "orange" },
  { id: 3, message: "Forecast accuracy improved", type: "success", icon: TrendingUp, color: "green" },
];

const Home = () => {
  const navigate = useNavigate();
  const [animateIn, setAnimateIn] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => setAnimateIn(true), 100);
    return () => clearTimeout(timer);
  }, []);

  const currentDate = new Date().toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
  });

  return (
    <div className="min-h-screen pb-8 space-y-6">
      {/* Hero Section */}
      <div
        className={`fade-in-up ${animateIn ? "opacity-100" : "opacity-0"}`}
      >
        <div className="flex items-start justify-between flex-wrap gap-4">
          <div className="flex items-center gap-4">
            <div className="h-16 w-16 rounded-2xl bg-teal-gradient flex items-center justify-center shadow-lg glow-teal">
              <Sparkles className="h-8 w-8 text-white" />
            </div>
            <div>
              <h1 className="text-4xl font-bold bg-gradient-to-r from-foreground to-muted-foreground bg-clip-text text-transparent">
                Welcome back, Admin
              </h1>
              <p className="text-muted-foreground mt-1">
                Here's what's happening with your supply chain today
              </p>
            </div>
          </div>
          <Badge className="gap-1.5 px-4 py-2 bg-silver-gradient border-none text-foreground">
            <Calendar className="h-4 w-4" />
            {currentDate}
          </Badge>
        </div>
      </div>

      {/* KPI Cards - Asymmetric Grid (4 cards with varied sizes) */}
      <div
        className={`grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 fade-in-up stagger-1 ${
          animateIn ? "opacity-100" : "opacity-0"
        }`}
      >
        {kpiData.map((kpi, index) => {
          const Icon = kpi.icon;
          return (
            <GradientCard
              key={index}
              variant={kpi.color as any}
              hover={true}
              glow={true}
              className="border-2 border-border/50"
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-3">
                    <div className={`h-10 w-10 rounded-xl bg-${kpi.color}-500/10 flex items-center justify-center`}>
                      <Icon className={`h-5 w-5 text-${kpi.color}-600`} />
                    </div>
                  </div>
                  <p className="text-sm text-muted-foreground mb-1">{kpi.label}</p>
                  <p className="text-3xl font-bold text-foreground">{kpi.value}</p>
                  <div className="flex items-center gap-1 mt-2 text-green-600">
                    <ArrowUpRight className="h-4 w-4" />
                    <span className="text-sm font-medium">{kpi.change}</span>
                  </div>
                </div>
              </div>
            </GradientCard>
          );
        })}
      </div>

      {/* Quick Actions */}
      <div
        className={`grid grid-cols-2 lg:grid-cols-4 gap-4 fade-in-up stagger-2 ${
          animateIn ? "opacity-100" : "opacity-0"
        }`}
      >
        <GradientCard
          variant="glass"
          hover={true}
          className="cursor-pointer group border-2 border-border/50"
          onClick={() => navigate("/upload")}
        >
          <div className="text-center py-4">
            <div className="h-14 w-14 mx-auto rounded-2xl bg-silver-gradient-dark flex items-center justify-center mb-3 group-hover:scale-110 transition-transform">
              <Upload className="h-7 w-7 text-foreground" />
            </div>
            <h3 className="font-semibold text-foreground">Upload Data</h3>
            <p className="text-xs text-muted-foreground mt-1">Import new data</p>
          </div>
        </GradientCard>

        <GradientCard
          variant="green"
          hover={true}
          className="cursor-pointer group border-2 border-green-500/20"
          onClick={() => navigate("/forecast")}
        >
          <div className="text-center py-4">
            <div className="h-14 w-14 mx-auto rounded-2xl bg-green-500/10 flex items-center justify-center mb-3 group-hover:scale-110 transition-transform">
              <TrendingUp className="h-7 w-7 text-green-600" />
            </div>
            <h3 className="font-semibold text-foreground">Quick Forecast</h3>
            <p className="text-xs text-muted-foreground mt-1">Generate predictions</p>
          </div>
        </GradientCard>

        <GradientCard
          variant="teal"
          hover={true}
          className="cursor-pointer group border-2 border-teal-500/20"
          onClick={() => navigate("/reports")}
        >
          <div className="text-center py-4">
            <div className="h-14 w-14 mx-auto rounded-2xl bg-teal-500/10 flex items-center justify-center mb-3 group-hover:scale-110 transition-transform">
              <FileText className="h-7 w-7 text-teal-600" />
            </div>
            <h3 className="font-semibold text-foreground">View Reports</h3>
            <p className="text-xs text-muted-foreground mt-1">Analytics & insights</p>
          </div>
        </GradientCard>

        <GradientCard
          variant="purple"
          hover={true}
          className="cursor-pointer group border-2 border-purple-500/20"
          onClick={() => navigate("/assistant")}
        >
          <div className="text-center py-4">
            <div className="h-14 w-14 mx-auto rounded-2xl bg-purple-500/10 flex items-center justify-center mb-3 group-hover:scale-110 transition-transform">
              <MessageSquare className="h-7 w-7 text-purple-600" />
            </div>
            <h3 className="font-semibold text-foreground">AI Assistant</h3>
            <p className="text-xs text-muted-foreground mt-1">Get smart insights</p>
          </div>
        </GradientCard>
      </div>

      {/* Asymmetric Content Grid - 8/4 Split */}
      <div
        className={`grid grid-cols-12 gap-6 fade-in-up stagger-3 ${
          animateIn ? "opacity-100" : "opacity-0"
        }`}
      >
        {/* Main Chart - 8/12 width */}
        <GradientCard
          variant="glass"
          title="Demand Trends"
          description="Forecast vs Actual Performance"
          className="col-span-12 lg:col-span-8 border-2 border-border/50"
          hover={true}
        >
          <ResponsiveContainer width="100%" height={320}>
            <AreaChart data={forecastData}>
              <defs>
                <linearGradient id="colorForecast" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="hsl(180 65% 55%)" stopOpacity={0.3} />
                  <stop offset="95%" stopColor="hsl(180 65% 55%)" stopOpacity={0} />
                </linearGradient>
                <linearGradient id="colorActual" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="hsl(142 60% 50%)" stopOpacity={0.3} />
                  <stop offset="95%" stopColor="hsl(142 60% 50%)" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
              <XAxis dataKey="month" stroke="hsl(var(--muted-foreground))" />
              <YAxis stroke="hsl(var(--muted-foreground))" />
              <Tooltip
                contentStyle={{
                  backgroundColor: "hsl(var(--card))",
                  border: "1px solid hsl(var(--border))",
                  borderRadius: "8px",
                }}
              />
              <Area
                type="monotone"
                dataKey="forecast"
                stroke="hsl(180 65% 55%)"
                strokeWidth={2}
                fill="url(#colorForecast)"
              />
              <Area
                type="monotone"
                dataKey="actual"
                stroke="hsl(142 60% 50%)"
                strokeWidth={2}
                fill="url(#colorActual)"
              />
            </AreaChart>
          </ResponsiveContainer>
        </GradientCard>

        {/* Sidebar - 4/12 width */}
        <div className="col-span-12 lg:col-span-4 space-y-6">
          {/* Alerts */}
          <GradientCard
            variant="silver"
            title="Alerts"
            className="border-2 border-border/50"
          >
            <div className="space-y-3">
              {alerts.map((alert) => {
                const Icon = alert.icon;
                return (
                  <div
                    key={alert.id}
                    className="flex items-start gap-3 p-3 rounded-lg bg-muted/30 hover:bg-muted/50 transition-colors cursor-pointer"
                  >
                    <Icon className={`h-5 w-5 text-${alert.color}-600 mt-0.5`} />
                    <div className="flex-1">
                      <p className="text-sm text-foreground">{alert.message}</p>
                    </div>
                  </div>
                );
              })}
            </div>
          </GradientCard>

          {/* Mini Stats */}
          <GradientCard
            variant="glass"
            title="Quick Stats"
            className="border-2 border-border/50"
          >
            <div className="grid grid-cols-2 gap-3">
              <div className="p-3 rounded-lg bg-teal-500/5 border border-teal-500/20">
                <p className="text-xs text-muted-foreground mb-1">Total Value</p>
                <p className="text-xl font-bold text-foreground">$2.4M</p>
                <p className="text-xs text-green-600 mt-1">+12.5%</p>
              </div>
              <div className="p-3 rounded-lg bg-purple-500/5 border border-purple-500/20">
                <p className="text-xs text-muted-foreground mb-1">Orders</p>
                <p className="text-xl font-bold text-foreground">342</p>
                <p className="text-xs text-green-600 mt-1">+8.2%</p>
              </div>
            </div>
          </GradientCard>
        </div>
      </div>

      {/* Recent Activity */}
      <GradientCard
        variant="glass"
        title="Recent Activity"
        className={`border-2 border-border/50 fade-in-up stagger-4 ${
          animateIn ? "opacity-100" : "opacity-0"
        }`}
      >
        <div className="space-y-3">
          {recentActivity.map((activity, index) => {
            const Icon = activity.icon;
            return (
              <div
                key={activity.id}
                className={`flex items-center justify-between p-4 rounded-lg hover:bg-muted/50 transition-colors cursor-pointer group ${
                  index === 0 ? "bg-muted/30" : ""
                }`}
              >
                <div className="flex items-center gap-4">
                  <div className="h-10 w-10 rounded-xl bg-teal-500/10 flex items-center justify-center">
                    <Icon className="h-5 w-5 text-teal-600" />
                  </div>
                  <div>
                    <p className="font-medium text-foreground">{activity.action}</p>
                    <p className="text-sm text-muted-foreground">{activity.item}</p>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <div className="flex items-center gap-1 text-muted-foreground">
                    <Clock className="h-4 w-4" />
                    <span className="text-sm">{activity.time}</span>
                  </div>
                  <ChevronRight className="h-5 w-5 text-muted-foreground opacity-0 group-hover:opacity-100 transition-opacity" />
                </div>
              </div>
            );
          })}
        </div>
      </GradientCard>
    </div>
  );
};

export default Home;

