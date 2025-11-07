import { useState, useEffect } from "react";
import { Sheet, SheetContent, SheetHeader, SheetTitle } from "@/components/ui/sheet";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Switch } from "@/components/ui/switch";
import { Separator } from "@/components/ui/separator";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { useTheme } from "next-themes";
import { toast } from "@/components/ui/sonner";
import {
  User,
  Mail,
  Phone,
  Building2,
  Briefcase,
  Camera,
  Lock,
  Bell,
  Moon,
  Sun,
  LogOut,
  Calendar,
  TrendingUp,
  FileText,
  Loader2,
  Check,
  Sparkles
} from "lucide-react";
import { useNavigate } from "react-router-dom";

interface ProfilePanelProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

const ProfilePanel = ({ open, onOpenChange }: ProfilePanelProps) => {
  const navigate = useNavigate();
  const { theme, setTheme } = useTheme();
  const [emailNotifications, setEmailNotifications] = useState(true);
  const [forecastAlerts, setForecastAlerts] = useState(true);
  const [inventoryAlerts, setInventoryAlerts] = useState(false);
  const [isUploadingPhoto, setIsUploadingPhoto] = useState(false);
  const [isChangingPassword, setIsChangingPassword] = useState(false);
  const [animateIn, setAnimateIn] = useState(false);

  // Trigger staggered animations when panel opens
  useEffect(() => {
    if (open) {
      setAnimateIn(false);
      const timer = setTimeout(() => setAnimateIn(true), 50);
      return () => clearTimeout(timer);
    }
  }, [open]);

  const handleLogout = () => {
    toast.success("Logged out successfully", {
      description: "Redirecting to login page...",
    });
    setTimeout(() => {
      onOpenChange(false);
      navigate("/login");
    }, 1000);
  };

  const handleChangePassword = () => {
    setIsChangingPassword(true);
    // Simulate API call
    setTimeout(() => {
      setIsChangingPassword(false);
      toast.success("Password change initiated", {
        description: "Check your email for the password reset link",
      });
    }, 1500);
  };

  const handleUploadPhoto = () => {
    setIsUploadingPhoto(true);
    // Simulate photo upload
    setTimeout(() => {
      setIsUploadingPhoto(false);
      toast.success("Profile photo updated", {
        description: "Your new photo has been saved successfully",
      });
    }, 2000);
  };

  const handleNotificationToggle = (type: string, value: boolean) => {
    const messages = {
      email: value ? "Email notifications enabled" : "Email notifications disabled",
      forecast: value ? "Forecast alerts enabled" : "Forecast alerts disabled",
      inventory: value ? "Inventory alerts enabled" : "Inventory alerts disabled",
    };

    toast.success("Settings updated", {
      description: messages[type as keyof typeof messages],
    });
  };

  return (
    <Sheet open={open} onOpenChange={onOpenChange}>
      <SheetContent side="right" className="w-full sm:max-w-md overflow-y-auto bg-gradient-to-b from-background to-muted/20">
        <SheetHeader className="space-y-1">
          <div className="flex items-center gap-2">
            <Sparkles className="h-5 w-5 text-primary animate-pulse" />
            <SheetTitle className="text-xl">Profile & Settings</SheetTitle>
          </div>
          <p className="text-sm text-muted-foreground">Manage your account and preferences</p>
        </SheetHeader>

        <div className="space-y-6 py-6">
          {/* Profile Picture Section */}
          <div
            className={`flex flex-col items-center space-y-4 transition-all duration-500 ${
              animateIn ? 'opacity-100 translate-y-0' : 'opacity-0 -translate-y-4'
            }`}
          >
            <div className="relative group">
              <div className="absolute -inset-1 bg-gradient-to-r from-primary/50 to-accent/50 rounded-full blur opacity-25 group-hover:opacity-75 transition duration-500"></div>
              <Avatar className="relative h-28 w-28 ring-4 ring-background shadow-xl transition-transform duration-300 group-hover:scale-105">
                <AvatarImage src="" alt="Riya Patel" />
                <AvatarFallback className="text-3xl bg-gradient-to-br from-primary to-primary/80 text-primary-foreground">
                  RP
                </AvatarFallback>
              </Avatar>
              <button
                onClick={handleUploadPhoto}
                disabled={isUploadingPhoto}
                className="absolute bottom-0 right-0 h-10 w-10 rounded-full bg-primary text-primary-foreground flex items-center justify-center hover:bg-primary/90 transition-all duration-300 hover:scale-110 active:scale-95 shadow-lg disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isUploadingPhoto ? (
                  <Loader2 className="h-4 w-4 animate-spin" />
                ) : (
                  <Camera className="h-4 w-4" />
                )}
              </button>
            </div>
            <div className="text-center space-y-1">
              <h3 className="text-xl font-bold text-foreground bg-gradient-to-r from-foreground to-foreground/70 bg-clip-text">
                Riya Patel
              </h3>
              <p className="text-sm font-medium text-muted-foreground flex items-center gap-1 justify-center">
                <Briefcase className="h-3 w-3" />
                Supply Chain Manager
              </p>
            </div>
          </div>

          <Separator className="my-6" />

          {/* User Information */}
          <div
            className={`space-y-4 transition-all duration-500 delay-100 ${
              animateIn ? 'opacity-100 translate-y-0' : 'opacity-0 -translate-y-4'
            }`}
          >
            <div className="flex items-center gap-2">
              <div className="h-1 w-1 rounded-full bg-primary animate-pulse"></div>
              <h4 className="text-sm font-bold text-foreground uppercase tracking-wide">User Information</h4>
            </div>

            <div className="space-y-2">
              {[
                { icon: User, label: "Name", value: "Riya Patel" },
                { icon: Briefcase, label: "Role", value: "Supply Chain Manager" },
                { icon: Building2, label: "Organization", value: "PowerGrid Infrastructure Pvt. Ltd." },
                { icon: Mail, label: "Email", value: "riya.patel@powergrid.com" },
                { icon: Phone, label: "Phone", value: "+91 98765 43210" },
              ].map((item, index) => (
                <div
                  key={item.label}
                  className="group flex items-center space-x-3 p-3 rounded-lg bg-muted/50 hover:bg-muted transition-all duration-300 hover:shadow-sm border border-transparent hover:border-border"
                  style={{ transitionDelay: `${index * 50}ms` }}
                >
                  <div className="flex-shrink-0 h-9 w-9 rounded-full bg-background flex items-center justify-center group-hover:bg-primary/10 transition-colors duration-300">
                    <item.icon className="h-4 w-4 text-muted-foreground group-hover:text-primary transition-colors duration-300" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-xs font-medium text-muted-foreground uppercase tracking-wide">{item.label}</p>
                    <p className="text-sm text-foreground font-medium truncate">{item.value}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <Separator className="my-6" />

          {/* Statistics Card */}
          <div
            className={`transition-all duration-500 delay-200 ${
              animateIn ? 'opacity-100 translate-y-0' : 'opacity-0 -translate-y-4'
            }`}
          >
            <Card className="bg-gradient-to-br from-primary/5 via-muted/50 to-accent/5 border-2 border-primary/10 shadow-lg hover:shadow-xl transition-all duration-300 overflow-hidden relative">
              <div className="absolute top-0 right-0 w-32 h-32 bg-primary/5 rounded-full -mr-16 -mt-16"></div>
              <CardHeader className="relative">
                <div className="flex items-center gap-2">
                  <TrendingUp className="h-5 w-5 text-primary" />
                  <CardTitle className="text-base font-bold">Activity Summary</CardTitle>
                </div>
                <p className="text-xs text-muted-foreground">Your recent performance metrics</p>
              </CardHeader>
              <CardContent className="space-y-4 relative">
                {[
                  { icon: Calendar, label: "Last Login", value: "Today, 9:30 AM", color: "text-blue-500" },
                  { icon: Briefcase, label: "Projects Managed", value: "12", color: "text-green-500", showProgress: true, progress: 60 },
                  { icon: TrendingUp, label: "Forecasts Generated", value: "47", color: "text-purple-500", showProgress: true, progress: 85 },
                ].map((stat, index) => (
                  <div key={stat.label} className="space-y-2">
                    <div className="flex items-center justify-between group">
                      <div className="flex items-center space-x-3">
                        <div className={`h-10 w-10 rounded-lg bg-background flex items-center justify-center shadow-sm group-hover:scale-110 transition-transform duration-300`}>
                          <stat.icon className={`h-5 w-5 ${stat.color}`} />
                        </div>
                        <span className="text-sm font-medium text-foreground">{stat.label}</span>
                      </div>
                      <span className="text-lg font-bold text-foreground">{stat.value}</span>
                    </div>
                    {stat.showProgress && (
                      <div className="h-2 bg-muted rounded-full overflow-hidden">
                        <div
                          className={`h-full bg-gradient-to-r ${
                            stat.color.includes('green')
                              ? 'from-green-400 to-green-600'
                              : 'from-purple-400 to-purple-600'
                          } transition-all duration-1000 ease-out`}
                          style={{
                            width: animateIn ? `${stat.progress}%` : '0%',
                            transitionDelay: `${300 + index * 100}ms`
                          }}
                        ></div>
                      </div>
                    )}
                  </div>
                ))}
              </CardContent>
            </Card>
          </div>

          <Separator className="my-6" />

          {/* Security Settings */}
          <div
            className={`space-y-4 transition-all duration-500 delay-300 ${
              animateIn ? 'opacity-100 translate-y-0' : 'opacity-0 -translate-y-4'
            }`}
          >
            <div className="flex items-center gap-2">
              <div className="h-1 w-1 rounded-full bg-primary animate-pulse"></div>
              <h4 className="text-sm font-bold text-foreground uppercase tracking-wide">Security</h4>
            </div>
            <Button
              variant="outline"
              className="w-full justify-start gap-3 h-12 group hover:bg-primary/5 hover:border-primary/50 transition-all duration-300 hover:shadow-md relative overflow-hidden"
              onClick={handleChangePassword}
              disabled={isChangingPassword}
            >
              <div className="absolute inset-0 bg-gradient-to-r from-primary/0 via-primary/5 to-primary/0 translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-1000"></div>
              <div className="h-8 w-8 rounded-lg bg-muted flex items-center justify-center group-hover:bg-primary/10 transition-colors duration-300">
                {isChangingPassword ? (
                  <Loader2 className="h-4 w-4 animate-spin text-primary" />
                ) : (
                  <Lock className="h-4 w-4 text-muted-foreground group-hover:text-primary transition-colors duration-300" />
                )}
              </div>
              <span className="font-medium">Change Password</span>
            </Button>
          </div>

          <Separator className="my-6" />

          {/* Notification Preferences */}
          <div
            className={`space-y-4 transition-all duration-500 delay-[400ms] ${
              animateIn ? 'opacity-100 translate-y-0' : 'opacity-0 -translate-y-4'
            }`}
          >
            <div className="flex items-center gap-2">
              <div className="h-1 w-1 rounded-full bg-primary animate-pulse"></div>
              <h4 className="text-sm font-bold text-foreground uppercase tracking-wide">Notification Preferences</h4>
            </div>

            <div className="space-y-3">
              {[
                { id: "email-notifications", icon: Bell, label: "Email Notifications", checked: emailNotifications, setter: setEmailNotifications, type: "email" },
                { id: "forecast-alerts", icon: TrendingUp, label: "Forecast Alerts", checked: forecastAlerts, setter: setForecastAlerts, type: "forecast" },
                { id: "inventory-alerts", icon: FileText, label: "Inventory Alerts", checked: inventoryAlerts, setter: setInventoryAlerts, type: "inventory" },
              ].map((item, index) => (
                <div
                  key={item.id}
                  className="group flex items-center justify-between p-4 rounded-xl bg-muted/30 hover:bg-muted/60 transition-all duration-300 border border-transparent hover:border-border hover:shadow-sm"
                  style={{ transitionDelay: `${index * 50}ms` }}
                >
                  <div className="flex items-center space-x-3">
                    <div className={`h-10 w-10 rounded-lg flex items-center justify-center transition-all duration-300 ${
                      item.checked ? 'bg-primary/10' : 'bg-background'
                    }`}>
                      <item.icon className={`h-5 w-5 transition-all duration-300 ${
                        item.checked ? 'text-primary scale-110' : 'text-muted-foreground'
                      }`} />
                    </div>
                    <div>
                      <Label htmlFor={item.id} className="text-sm font-medium cursor-pointer">
                        {item.label}
                      </Label>
                      <p className="text-xs text-muted-foreground">
                        {item.checked ? 'Enabled' : 'Disabled'}
                      </p>
                    </div>
                  </div>
                  <Switch
                    id={item.id}
                    checked={item.checked}
                    onCheckedChange={(value) => {
                      item.setter(value);
                      handleNotificationToggle(item.type, value);
                    }}
                    className="data-[state=checked]:bg-primary"
                  />
                </div>
              ))}
            </div>
          </div>

          <Separator className="my-6" />

          {/* Theme Settings */}
          <div
            className={`space-y-4 transition-all duration-500 delay-[500ms] ${
              animateIn ? 'opacity-100 translate-y-0' : 'opacity-0 -translate-y-4'
            }`}
          >
            <div className="flex items-center gap-2">
              <div className="h-1 w-1 rounded-full bg-primary animate-pulse"></div>
              <h4 className="text-sm font-bold text-foreground uppercase tracking-wide">Appearance</h4>
            </div>

            <div className="group p-4 rounded-xl bg-gradient-to-r from-muted/30 to-muted/50 hover:from-muted/50 hover:to-muted/70 transition-all duration-300 border border-transparent hover:border-border hover:shadow-md">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <div className={`h-12 w-12 rounded-xl flex items-center justify-center transition-all duration-500 ${
                    theme === "dark"
                      ? 'bg-slate-800 rotate-0'
                      : 'bg-amber-100 rotate-180'
                  }`}>
                    {theme === "dark" ? (
                      <Moon className="h-6 w-6 text-slate-300 transition-transform duration-500" />
                    ) : (
                      <Sun className="h-6 w-6 text-amber-500 transition-transform duration-500" />
                    )}
                  </div>
                  <div>
                    <Label htmlFor="theme-toggle" className="text-sm font-medium cursor-pointer">
                      Dark Mode
                    </Label>
                    <p className="text-xs text-muted-foreground">
                      {theme === "dark" ? 'Night theme active' : 'Light theme active'}
                    </p>
                  </div>
                </div>
                <Switch
                  id="theme-toggle"
                  checked={theme === "dark"}
                  onCheckedChange={(checked) => {
                    setTheme(checked ? "dark" : "light");
                    toast.success("Theme updated", {
                      description: `Switched to ${checked ? 'dark' : 'light'} mode`,
                    });
                  }}
                  className="data-[state=checked]:bg-slate-700"
                />
              </div>
            </div>
          </div>

          <Separator className="my-6" />

          {/* Logout Button */}
          <div
            className={`transition-all duration-500 delay-[600ms] ${
              animateIn ? 'opacity-100 translate-y-0' : 'opacity-0 -translate-y-4'
            }`}
          >
            <Button
              variant="destructive"
              className="w-full gap-3 h-12 group relative overflow-hidden hover:shadow-lg transition-all duration-300"
              onClick={handleLogout}
            >
              <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-700"></div>
              <LogOut className="h-5 w-5 group-hover:rotate-12 transition-transform duration-300" />
              <span className="font-semibold">Logout</span>
            </Button>
          </div>
        </div>
      </SheetContent>
    </Sheet>
  );
};

export default ProfilePanel;

