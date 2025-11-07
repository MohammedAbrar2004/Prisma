import { ReactNode } from "react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

interface GradientButtonProps {
  children: ReactNode;
  variant?: "teal" | "purple" | "green" | "silver" | "default";
  size?: "default" | "sm" | "lg" | "icon";
  glow?: boolean;
  onClick?: () => void;
  type?: "button" | "submit" | "reset";
  disabled?: boolean;
  className?: string;
}

const GradientButton = ({
  children,
  variant = "teal",
  size = "default",
  glow = true,
  onClick,
  type = "button",
  disabled = false,
  className,
}: GradientButtonProps) => {
  const variantClasses = {
    teal: "bg-teal-gradient text-white hover:opacity-90",
    purple: "bg-purple-gradient text-white hover:opacity-90",
    green: "bg-green-gradient text-white hover:opacity-90",
    silver: "bg-silver-gradient-dark text-foreground hover:opacity-90",
    default: "bg-primary text-primary-foreground hover:bg-primary/90",
  };

  const glowClasses = glow && !disabled ? "glow-hover" : "";

  return (
    <Button
      type={type}
      size={size}
      disabled={disabled}
      onClick={onClick}
      className={cn(
        variantClasses[variant],
        glowClasses,
        "transition-all duration-300 hover:scale-105",
        disabled && "opacity-50 cursor-not-allowed hover:scale-100",
        className
      )}
    >
      {children}
    </Button>
  );
};

export default GradientButton;

