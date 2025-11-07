"""
PRISMA Web Enrichment Module

This module provides web-based procurement signal enrichment by:
- Scraping whitelisted public sources (PWD, IMD, fuel prices, logistics)
- Combining structured API data with web-scraped information
- Scoring relevance and confidence for each signal
- Aggregating signals into normalized JSON bundles

Key Features:
- Modular scraper architecture with base classes
- Async/concurrent scraping with rate limiting
- Robots.txt compliance
- Caching (file-based and optional Redis)
- Mock mode for testing
- Google Custom Search Engine integration
- Clean integration with existing weather API
"""

from .models import (
    EnrichmentSignal,
    EnrichmentSource,
    EnrichmentRequest,
    EnrichmentResponse,
    SignalEffect,
    SignalType
)

from .engine import WebEnrichmentEngine
from .scrapers import ScraperRegistry

__all__ = [
    "EnrichmentSignal",
    "EnrichmentSource",
    "EnrichmentRequest",
    "EnrichmentResponse",
    "SignalEffect",
    "SignalType",
    "WebEnrichmentEngine",
    "ScraperRegistry"
]

__version__ = "0.1.0"

