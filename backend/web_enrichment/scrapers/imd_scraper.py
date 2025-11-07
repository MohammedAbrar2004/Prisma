"""
IMD (India Meteorological Department) Scraper

Scrapes weather warnings, bulletins, and advisories from IMD
"""

import re
import uuid
from datetime import datetime, timedelta
from typing import List, Optional

from ..base_scraper import BaseScraper
from ..models import EnrichmentSignal, SignalType, SignalEffect


class IMDScraper(BaseScraper):
    """Scraper for India Meteorological Department"""
    
    # Whitelisted IMD domains
    ALLOWED_DOMAINS = [
        'mausam.imd.gov.in',
        'imd.gov.in',
        'rmc.imd.gov.in'
    ]
    
    def __init__(self):
        super().__init__(
            name="India Meteorological Department",
            requests_per_minute=6,  # Conservative rate limit
            cache_ttl_hours=6,  # Weather data changes frequently
            respect_robots=True
        )
        self.base_url = "https://mausam.imd.gov.in"
    
    def get_signal_type(self) -> SignalType:
        return SignalType.WEATHER
    
    def scrape(
        self,
        region: Optional[str] = None,
        materials: Optional[List[str]] = None,
        time_window_days: int = 30,
        use_cache: bool = True
    ) -> List[EnrichmentSignal]:
        """
        Scrape IMD for weather warnings and bulletins
        
        Returns signals for:
        - Heavy rainfall warnings
        - Cyclone/storm alerts
        - Extreme temperature warnings
        - Fog/visibility warnings
        """
        signals = []
        
        # Map region to IMD regional center
        region_urls = self._get_region_urls(region)
        
        for url in region_urls:
            try:
                html = self.fetch_url(url, use_cache=use_cache)
                if not html:
                    continue
                
                soup = self.parse_html(html)
                extracted_signals = self._extract_signals(soup, region, materials)
                signals.extend(extracted_signals)
            
            except Exception as e:
                print(f"IMD scraper error for {url}: {e}")
        
        return signals
    
    def _get_region_urls(self, region: Optional[str]) -> List[str]:
        """Get IMD URLs for specific region"""
        # Map Indian states to IMD regional centers
        region_map = {
            'Maharashtra': f'{self.base_url}/mumbai',
            'Gujarat': f'{self.base_url}/ahmedabad',
            'Karnataka': f'{self.base_url}/bengaluru',
            'Tamil Nadu': f'{self.base_url}/chennai',
            'Delhi': f'{self.base_url}/delhi',
        }
        
        if region and region in region_map:
            return [region_map[region], f'{self.base_url}/warnings']
        
        # Default: national warnings
        return [f'{self.base_url}/warnings', f'{self.base_url}/']
    
    def _extract_signals(
        self,
        soup,
        region: Optional[str],
        materials: Optional[List[str]]
    ) -> List[EnrichmentSignal]:
        """Extract signals from IMD page"""
        signals = []
        
        # Look for warning/alert sections
        warning_sections = soup.find_all(['div', 'article', 'section'], 
                                        class_=re.compile(r'(warning|alert|bulletin)', re.I))
        
        for section in warning_sections:
            try:
                signal = self._parse_warning_section(section, region, materials)
                if signal:
                    signals.append(signal)
            except Exception as e:
                print(f"Error parsing IMD section: {e}")
        
        # Also look for table-based warnings
        tables = soup.find_all('table', class_=re.compile(r'(warning|forecast)', re.I))
        for table in tables:
            try:
                table_signals = self._parse_warning_table(table, region, materials)
                signals.extend(table_signals)
            except Exception as e:
                print(f"Error parsing IMD table: {e}")
        
        return signals
    
    def _parse_warning_section(self, section, region, materials) -> Optional[EnrichmentSignal]:
        """Parse a warning section into a signal"""
        # Extract title
        title_elem = section.find(['h1', 'h2', 'h3', 'h4', 'strong'])
        if not title_elem:
            return None
        
        title = title_elem.get_text(strip=True)
        
        # Extract full text
        full_text = section.get_text(separator=' ', strip=True)
        
        # Extract date if available
        date_match = re.search(r'(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})', full_text)
        published_date = None
        if date_match:
            try:
                published_date = datetime.strptime(date_match.group(1), '%d-%m-%Y')
            except:
                published_date = datetime.now()
        else:
            published_date = datetime.now()
        
        # Determine effects and severity
        effects, impact_score = self._analyze_weather_impact(full_text, materials)
        
        # Calculate relevance
        relevance = self._calculate_relevance(full_text, region, materials)
        
        # Create signal
        signal = EnrichmentSignal(
            signal_id=f"imd_{uuid.uuid4().hex[:12]}",
            signal_type=SignalType.WEATHER,
            source=self.create_source(self.base_url, reliability=0.95),
            title=title[:200],  # Limit title length
            summary=full_text[:500],  # First 500 chars as summary
            full_text=full_text,
            url=self.base_url,
            region=region or self._extract_region(full_text),
            materials_affected=materials or self._infer_affected_materials(full_text),
            published_date=published_date,
            effective_date=published_date,
            expiry_date=published_date + timedelta(days=7),
            relevance_score=relevance,
            confidence_score=0.9,  # IMD is highly reliable
            impact_score=impact_score,
            effects=effects,
            tags=['weather', 'imd', 'official']
        )
        
        return signal
    
    def _parse_warning_table(self, table, region, materials) -> List[EnrichmentSignal]:
        """Parse warning table into signals"""
        signals = []
        rows = table.find_all('tr')[1:]  # Skip header
        
        for row in rows:
            cells = row.find_all(['td', 'th'])
            if len(cells) < 2:
                continue
            
            # Extract data from cells
            row_text = ' '.join([cell.get_text(strip=True) for cell in cells])
            
            # Check relevance
            if region and region.lower() not in row_text.lower():
                continue
            
            signal = EnrichmentSignal(
                signal_id=f"imd_table_{uuid.uuid4().hex[:12]}",
                signal_type=SignalType.WEATHER,
                source=self.create_source(self.base_url, reliability=0.95),
                title=f"Weather advisory: {row_text[:100]}",
                summary=row_text[:300],
                region=region or self._extract_region(row_text),
                materials_affected=materials or [],
                published_date=datetime.now(),
                relevance_score=0.7,
                confidence_score=0.9,
                impact_score=0.6,
                effects=[SignalEffect.LEAD_TIME_INCREASED],
                tags=['weather', 'imd', 'table']
            )
            signals.append(signal)
        
        return signals
    
    def _analyze_weather_impact(self, text: str, materials: Optional[List[str]]) -> tuple:
        """Analyze weather text to determine effects and impact"""
        text_lower = text.lower()
        effects = []
        impact_score = 0.5
        
        # Heavy rain
        if any(word in text_lower for word in ['heavy rain', 'very heavy', 'extremely heavy', 'torrential']):
            effects.extend([
                SignalEffect.LEAD_TIME_INCREASED,
                SignalEffect.AVAILABILITY_REDUCED,
                SignalEffect.DEMAND_INCREASED  # Pre-stocking
            ])
            impact_score = 0.8
        
        # Cyclone/storm
        if any(word in text_lower for word in ['cyclone', 'storm', 'hurricane', 'depression']):
            effects.extend([
                SignalEffect.RISK_INCREASED,
                SignalEffect.LEAD_TIME_INCREASED,
                SignalEffect.AVAILABILITY_REDUCED
            ])
            impact_score = 0.9
        
        # Extreme temperature
        if any(word in text_lower for word in ['heat wave', 'cold wave', 'extreme temperature']):
            effects.append(SignalEffect.LEAD_TIME_INCREASED)
            impact_score = 0.6
        
        # Fog/visibility
        if any(word in text_lower for word in ['dense fog', 'poor visibility']):
            effects.append(SignalEffect.LEAD_TIME_INCREASED)
            impact_score = 0.5
        
        return effects or [SignalEffect.RISK_INCREASED], impact_score
    
    def _calculate_relevance(self, text: str, region: Optional[str], materials: Optional[List[str]]) -> float:
        """Calculate relevance score"""
        score = 0.5  # Base score
        
        text_lower = text.lower()
        
        # Region match
        if region and region.lower() in text_lower:
            score += 0.3
        
        # Material mentions
        if materials:
            material_mentions = sum(1 for mat in materials if mat.lower() in text_lower)
            score += min(0.2, material_mentions * 0.1)
        
        # Severity keywords
        severity_keywords = ['warning', 'alert', 'severe', 'extreme', 'heavy', 'very']
        severity_count = sum(1 for kw in severity_keywords if kw in text_lower)
        score += min(0.2, severity_count * 0.05)
        
        return min(1.0, score)
    
    def _extract_region(self, text: str) -> Optional[str]:
        """Extract region from text"""
        indian_states = [
            'Maharashtra', 'Gujarat', 'Karnataka', 'Tamil Nadu', 'Delhi',
            'Uttar Pradesh', 'Rajasthan', 'West Bengal', 'Madhya Pradesh'
        ]
        
        for state in indian_states:
            if state.lower() in text.lower():
                return state
        
        return None
    
    def _infer_affected_materials(self, text: str) -> List[str]:
        """Infer which materials might be affected"""
        # Weather typically affects outdoor construction materials
        return ['Concrete', 'Steel', 'Cement', 'Sand', 'Aggregates']

