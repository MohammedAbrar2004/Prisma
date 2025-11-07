import { ReactNode } from "react";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { cn } from "@/lib/utils";

interface GradientCardProps {
  children?: ReactNode;
  title?: string;
  description?: string;
  footer?: ReactNode;
  variant?: "default" | "glass" | "silver" | "teal" | "purple" | "green";
  hover?: boolean;
  glow?: boolean;
  className?: string;
  headerClassName?: string;
  contentClassName?: string;
}

const GradientCard = ({
  children,
  title,
  description,
  footer,
  variant = "default",
  hover = true,
  glow = false,
  className,
  headerClassName,
  contentClassName,
}: GradientCardProps) => {
  const variantClasses = {
    default: "bg-gradient-to-br from-card via-card to-muted/20",
    glass: "glass",
    silver: "bg-silver-gradient dark:bg-silver-gradient-dark",
    teal: "bg-gradient-to-br from-card to-teal-500/5",
    purple: "bg-gradient-to-br from-card to-purple-500/5",
    green: "bg-gradient-to-br from-card to-green-500/5",
  };

  const hoverClasses = hover
    ? "transition-all duration-300 hover:-translate-y-1 hover:shadow-lg"
    : "";

  const glowClasses = glow ? "glow-hover" : "";

  return (
    <Card
      className={cn(
        variantClasses[variant],
        hoverClasses,
        glowClasses,
        className
      )}
    >
      {(title || description) && (
        <CardHeader className={headerClassName}>
          {title && <CardTitle>{title}</CardTitle>}
          {description && <CardDescription>{description}</CardDescription>}
        </CardHeader>
      )}
      {children && (
        <CardContent className={contentClassName}>{children}</CardContent>
      )}
      {footer && <CardFooter>{footer}</CardFooter>}
    </Card>
  );
};

export default GradientCard;

