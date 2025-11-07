"""
PRISMA Backend - Main FastAPI Application

This is the entry point for the PRISMA backend server.

Usage:
    uvicorn main:app --reload --port 8000
    
or:
    python main.py
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import routers
from routes.signals import router as signals_router
from routes.enrichment import router as enrichment_router

# ============================================================================
# App Initialization
# ============================================================================

app = FastAPI(
    title="PRISMA API",
    description="""
    ## PRISMA - Predictive Resource Intelligence & Supply-chain Management using AI
    
    This API provides intelligent decision-support for material demand forecasting,
    external risk signal analysis, and procurement recommendations.
    
    ### Features
    
    * **External Signals** - Real-time commodity prices, weather, and infrastructure data
    * **Demand Forecasting** - ML-based material demand predictions (coming soon)
    * **LLM Reasoning** - AI-powered explanations and recommendations (coming soon)
    * **Requirements Upload** - Parse and normalize company requirements (coming soon)
    
    ### Getting Started
    
    1. Configure API keys in `.env` file (copy from `env.example`)
    2. Start the server: `uvicorn main:app --reload`
    3. Visit `/docs` for interactive API documentation
    4. Test signals endpoint: `GET /signals/test-company`
    
    ### External APIs Used
    
    * MetalpriceAPI - Metal/commodity prices
    * CommodityAPI - Broader commodity tracking
    * WeatherAPI - Regional weather forecasts
    * World Bank API - Infrastructure and economic indicators
    """,
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ============================================================================
# CORS Configuration
# ============================================================================

# Get allowed origins from environment
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# Register Routers
# ============================================================================

app.include_router(signals_router)
app.include_router(enrichment_router)

# ============================================================================
# Root Endpoints
# ============================================================================

@app.get("/")
async def root():
    """
    Root endpoint - API welcome message
    """
    return {
        "message": "Welcome to PRISMA API",
        "version": "0.1.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
async def health():
    """
    Basic health check endpoint
    """
    return {
        "status": "healthy",
        "service": "PRISMA Backend",
        "version": "0.1.0"
    }


# ============================================================================
# Startup/Shutdown Events
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """
    Run on application startup
    """
    print("=" * 60)
    print("🚀 PRISMA Backend Starting...")
    print("=" * 60)
    print(f"Environment: {os.getenv('ENVIRONMENT', 'development')}")
    print(f"Docs available at: http://localhost:8000/docs")
    print("=" * 60)


@app.on_event("shutdown")
async def shutdown_event():
    """
    Run on application shutdown
    """
    print("👋 PRISMA Backend Shutting Down...")


# ============================================================================
# Run Server (if executed directly)
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True,  # Enable auto-reload during development
        log_level="info"
    )

