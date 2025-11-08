"""
PRISMA Search Module

This module provides industry intelligence and custom search capabilities.

Main components:
- industry: Industry trend signals and intelligence

Usage:
    from search import get_industry_trends
    
    trends = get_industry_trends("Construction")
"""

from .industry import get_industry_trends, get_industry_signals

__all__ = [
    "get_industry_trends",
    "get_industry_signals",
]

