"""
PRISMA Signals API Router

This module provides REST API endpoints for accessing external demand signals.

Design:
- Thin routing layer - no business logic here
- All heavy lifting delegated to external_signals.engine
- Clean, RESTful interface
"""

from typing import Optional
from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import JSONResponse

# Import from our signals engine
import sys
from pathlib import Path

# Add parent directory to path so we can import from external_signals
sys.path.insert(0, str(Path(__file__).parent.parent))

from external_signals import build_signals, test_api_connections


# ============================================================================
# Router Setup
# ============================================================================

router = APIRouter(
    prefix="/signals",
    tags=["signals"],
    responses={404: {"description": "Not found"}},
)


# ============================================================================
# API Endpoints
# ============================================================================

@router.get("/{company_id}")
async def get_signals(
    company_id: str,
    region: Optional[str] = Query(None, description="Filter signals by region (e.g., 'Maharashtra')"),
    materials: Optional[str] = Query(None, description="Comma-separated list of materials (e.g., 'Steel,Copper')"),
    horizon: str = Query("next_month", description="Time horizon for signals"),
    use_real_apis: bool = Query(True, description="Whether to use real API calls (if configured)")
):
    """
    Get external demand signals for a company.
    
    This endpoint returns structured demand risk signals based on:
    - Commodity/metal price trends
    - Weather forecasts
    - Infrastructure activity indicators
    - Economic data
    
    **Parameters:**
    - `company_id`: Your company identifier
    - `region`: Optional region filter (e.g., "Maharashtra", "Gujarat")
    - `materials`: Optional comma-separated materials (e.g., "Steel,Copper,Aluminum")
    - `horizon`: Time horizon - "next_month", "next_quarter", etc.
    - `use_real_apis`: Set to false to use only mock data
    
    **Returns:**
    ```json
    {
      "company_id": "abc-corp",
      "horizon": "next_month",
      "region_filter": "Maharashtra",
      "signals": [
        {
          "region": "Maharashtra",
          "material": "Steel",
          "demand_direction": "increase",
          "demand_score": 0.82,
          "confidence": 0.85,
          "drivers": ["Steel price up 9%", "New infra projects"],
          ...
        }
      ],
      "data_sources": ["mock", "commodity_api", "weather_api"],
      "generated_at": "2025-11-07T19:00:00"
    }
    ```
    """
    
    try:
        # Parse materials if provided
        materials_list = None
        if materials:
            materials_list = [m.strip() for m in materials.split(",")]
        
        # Call the signals engine
        result = build_signals(
            company_id=company_id,
            region=region,
            materials=materials_list,
            horizon=horizon,
            use_real_apis=use_real_apis
        )
        
        return JSONResponse(content=result)
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating signals: {str(e)}"
        )


@router.get("/health/check")
async def health_check():
    """
    Health check endpoint - tests connectivity to external APIs.
    
    Useful for:
    - Debugging API configuration
    - Monitoring external service status
    - Validating API keys
    
    **Returns:**
    ```json
    {
      "status": "healthy",
      "apis": {
        "metalprice": "connected",
        "commodity": "not_configured",
        "weather": "connected",
        "worldbank": "connected"
      }
    }
    ```
    """
    
    try:
        api_status = test_api_connections()
        
        # Determine overall health
        configured_apis = [k for k, v in api_status.items() if v not in ["not_configured"]]
        healthy_apis = [k for k, v in api_status.items() if v == "connected"]
        
        overall_status = "healthy" if len(healthy_apis) >= 1 else "degraded"
        
        return JSONResponse(content={
            "status": overall_status,
            "apis": api_status,
            "summary": f"{len(healthy_apis)}/{len(configured_apis)} configured APIs responding"
        })
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Health check failed: {str(e)}"
        )


@router.get("/debug/mock/{company_id}")
async def get_mock_signals_debug(company_id: str):
    """
    Debug endpoint - returns only mock signals without any API calls.
    
    Useful for:
    - Testing without API keys
    - Understanding the signal format
    - Development/demo purposes
    """
    
    from external_signals import get_mock_signals
    
    try:
        result = get_mock_signals(company_id)
        return JSONResponse(content=result)
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating mock signals: {str(e)}"
        )


# ============================================================================
# Router metadata
# ============================================================================

def get_router():
    """
    Returns the configured router for mounting in the main FastAPI app.
    
    Usage in main.py:
    ```python
    from routes.signals import get_router
    app.include_router(get_router())
    ```
    """
    return router

