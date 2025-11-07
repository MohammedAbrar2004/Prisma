"""
Web Enrichment API Router

Provides /ext/enrich endpoint for web-based procurement signal enrichment
"""

from typing import Optional
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from web_enrichment import WebEnrichmentEngine
from web_enrichment.models import EnrichmentRequest, EnrichmentResponse
from web_enrichment.cse_integration import CustomSearchEngine


# ============================================================================
# Router Setup
# ============================================================================

router = APIRouter(
    prefix="/ext",
    tags=["enrichment"],
    responses={404: {"description": "Not found"}},
)

# Initialize engine (singleton)
_engine: Optional[WebEnrichmentEngine] = None
_cse: Optional[CustomSearchEngine] = None


def get_engine() -> WebEnrichmentEngine:
    """Get or create enrichment engine"""
    global _engine
    if _engine is None:
        _engine = WebEnrichmentEngine(max_workers=4)
    return _engine


def get_cse() -> CustomSearchEngine:
    """Get or create CSE client"""
    global _cse
    if _cse is None:
        _cse = CustomSearchEngine()
    return _cse


# ============================================================================
# API Endpoints
# ============================================================================

@router.post("/enrich", response_model=EnrichmentResponse)
async def enrich_signals(request: EnrichmentRequest):
    """
    Enrich procurement signals with web-scraped data
    
    This endpoint combines structured API data with web-scraped information from
    whitelisted public sources to provide comprehensive procurement intelligence.
    
    **Data Sources:**
    - India Meteorological Department (IMD) - Weather warnings
    - Public Works Department (PWD) - Traffic advisories
    - Fuel price trackers - Diesel/petrol prices
    - Port authorities - Logistics updates
    - Google Custom Search (optional) - Discovery
    
    **Features:**
    - Concurrent scraping with rate limiting
    - Robots.txt compliance
    - Caching (24h TTL)
    - Relevance scoring
    - Impact analysis
    - Signal aggregation
    
    **Example Request:**
    ```json
    {
      "site": "Mumbai Metro Project",
      "materials": ["Steel", "Concrete", "Copper"],
      "region": "Maharashtra",
      "time_window_days": 30,
      "use_scrapers": true,
      "use_cse": false,
      "min_relevance": 0.5
    }
    ```
    
    **Example Response:**
    ```json
    {
      "request_id": "req_20251107_001",
      "site": "Mumbai Metro Project",
      "signals": [
        {
          "signal_id": "imd_001",
          "signal_type": "weather",
          "title": "Heavy rainfall warning",
          "relevance_score": 0.85,
          "impact_score": 0.75,
          "effects": ["lead_time_increased", "demand_increased"]
        }
      ],
      "aggregates": {
        "total_signals": 15,
        "by_type": {"weather": 5, "traffic": 3},
        "avg_relevance": 0.72
      }
    }
    ```
    """
    try:
        engine = get_engine()
        response = engine.enrich(request)
        
        # Add CSE results if requested
        if request.use_cse:
            cse = get_cse()
            if cse.is_configured():
                cse_signals = cse.search(
                    query=f"procurement {request.site}",
                    region=request.region,
                    materials=request.materials,
                    max_results=5
                )
                response.signals.extend(cse_signals)
                if cse_signals:
                    response.sources_used.append("Google Custom Search")
        
        return response
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Enrichment error: {str(e)}"
        )


@router.get("/enrich/{site}")
async def enrich_signals_get(
    site: str,
    materials: str = Query(..., description="Comma-separated materials (e.g., 'Steel,Concrete')"),
    region: Optional[str] = Query(None, description="Geographic region"),
    time_window_days: int = Query(30, ge=1, le=365),
    use_scrapers: bool = Query(True),
    use_cse: bool = Query(False),
    use_cache: bool = Query(True),
    mock_mode: bool = Query(False),
    min_relevance: float = Query(0.3, ge=0.0, le=1.0)
):
    """
    GET version of enrichment endpoint
    
    Simpler interface for quick testing:
    ```
    GET /ext/enrich/Mumbai%20Metro?materials=Steel,Concrete&region=Maharashtra
    ```
    """
    try:
        # Parse materials
        materials_list = [m.strip() for m in materials.split(",")]
        
        # Create request
        request = EnrichmentRequest(
            site=site,
            materials=materials_list,
            region=region,
            time_window_days=time_window_days,
            use_scrapers=use_scrapers,
            use_cse=use_cse,
            use_cache=use_cache,
            mock_mode=mock_mode,
            min_relevance=min_relevance
        )
        
        # Process
        engine = get_engine()
        response = engine.enrich(request)
        
        # Add CSE if requested
        if use_cse:
            cse = get_cse()
            if cse.is_configured():
                cse_signals = cse.search(
                    query=f"procurement {site}",
                    region=region,
                    materials=materials_list,
                    max_results=5
                )
                response.signals.extend(cse_signals)
                if cse_signals:
                    response.sources_used.append("Google Custom Search")
        
        return JSONResponse(content=response.model_dump(mode='json'))
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Enrichment error: {str(e)}"
        )


@router.get("/health")
async def health_check():
    """
    Health check for enrichment module
    
    Returns:
    - Engine status
    - Scraper count
    - CSE configuration status
    """
    try:
        engine = get_engine()
        cse = get_cse()
        
        return JSONResponse(content={
            "status": "healthy",
            "module": "web_enrichment",
            "scrapers_available": len(engine.scrapers),
            "scraper_names": list(engine.scrapers.keys()),
            "cse_configured": cse.is_configured(),
            "max_workers": engine.max_workers
        })
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Health check failed: {str(e)}"
        )


@router.get("/sources")
async def list_sources():
    """
    List all available data sources
    
    Returns information about:
    - Registered scrapers
    - Whitelisted domains
    - CSE configuration
    """
    try:
        engine = get_engine()
        cse = get_cse()
        
        scrapers_info = []
        for name, scraper in engine.scrapers.items():
            scrapers_info.append({
                "name": name,
                "type": scraper.get_signal_type().value,
                "rate_limit": f"{scraper.rate_limiter.requests_per_minute} req/min",
                "cache_ttl": f"{scraper.cache_manager.ttl.total_seconds() / 3600:.0f} hours",
                "respects_robots": scraper.respect_robots
            })
        
        return JSONResponse(content={
            "scrapers": scrapers_info,
            "cse_whitelisted_domains": cse.WHITELISTED_DOMAINS if cse.is_configured() else [],
            "total_sources": len(scrapers_info) + (1 if cse.is_configured() else 0)
        })
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error listing sources: {str(e)}"
        )


@router.post("/clear-cache")
async def clear_cache():
    """
    Clear all cached scraper data
    
    Useful for:
    - Testing
    - Forcing fresh data fetch
    - Clearing stale cache
    """
    try:
        engine = get_engine()
        
        cleared_count = 0
        for scraper in engine.scrapers.values():
            try:
                scraper.cache_manager.clear()
                cleared_count += 1
            except Exception as e:
                print(f"Error clearing cache for {scraper.name}: {e}")
        
        return JSONResponse(content={
            "status": "success",
            "message": f"Cleared cache for {cleared_count} scrapers"
        })
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error clearing cache: {str(e)}"
        )


# ============================================================================
# Cleanup on shutdown
# ============================================================================

@router.on_event("shutdown")
async def shutdown_event():
    """Clean up resources on shutdown"""
    global _engine
    if _engine:
        _engine.close()


# ============================================================================
# Router metadata
# ============================================================================

def get_router():
    """
    Returns the configured router for mounting in the main FastAPI app.
    
    Usage in main.py:
    ```python
    from routes.enrichment import get_router
    app.include_router(get_router())
    ```
    """
    return router

