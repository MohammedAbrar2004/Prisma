"""
Data models for web enrichment module
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field, HttpUrl


class SignalType(str, Enum):
    """Type of procurement signal"""
    WEATHER = "weather"
    TRAFFIC = "traffic"
    DISASTER = "disaster"
    FUEL_PRICE = "fuel_price"
    SUPPLIER = "supplier"
    LOGISTICS = "logistics"
    PORT = "port"
    REGULATORY = "regulatory"
    MARKET = "market"


class SignalEffect(str, Enum):
    """Effect on procurement"""
    PRICE_INCREASE = "price_increase"
    PRICE_DECREASE = "price_decrease"
    AVAILABILITY_REDUCED = "availability_reduced"
    AVAILABILITY_INCREASED = "availability_increased"
    LEAD_TIME_INCREASED = "lead_time_increased"
    LEAD_TIME_DECREASED = "lead_time_decreased"
    RISK_INCREASED = "risk_increased"
    RISK_DECREASED = "risk_decreased"
    DEMAND_INCREASED = "demand_increased"
    DEMAND_DECREASED = "demand_decreased"


class EnrichmentSource(BaseModel):
    """Source of enrichment data"""
    name: str = Field(..., description="Source name (e.g., 'IMD', 'PWD Maharashtra')")
    type: str = Field(..., description="Source type (api, scraper, cse)")
    url: Optional[str] = Field(None, description="Source URL")
    last_updated: datetime = Field(default_factory=datetime.now)
    reliability_score: float = Field(0.7, ge=0.0, le=1.0, description="Source reliability (0-1)")


class EnrichmentSignal(BaseModel):
    """Individual enrichment signal from web/API sources"""
    
    # Core identification
    signal_id: str = Field(..., description="Unique signal identifier")
    signal_type: SignalType = Field(..., description="Type of signal")
    source: EnrichmentSource = Field(..., description="Data source")
    
    # Content
    title: str = Field(..., description="Signal title/headline")
    summary: str = Field(..., description="Brief summary of the signal")
    full_text: Optional[str] = Field(None, description="Full extracted text")
    url: Optional[str] = Field(None, description="Source URL")
    
    # Context
    region: Optional[str] = Field(None, description="Geographic region (e.g., 'Maharashtra')")
    location: Optional[str] = Field(None, description="Specific location")
    materials_affected: List[str] = Field(default_factory=list, description="Materials impacted")
    
    # Temporal
    published_date: Optional[datetime] = Field(None, description="Publication date")
    effective_date: Optional[datetime] = Field(None, description="When effect starts")
    expiry_date: Optional[datetime] = Field(None, description="When effect ends")
    
    # Scoring
    relevance_score: float = Field(0.5, ge=0.0, le=1.0, description="Relevance to query (0-1)")
    confidence_score: float = Field(0.5, ge=0.0, le=1.0, description="Confidence in signal (0-1)")
    impact_score: float = Field(0.5, ge=0.0, le=1.0, description="Potential impact (0-1)")
    
    # Effects
    effects: List[SignalEffect] = Field(default_factory=list, description="Procurement effects")
    effect_magnitude: Optional[float] = Field(None, description="Magnitude of effect (e.g., +15% price)")
    
    # Metadata
    extracted_at: datetime = Field(default_factory=datetime.now)
    tags: List[str] = Field(default_factory=list, description="Additional tags")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
    class Config:
        json_schema_extra = {
            "example": {
                "signal_id": "imd_2025_11_07_001",
                "signal_type": "weather",
                "source": {
                    "name": "India Meteorological Department",
                    "type": "scraper",
                    "url": "https://mausam.imd.gov.in",
                    "reliability_score": 0.95
                },
                "title": "Heavy rainfall warning for Maharashtra",
                "summary": "IMD issues orange alert for heavy to very heavy rainfall in Mumbai and surrounding areas for next 48 hours",
                "region": "Maharashtra",
                "materials_affected": ["Concrete", "Steel", "Cement"],
                "published_date": "2025-11-07T10:00:00",
                "relevance_score": 0.9,
                "confidence_score": 0.95,
                "impact_score": 0.8,
                "effects": ["lead_time_increased", "availability_reduced", "demand_increased"]
            }
        }


class EnrichmentRequest(BaseModel):
    """Request for web enrichment"""
    site: str = Field(..., description="Project site/location")
    materials: List[str] = Field(..., description="Materials to track")
    region: Optional[str] = Field(None, description="Geographic region")
    time_window_days: int = Field(30, ge=1, le=365, description="Time window in days")
    
    # Options
    use_scrapers: bool = Field(True, description="Enable web scraping")
    use_cse: bool = Field(False, description="Enable Google Custom Search")
    use_cache: bool = Field(True, description="Use cached data if available")
    mock_mode: bool = Field(False, description="Return mock data for testing")
    
    # Filters
    min_relevance: float = Field(0.3, ge=0.0, le=1.0, description="Minimum relevance score")
    signal_types: Optional[List[SignalType]] = Field(None, description="Filter by signal types")
    
    class Config:
        json_schema_extra = {
            "example": {
                "site": "Mumbai Metro Project",
                "materials": ["Steel", "Concrete", "Copper"],
                "region": "Maharashtra",
                "time_window_days": 30,
                "use_scrapers": True,
                "use_cse": False,
                "min_relevance": 0.5
            }
        }


class SignalAggregate(BaseModel):
    """Aggregated signal statistics"""
    total_signals: int = 0
    by_type: Dict[str, int] = Field(default_factory=dict)
    by_effect: Dict[str, int] = Field(default_factory=dict)
    avg_relevance: float = 0.0
    avg_confidence: float = 0.0
    avg_impact: float = 0.0
    high_impact_count: int = 0  # impact_score > 0.7
    materials_coverage: Dict[str, int] = Field(default_factory=dict)


class EnrichmentResponse(BaseModel):
    """Response from web enrichment"""
    request_id: str = Field(..., description="Unique request identifier")
    site: str
    region: Optional[str] = None
    materials: List[str]
    
    # Signals
    signals: List[EnrichmentSignal] = Field(default_factory=list)
    
    # Aggregates
    aggregates: SignalAggregate = Field(default_factory=SignalAggregate)
    
    # Metadata
    sources_used: List[str] = Field(default_factory=list)
    cache_hit: bool = False
    processing_time_ms: float = 0.0
    generated_at: datetime = Field(default_factory=datetime.now)
    
    class Config:
        json_schema_extra = {
            "example": {
                "request_id": "req_2025_11_07_001",
                "site": "Mumbai Metro Project",
                "region": "Maharashtra",
                "materials": ["Steel", "Concrete"],
                "signals": [],
                "aggregates": {
                    "total_signals": 15,
                    "by_type": {"weather": 5, "traffic": 3, "fuel_price": 2},
                    "avg_relevance": 0.75,
                    "high_impact_count": 8
                },
                "sources_used": ["IMD", "PWD Maharashtra", "Fuel Price API"],
                "processing_time_ms": 1250.5
            }
        }

