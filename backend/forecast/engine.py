"""
PRISMA Forecast Engine

Generates material demand forecasts from company requirements.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import json


class ForecastConfig:
    """Forecast generation configuration"""
    DEFAULT_GROWTH_RATE = 0.10  # 10% growth
    DEFAULT_CONFIDENCE = 0.75
    HORIZON_MONTHS = 1


def generate_forecasts(
    company_profile: Dict[str, Any],
    horizon: str = "next_month",
    growth_rate: Optional[float] = None
) -> Dict[str, Any]:
    """
    Generate demand forecasts from company requirements.
    
    Args:
        company_profile: Company profile with projects and materials
        horizon: Time horizon (next_month, next_quarter)
        growth_rate: Growth rate multiplier (default: 0.10)
    
    Returns:
        Forecasts dictionary with predictions
    """
    company_id = company_profile.get("company_id", "unknown")
    projects = company_profile.get("projects", [])
    
    if not projects:
        return {
            "company_id": company_id,
            "forecast_date": datetime.now().isoformat(),
            "horizon": horizon,
            "method": "rule_based",
            "forecasts": [],
            "notes": "No projects found"
        }
    
    forecasts = []
    growth = growth_rate or ForecastConfig.DEFAULT_GROWTH_RATE
    
    # Calculate target month
    if horizon == "next_month":
        target_date = datetime.now() + timedelta(days=30)
    elif horizon == "next_quarter":
        target_date = datetime.now() + timedelta(days=90)
    else:
        target_date = datetime.now() + timedelta(days=30)
    
    target_month = target_date.strftime("%Y-%m")
    
    for project in projects:
        project_id = project.get("id", "unknown")
        materials = project.get("materials", [])
        status = project.get("status", "active")
        
        # Adjust growth based on project status
        status_multiplier = {
            "active": 1.0,
            "planning": 0.5,
            "on_hold": 0.0,
            "completed": 0.0
        }.get(status.lower(), 1.0)
        
        for material in materials:
            material_name = material.get("name", "")
            current_usage = material.get("current_month_usage", 0)
            unit = material.get("unit", "units")
            
            if current_usage <= 0:
                continue
            
            # Generate forecast
            predicted_demand = current_usage * (1 + growth * status_multiplier)
            
            # Confidence based on project status
            confidence = ForecastConfig.DEFAULT_CONFIDENCE
            if status.lower() == "planning":
                confidence = 0.60
            elif status.lower() == "on_hold":
                confidence = 0.30
            
            forecasts.append({
                "project_id": project_id,
                "material": material_name,
                "current_usage": current_usage,
                "predicted_demand": round(predicted_demand, 2),
                "unit": unit,
                "confidence": confidence,
                "month": target_month
            })
    
    return {
        "company_id": company_id,
        "forecast_date": datetime.now().isoformat(),
        "horizon": horizon,
        "method": "rule_based_mvp",
        "forecasts": forecasts,
        "notes": f"Generated from {len(projects)} projects using {growth*100:.0f}% growth rule"
    }

