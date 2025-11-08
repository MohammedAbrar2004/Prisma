"""
PRISMA Analysis API Router

This module provides REST API endpoints for LLM-powered demand analysis.

Design:
- Thin routing layer - delegates to llm.engine
- Wires together: company profile + forecasts + signals → LLM → recommendations
- Clean, RESTful interface

Integration:
- Loads mock data from backend/data/ (MVP)
- Calls external_signals.engine.build_signals()
- Calls llm.engine.analyze_prisma()
- Returns structured JSON response
"""

from typing import Optional, Dict, Any
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

import sys
import json
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import our modules
from external_signals import build_signals
from llm import analyze_prisma, test_ollama_connection
from forecast import generate_forecasts


# ============================================================================
# Router Setup
# ============================================================================

router = APIRouter(
    prefix="/analyze",
    tags=["analyze"],
    responses={
        404: {"description": "Not found"},
        500: {"description": "Internal server error"}
    },
)


# ============================================================================
# Request/Response Models
# ============================================================================

class AnalyzeRequest(BaseModel):
    """
    Request model for company analysis.
    
    Fields:
        company_id: Company identifier (must exist in mock data or DB)
        question: Optional specific question to answer
        region: Optional region filter for signals
        materials: Optional list of materials to focus on
        industry: Optional industry/sector for trend analysis
        horizon: Time horizon for analysis (default: "next_month")
        use_real_apis: Whether to use real external APIs (default: True)
    """
    
    company_id: str = Field(
        ..., 
        description="Company identifier",
        example="abc-infra"
    )
    question: Optional[str] = Field(
        None,
        description="Specific question to answer about procurement/demand",
        example="Should we increase steel inventory for Q1?"
    )
    region: Optional[str] = Field(
        None,
        description="Region filter for signals",
        example="Maharashtra"
    )
    materials: Optional[list[str]] = Field(
        None,
        description="List of materials to focus analysis on",
        example=["Steel", "Copper"]
    )
    industry: Optional[str] = Field(
        None,
        description="Industry/sector for trend analysis",
        example="construction"
    )
    horizon: str = Field(
        "next_month",
        description="Time horizon for analysis",
        example="next_month"
    )
    use_real_apis: bool = Field(
        True,
        description="Whether to use real external APIs"
    )


# ============================================================================
# API Endpoints
# ============================================================================

@router.post("/")
async def analyze_company(req: AnalyzeRequest):
    """
    Analyze company demand and generate procurement recommendations.
    
    This endpoint orchestrates the full PRISMA analysis pipeline:
    
    1. **Load Company Profile** - from mock_requirements.json
    2. **Load Forecasts** - from mock_forecasts.json
    3. **Fetch External Signals** - commodity prices, weather, industry trends
    4. **LLM Analysis** - generate insights and recommendations
    5. **Return Results** - structured JSON with actionable insights
    
    **Request Body:**
    ```json
    {
      "company_id": "abc-infra",
      "question": "Should we increase steel procurement?",
      "region": "Maharashtra",
      "materials": ["Steel", "Copper"],
      "industry": "construction",
      "horizon": "next_month"
    }
    ```
    
    **Response:**
    ```json
    {
      "company_id": "abc-infra",
      "summary": "Steel demand expected to increase 15% with moderate price risk...",
      "recommended_actions": [
        {
          "material": "Steel",
          "action": "Increase inventory by 20%",
          "reason": "Price trending upward with strong demand signals"
        }
      ],
      "risks": [
        {
          "material": "Steel",
          "risk_level": "medium",
          "drivers": ["Price volatility", "Supply constraints"]
        }
      ],
      "watchlist_materials": [
        {
          "material": "Copper",
          "reason": "Moderate demand increase expected"
        }
      ],
      "data_sources": ["mock", "commodity_api", "industry_intelligence"],
      "generated_at": "2025-11-08T10:00:00"
    }
    ```
    
    **Error Responses:**
    - 404: Company not found
    - 500: Analysis failed (Ollama not available, invalid data, etc.)
    """
    
    try:
        # Step 1: Load company profile
        company_profile = load_company_profile(req.company_id)
        if not company_profile:
            raise HTTPException(
                status_code=404,
                detail=f"Company profile not found for company_id: {req.company_id}"
            )
        
        # Step 2: Generate forecasts dynamically
        forecasts = generate_forecasts(
            company_profile=company_profile,
            horizon=req.horizon
        )
        
        # Step 3: Fetch external signals
        signals = build_signals(
            company_id=req.company_id,
            region=req.region,
            materials=req.materials,
            horizon=req.horizon,
            use_real_apis=req.use_real_apis,
            industry=req.industry
        )
        
        # Step 4: Call LLM for analysis
        analysis_result = analyze_prisma(
            company_profile=company_profile,
            forecasts=forecasts,
            signals=signals,
            question=req.question
        )
        
        # Step 5: Enrich response with metadata
        response = {
            **analysis_result,
            "company_id": req.company_id,
            "data_sources": signals.get("data_sources", []),
            "generated_at": signals.get("generated_at"),
            "horizon": req.horizon,
            "region": req.region,
            "industry": req.industry
        }
        
        return JSONResponse(content=response)
    
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    
    except ConnectionError as e:
        # LLM service unavailable
        raise HTTPException(
            status_code=503,
            detail=str(e)
        )
    
    except ValueError as e:
        # Invalid data or parsing error
        raise HTTPException(
            status_code=400,
            detail=f"Invalid data: {str(e)}"
        )
    
    except Exception as e:
        # Unexpected error
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )


@router.get("/health")
async def analyze_health():
    """
    Health check for analysis service.
    
    Checks:
    - Ollama connectivity
    - Mock data availability
    
    Returns:
    ```json
    {
      "status": "healthy",
      "ollama": {
        "status": "connected",
        "model": "llama3"
      },
      "data": {
        "company_profiles": true,
        "forecasts": true
      }
    }
    ```
    """
    
    try:
        # Check Ollama connection
        ollama_status = test_ollama_connection()
        
        # Check mock data availability
        data_path = Path(__file__).parent.parent / "data"
        requirements_exist = (data_path / "mock_requirements.json").exists()
        forecasts_exist = (data_path / "mock_forecasts.json").exists()
        
        overall_healthy = (
            ollama_status.get("status") == "connected" and
            requirements_exist and
            forecasts_exist
        )
        
        return JSONResponse(content={
            "status": "healthy" if overall_healthy else "degraded",
            "ollama": ollama_status,
            "data": {
                "company_profiles": requirements_exist,
                "forecasts": forecasts_exist
            },
            "message": "All systems operational" if overall_healthy else "Some components unavailable"
        })
    
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "error": str(e)
            }
        )


@router.post("/ask")
async def ask_question(req: AnalyzeRequest):
    """
    Free-form Q&A endpoint (same as /analyze but emphasizes question).
    
    This is an alias to /analyze that emphasizes the conversational aspect.
    Use this when you have a specific question about procurement or demand.
    
    Example questions:
    - "What are the biggest risks to our steel supply chain?"
    - "Should we accelerate copper procurement for Q1?"
    - "Which materials need the most attention right now?"
    """
    
    # Just call the main analyze endpoint
    return await analyze_company(req)


class DirectAnalyzeRequest(BaseModel):
    """Request model for direct LLM analysis"""
    company_profile: Dict[str, Any]
    forecasts: Dict[str, Any]
    signals: Dict[str, Any]
    question: Optional[str] = None


@router.post("/direct")
async def analyze_direct(req: DirectAnalyzeRequest):
    """
    Direct LLM analysis with custom data (for UI testing).
    
    Bypasses data loading, accepts raw JSON directly.
    If forecasts not provided, generates them from company_profile.
    """
    try:
        from llm import analyze_prisma
        from search.industry import get_industry_trends
        
        # Generate forecasts if not provided
        if not req.forecasts or not req.forecasts.get("forecasts"):
            req.forecasts = generate_forecasts(
                company_profile=req.company_profile,
                horizon="next_month"
            )
        
        # Enhance signals with Google Search if industry info available
        if not req.signals or not req.signals.get("signals"):
            # Extract industry from company profile or use default
            industry = req.company_profile.get("industry", "construction")
            materials = []
            
            # Extract materials from projects
            for project in req.company_profile.get("projects", []):
                for material in project.get("materials", []):
                    mat_name = material.get("name", "")
                    if mat_name and mat_name not in materials:
                        materials.append(mat_name)
            
            # Get industry trends via Google Search
            trends = get_industry_trends(
                industry=industry,
                materials=materials if materials else None,
                use_google_search=True
            )
            
            # Convert trends to signals format
            trend_signals = []
            if trends:
                for trend in trends:
                    for material in trend.get("materials_affected", materials or ["General"]):
                        trend_signals.append({
                            "material": material,
                            "region": "Global",
                            "demand_direction": trend.get("impact", "stable"),
                            "demand_score": 0.70,
                            "confidence": trend.get("confidence", 0.70),
                            "drivers": [trend.get("title", ""), trend.get("description", "")[:100]],
                            "source": "google_search"
                        })
            
            # Ensure signals always has a valid structure
            req.signals = {
                "signals": trend_signals if trend_signals else [],
                "data_sources": ["google_search"] if trend_signals else []
            }
        
        # Ensure signals is never None
        if not req.signals:
            req.signals = {"signals": [], "data_sources": []}
        
        result = analyze_prisma(
            company_profile=req.company_profile,
            forecasts=req.forecasts,
            signals=req.signals,
            question=req.question
        )
        
        return JSONResponse(content=result)
    
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        # Log the full error for debugging
        import traceback
        error_details = traceback.format_exc()
        print(f"ERROR in /analyze/direct: {str(e)}")
        print(f"Traceback:\n{error_details}")
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}. Check server logs for details."
        )


# ============================================================================
# Helper Functions
# ============================================================================

def load_company_profile(company_id: str) -> dict:
    """
    Load company profile from mock data.
    
    In production, this would query a database or service.
    For MVP, we read from backend/data/mock_requirements.json.
    
    Args:
        company_id: Company identifier
    
    Returns:
        Company profile dict or None if not found
    """
    
    try:
        data_path = Path(__file__).parent.parent / "data" / "mock_requirements.json"
        
        with open(data_path, "r") as f:
            data = json.load(f)
        
        # Check if company_id matches
        if data.get("company_id") == company_id:
            return data
        
        # For MVP, we only have one company
        # Return it anyway if it exists
        if data.get("company_id"):
            print(f"Warning: Requested {company_id} but returning {data.get('company_id')}")
            return data
        
        return None
    
    except FileNotFoundError:
        print(f"Error: mock_requirements.json not found at {data_path}")
        return None
    
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in mock_requirements.json: {e}")
        return None


def load_forecasts(company_id: str) -> dict:
    """
    Load demand forecasts from mock data.
    
    In production, this would query forecast engine or database.
    For MVP, we read from backend/data/mock_forecasts.json.
    
    Args:
        company_id: Company identifier
    
    Returns:
        Forecasts dict or None if not found
    """
    
    try:
        data_path = Path(__file__).parent.parent / "data" / "mock_forecasts.json"
        
        with open(data_path, "r") as f:
            data = json.load(f)
        
        # Check if company_id matches
        if data.get("company_id") == company_id:
            return data
        
        # For MVP, return available data
        if data.get("company_id"):
            print(f"Warning: Requested {company_id} but returning {data.get('company_id')}")
            return data
        
        return None
    
    except FileNotFoundError:
        print(f"Error: mock_forecasts.json not found at {data_path}")
        return None
    
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in mock_forecasts.json: {e}")
        return None


# ============================================================================
# Router Metadata
# ============================================================================

def get_router():
    """
    Returns the configured router for mounting in the main FastAPI app.
    
    Usage in main.py:
    ```python
    from routes.analyze import router as analyze_router
    app.include_router(analyze_router)
    ```
    """
    return router

