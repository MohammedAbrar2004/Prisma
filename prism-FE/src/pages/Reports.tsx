import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { FileText, Download, Calendar } from "lucide-react";
import { Badge } from "@/components/ui/badge";

const reports = [
  {
    title: "Monthly Procurement Report",
    description: "May 2025 procurement summary and analysis",
    date: "May 30, 2025",
    type: "Procurement",
    size: "2.4 MB",
  },
  {
    title: "Q1 Forecast Accuracy Report",
    description: "Quarterly performance and accuracy metrics",
    date: "Apr 15, 2025",
    type: "Analytics",
    size: "1.8 MB",
  },
  {
    title: "Inventory Status Report",
    description: "Current stock levels and reorder recommendations",
    date: "May 28, 2025",
    type: "Inventory",
    size: "1.2 MB",
  },
  {
    title: "Supplier Performance Review",
    description: "Delivery times, costs, and quality assessment",
    date: "May 20, 2025",
    type: "Procurement",
    size: "3.1 MB",
  },
  {
    title: "Cost Optimization Report",
    description: "Savings achieved through AI recommendations",
    date: "May 25, 2025",
    type: "Analytics",
    size: "1.5 MB",
  },
];

const Reports = () => {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-foreground">Reports</h1>
          <p className="text-muted-foreground mt-2">Generated insights and analytics reports</p>
        </div>
        <Button className="gap-2">
          <FileText className="h-4 w-4" />
          Generate New Report
        </Button>
      </div>

      {/* Reports Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {reports.map((report, index) => (
          <Card key={index} className="hover:shadow-md transition-shadow">
            <CardHeader>
              <div className="flex justify-between items-start">
                <div className="flex-1">
                  <CardTitle className="text-lg">{report.title}</CardTitle>
                  <CardDescription className="mt-2">{report.description}</CardDescription>
                </div>
                <FileText className="h-8 w-8 text-primary flex-shrink-0 ml-4" />
              </div>
            </CardHeader>
            <CardContent>
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-4 text-sm text-muted-foreground">
                  <div className="flex items-center gap-1">
                    <Calendar className="h-4 w-4" />
                    {report.date}
                  </div>
                  <Badge variant="secondary">{report.type}</Badge>
                  <span>{report.size}</span>
                </div>
                <Button variant="secondary" size="sm" className="gap-2">
                  <Download className="h-4 w-4" />
                  PDF
                </Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Report Types */}
      <Card>
        <CardHeader>
          <CardTitle>Available Report Types</CardTitle>
          <CardDescription>Generate custom reports based on your needs</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="p-4 border border-border rounded-lg hover:border-primary transition-colors cursor-pointer">
              <h3 className="font-medium text-foreground mb-2">Procurement Reports</h3>
              <p className="text-sm text-muted-foreground">
                Order summaries, supplier performance, cost analysis
              </p>
            </div>
            <div className="p-4 border border-border rounded-lg hover:border-primary transition-colors cursor-pointer">
              <h3 className="font-medium text-foreground mb-2">Forecast Reports</h3>
              <p className="text-sm text-muted-foreground">
                Demand predictions, accuracy metrics, trend analysis
              </p>
            </div>
            <div className="p-4 border border-border rounded-lg hover:border-primary transition-colors cursor-pointer">
              <h3 className="font-medium text-foreground mb-2">Inventory Reports</h3>
              <p className="text-sm text-muted-foreground">
                Stock levels, reorder alerts, utilization rates
              </p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default Reports;
