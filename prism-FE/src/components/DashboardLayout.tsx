import { ReactNode, useState } from "react";
import { NavLink } from "@/components/NavLink";
import {
  Upload,
  TrendingUp,
  ShoppingCart,
  Package,
  FileText,
  MessageSquare,
} from "lucide-react";
import { cn } from "@/lib/utils";
import ProfilePanel from "@/components/ProfilePanel";

interface DashboardLayoutProps {
  children: ReactNode;
}

const navigation = [
  { name: "Overview", href: "/dashboard", icon: TrendingUp },
  { name: "Data Upload", href: "/upload", icon: Upload },
  { name: "Forecast", href: "/forecast", icon: TrendingUp },
  { name: "Procurement", href: "/procurement", icon: ShoppingCart },
  { name: "Inventory", href: "/inventory", icon: Package },
  { name: "Reports", href: "/reports", icon: FileText },
];

const DashboardLayout = ({ children }: DashboardLayoutProps) => {
  const [profileOpen, setProfileOpen] = useState(false);

  return (
    <div className="min-h-screen flex w-full bg-background">
      {/* Sidebar */}
      <aside className="w-64 bg-card border-r border-border flex flex-col">
        <div className="p-6 border-b border-border">
          <div className="flex flex-col items-center space-y-2">
            <img
              src="/logo.png"
              alt="PRISMA Logo"
              className="h-16 w-auto object-contain"
            />
            <img
              src="/prisma-text.png"
              alt="PRISMA"
              className="h-5 w-auto object-contain"
            />
            <p className="text-xs text-muted-foreground">Supply Chain AI</p>
          </div>
        </div>
        <nav className="flex-1 p-4 space-y-1">
          {navigation.map((item) => (
            <NavLink
              key={item.name}
              to={item.href}
              end
              className="flex items-center space-x-3 px-3 py-2 rounded-lg text-foreground hover:bg-accent transition-colors"
              activeClassName="bg-accent text-accent-foreground font-medium"
            >
              <item.icon className="h-5 w-5" />
              <span>{item.name}</span>
            </NavLink>
          ))}
        </nav>
      </aside>

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <header className="bg-card border-b border-border px-6 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-lg font-semibold text-foreground">Welcome back, Riya</h2>
              <p className="text-sm text-muted-foreground">PowerGrid Infrastructure Pvt. Ltd.</p>
            </div>
            <button
              onClick={() => setProfileOpen(true)}
              className="h-10 w-10 rounded-full bg-primary text-primary-foreground flex items-center justify-center font-medium hover:bg-primary/90 transition-colors cursor-pointer"
            >
              RP
            </button>
          </div>
        </header>

        {/* Page Content */}
        <main className="flex-1 p-6 overflow-auto">{children}</main>
      </div>

      {/* AI Assistant Toggle - Floating Button */}
      <NavLink
        to="/assistant"
        className={cn(
          "fixed bottom-6 right-6 h-14 w-14 rounded-full shadow-lg",
          "bg-primary text-primary-foreground",
          "flex items-center justify-center",
          "hover:scale-110 transition-transform"
        )}
      >
        <MessageSquare className="h-6 w-6" />
      </NavLink>

      {/* Profile Panel */}
      <ProfilePanel open={profileOpen} onOpenChange={setProfileOpen} />
    </div>
  );
};

export default DashboardLayout;
