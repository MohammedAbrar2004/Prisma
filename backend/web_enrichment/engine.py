"""
Web Enrichment Engine

Main orchestrator for web-based procurement signal enrichment
"""

import os
import time
import uuid
import asyncio
from datetime import datetime
from typing import List, Optional, Dict
from concurrent.futures import ThreadPoolExecutor, as_completed

from .models import (
    EnrichmentRequest,
    EnrichmentResponse,
    EnrichmentSignal,
    SignalAggregate,
    SignalType
)
from .scrapers import ScraperRegistry
from .base_scraper import BaseScraper


class WebEnrichmentEngine:
    """
    Main engine for web enrichment
    
    Orchestrates:
    - Multiple scrapers running concurrently
    - Signal aggregation and deduplication
    - Relevance scoring and filtering
    - Caching and mock mode
    """
    
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
        self.scrapers: Dict[str, BaseScraper] = {}
        self._initialize_scrapers()
    
    def _initialize_scrapers(self):
        """Initialize all registered scrapers"""
        for scraper_class in ScraperRegistry.get_all_scrapers():
            try:
                scraper = scraper_class()
                self.scrapers[scraper.name] = scraper
            except Exception as e:
                print(f"Failed to initialize scraper {scraper_class.__name__}: {e}")
    
    def enrich(self, request: EnrichmentRequest) -> EnrichmentResponse:
        """
        Main enrichment method
        
        Args:
            request: EnrichmentRequest with site, materials, filters
            
        Returns:
            EnrichmentResponse with signals and aggregates
        """
        start_time = time.time()
        request_id = f"req_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
        
        # Mock mode
        if request.mock_mode:
            return self._generate_mock_response(request, request_id)
        
        # Collect signals from all scrapers
        all_signals = self._collect_signals(request)
        
        # Filter by relevance
        filtered_signals = self._filter_signals(all_signals, request.min_relevance)
        
        # Filter by signal types if specified
        if request.signal_types:
            filtered_signals = [
                s for s in filtered_signals 
                if s.signal_type in request.signal_types
            ]
        
        # Sort by relevance * impact
        filtered_signals.sort(
            key=lambda s: s.relevance_score * s.impact_score,
            reverse=True
        )
        
        # Generate aggregates
        aggregates = self._generate_aggregates(filtered_signals, request.materials)
        
        # Get sources used
        sources_used = list(set(s.source.name for s in filtered_signals))
        
        # Calculate processing time
        processing_time = (time.time() - start_time) * 1000  # ms
        
        response = EnrichmentResponse(
            request_id=request_id,
            site=request.site,
            region=request.region,
            materials=request.materials,
            signals=filtered_signals,
            aggregates=aggregates,
            sources_used=sources_used,
            cache_hit=False,  # TODO: Implement response-level caching
            processing_time_ms=processing_time,
            generated_at=datetime.now()
        )
        
        return response
    
    def _collect_signals(self, request: EnrichmentRequest) -> List[EnrichmentSignal]:
        """Collect signals from all scrapers concurrently"""
        all_signals = []
        
        if not request.use_scrapers:
            return all_signals
        
        # Run scrapers concurrently
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_scraper = {
                executor.submit(
                    self._run_scraper,
                    scraper,
                    request.region,
                    request.materials,
                    request.time_window_days,
                    request.use_cache
                ): scraper
                for scraper in self.scrapers.values()
            }
            
            for future in as_completed(future_to_scraper):
                scraper = future_to_scraper[future]
                try:
                    signals = future.result(timeout=30)  # 30s timeout per scraper
                    all_signals.extend(signals)
                    print(f"✓ {scraper.name}: {len(signals)} signals")
                except Exception as e:
                    print(f"✗ {scraper.name} failed: {e}")
        
        return all_signals
    
    def _run_scraper(
        self,
        scraper: BaseScraper,
        region: Optional[str],
        materials: List[str],
        time_window_days: int,
        use_cache: bool
    ) -> List[EnrichmentSignal]:
        """Run a single scraper"""
        try:
            return scraper.scrape(
                region=region,
                materials=materials,
                time_window_days=time_window_days,
                use_cache=use_cache
            )
        except Exception as e:
            print(f"Scraper {scraper.name} error: {e}")
            return []
    
    def _filter_signals(
        self,
        signals: List[EnrichmentSignal],
        min_relevance: float
    ) -> List[EnrichmentSignal]:
        """Filter signals by minimum relevance"""
        return [s for s in signals if s.relevance_score >= min_relevance]
    
    def _generate_aggregates(
        self,
        signals: List[EnrichmentSignal],
        materials: List[str]
    ) -> SignalAggregate:
        """Generate aggregate statistics"""
        if not signals:
            return SignalAggregate()
        
        # Count by type
        by_type = {}
        for signal in signals:
            type_name = signal.signal_type.value
            by_type[type_name] = by_type.get(type_name, 0) + 1
        
        # Count by effect
        by_effect = {}
        for signal in signals:
            for effect in signal.effects:
                effect_name = effect.value
                by_effect[effect_name] = by_effect.get(effect_name, 0) + 1
        
        # Calculate averages
        avg_relevance = sum(s.relevance_score for s in signals) / len(signals)
        avg_confidence = sum(s.confidence_score for s in signals) / len(signals)
        avg_impact = sum(s.impact_score for s in signals) / len(signals)
        
        # High impact count
        high_impact_count = sum(1 for s in signals if s.impact_score > 0.7)
        
        # Materials coverage
        materials_coverage = {}
        for material in materials:
            count = sum(
                1 for s in signals 
                if material in s.materials_affected or 'General' in s.materials_affected
            )
            materials_coverage[material] = count
        
        return SignalAggregate(
            total_signals=len(signals),
            by_type=by_type,
            by_effect=by_effect,
            avg_relevance=round(avg_relevance, 2),
            avg_confidence=round(avg_confidence, 2),
            avg_impact=round(avg_impact, 2),
            high_impact_count=high_impact_count,
            materials_coverage=materials_coverage
        )
    
    def _generate_mock_response(
        self,
        request: EnrichmentRequest,
        request_id: str
    ) -> EnrichmentResponse:
        """Generate mock response for testing"""
        from .scrapers.fuel_scraper import FuelPriceScraper
        
        # Generate some mock signals
        mock_signals = []
        
        # Add mock fuel signals
        fuel_scraper = FuelPriceScraper()
        mock_signals.extend(
            fuel_scraper.get_mock_signals(request.region, request.materials)
        )
        
        # Add a mock weather signal
        from .models import EnrichmentSource, SignalEffect
        mock_signals.append(
            EnrichmentSignal(
                signal_id="mock_weather_001",
                signal_type=SignalType.WEATHER,
                source=EnrichmentSource(
                    name="Mock Weather Service",
                    type="mock",
                    reliability_score=1.0
                ),
                title="Mock: Heavy rainfall expected",
                summary="This is mock data for testing. Heavy rainfall expected in the region for next 3 days.",
                region=request.region or "Maharashtra",
                materials_affected=request.materials,
                published_date=datetime.now(),
                relevance_score=0.85,
                confidence_score=0.9,
                impact_score=0.75,
                effects=[SignalEffect.LEAD_TIME_INCREASED, SignalEffect.DEMAND_INCREASED],
                tags=['mock', 'weather']
            )
        )
        
        # Generate aggregates
        aggregates = self._generate_aggregates(mock_signals, request.materials)
        
        return EnrichmentResponse(
            request_id=request_id,
            site=request.site,
            region=request.region,
            materials=request.materials,
            signals=mock_signals,
            aggregates=aggregates,
            sources_used=["Mock Data"],
            cache_hit=False,
            processing_time_ms=10.0,
            generated_at=datetime.now()
        )
    
    def close(self):
        """Clean up resources"""
        for scraper in self.scrapers.values():
            try:
                scraper.close()
            except Exception as e:
                print(f"Error closing scraper: {e}")

