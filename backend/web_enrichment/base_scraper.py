"""
Base scraper framework with rate limiting, caching, and robots.txt compliance
"""

import os
import time
import hashlib
import json
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from pathlib import Path
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

import requests
from bs4 import BeautifulSoup

from .models import EnrichmentSignal, EnrichmentSource, SignalType


class RateLimiter:
    """Simple rate limiter for API/scraping requests"""
    
    def __init__(self, requests_per_minute: int = 10):
        self.requests_per_minute = requests_per_minute
        self.min_interval = 60.0 / requests_per_minute
        self.last_request_time = 0.0
    
    def wait_if_needed(self):
        """Wait if necessary to respect rate limit"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.min_interval:
            sleep_time = self.min_interval - time_since_last
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()


class CacheManager:
    """File-based cache manager for scraped data"""
    
    def __init__(self, cache_dir: str = ".cache/web_enrichment", ttl_hours: int = 24):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.ttl = timedelta(hours=ttl_hours)
    
    def _get_cache_key(self, url: str, params: Optional[Dict] = None) -> str:
        """Generate cache key from URL and params"""
        key_str = url
        if params:
            key_str += json.dumps(params, sort_keys=True)
        return hashlib.md5(key_str.encode()).hexdigest()
    
    def get(self, url: str, params: Optional[Dict] = None) -> Optional[Dict]:
        """Get cached data if available and not expired"""
        cache_key = self._get_cache_key(url, params)
        cache_file = self.cache_dir / f"{cache_key}.json"
        
        if not cache_file.exists():
            return None
        
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                cached_data = json.load(f)
            
            # Check expiry
            cached_time = datetime.fromisoformat(cached_data['cached_at'])
            if datetime.now() - cached_time > self.ttl:
                cache_file.unlink()  # Delete expired cache
                return None
            
            return cached_data['data']
        
        except Exception as e:
            print(f"Cache read error: {e}")
            return None
    
    def set(self, url: str, data: Dict, params: Optional[Dict] = None):
        """Cache data"""
        cache_key = self._get_cache_key(url, params)
        cache_file = self.cache_dir / f"{cache_key}.json"
        
        try:
            cache_data = {
                'url': url,
                'params': params,
                'cached_at': datetime.now().isoformat(),
                'data': data
            }
            
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, indent=2, default=str)
        
        except Exception as e:
            print(f"Cache write error: {e}")
    
    def clear(self):
        """Clear all cached data"""
        for cache_file in self.cache_dir.glob("*.json"):
            cache_file.unlink()


class RobotsChecker:
    """Check robots.txt compliance"""
    
    def __init__(self):
        self.parsers: Dict[str, RobotFileParser] = {}
    
    def can_fetch(self, url: str, user_agent: str = "PRISMA-Bot/1.0") -> bool:
        """Check if URL can be fetched according to robots.txt"""
        parsed = urlparse(url)
        base_url = f"{parsed.scheme}://{parsed.netloc}"
        
        if base_url not in self.parsers:
            parser = RobotFileParser()
            parser.set_url(f"{base_url}/robots.txt")
            try:
                parser.read()
                self.parsers[base_url] = parser
            except Exception as e:
                print(f"Could not read robots.txt for {base_url}: {e}")
                # If we can't read robots.txt, assume we can fetch (be conservative)
                return True
        
        return self.parsers[base_url].can_fetch(user_agent, url)


class BaseScraper(ABC):
    """
    Abstract base class for all scrapers
    
    Provides:
    - Rate limiting
    - Caching
    - Robots.txt compliance
    - Common HTTP request handling
    - Error handling
    """
    
    def __init__(
        self,
        name: str,
        source_type: str = "scraper",
        requests_per_minute: int = 10,
        cache_ttl_hours: int = 24,
        respect_robots: bool = True,
        user_agent: str = "PRISMA-Bot/1.0 (Procurement Intelligence)"
    ):
        self.name = name
        self.source_type = source_type
        self.user_agent = user_agent
        self.respect_robots = respect_robots
        
        # Initialize components
        self.rate_limiter = RateLimiter(requests_per_minute)
        self.cache_manager = CacheManager(ttl_hours=cache_ttl_hours)
        self.robots_checker = RobotsChecker()
        
        # Session for connection pooling
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': self.user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        })
    
    def _can_fetch(self, url: str) -> bool:
        """Check if URL can be fetched"""
        if not self.respect_robots:
            return True
        return self.robots_checker.can_fetch(url, self.user_agent)
    
    def fetch_url(
        self,
        url: str,
        params: Optional[Dict] = None,
        use_cache: bool = True,
        timeout: int = 10
    ) -> Optional[str]:
        """
        Fetch URL content with rate limiting, caching, and robots.txt compliance
        
        Returns:
            HTML content as string, or None if fetch failed
        """
        # Check robots.txt
        if not self._can_fetch(url):
            print(f"Blocked by robots.txt: {url}")
            return None
        
        # Check cache
        if use_cache:
            cached = self.cache_manager.get(url, params)
            if cached:
                return cached.get('content')
        
        # Rate limit
        self.rate_limiter.wait_if_needed()
        
        # Fetch
        try:
            response = self.session.get(url, params=params, timeout=timeout)
            response.raise_for_status()
            content = response.text
            
            # Cache the result
            if use_cache:
                self.cache_manager.set(url, {'content': content}, params)
            
            return content
        
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    def parse_html(self, html: str) -> BeautifulSoup:
        """Parse HTML content"""
        return BeautifulSoup(html, 'html.parser')
    
    def create_source(self, url: Optional[str] = None, reliability: float = 0.7) -> EnrichmentSource:
        """Create source metadata"""
        return EnrichmentSource(
            name=self.name,
            type=self.source_type,
            url=url,
            reliability_score=reliability,
            last_updated=datetime.now()
        )
    
    @abstractmethod
    def scrape(
        self,
        region: Optional[str] = None,
        materials: Optional[List[str]] = None,
        time_window_days: int = 30,
        use_cache: bool = True
    ) -> List[EnrichmentSignal]:
        """
        Scrape and return enrichment signals
        
        Must be implemented by subclasses
        """
        pass
    
    @abstractmethod
    def get_signal_type(self) -> SignalType:
        """Return the type of signals this scraper produces"""
        pass
    
    def close(self):
        """Clean up resources"""
        self.session.close()

