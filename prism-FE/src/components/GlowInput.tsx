import { forwardRef } from "react";
import { Input } from "@/components/ui/input";
import { cn } from "@/lib/utils";

interface GlowInputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  glowColor?: "teal" | "purple" | "green" | "default";
}

const GlowInput = forwardRef<HTMLInputElement, GlowInputProps>(
  ({ className, glowColor = "teal", ...props }, ref) => {
    const glowClasses = {
      teal: "focus:ring-2 focus:ring-teal-500/50 focus:border-teal-500",
      purple: "focus:ring-2 focus:ring-purple-500/50 focus:border-purple-500",
      green: "focus:ring-2 focus:ring-green-500/50 focus:border-green-500",
      default: "focus:ring-2 focus:ring-primary/50 focus:border-primary",
    };

    return (
      <Input
        ref={ref}
        className={cn(
          "transition-all duration-300",
          glowClasses[glowColor],
          className
        )}
        {...props}
      />
    );
  }
);

GlowInput.displayName = "GlowInput";

export default GlowInput;

