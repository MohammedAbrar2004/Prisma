"""
PRISMA Forecast API Router

Generates forecasts from company requirements.
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from forecast import generate_forecasts


router = APIRouter(
    prefix="/forecast",
    tags=["forecast"],
)


class ForecastRequest(BaseModel):
    """Request model for forecast generation"""
    company_profile: Dict[str, Any]
    horizon: str = Field("next_month", description="Time horizon")
    growth_rate: Optional[float] = Field(None, description="Growth rate (default: 0.10)")


@router.post("/generate")
async def generate_forecast_endpoint(req: ForecastRequest):
    """
    Generate forecasts from company profile.
    
    Takes company requirements and generates material demand predictions.
    """
    try:
        result = generate_forecasts(
            company_profile=req.company_profile,
            horizon=req.horizon,
            growth_rate=req.growth_rate
        )
        return JSONResponse(content=result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

