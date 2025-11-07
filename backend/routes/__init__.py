"""
PRISMA API Routes

This package contains all FastAPI routers for the PRISMA backend.
"""

from .signals import router as signals_router

__all__ = ["signals_router"]

