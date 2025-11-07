import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { ThemeProvider } from "next-themes";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import DataUpload from "./pages/DataUpload";
import Forecast from "./pages/Forecast";
import Procurement from "./pages/Procurement";
import Inventory from "./pages/Inventory";
import Reports from "./pages/Reports";
import AIAssistant from "./pages/AIAssistant";
import DashboardLayout from "./components/DashboardLayout";
import NotFound from "./pages/NotFound";

const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <ThemeProvider attribute="class" defaultTheme="light" enableSystem={false}>
      <TooltipProvider>
        <Toaster />
        <Sonner />
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<Navigate to="/login" replace />} />
            <Route path="/login" element={<Login />} />
            <Route path="/dashboard" element={<DashboardLayout><Dashboard /></DashboardLayout>} />
            <Route path="/upload" element={<DashboardLayout><DataUpload /></DashboardLayout>} />
            <Route path="/forecast" element={<DashboardLayout><Forecast /></DashboardLayout>} />
            <Route path="/procurement" element={<DashboardLayout><Procurement /></DashboardLayout>} />
            <Route path="/inventory" element={<DashboardLayout><Inventory /></DashboardLayout>} />
            <Route path="/reports" element={<DashboardLayout><Reports /></DashboardLayout>} />
            <Route path="/assistant" element={<DashboardLayout><AIAssistant /></DashboardLayout>} />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </BrowserRouter>
      </TooltipProvider>
    </ThemeProvider>
  </QueryClientProvider>
);

export default App;
