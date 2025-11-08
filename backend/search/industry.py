"""
PRISMA Industry Intelligence Module

Provides industry-specific trend signals and intelligence data.

Design:
- MVP: Returns hardcoded sample trends based on industry
- Production: Integrates with Google Programmable Search Engine

Integration:
- Called by external_signals.engine.build_signals()
- Signals feed into LLM reasoning layer
- Structured format compatible with DemandSignal
"""

import os
import requests
from typing import List, Dict, Any, Optional
from datetime import datetime


# ============================================================================
# Industry Trend Data (MVP - Hardcoded)
# ============================================================================

# Sample industry trends for MVP
# In production, this would come from APIs, databases, or custom search
INDUSTRY_TRENDS_DATABASE = {
    "construction": [
        {
            "trend_id": "const-001",
            "title": "Infrastructure spending increase in Asia-Pacific",
            "description": "Governments across APAC region announced $2.5T infrastructure investment plan for 2024-2026",
            "impact": "increase",
            "materials_affected": ["Steel", "Concrete", "Copper"],
            "confidence": 0.85,
            "source": "Industry Report",
            "date": "2025-11-01"
        },
        {
            "trend_id": "const-002",
            "title": "Green building materials adoption accelerating",
            "description": "Shift toward sustainable construction materials driving demand for recycled steel and eco-friendly concrete",
            "impact": "stable",
            "materials_affected": ["Steel", "Concrete"],
            "confidence": 0.75,
            "source": "Market Analysis",
            "date": "2025-10-28"
        }
    ],
    "infrastructure": [
        {
            "trend_id": "infra-001",
            "title": "Smart city projects expanding globally",
            "description": "Over 200 smart city initiatives launched worldwide, requiring advanced infrastructure materials",
            "impact": "increase",
            "materials_affected": ["Steel", "Copper", "Fiber Optics"],
            "confidence": 0.80,
            "source": "Industry Report",
            "date": "2025-11-02"
        },
        {
            "trend_id": "infra-002",
            "title": "Bridge modernization programs in North America",
            "description": "$1.2 trillion allocated for aging bridge repairs and replacements",
            "impact": "increase",
            "materials_affected": ["Steel", "Concrete"],
            "confidence": 0.88,
            "source": "Government Policy",
            "date": "2025-10-25"
        }
    ],
    "manufacturing": [
        {
            "trend_id": "mfg-001",
            "title": "Automotive industry electrification",
            "description": "EV production ramping up, changing metal demand mix toward copper and aluminum",
            "impact": "increase",
            "materials_affected": ["Copper", "Aluminum", "Lithium"],
            "confidence": 0.90,
            "source": "Industry Report",
            "date": "2025-11-03"
        },
        {
            "trend_id": "mfg-002",
            "title": "Supply chain reshoring trend continues",
            "description": "Manufacturers bringing production closer to home markets, increasing regional material demand",
            "impact": "increase",
            "materials_affected": ["Steel", "Aluminum", "Plastics"],
            "confidence": 0.78,
            "source": "Market Analysis",
            "date": "2025-10-30"
        }
    ],
    "energy": [
        {
            "trend_id": "energy-001",
            "title": "Renewable energy infrastructure buildout",
            "description": "Solar and wind farm construction at record pace, driving demand for specialty materials",
            "impact": "increase",
            "materials_affected": ["Steel", "Copper", "Aluminum"],
            "confidence": 0.85,
            "source": "Industry Report",
            "date": "2025-11-01"
        },
        {
            "trend_id": "energy-002",
            "title": "Grid modernization projects",
            "description": "Electrical grid upgrades to support renewable integration and EV charging infrastructure",
            "impact": "increase",
            "materials_affected": ["Copper", "Aluminum"],
            "confidence": 0.82,
            "source": "Government Policy",
            "date": "2025-10-27"
        }
    ],
    "general": [
        {
            "trend_id": "gen-001",
            "title": "Global economic recovery continues",
            "description": "Steady GDP growth supporting infrastructure and manufacturing demand",
            "impact": "increase",
            "materials_affected": ["Steel", "Copper", "Aluminum", "Concrete"],
            "confidence": 0.70,
            "source": "Economic Outlook",
            "date": "2025-11-04"
        }
    ]
}


# ============================================================================
# Google Programmable Search Engine Configuration
# ============================================================================

GOOGLE_SEARCH_API_KEY = os.getenv("GOOGLE_SEARCH_API_KEY", "")
GOOGLE_SEARCH_ENGINE_ID = os.getenv("GOOGLE_SEARCH_ENGINE_ID", "")
GOOGLE_SEARCH_BASE_URL = "https://www.googleapis.com/customsearch/v1"


def search_google(query: str, num_results: int = 5) -> List[Dict[str, Any]]:
    """
    Search Google Programmable Search Engine for industry trends.
    
    Args:
        query: Search query
        num_results: Number of results to return
    
    Returns:
        List of search results with title, snippet, link
    """
    if not GOOGLE_SEARCH_API_KEY or not GOOGLE_SEARCH_ENGINE_ID:
        return []
    
    try:
        params = {
            "key": GOOGLE_SEARCH_API_KEY,
            "cx": GOOGLE_SEARCH_ENGINE_ID,
            "q": query,
            "num": min(num_results, 10)
        }
        
        response = requests.get(GOOGLE_SEARCH_BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        items = data.get("items", [])
        
        return [
            {
                "title": item.get("title", ""),
                "snippet": item.get("snippet", ""),
                "link": item.get("link", ""),
                "source": "google_search"
            }
            for item in items
        ]
    
    except Exception as e:
        print(f"Google Search error: {e}")
        return []


# ============================================================================
# Core Functions
# ============================================================================

def get_industry_trends(
    industry: str,
    materials: Optional[List[str]] = None,
    use_google_search: bool = True
) -> List[Dict[str, Any]]:
    """
    Get industry trend signals for a specific industry/sector.
    
    Implementation:
    - Uses Google Programmable Search Engine if configured
    - Falls back to hardcoded trends if search unavailable
    - Filters by industry and optionally by materials
    
    Args:
        industry: Industry name (e.g., "construction", "infrastructure", "manufacturing")
        materials: Optional list of materials to filter trends
        use_google_search: Whether to use Google Search (default: True)
    
    Returns:
        List of industry trend dictionaries
    
    Example:
        >>> trends = get_industry_trends("construction", materials=["Steel"])
        >>> for trend in trends:
        ...     print(trend['title'])
    """
    
    trends = []
    
    # Try Google Search if configured
    if use_google_search and GOOGLE_SEARCH_API_KEY and GOOGLE_SEARCH_ENGINE_ID:
        # Build search query
        query_parts = [f"{industry} industry"]
        if materials:
            query_parts.append(f"{', '.join(materials)} materials")
        query_parts.append("demand trends 2025")
        
        query = " ".join(query_parts)
        search_results = search_google(query, num_results=5)
        
        # Convert search results to trend format
        for result in search_results:
            trends.append({
                "trend_id": f"google-{hash(result['link']) % 10000}",
                "title": result["title"],
                "description": result["snippet"],
                "impact": "increase",  # Default, LLM can refine
                "materials_affected": materials or ["General"],
                "confidence": 0.70,
                "source": "Google Search",
                "link": result["link"],
                "date": datetime.now().strftime("%Y-%m-%d")
            })
    
    # Fallback to hardcoded trends
    if not trends:
        industry_key = industry.lower().strip()
        trends = INDUSTRY_TRENDS_DATABASE.get(
            industry_key,
            INDUSTRY_TRENDS_DATABASE.get("general", [])
        ).copy()
    
    # Filter by materials if specified
    if materials:
        normalized_materials = [m.strip().title() for m in materials]
        filtered_trends = []
        
        for trend in trends:
            trend_materials = trend.get("materials_affected", [])
            if any(mat in normalized_materials for mat in trend_materials):
                filtered_trends.append(trend)
        
        return filtered_trends
    
    return trends


def get_industry_signals(
    industry: str,
    company_id: str,
    materials: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Convert industry trends into signal format compatible with external_signals.
    
    This function transforms industry trends into the DemandSignal-compatible
    format used by the external_signals engine.
    
    Args:
        industry: Industry name
        company_id: Company identifier
        materials: Optional list of materials to filter
    
    Returns:
        Dictionary with structure similar to external_signals output
    
    Example:
        >>> signals = get_industry_signals("construction", "abc-corp", ["Steel"])
        >>> print(signals['signals'][0]['material'])
        "Steel"
    """
    
    # Get raw trends
    trends = get_industry_trends(industry, materials)
    
    # Convert to signal format
    signals = []
    
    for trend in trends:
        # Create a signal for each affected material
        for material in trend.get("materials_affected", []):
            # Skip if materials filter doesn't match
            if materials and material not in [m.strip().title() for m in materials]:
                continue
            
            # Map impact to demand direction
            impact = trend.get("impact", "stable")
            demand_score = {
                "increase": 0.75,
                "decrease": 0.25,
                "stable": 0.50
            }.get(impact, 0.50)
            
            signal = {
                "company_id": company_id,
                "region": "Global",  # Industry trends are typically global
                "material": material,
                "material_category": "Industry Intelligence",
                "horizon": "next_quarter",
                "demand_direction": impact,
                "demand_score": demand_score,
                "confidence": trend.get("confidence", 0.70),
                "drivers": [
                    trend.get("title", "Industry trend"),
                    f"Source: {trend.get('source', 'Industry Report')}"
                ],
                "source": "industry_intelligence",
                "last_updated": datetime.now().isoformat()
            }
            
            signals.append(signal)
    
    return {
        "company_id": company_id,
        "industry": industry,
        "signals": signals,
        "data_source": "industry_intelligence",
        "generated_at": datetime.now().isoformat()
    }


def search_industry_trends(
    query: str,
    limit: int = 5
) -> List[Dict[str, Any]]:
    """
    Search industry trends by query string.
    
    MVP Implementation:
    - Simple keyword matching across all trends
    
    Future Production:
    - Full-text search with ranking
    - Integration with search engines
    - Semantic search capabilities
    
    Args:
        query: Search query
        limit: Maximum number of results
    
    Returns:
        List of matching trends
    
    Example:
        >>> results = search_industry_trends("steel infrastructure")
        >>> print(len(results))
        3
    """
    
    query_lower = query.lower()
    matching_trends = []
    
    # Search across all industry categories
    for industry, trends in INDUSTRY_TRENDS_DATABASE.items():
        for trend in trends:
            # Check if query matches title, description, or materials
            title = trend.get("title", "").lower()
            description = trend.get("description", "").lower()
            materials = " ".join(trend.get("materials_affected", [])).lower()
            
            if (query_lower in title or 
                query_lower in description or 
                query_lower in materials):
                
                # Add industry context to result
                trend_with_context = trend.copy()
                trend_with_context["industry"] = industry
                matching_trends.append(trend_with_context)
    
    # Return limited results
    return matching_trends[:limit]


def get_available_industries() -> List[str]:
    """
    Get list of available industries in the database.
    
    Returns:
        List of industry names
    
    Example:
        >>> industries = get_available_industries()
        >>> print(industries)
        ['construction', 'infrastructure', 'manufacturing', 'energy', 'general']
    """
    return list(INDUSTRY_TRENDS_DATABASE.keys())


# ============================================================================
# TODO: Future Production Enhancements
# ============================================================================

"""
Future enhancements for production:

1. Custom Search Engine Integration:
   - Google Programmable Search Engine API
   - Bing Custom Search API
   - Curated industry sources

2. News API Integration:
   - NewsAPI.org
   - GNews API
   - Industry-specific news feeds

3. Research Database Integration:
   - Market research APIs
   - Industry report databases
   - Trade association data

4. Real-time Updates:
   - WebSocket for live trend updates
   - Scheduled crawlers for fresh data
   - Event-driven trend detection

5. Machine Learning:
   - Trend scoring and ranking
   - Semantic search
   - Automated trend extraction from text

6. Caching Strategy:
   - Redis cache for frequently accessed trends
   - TTL-based refresh
   - Background updates

Example future implementation:

def get_industry_trends_production(industry: str) -> List[Dict]:
    # Check cache first
    cached = redis.get(f"industry_trends:{industry}")
    if cached:
        return json.loads(cached)
    
    # Query custom search engine
    search_results = custom_search_api.query(
        q=f"{industry} materials demand trends",
        dateRestrict="m1"  # Last month
    )
    
    # Process and structure results
    trends = process_search_results(search_results)
    
    # Cache for 1 hour
    redis.setex(
        f"industry_trends:{industry}",
        3600,
        json.dumps(trends)
    )
    
    return trends
"""


# ============================================================================
# Module Exports
# ============================================================================

__all__ = [
    "get_industry_trends",
    "get_industry_signals",
    "search_industry_trends",
    "get_available_industries",
]

