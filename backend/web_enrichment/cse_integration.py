"""
Google Custom Search Engine Integration

Discovers relevant content from whitelisted domains
"""

import os
import uuid
from datetime import datetime, timedelta
from typing import List, Optional
import requests

from .models import EnrichmentSignal, EnrichmentSource, SignalType, SignalEffect


class CustomSearchEngine:
    """
    Google Custom Search Engine integration for discovering signals
    
    Searches only whitelisted domains for relevant procurement information
    """
    
    # Whitelisted domains for CSE
    WHITELISTED_DOMAINS = [
        'mausam.imd.gov.in',
        'imd.gov.in',
        'pwd.maharashtra.gov.in',
        'gujaratpwd.gov.in',
        'indianports.gov.in',
        'jnport.gov.in',
        'mypetrolprice.com',
        'shipmin.gov.in'
    ]
    
    def __init__(self):
        self.api_key = os.getenv('GOOGLE_CSE_API_KEY', '')
        self.cse_id = os.getenv('GOOGLE_CSE_ID', '')
        self.base_url = 'https://www.googleapis.com/customsearch/v1'
    
    def is_configured(self) -> bool:
        """Check if CSE is configured"""
        return bool(self.api_key and self.cse_id)
    
    def search(
        self,
        query: str,
        region: Optional[str] = None,
        materials: Optional[List[str]] = None,
        max_results: int = 10
    ) -> List[EnrichmentSignal]:
        """
        Search for relevant signals using Google CSE
        
        Args:
            query: Search query
            region: Geographic region to focus on
            materials: Materials to search for
            max_results: Maximum number of results
            
        Returns:
            List of EnrichmentSignals from search results
        """
        if not self.is_configured():
            print("Google CSE not configured")
            return []
        
        # Build search query
        full_query = self._build_query(query, region, materials)
        
        # Restrict to whitelisted domains
        site_restrict = ' OR '.join([f'site:{domain}' for domain in self.WHITELISTED_DOMAINS])
        full_query = f"{full_query} ({site_restrict})"
        
        signals = []
        
        try:
            # Make API request
            params = {
                'key': self.api_key,
                'cx': self.cse_id,
                'q': full_query,
                'num': min(max_results, 10)  # Max 10 per request
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            items = data.get('items', [])
            
            # Convert search results to signals
            for item in items:
                signal = self._result_to_signal(item, region, materials)
                if signal:
                    signals.append(signal)
        
        except requests.RequestException as e:
            print(f"CSE API error: {e}")
        except Exception as e:
            print(f"CSE processing error: {e}")
        
        return signals
    
    def _build_query(
        self,
        base_query: str,
        region: Optional[str],
        materials: Optional[List[str]]
    ) -> str:
        """Build enhanced search query"""
        query_parts = [base_query]
        
        if region:
            query_parts.append(region)
        
        if materials:
            # Add top 2 materials to query
            query_parts.extend(materials[:2])
        
        return ' '.join(query_parts)
    
    def _result_to_signal(
        self,
        result: dict,
        region: Optional[str],
        materials: Optional[List[str]]
    ) -> Optional[EnrichmentSignal]:
        """Convert CSE result to EnrichmentSignal"""
        try:
            title = result.get('title', '')
            snippet = result.get('snippet', '')
            url = result.get('link', '')
            
            # Determine signal type from URL/content
            signal_type = self._infer_signal_type(url, title, snippet)
            
            # Determine effects
            effects = self._infer_effects(title, snippet)
            
            # Calculate scores
            relevance = self._calculate_relevance(title, snippet, region, materials)
            
            signal = EnrichmentSignal(
                signal_id=f"cse_{uuid.uuid4().hex[:12]}",
                signal_type=signal_type,
                source=EnrichmentSource(
                    name="Google Custom Search",
                    type="cse",
                    url=url,
                    reliability_score=0.7
                ),
                title=title[:200],
                summary=snippet[:500],
                url=url,
                region=region,
                materials_affected=materials or [],
                published_date=datetime.now(),
                relevance_score=relevance,
                confidence_score=0.65,  # Lower confidence for discovered content
                impact_score=0.5,
                effects=effects,
                tags=['cse', 'discovered']
            )
            
            return signal
        
        except Exception as e:
            print(f"Error converting CSE result: {e}")
            return None
    
    def _infer_signal_type(self, url: str, title: str, snippet: str) -> SignalType:
        """Infer signal type from URL and content"""
        url_lower = url.lower()
        content = (title + ' ' + snippet).lower()
        
        if 'imd.gov.in' in url_lower or 'mausam' in url_lower:
            return SignalType.WEATHER
        elif 'pwd' in url_lower or 'traffic' in content:
            return SignalType.TRAFFIC
        elif 'port' in url_lower or 'shipping' in content:
            return SignalType.LOGISTICS
        elif 'fuel' in url_lower or 'petrol' in content or 'diesel' in content:
            return SignalType.FUEL_PRICE
        else:
            return SignalType.MARKET
    
    def _infer_effects(self, title: str, snippet: str) -> List[SignalEffect]:
        """Infer procurement effects from content"""
        content = (title + ' ' + snippet).lower()
        effects = []
        
        if any(kw in content for kw in ['delay', 'postpone', 'late']):
            effects.append(SignalEffect.LEAD_TIME_INCREASED)
        
        if any(kw in content for kw in ['price increase', 'hike', 'surge']):
            effects.append(SignalEffect.PRICE_INCREASE)
        
        if any(kw in content for kw in ['shortage', 'unavailable', 'out of stock']):
            effects.append(SignalEffect.AVAILABILITY_REDUCED)
        
        if any(kw in content for kw in ['risk', 'warning', 'alert']):
            effects.append(SignalEffect.RISK_INCREASED)
        
        return effects or [SignalEffect.RISK_INCREASED]
    
    def _calculate_relevance(
        self,
        title: str,
        snippet: str,
        region: Optional[str],
        materials: Optional[List[str]]
    ) -> float:
        """Calculate relevance score"""
        score = 0.5  # Base score for CSE results
        content = (title + ' ' + snippet).lower()
        
        # Region match
        if region and region.lower() in content:
            score += 0.2
        
        # Material match
        if materials:
            material_matches = sum(1 for m in materials if m.lower() in content)
            score += min(0.2, material_matches * 0.1)
        
        # Recency indicators
        if any(kw in content for kw in ['today', 'latest', 'current', 'now']):
            score += 0.1
        
        return min(1.0, score)

