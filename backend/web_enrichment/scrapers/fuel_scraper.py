"""
Fuel Price Scraper

Scrapes diesel/petrol prices from public sources
"""

import re
import uuid
from datetime import datetime, timedelta
from typing import List, Optional, Dict

from ..base_scraper import BaseScraper
from ..models import EnrichmentSignal, SignalType, SignalEffect


class FuelPriceScraper(BaseScraper):
    """Scraper for fuel prices (diesel/petrol)"""
    
    # Whitelisted fuel price domains
    ALLOWED_DOMAINS = [
        'mypetrolprice.com',
        'goodreturns.in',
        'iocl.com',
        'bharatpetroleum.in'
    ]
    
    def __init__(self):
        super().__init__(
            name="Fuel Price Tracker",
            requests_per_minute=10,
            cache_ttl_hours=24,  # Prices change daily
            respect_robots=True
        )
        self.base_url = "https://www.mypetrolprice.com"
    
    def get_signal_type(self) -> SignalType:
        return SignalType.FUEL_PRICE
    
    def scrape(
        self,
        region: Optional[str] = None,
        materials: Optional[List[str]] = None,
        time_window_days: int = 30,
        use_cache: bool = True
    ) -> List[EnrichmentSignal]:
        """
        Scrape fuel prices and generate signals for:
        - Diesel price changes (affects transport costs)
        - Petrol price changes
        - Price trends
        """
        signals = []
        
        # Get city for region
        city = self._region_to_city(region)
        
        try:
            # Fetch current prices
            url = f"{self.base_url}/{city.lower()}" if city else self.base_url
            html = self.fetch_url(url, use_cache=use_cache)
            
            if html:
                soup = self.parse_html(html)
                price_signals = self._extract_price_signals(soup, region, materials, city)
                signals.extend(price_signals)
        
        except Exception as e:
            print(f"Fuel price scraper error: {e}")
        
        return signals
    
    def _region_to_city(self, region: Optional[str]) -> str:
        """Map region to major city"""
        city_map = {
            'Maharashtra': 'Mumbai',
            'Gujarat': 'Ahmedabad',
            'Karnataka': 'Bangalore',
            'Tamil Nadu': 'Chennai',
            'Delhi': 'Delhi'
        }
        return city_map.get(region, 'Mumbai')
    
    def _extract_price_signals(self, soup, region, materials, city) -> List[EnrichmentSignal]:
        """Extract fuel price signals"""
        signals = []
        
        # Look for price elements
        price_sections = soup.find_all(['div', 'span', 'td'], 
                                      class_=re.compile(r'(price|rate|cost)', re.I))
        
        # Extract diesel and petrol prices
        diesel_price = self._extract_price(soup, 'diesel')
        petrol_price = self._extract_price(soup, 'petrol')
        
        # Create signal for diesel (most relevant for construction)
        if diesel_price:
            diesel_signal = self._create_fuel_signal(
                fuel_type='Diesel',
                price=diesel_price,
                region=region,
                city=city,
                materials=materials
            )
            signals.append(diesel_signal)
        
        # Create signal for petrol
        if petrol_price:
            petrol_signal = self._create_fuel_signal(
                fuel_type='Petrol',
                price=petrol_price,
                region=region,
                city=city,
                materials=materials
            )
            signals.append(petrol_signal)
        
        return signals
    
    def _extract_price(self, soup, fuel_type: str) -> Optional[float]:
        """Extract price for specific fuel type"""
        # Look for price near fuel type mention
        fuel_pattern = re.compile(fuel_type, re.I)
        price_pattern = re.compile(r'₹?\s*(\d+\.?\d*)')
        
        # Find elements mentioning the fuel type
        fuel_elements = soup.find_all(text=fuel_pattern)
        
        for elem in fuel_elements:
            # Look for price in nearby elements
            parent = elem.parent
            if parent:
                text = parent.get_text()
                price_match = price_pattern.search(text)
                if price_match:
                    try:
                        return float(price_match.group(1))
                    except ValueError:
                        continue
        
        return None
    
    def _create_fuel_signal(
        self,
        fuel_type: str,
        price: float,
        region: Optional[str],
        city: str,
        materials: Optional[List[str]]
    ) -> EnrichmentSignal:
        """Create a fuel price signal"""
        
        # Determine effect based on price level
        # (In real implementation, compare with historical prices)
        effects = [SignalEffect.PRICE_INCREASE]  # Assume increase for demo
        impact_score = 0.6 if fuel_type == 'Diesel' else 0.4
        
        # Diesel is more relevant for construction/logistics
        relevance = 0.8 if fuel_type == 'Diesel' else 0.5
        
        signal = EnrichmentSignal(
            signal_id=f"fuel_{fuel_type.lower()}_{uuid.uuid4().hex[:8]}",
            signal_type=SignalType.FUEL_PRICE,
            source=self.create_source(self.base_url, reliability=0.85),
            title=f"{fuel_type} Price in {city}: ₹{price:.2f}/L",
            summary=f"Current {fuel_type.lower()} price in {city} is ₹{price:.2f} per liter. "
                   f"This affects transportation and logistics costs for material delivery.",
            region=region,
            location=city,
            materials_affected=materials or ['General'],
            published_date=datetime.now(),
            effective_date=datetime.now(),
            expiry_date=datetime.now() + timedelta(days=1),  # Daily prices
            relevance_score=relevance,
            confidence_score=0.9,
            impact_score=impact_score,
            effects=effects,
            effect_magnitude=price,  # Store actual price
            tags=['fuel', fuel_type.lower(), 'transport', 'logistics'],
            metadata={
                'fuel_type': fuel_type,
                'price_per_liter': price,
                'currency': 'INR',
                'city': city
            }
        )
        
        return signal
    
    def get_mock_signals(self, region: Optional[str], materials: Optional[List[str]]) -> List[EnrichmentSignal]:
        """Generate mock fuel price signals for testing"""
        city = self._region_to_city(region)
        
        signals = [
            self._create_fuel_signal('Diesel', 89.50, region, city, materials),
            self._create_fuel_signal('Petrol', 102.30, region, city, materials)
        ]
        
        return signals

