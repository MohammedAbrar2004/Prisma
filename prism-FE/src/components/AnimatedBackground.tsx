/**
 * AnimatedBackground Component
 * 
 * A subtle, professional animated gradient background using silver/grey tones
 * that complements the PRISMA design system. Features smooth, slow animations
 * that create visual interest without distracting from content.
 * 
 * Performance optimized with CSS animations and GPU acceleration.
 */

const AnimatedBackground = () => {
  return (
    <>
      {/* Main animated gradient background */}
      <div className="fixed inset-0 -z-10 overflow-hidden pointer-events-none">
        {/* Base gradient layer */}
        <div className="absolute inset-0 bg-gradient-to-br from-background via-muted/30 to-background"></div>
        
        {/* Animated gradient orbs - Light mode */}
        <div className="absolute inset-0 dark:opacity-0 transition-opacity duration-500">
          {/* Large orb - top left */}
          <div 
            className="absolute -top-[40%] -left-[20%] w-[80%] h-[80%] rounded-full opacity-30 blur-3xl animate-gradient-shift-slow"
            style={{
              background: 'radial-gradient(circle, hsl(0 0% 85%) 0%, hsl(0 0% 92%) 25%, transparent 70%)',
              animation: 'gradient-float-1 20s ease-in-out infinite'
            }}
          ></div>
          
          {/* Medium orb - top right */}
          <div 
            className="absolute -top-[30%] -right-[15%] w-[60%] h-[60%] rounded-full opacity-25 blur-3xl"
            style={{
              background: 'radial-gradient(circle, hsl(0 0% 88%) 0%, hsl(0 0% 94%) 25%, transparent 70%)',
              animation: 'gradient-float-2 25s ease-in-out infinite'
            }}
          ></div>
          
          {/* Small orb - center */}
          <div 
            className="absolute top-[40%] left-[50%] w-[50%] h-[50%] rounded-full opacity-20 blur-3xl"
            style={{
              background: 'radial-gradient(circle, hsl(0 0% 90%) 0%, hsl(0 0% 95%) 25%, transparent 70%)',
              animation: 'gradient-float-3 30s ease-in-out infinite'
            }}
          ></div>
          
          {/* Accent orb - bottom right with subtle primary color hint */}
          <div 
            className="absolute -bottom-[30%] -right-[20%] w-[70%] h-[70%] rounded-full opacity-15 blur-3xl"
            style={{
              background: 'radial-gradient(circle, hsl(0 0% 82%) 0%, hsl(0 0% 93%) 30%, transparent 70%)',
              animation: 'gradient-float-4 28s ease-in-out infinite'
            }}
          ></div>
          
          {/* Small accent orb - bottom left */}
          <div 
            className="absolute -bottom-[20%] -left-[10%] w-[45%] h-[45%] rounded-full opacity-18 blur-3xl"
            style={{
              background: 'radial-gradient(circle, hsl(0 0% 86%) 0%, hsl(0 0% 94%) 25%, transparent 70%)',
              animation: 'gradient-float-5 22s ease-in-out infinite'
            }}
          ></div>
        </div>
        
        {/* Animated gradient orbs - Dark mode */}
        <div className="absolute inset-0 opacity-0 dark:opacity-100 transition-opacity duration-500">
          {/* Large orb - top left */}
          <div 
            className="absolute -top-[40%] -left-[20%] w-[80%] h-[80%] rounded-full opacity-20 blur-3xl"
            style={{
              background: 'radial-gradient(circle, hsl(0 0% 20%) 0%, hsl(0 0% 15%) 25%, transparent 70%)',
              animation: 'gradient-float-1 20s ease-in-out infinite'
            }}
          ></div>
          
          {/* Medium orb - top right */}
          <div 
            className="absolute -top-[30%] -right-[15%] w-[60%] h-[60%] rounded-full opacity-15 blur-3xl"
            style={{
              background: 'radial-gradient(circle, hsl(0 0% 22%) 0%, hsl(0 0% 16%) 25%, transparent 70%)',
              animation: 'gradient-float-2 25s ease-in-out infinite'
            }}
          ></div>
          
          {/* Small orb - center */}
          <div 
            className="absolute top-[40%] left-[50%] w-[50%] h-[50%] rounded-full opacity-12 blur-3xl"
            style={{
              background: 'radial-gradient(circle, hsl(0 0% 24%) 0%, hsl(0 0% 17%) 25%, transparent 70%)',
              animation: 'gradient-float-3 30s ease-in-out infinite'
            }}
          ></div>
          
          {/* Accent orb - bottom right */}
          <div 
            className="absolute -bottom-[30%] -right-[20%] w-[70%] h-[70%] rounded-full opacity-10 blur-3xl"
            style={{
              background: 'radial-gradient(circle, hsl(0 0% 26%) 0%, hsl(0 0% 18%) 30%, transparent 70%)',
              animation: 'gradient-float-4 28s ease-in-out infinite'
            }}
          ></div>
          
          {/* Small accent orb - bottom left */}
          <div 
            className="absolute -bottom-[20%] -left-[10%] w-[45%] h-[45%] rounded-full opacity-14 blur-3xl"
            style={{
              background: 'radial-gradient(circle, hsl(0 0% 23%) 0%, hsl(0 0% 16%) 25%, transparent 70%)',
              animation: 'gradient-float-5 22s ease-in-out infinite'
            }}
          ></div>
        </div>
        
        {/* Subtle noise texture overlay for depth */}
        <div 
          className="absolute inset-0 opacity-[0.015] dark:opacity-[0.025] mix-blend-overlay"
          style={{
            backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 400 400' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E")`,
            backgroundRepeat: 'repeat',
            backgroundSize: '200px 200px'
          }}
        ></div>
        
        {/* Subtle radial vignette for depth */}
        <div 
          className="absolute inset-0 opacity-40 dark:opacity-60"
          style={{
            background: 'radial-gradient(ellipse at center, transparent 0%, hsl(0 0% 0% / 0.03) 100%)'
          }}
        ></div>
      </div>

      {/* CSS Animations */}
      <style>{`
        @keyframes gradient-float-1 {
          0%, 100% {
            transform: translate(0, 0) scale(1);
          }
          33% {
            transform: translate(10%, 15%) scale(1.1);
          }
          66% {
            transform: translate(-5%, 10%) scale(0.95);
          }
        }

        @keyframes gradient-float-2 {
          0%, 100% {
            transform: translate(0, 0) scale(1);
          }
          33% {
            transform: translate(-15%, 10%) scale(1.05);
          }
          66% {
            transform: translate(-8%, -12%) scale(0.98);
          }
        }

        @keyframes gradient-float-3 {
          0%, 100% {
            transform: translate(-50%, -50%) scale(1);
          }
          33% {
            transform: translate(-45%, -55%) scale(1.08);
          }
          66% {
            transform: translate(-55%, -48%) scale(0.96);
          }
        }

        @keyframes gradient-float-4 {
          0%, 100% {
            transform: translate(0, 0) scale(1);
          }
          33% {
            transform: translate(-12%, -8%) scale(1.06);
          }
          66% {
            transform: translate(8%, -15%) scale(0.97);
          }
        }

        @keyframes gradient-float-5 {
          0%, 100% {
            transform: translate(0, 0) scale(1);
          }
          33% {
            transform: translate(15%, -10%) scale(1.04);
          }
          66% {
            transform: translate(5%, 12%) scale(0.99);
          }
        }

        /* GPU acceleration for smooth performance */
        @media (prefers-reduced-motion: no-preference) {
          [style*="gradient-float"] {
            will-change: transform;
            transform: translateZ(0);
            backface-visibility: hidden;
          }
        }

        /* Disable animations for users who prefer reduced motion */
        @media (prefers-reduced-motion: reduce) {
          [style*="gradient-float"] {
            animation: none !important;
          }
        }
      `}</style>
    </>
  );
};

export default AnimatedBackground;

