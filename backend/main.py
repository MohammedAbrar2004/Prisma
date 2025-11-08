"""
PRISMA Backend - Main FastAPI Application

This is the entry point for the PRISMA backend server.

Usage:
    uvicorn main:app --reload --port 8000
    
or:
    python main.py
"""

import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import routers
from routes.signals import router as signals_router
from routes.analyze import router as analyze_router
from routes.forecast import router as forecast_router
from routes.admin import router as admin_router

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
    * **Industry Intelligence** - Sector-specific trend analysis and insights
    * **LLM Reasoning** - AI-powered explanations and recommendations using Ollama (llama3)
    * **Demand Analysis** - Comprehensive procurement recommendations based on forecasts and signals
    * **Requirements Upload** - Parse and normalize company requirements (coming soon)
    
    ### Getting Started
    
    1. Ensure Ollama is running: `ollama serve` with llama3 model installed
    2. Configure API keys in `.env` file (copy from `env.example`)
    3. Start the server: `uvicorn main:app --reload`
    4. Visit `/docs` for interactive API documentation
    5. Test analysis endpoint: `POST /analyze` with company_id
    
    ### Key Endpoints
    
    * `GET /signals/{company_id}` - Get external demand signals
    * `POST /analyze` - Get AI-powered procurement recommendations
    * `POST /analyze/ask` - Ask specific questions about demand/procurement
    * `POST /forecast/generate` - Generate demand forecasts
    * `GET /admin/cache/stats` - Cache statistics
    * `GET /admin/diagnostics` - System diagnostics
    
    ### External APIs Used
    
    * Ollama (Local) - LLM reasoning with llama3
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
app.include_router(analyze_router)
app.include_router(forecast_router)
app.include_router(admin_router)

# Serve static files (UI)
try:
    from pathlib import Path
    static_path = Path(__file__).parent / "static"
    if static_path.exists():
        app.mount("/static", StaticFiles(directory=str(static_path)), name="static")
except:
    pass

# ============================================================================
# Root Endpoints
# ============================================================================

@app.get("/")
async def root():
    """
    Root endpoint - API welcome message
    """
    from fastapi.responses import FileResponse
    from pathlib import Path
    
    ui_path = Path(__file__).parent / "static" / "index.html"
    if ui_path.exists():
        return FileResponse(str(ui_path))
    
    return {
        "message": "Welcome to PRISMA API",
        "version": "0.1.0",
        "docs": "/docs",
        "health": "/health",
        "ui": "/static/index.html"
    }


@app.get("/health")
async def health():
    """
    Comprehensive health check endpoint
    
    Checks:
    - API availability
    - Ollama connection
    - Cache system
    - External signals
    
    Returns detailed system status
    """
    from llm import test_ollama_connection
    
    # Check Ollama
    try:
        ollama_status = test_ollama_connection()
    except:
        ollama_status = {"status": "error", "message": "Failed to connect"}
    
    # Check cache
    try:
        from utils.cache_manager import cache_stats
        cache_status = cache_stats()
    except:
        cache_status = {"enabled": False, "error": "cache_manager not available"}
    
    # Overall health
    is_healthy = ollama_status.get("status") == "connected"
    
    return {
        "status": "healthy" if is_healthy else "degraded",
        "service": "PRISMA Backend",
        "version": "0.1.0",
        "components": {
            "api": {"status": "operational"},
            "llm": ollama_status,
            "cache": cache_status,
        },
        "message": "All systems operational" if is_healthy else "Some components unavailable"
    }


@app.get("/data/{filename}")
async def serve_data(filename: str):
    """Serve mock data files for UI"""
    from pathlib import Path
    import json
    
    data_path = Path(__file__).parent / "data" / filename
    if data_path.exists() and filename.endswith('.json'):
        with open(data_path) as f:
            return json.load(f)
    raise HTTPException(status_code=404, detail="File not found")


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
    
    # Initialize cache directory
    try:
        from pathlib import Path
        cache_dir = Path(__file__).parent / ".cache"
        cache_dir.mkdir(exist_ok=True)
        print(f"Cache directory: {cache_dir}")
    except Exception as e:
        print(f"Warning: Could not create cache directory: {e}")
    
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

