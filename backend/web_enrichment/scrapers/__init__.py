"""
Domain-specific scrapers for various public sources
"""

from typing import Dict, Type, List
from ..base_scraper import BaseScraper
from .imd_scraper import IMDScraper
from .pwd_scraper import PWDScraper
from .fuel_scraper import FuelPriceScraper
from .logistics_scraper import LogisticsScraper


class ScraperRegistry:
    """Registry of all available scrapers"""
    
    _scrapers: Dict[str, Type[BaseScraper]] = {
        'imd': IMDScraper,
        'pwd': PWDScraper,
        'fuel': FuelPriceScraper,
        'logistics': LogisticsScraper,
    }
    
    @classmethod
    def get_scraper(cls, name: str) -> Type[BaseScraper]:
        """Get scraper class by name"""
        return cls._scrapers.get(name)
    
    @classmethod
    def get_all_scrapers(cls) -> List[Type[BaseScraper]]:
        """Get all registered scraper classes"""
        return list(cls._scrapers.values())
    
    @classmethod
    def register(cls, name: str, scraper_class: Type[BaseScraper]):
        """Register a new scraper"""
        cls._scrapers[name] = scraper_class


__all__ = [
    'ScraperRegistry',
    'IMDScraper',
    'PWDScraper',
    'FuelPriceScraper',
    'LogisticsScraper'
]

