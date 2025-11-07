"""
Logistics & Port Scraper

Scrapes port updates, shipping delays, and logistics notices
"""

import re
import uuid
from datetime import datetime, timedelta
from typing import List, Optional

from ..base_scraper import BaseScraper
from ..models import EnrichmentSignal, SignalType, SignalEffect


class LogisticsScraper(BaseScraper):
    """Scraper for logistics and port information"""
    
    # Whitelisted logistics/port domains
    ALLOWED_DOMAINS = [
        'indianports.gov.in',
        'jnport.gov.in',  # Jawaharlal Nehru Port
        'mumbaiport.gov.in',
        'cochinport.gov.in',
        'shipmin.gov.in'  # Ministry of Shipping
    ]
    
    def __init__(self):
        super().__init__(
            name="Logistics & Port Tracker",
            requests_per_minute=8,
            cache_ttl_hours=12,
            respect_robots=True
        )
    
    def get_signal_type(self) -> SignalType:
        return SignalType.LOGISTICS
    
    def scrape(
        self,
        region: Optional[str] = None,
        materials: Optional[List[str]] = None,
        time_window_days: int = 30,
        use_cache: bool = True
    ) -> List[EnrichmentSignal]:
        """
        Scrape logistics information for:
        - Port delays/congestion
        - Shipping schedule changes
        - Container availability
        - Customs/clearance issues
        """
        signals = []
        
        # Get relevant port URLs
        port_urls = self._get_port_urls(region)
        
        for url in port_urls:
            try:
                html = self.fetch_url(url, use_cache=use_cache)
                if not html:
                    continue
                
                soup = self.parse_html(html)
                extracted = self._extract_logistics_signals(soup, region, materials)
                signals.extend(extracted)
            
            except Exception as e:
                print(f"Logistics scraper error for {url}: {e}")
        
        return signals
    
    def _get_port_urls(self, region: Optional[str]) -> List[str]:
        """Get port URLs based on region"""
        # Map regions to nearest major ports
        region_ports = {
            'Maharashtra': [
                'https://jnport.gov.in',
                'https://mumbaiport.gov.in'
            ],
            'Gujarat': [
                'https://www.indianports.gov.in'  # Kandla, Mundra
            ],
            'Karnataka': [
                'https://www.indianports.gov.in'  # Mangalore
            ],
            'Tamil Nadu': [
                'https://www.indianports.gov.in'  # Chennai
            ]
        }
        
        if region and region in region_ports:
            return region_ports[region]
        
        # Default: major ports
        return [
            'https://jnport.gov.in',
            'https://www.indianports.gov.in'
        ]
    
    def _extract_logistics_signals(self, soup, region, materials) -> List[EnrichmentSignal]:
        """Extract logistics/port signals"""
        signals = []
        
        # Look for notices, alerts, updates
        notice_sections = soup.find_all(
            ['div', 'article', 'li', 'tr'],
            class_=re.compile(r'(notice|alert|update|news|announcement)', re.I)
        )
        
        for section in notice_sections:
            try:
                signal = self._parse_logistics_notice(section, region, materials)
                if signal:
                    signals.append(signal)
            except Exception as e:
                print(f"Error parsing logistics notice: {e}")
        
        # Look for delay/congestion indicators
        delay_keywords = ['delay', 'congestion', 'backlog', 'waiting', 'queue']
        for keyword in delay_keywords:
            elements = soup.find_all(text=re.compile(keyword, re.I))
            for elem in elements[:3]:  # Limit to 3 per keyword
                try:
                    signal = self._parse_delay_mention(elem, region, materials)
                    if signal:
                        signals.append(signal)
                except Exception as e:
                    print(f"Error parsing delay mention: {e}")
        
        return signals
    
    def _parse_logistics_notice(self, section, region, materials) -> Optional[EnrichmentSignal]:
        """Parse a logistics notice"""
        text = section.get_text(separator=' ', strip=True)
        
        # Skip if too short or not relevant
        if len(text) < 30:
            return None
        
        # Check relevance
        relevance_keywords = ['cargo', 'container', 'ship', 'vessel', 'import', 'export', 
                             'customs', 'clearance', 'delay', 'schedule']
        if not any(kw in text.lower() for kw in relevance_keywords):
            return None
        
        # Extract title
        title_elem = section.find(['strong', 'b', 'h3', 'h4', 'a'])
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
        effects, impact_score = self._analyze_logistics_impact(text, materials)
        
        # Calculate relevance
        relevance = self._calculate_relevance(text, region, materials)
        
        if relevance < 0.3:
            return None
        
        signal = EnrichmentSignal(
            signal_id=f"logistics_{uuid.uuid4().hex[:12]}",
            signal_type=SignalType.LOGISTICS,
            source=self.create_source(reliability=0.80),
            title=title[:200],
            summary=text[:500],
            full_text=text,
            region=region,
            materials_affected=materials or self._infer_affected_materials(text),
            published_date=published_date,
            effective_date=published_date,
            expiry_date=published_date + timedelta(days=14),
            relevance_score=relevance,
            confidence_score=0.75,
            impact_score=impact_score,
            effects=effects,
            tags=['logistics', 'port', 'shipping']
        )
        
        return signal
    
    def _parse_delay_mention(self, elem, region, materials) -> Optional[EnrichmentSignal]:
        """Parse a delay mention into signal"""
        parent = elem.parent
        if not parent:
            return None
        
        text = parent.get_text(separator=' ', strip=True)
        
        if len(text) < 20:
            return None
        
        signal = EnrichmentSignal(
            signal_id=f"logistics_delay_{uuid.uuid4().hex[:8]}",
            signal_type=SignalType.LOGISTICS,
            source=self.create_source(reliability=0.70),
            title=f"Logistics delay indicator: {text[:100]}",
            summary=text[:300],
            region=region,
            materials_affected=materials or ['General'],
            published_date=datetime.now(),
            relevance_score=0.6,
            confidence_score=0.65,
            impact_score=0.6,
            effects=[SignalEffect.LEAD_TIME_INCREASED, SignalEffect.AVAILABILITY_REDUCED],
            tags=['logistics', 'delay']
        )
        
        return signal
    
    def _analyze_logistics_impact(self, text: str, materials: Optional[List[str]]) -> tuple:
        """Analyze logistics text for impact"""
        text_lower = text.lower()
        effects = []
        impact_score = 0.5
        
        # Delays
        if any(kw in text_lower for kw in ['delay', 'delayed', 'postponed']):
            effects.extend([
                SignalEffect.LEAD_TIME_INCREASED,
                SignalEffect.AVAILABILITY_REDUCED
            ])
            impact_score = 0.7
        
        # Congestion
        if any(kw in text_lower for kw in ['congestion', 'backlog', 'queue', 'waiting']):
            effects.append(SignalEffect.LEAD_TIME_INCREASED)
            impact_score = 0.6
        
        # Strike/closure
        if any(kw in text_lower for kw in ['strike', 'closed', 'shutdown', 'suspended']):
            effects.extend([
                SignalEffect.AVAILABILITY_REDUCED,
                SignalEffect.PRICE_INCREASE,
                SignalEffect.RISK_INCREASED
            ])
            impact_score = 0.9
        
        # Container shortage
        if any(kw in text_lower for kw in ['container shortage', 'lack of containers']):
            effects.extend([
                SignalEffect.AVAILABILITY_REDUCED,
                SignalEffect.PRICE_INCREASE
            ])
            impact_score = 0.8
        
        return effects or [SignalEffect.LEAD_TIME_INCREASED], impact_score
    
    def _calculate_relevance(self, text: str, region: Optional[str], materials: Optional[List[str]]) -> float:
        """Calculate relevance score"""
        score = 0.4
        text_lower = text.lower()
        
        # Material mentions
        if materials:
            material_keywords = ['steel', 'iron', 'metal', 'cement', 'concrete', 'copper', 'aluminum']
            if any(kw in text_lower for kw in material_keywords):
                score += 0.3
        
        # Import/export
        if any(kw in text_lower for kw in ['import', 'export', 'cargo', 'shipment']):
            score += 0.2
        
        # Severity
        if any(kw in text_lower for kw in ['critical', 'severe', 'major', 'significant']):
            score += 0.1
        
        return min(1.0, score)
    
    def _infer_affected_materials(self, text: str) -> List[str]:
        """Infer affected materials"""
        text_lower = text.lower()
        materials = []
        
        material_map = {
            'steel': 'Steel',
            'iron': 'Steel',
            'cement': 'Cement',
            'concrete': 'Concrete',
            'copper': 'Copper',
            'aluminum': 'Aluminum',
            'aluminium': 'Aluminum'
        }
        
        for keyword, material in material_map.items():
            if keyword in text_lower and material not in materials:
                materials.append(material)
        
        return materials or ['General']

