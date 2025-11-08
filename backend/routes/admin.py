"""
PRISMA Admin API Router

Administrative endpoints for system management and monitoring.

Endpoints:
- Cache management
- System statistics
- Health diagnostics
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

# ============================================================================
# Router Setup
# ============================================================================

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    responses={
        404: {"description": "Not found"},
        500: {"description": "Internal server error"}
    },
)


# ============================================================================
# Cache Management Endpoints
# ============================================================================

@router.get("/cache/stats")
async def get_cache_stats():
    """
    Get cache statistics.
    
    Returns information about:
    - Cache size (entries and bytes)
    - Cache directory location
    - Cache enabled status
    
    Example Response:
    ```json
    {
      "enabled": true,
      "cache_dir": "S:/Projects/Prisma/backend/.cache",
      "total_entries": 42,
      "total_size_bytes": 123456,
      "total_size_mb": 0.12
    }
    ```
    """
    try:
        from utils.cache_manager import cache_stats
        stats = cache_stats()
        return JSONResponse(content=stats)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get cache stats: {str(e)}"
        )


@router.delete("/cache/clear")
async def clear_cache():
    """
    Clear all cached data.
    
    Use this to:
    - Force fresh API calls
    - Clear stale data
    - Free up disk space
    - Reset after configuration changes
    
    ⚠️ Warning: This will slow down the next few requests as caches rebuild.
    
    Returns:
    ```json
    {
      "message": "Cache cleared successfully",
      "entries_deleted": 42
    }
    ```
    """
    try:
        from utils.cache_manager import clear_cache
        entries_deleted = clear_cache()
        return JSONResponse(content={
            "message": "Cache cleared successfully",
            "entries_deleted": entries_deleted
        })
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to clear cache: {str(e)}"
        )


class DeleteCacheKeyRequest(BaseModel):
    key: str


@router.delete("/cache/key")
async def delete_cache_key(req: DeleteCacheKeyRequest):
    """
    Delete a specific cache key.
    
    Use this to invalidate specific cached data without clearing everything.
    
    Request Body:
    ```json
    {
      "key": "google_search:construction industry:5"
    }
    ```
    
    Returns:
    ```json
    {
      "message": "Cache key deleted",
      "key": "google_search:construction industry:5"
    }
    ```
    """
    try:
        from utils.cache_manager import CacheManager
        cache = CacheManager()
        deleted = cache.delete(req.key)
        
        if deleted:
            return JSONResponse(content={
                "message": "Cache key deleted",
                "key": req.key
            })
        else:
            raise HTTPException(
                status_code=404,
                detail=f"Cache key not found: {req.key}"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete cache key: {str(e)}"
        )


# ============================================================================
# System Diagnostics
# ============================================================================

@router.get("/diagnostics")
async def system_diagnostics():
    """
    Comprehensive system diagnostics.
    
    Checks all major components:
    - LLM (Ollama)
    - Cache system
    - External APIs
    - Data files
    
    Useful for troubleshooting issues.
    
    Returns:
    ```json
    {
      "llm": {
        "status": "connected",
        "model": "llama3",
        "url": "http://localhost:11434"
      },
      "cache": {
        "enabled": true,
        "entries": 42,
        "size_mb": 0.12
      },
      "data_files": {
        "mock_requirements": true,
        "mock_forecasts": true
      },
      "api_keys": {
        "metalpriceapi": false,
        "google_search": true
      }
    }
    ```
    """
    try:
        from llm import test_ollama_connection, LLMConfig
        from utils.cache_manager import cache_stats
        import os
        
        # Check LLM
        try:
            llm_status = test_ollama_connection()
            llm_status["url"] = LLMConfig.OLLAMA_BASE_URL
        except:
            llm_status = {"status": "error", "message": "Ollama not available"}
        
        # Check cache
        cache_status = cache_stats()
        
        # Check data files
        data_path = Path(__file__).parent.parent / "data"
        data_files_status = {
            "mock_requirements": (data_path / "mock_requirements.json").exists(),
            "mock_forecasts": (data_path / "mock_forecasts.json").exists()
        }
        
        # Check API keys (don't expose values)
        api_keys_status = {
            "metalpriceapi": bool(os.getenv("METALPRICEAPI_KEY")),
            "commodityapi": bool(os.getenv("COMMODITYAPI_KEY")),
            "weatherapi": bool(os.getenv("WEATHERAPI_KEY")),
            "google_search": bool(os.getenv("GOOGLE_SEARCH_API_KEY"))
        }
        
        return JSONResponse(content={
            "llm": llm_status,
            "cache": cache_status,
            "data_files": data_files_status,
            "api_keys": api_keys_status,
            "timestamp": __import__('datetime').datetime.now().isoformat()
        })
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Diagnostics failed: {str(e)}"
        )


# ============================================================================
# Router Metadata
# ============================================================================

def get_router():
    """
    Returns the configured router for mounting in the main FastAPI app.
    """
    return router

