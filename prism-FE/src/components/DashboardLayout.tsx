import { ReactNode, useState } from "react";
import { NavLink } from "@/components/NavLink";
import {
  Upload,
  TrendingUp,
  ShoppingCart,
  Package,
  FileText,
  Home,
  Sparkles,
} from "lucide-react";
import { cn } from "@/lib/utils";
import ProfilePanel from "@/components/ProfilePanel";
import FloatingAIAssistant from "@/components/FloatingAIAssistant";

interface DashboardLayoutProps {
  children: ReactNode;
}

const navigation = [
  { name: "Home", href: "/home", icon: Home },
  { name: "Data Upload", href: "/upload", icon: Upload },
  { name: "Forecast", href: "/forecast", icon: TrendingUp },
  { name: "Procurement", href: "/procurement", icon: ShoppingCart },
  { name: "Inventory", href: "/inventory", icon: Package },
  { name: "Reports", href: "/reports", icon: FileText },
];

const DashboardLayout = ({ children }: DashboardLayoutProps) => {
  const [profileOpen, setProfileOpen] = useState(false);

  return (
    <div className="min-h-screen flex w-full">
      {/* Sidebar with Glass Effect */}
      <aside className="w-64 bg-silver-gradient dark:bg-silver-gradient-dark border-r border-border/50 flex flex-col backdrop-blur-sm">
        <div className="p-6 border-b border-border/50">
          <div className="flex flex-col items-center space-y-3">
            <div className="relative">
              <div className="absolute inset-0 bg-teal-gradient rounded-full blur-lg opacity-30" />
              <img
                src="/logo.png"
                alt="PRISM Logo"
                className="h-16 w-auto object-contain relative z-10"
              />
            </div>
            <div className="text-center">
              <div className="flex items-center justify-center gap-2">
                <h2 className="text-xl font-bold bg-gradient-to-r from-foreground to-muted-foreground bg-clip-text text-transparent">
                  PRISM
                </h2>
                <Sparkles className="h-4 w-4 text-teal-500" />
              </div>
              <p className="text-xs text-muted-foreground mt-1">Supply Chain AI</p>
            </div>
          </div>
        </div>
        <nav className="flex-1 p-4 space-y-1">
          {navigation.map((item) => (
            <NavLink
              key={item.name}
              to={item.href}
              end
              className="flex items-center space-x-3 px-4 py-3 rounded-xl text-foreground hover:bg-white/50 dark:hover:bg-black/20 transition-all duration-300 group"
              activeClassName="bg-teal-gradient text-white font-medium shadow-lg glow-teal"
            >
              <item.icon className="h-5 w-5 group-hover:scale-110 transition-transform" />
              <span>{item.name}</span>
            </NavLink>
          ))}
        </nav>
      </aside>

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        {/* Header with Glass Effect */}
        <header className="glass border-b border-border/50 px-6 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-lg font-semibold text-foreground">Welcome back, Riya</h2>
              <p className="text-sm text-muted-foreground">PowerGrid Infrastructure Pvt. Ltd.</p>
            </div>
            <button
              onClick={() => setProfileOpen(true)}
              className="h-11 w-11 rounded-full bg-teal-gradient text-white flex items-center justify-center font-medium hover:scale-110 transition-all duration-300 shadow-lg glow-teal cursor-pointer"
            >
              RP
            </button>
          </div>
        </header>

        {/* Page Content */}
        <main className="flex-1 p-6 overflow-auto">{children}</main>
      </div>

      {/* Floating AI Assistant */}
      <FloatingAIAssistant />

      {/* Profile Panel */}
      <ProfilePanel open={profileOpen} onOpenChange={setProfileOpen} />
    </div>
  );
};

export default DashboardLayout;
