"""
PRISMA LLM Module

This module provides LLM reasoning capabilities for PRISMA.

Main components:
- config: LLM configuration (Ollama settings)
- engine: Core LLM functions (prompt building, Ollama calls, analysis)
- utils: Helper utilities for data processing

Usage:
    from llm import analyze_prisma, LLMConfig
    
    result = analyze_prisma(company_profile, forecasts, signals)
    print(result['summary'])
"""

from .config import LLMConfig, OLLAMA_BASE_URL, LLM_MODEL_NAME
from .engine import (
    analyze_prisma,
    build_prisma_prompt,
    call_ollama,
    extract_json_block,
    test_ollama_connection,
)
from .utils import (
    format_analysis_summary,
    normalize_material_name,
    validate_company_profile,
    validate_forecasts,
    validate_signals,
)

__all__ = [
    # Config
    "LLMConfig",
    "OLLAMA_BASE_URL",
    "LLM_MODEL_NAME",
    # Engine
    "analyze_prisma",
    "build_prisma_prompt",
    "call_ollama",
    "extract_json_block",
    "test_ollama_connection",
    # Utils
    "format_analysis_summary",
    "normalize_material_name",
    "validate_company_profile",
    "validate_forecasts",
    "validate_signals",
]

