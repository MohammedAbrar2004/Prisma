import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Eye, EyeOff, Sparkles } from "lucide-react";
import { Label } from "@/components/ui/label";
import GradientCard from "@/components/GradientCard";
import GradientButton from "@/components/GradientButton";
import GlowInput from "@/components/GlowInput";

const Login = () => {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [animateIn, setAnimateIn] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => setAnimateIn(true), 100);
    return () => clearTimeout(timer);
  }, []);

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    // Mock login - in production, this would validate credentials
    navigate("/home");
  };

  return (
    <div className="min-h-screen flex items-center justify-center px-4 relative overflow-hidden">
      {/* Particle effects */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        {[...Array(20)].map((_, i) => (
          <div
            key={i}
            className="absolute w-1 h-1 bg-silver-400 rounded-full opacity-30"
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
              animation: `pulse ${2 + Math.random() * 3}s ease-in-out infinite`,
              animationDelay: `${Math.random() * 2}s`,
            }}
          />
        ))}
      </div>

      {/* Login Card */}
      <div
        className={`w-full max-w-md transition-all duration-700 ${
          animateIn ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"
        }`}
      >
        <GradientCard
          variant="glass"
          className="border-2 border-border/50 shadow-2xl"
          glow={true}
        >
          <div className="p-8 space-y-6">
            {/* Logo and Branding */}
            <div className="text-center space-y-4">
              <div className="flex justify-center">
                <div className="relative">
                  <div className="absolute inset-0 bg-teal-gradient rounded-full blur-xl opacity-50 animate-pulse" />
                  <img
                    src="/logo.png"
                    alt="PRISM Logo"
                    className="h-24 w-auto object-contain relative z-10"
                  />
                </div>
              </div>
              <div className="space-y-2">
                <div className="flex items-center justify-center gap-2">
                  <h1 className="text-3xl font-bold bg-gradient-to-r from-foreground to-muted-foreground bg-clip-text text-transparent">
                    PRISM
                  </h1>
                  <Sparkles className="h-5 w-5 text-teal-500 animate-pulse" />
                </div>
                <p className="text-muted-foreground text-sm">
                  Smart Procurement Forecasting
                </p>
                <div className="inline-block px-3 py-1 rounded-full bg-silver-gradient-dark text-xs font-medium">
                  AI-Powered Supply Chain Intelligence
                </div>
              </div>
            </div>

            {/* Login Form */}
            <form onSubmit={handleLogin} className="space-y-5">
              <div className="space-y-2">
                <Label htmlFor="email" className="text-sm font-medium">
                  Email Address
                </Label>
                <GlowInput
                  id="email"
                  type="email"
                  placeholder="riya.patel@powergrid.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                  glowColor="teal"
                  className="h-11"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="password" className="text-sm font-medium">
                  Password
                </Label>
                <div className="relative">
                  <GlowInput
                    id="password"
                    type={showPassword ? "text" : "password"}
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                    glowColor="teal"
                    className="h-11 pr-10"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground transition-colors"
                  >
                    {showPassword ? (
                      <EyeOff className="h-4 w-4" />
                    ) : (
                      <Eye className="h-4 w-4" />
                    )}
                  </button>
                </div>
              </div>

              <div className="flex items-center justify-between text-sm">
                <label className="flex items-center gap-2 cursor-pointer">
                  <input
                    type="checkbox"
                    className="rounded border-border focus:ring-2 focus:ring-teal-500/50"
                  />
                  <span className="text-muted-foreground">Remember me</span>
                </label>
                <a
                  href="#"
                  className="text-teal-600 hover:text-teal-700 dark:text-teal-400 dark:hover:text-teal-300 font-medium"
                >
                  Forgot password?
                </a>
              </div>

              <GradientButton
                type="submit"
                variant="teal"
                className="w-full h-11 text-base font-semibold"
                glow={true}
              >
                Sign In to PRISM
              </GradientButton>
            </form>

            {/* Footer */}
            <div className="text-center text-xs text-muted-foreground pt-4 border-t border-border/50">
              <p>Secure enterprise-grade authentication</p>
              <p className="mt-1">© 2024 PRISM. All rights reserved.</p>
            </div>
          </div>
        </GradientCard>
      </div>
    </div>
  );
};

export default Login;
