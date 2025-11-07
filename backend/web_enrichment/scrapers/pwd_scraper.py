"""
PWD (Public Works Department) Scraper

Scrapes traffic advisories, road closures, and infrastructure notices
"""

import re
import uuid
from datetime import datetime, timedelta
from typing import List, Optional

from ..base_scraper import BaseScraper
from ..models import EnrichmentSignal, SignalType, SignalEffect


class PWDScraper(BaseScraper):
    """Scraper for Public Works Department advisories"""
    
    # Whitelisted PWD domains by state
    ALLOWED_DOMAINS = [
        'pwd.maharashtra.gov.in',
        'mahapwd.com',
        'gujaratpwd.gov.in',
        'karnatakapwd.gov.in'
    ]
    
    # State-specific PWD URLs
    STATE_URLS = {
        'Maharashtra': 'https://pwd.maharashtra.gov.in',
        'Gujarat': 'https://gujaratpwd.gov.in',
        'Karnataka': 'https://karnatakapwd.gov.in',
    }
    
    def __init__(self):
        super().__init__(
            name="Public Works Department",
            requests_per_minute=8,
            cache_ttl_hours=12,
            respect_robots=True
        )
    
    def get_signal_type(self) -> SignalType:
        return SignalType.TRAFFIC
    
    def scrape(
        self,
        region: Optional[str] = None,
        materials: Optional[List[str]] = None,
        time_window_days: int = 30,
        use_cache: bool = True
    ) -> List[EnrichmentSignal]:
        """
        Scrape PWD for:
        - Road closures
        - Traffic diversions
        - Infrastructure work notices
        - Bridge/highway maintenance
        """
        signals = []
        
        # Get URLs for region
        urls = self._get_urls_for_region(region)
        
        for url in urls:
            try:
                html = self.fetch_url(url, use_cache=use_cache)
                if not html:
                    continue
                
                soup = self.parse_html(html)
                extracted = self._extract_advisories(soup, region, materials)
                signals.extend(extracted)
            
            except Exception as e:
                print(f"PWD scraper error for {url}: {e}")
        
        return signals
    
    def _get_urls_for_region(self, region: Optional[str]) -> List[str]:
        """Get PWD URLs for specific region"""
        if region and region in self.STATE_URLS:
            base = self.STATE_URLS[region]
            return [
                base,
                f"{base}/notices",
                f"{base}/advisories",
                f"{base}/traffic"
            ]
        
        # Default: Maharashtra (most common)
        return [self.STATE_URLS['Maharashtra']]
    
    def _extract_advisories(self, soup, region, materials) -> List[EnrichmentSignal]:
        """Extract traffic/infrastructure advisories"""
        signals = []
        
        # Look for notice/advisory sections
        advisory_sections = soup.find_all(
            ['div', 'article', 'li'],
            class_=re.compile(r'(notice|advisory|alert|announcement)', re.I)
        )
        
        for section in advisory_sections:
            try:
                signal = self._parse_advisory(section, region, materials)
                if signal:
                    signals.append(signal)
            except Exception as e:
                print(f"Error parsing PWD advisory: {e}")
        
        # Look for links to PDF notices
        pdf_links = soup.find_all('a', href=re.compile(r'\.pdf$', re.I))
        for link in pdf_links[:5]:  # Limit to 5 PDFs
            try:
                signal = self._parse_pdf_link(link, region, materials)
                if signal:
                    signals.append(signal)
            except Exception as e:
                print(f"Error parsing PWD PDF link: {e}")
        
        return signals
    
    def _parse_advisory(self, section, region, materials) -> Optional[EnrichmentSignal]:
        """Parse an advisory section"""
        text = section.get_text(separator=' ', strip=True)
        
        # Skip if too short
        if len(text) < 20:
            return None
        
        # Extract title (first line or strong text)
        title_elem = section.find(['strong', 'b', 'h3', 'h4'])
        title = title_elem.get_text(strip=True) if title_elem else text[:100]
        
        # Extract date
        date_match = re.search(r'(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})', text)
        published_date = datetime.now()
        if date_match:
            try:
                published_date = datetime.strptime(date_match.group(1), '%d-%m-%Y')
            except:
                pass
        
        # Analyze impact
        effects, impact_score = self._analyze_traffic_impact(text, materials)
        
        # Calculate relevance
        relevance = self._calculate_relevance(text, region, materials)
        
        # Skip low relevance
        if relevance < 0.3:
            return None
        
        signal = EnrichmentSignal(
            signal_id=f"pwd_{uuid.uuid4().hex[:12]}",
            signal_type=SignalType.TRAFFIC,
            source=self.create_source(reliability=0.85),
            title=title[:200],
            summary=text[:500],
            full_text=text,
            region=region or self._extract_region(text),
            materials_affected=materials or self._infer_affected_materials(text),
            published_date=published_date,
            effective_date=published_date,
            expiry_date=published_date + timedelta(days=30),
            relevance_score=relevance,
            confidence_score=0.8,
            impact_score=impact_score,
            effects=effects,
            tags=['traffic', 'pwd', 'infrastructure']
        )
        
        return signal
    
    def _parse_pdf_link(self, link, region, materials) -> Optional[EnrichmentSignal]:
        """Parse PDF link into signal"""
        href = link.get('href', '')
        link_text = link.get_text(strip=True)
        
        # Skip if not relevant
        if not any(kw in link_text.lower() for kw in ['notice', 'advisory', 'closure', 'diversion', 'work']):
            return None
        
        signal = EnrichmentSignal(
            signal_id=f"pwd_pdf_{uuid.uuid4().hex[:12]}",
            signal_type=SignalType.TRAFFIC,
            source=self.create_source(reliability=0.85),
            title=f"PWD Notice: {link_text[:150]}",
            summary=f"Official PWD document: {link_text}",
            url=href,
            region=region,
            materials_affected=materials or ['General'],
            published_date=datetime.now(),
            relevance_score=0.6,
            confidence_score=0.85,
            impact_score=0.5,
            effects=[SignalEffect.LEAD_TIME_INCREASED],
            tags=['traffic', 'pwd', 'document']
        )
        
        return signal
    
    def _analyze_traffic_impact(self, text: str, materials: Optional[List[str]]) -> tuple:
        """Analyze traffic advisory impact"""
        text_lower = text.lower()
        effects = []
        impact_score = 0.5
        
        # Road closure
        if any(kw in text_lower for kw in ['road closed', 'closure', 'blocked', 'shut']):
            effects.extend([
                SignalEffect.LEAD_TIME_INCREASED,
                SignalEffect.AVAILABILITY_REDUCED,
                SignalEffect.PRICE_INCREASE
            ])
            impact_score = 0.8
        
        # Diversion
        if any(kw in text_lower for kw in ['diversion', 'alternate route', 'detour']):
            effects.append(SignalEffect.LEAD_TIME_INCREASED)
            impact_score = 0.6
        
        # Construction/maintenance
        if any(kw in text_lower for kw in ['construction', 'maintenance', 'repair', 'work in progress']):
            effects.append(SignalEffect.LEAD_TIME_INCREASED)
            impact_score = 0.5
        
        # Heavy traffic
        if any(kw in text_lower for kw in ['heavy traffic', 'congestion', 'jam']):
            effects.append(SignalEffect.LEAD_TIME_INCREASED)
            impact_score = 0.4
        
        return effects or [SignalEffect.LEAD_TIME_INCREASED], impact_score
    
    def _calculate_relevance(self, text: str, region: Optional[str], materials: Optional[List[str]]) -> float:
        """Calculate relevance score"""
        score = 0.4
        text_lower = text.lower()
        
        # Region match
        if region and region.lower() in text_lower:
            score += 0.3
        
        # Material transport keywords
        transport_keywords = ['truck', 'vehicle', 'transport', 'delivery', 'supply', 'logistics']
        if any(kw in text_lower for kw in transport_keywords):
            score += 0.2
        
        # Severity
        if any(kw in text_lower for kw in ['urgent', 'immediate', 'emergency', 'critical']):
            score += 0.1
        
        return min(1.0, score)
    
    def _extract_region(self, text: str) -> Optional[str]:
        """Extract region from text"""
        states = ['Maharashtra', 'Gujarat', 'Karnataka', 'Tamil Nadu', 'Delhi']
        cities = ['Mumbai', 'Pune', 'Ahmedabad', 'Bangalore', 'Chennai']
        
        text_lower = text.lower()
        
        for state in states:
            if state.lower() in text_lower:
                return state
        
        for city in cities:
            if city.lower() in text_lower:
                # Map city to state
                city_state_map = {
                    'Mumbai': 'Maharashtra',
                    'Pune': 'Maharashtra',
                    'Ahmedabad': 'Gujarat',
                    'Bangalore': 'Karnataka',
                    'Chennai': 'Tamil Nadu'
                }
                return city_state_map.get(city)
        
        return None
    
    def _infer_affected_materials(self, text: str) -> List[str]:
        """Infer affected materials from text"""
        # Traffic issues affect all materials that need transport
        return ['Steel', 'Concrete', 'Cement', 'Aggregates', 'General']

