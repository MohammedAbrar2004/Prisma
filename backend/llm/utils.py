"""
PRISMA LLM Utilities

Helper functions for LLM operations and data processing.

This module provides utility functions for:
- Safe JSON extraction and normalization
- Input data validation and normalization
- Response formatting
- Debugging and logging helpers
"""

import json
import re
from typing import Any, Dict, List, Optional, Union


# ============================================================================
# JSON Utilities
# ============================================================================

def safe_json_loads(json_str: str, default: Any = None) -> Any:
    """
    Safely parse JSON string with fallback.
    
    Args:
        json_str: JSON string to parse
        default: Default value if parsing fails
    
    Returns:
        Parsed JSON or default value
    
    Example:
        >>> safe_json_loads('{"key": "value"}')
        {'key': 'value'}
        >>> safe_json_loads('invalid json', default={})
        {}
    """
    try:
        return json.loads(json_str)
    except (json.JSONDecodeError, TypeError):
        return default


def normalize_json_response(response: Union[str, Dict]) -> Dict[str, Any]:
    """
    Normalize LLM response to dict format.
    
    Handles cases where response might be:
    - Already a dict
    - A JSON string
    - A string containing JSON
    
    Args:
        response: LLM response in various formats
    
    Returns:
        Normalized dictionary
    
    Raises:
        ValueError: If response cannot be normalized
    """
    if isinstance(response, dict):
        return response
    
    if isinstance(response, str):
        # Try direct JSON parse
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            # Try to extract JSON from text
            from .engine import extract_json_block
            return extract_json_block(response)
    
    raise ValueError(f"Cannot normalize response of type {type(response)}")


# ============================================================================
# Input Validation & Normalization
# ============================================================================

def validate_company_profile(profile: Dict[str, Any]) -> bool:
    """
    Validate company profile structure.
    
    Args:
        profile: Company profile dictionary
    
    Returns:
        True if valid, False otherwise
    
    Example:
        >>> profile = {"company_id": "abc", "projects": [...]}
        >>> validate_company_profile(profile)
        True
    """
    required_fields = ["company_id"]
    return all(field in profile for field in required_fields)


def validate_forecasts(forecasts: Dict[str, Any]) -> bool:
    """
    Validate forecasts structure.
    
    Args:
        forecasts: Forecasts dictionary
    
    Returns:
        True if valid, False otherwise
    """
    required_fields = ["forecasts"]
    return all(field in forecasts for field in required_fields)


def validate_signals(signals: Dict[str, Any]) -> bool:
    """
    Validate signals structure.
    
    Args:
        signals: Signals dictionary
    
    Returns:
        True if valid, False otherwise
    """
    required_fields = ["signals"]
    return all(field in signals for field in required_fields)


def normalize_material_name(material: str) -> str:
    """
    Normalize material name for consistent matching.
    
    Args:
        material: Raw material name
    
    Returns:
        Normalized material name
    
    Example:
        >>> normalize_material_name("  steel  ")
        "Steel"
        >>> normalize_material_name("COPPER")
        "Copper"
    """
    return material.strip().title()


# ============================================================================
# Response Formatting
# ============================================================================

def format_analysis_summary(result: Dict[str, Any]) -> str:
    """
    Format analysis result as human-readable text.
    
    Args:
        result: Analysis result from analyze_prisma
    
    Returns:
        Formatted text summary
    
    Example:
        >>> formatted = format_analysis_summary(analysis_result)
        >>> print(formatted)
        Summary: Steel demand expected to increase...
        
        Recommended Actions:
        - Steel: Increase inventory...
    """
    lines = []
    
    # Summary
    lines.append("=== ANALYSIS SUMMARY ===")
    lines.append(result.get('summary', 'No summary available'))
    lines.append("")
    
    # Recommended Actions
    actions = result.get('recommended_actions', [])
    if actions:
        lines.append("=== RECOMMENDED ACTIONS ===")
        for action in actions:
            material = action.get('material', 'Unknown')
            action_text = action.get('action', 'No action')
            reason = action.get('reason', 'No reason provided')
            lines.append(f"• {material}: {action_text}")
            lines.append(f"  Reason: {reason}")
        lines.append("")
    
    # Risks
    risks = result.get('risks', [])
    if risks:
        lines.append("=== IDENTIFIED RISKS ===")
        for risk in risks:
            material = risk.get('material', 'Unknown')
            level = risk.get('risk_level', 'unknown').upper()
            drivers = risk.get('drivers', [])
            lines.append(f"• {material}: {level} RISK")
            if drivers:
                lines.append(f"  Drivers: {', '.join(drivers)}")
        lines.append("")
    
    # Watchlist
    watchlist = result.get('watchlist_materials', [])
    if watchlist:
        lines.append("=== WATCHLIST ===")
        for item in watchlist:
            material = item.get('material', 'Unknown')
            reason = item.get('reason', 'No reason provided')
            lines.append(f"• {material}: {reason}")
        lines.append("")
    
    return "\n".join(lines)


# ============================================================================
# Data Extraction Helpers
# ============================================================================

def extract_materials_from_profile(profile: Dict[str, Any]) -> List[str]:
    """
    Extract unique material names from company profile.
    
    Args:
        profile: Company profile dictionary
    
    Returns:
        List of unique material names
    
    Example:
        >>> materials = extract_materials_from_profile(profile)
        >>> print(materials)
        ['Steel', 'Copper', 'Concrete']
    """
    materials = set()
    
    projects = profile.get('projects', [])
    for project in projects:
        project_materials = project.get('materials', [])
        for material in project_materials:
            name = material.get('name', '')
            if name:
                materials.add(normalize_material_name(name))
    
    return sorted(list(materials))


def extract_materials_from_forecasts(forecasts: Dict[str, Any]) -> List[str]:
    """
    Extract unique material names from forecasts.
    
    Args:
        forecasts: Forecasts dictionary
    
    Returns:
        List of unique material names
    """
    materials = set()
    
    forecast_list = forecasts.get('forecasts', [])
    for forecast in forecast_list:
        material = forecast.get('material', '')
        if material:
            materials.add(normalize_material_name(material))
    
    return sorted(list(materials))


def extract_materials_from_signals(signals: Dict[str, Any]) -> List[str]:
    """
    Extract unique material names from signals.
    
    Args:
        signals: Signals dictionary
    
    Returns:
        List of unique material names
    """
    materials = set()
    
    signal_list = signals.get('signals', [])
    for signal in signal_list:
        material = signal.get('material', '')
        if material:
            materials.add(normalize_material_name(material))
    
    return sorted(list(materials))


# ============================================================================
# Debugging Helpers
# ============================================================================

def truncate_for_logging(data: Any, max_length: int = 500) -> str:
    """
    Truncate data for safe logging.
    
    Args:
        data: Data to truncate
        max_length: Maximum length
    
    Returns:
        Truncated string representation
    """
    data_str = str(data)
    if len(data_str) > max_length:
        return data_str[:max_length] + "..."
    return data_str


def get_data_summary(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get summary statistics of data for debugging.
    
    Args:
        data: Data dictionary
    
    Returns:
        Summary statistics
    
    Example:
        >>> summary = get_data_summary({"signals": [1, 2, 3], "count": 3})
        >>> print(summary)
        {'keys': ['signals', 'count'], 'total_keys': 2, 'signals_length': 3}
    """
    summary = {
        "keys": list(data.keys()),
        "total_keys": len(data),
    }
    
    # Add list lengths
    for key, value in data.items():
        if isinstance(value, list):
            summary[f"{key}_length"] = len(value)
        elif isinstance(value, dict):
            summary[f"{key}_keys"] = len(value)
    
    return summary


# ============================================================================
# Module Exports
# ============================================================================

__all__ = [
    "safe_json_loads",
    "normalize_json_response",
    "validate_company_profile",
    "validate_forecasts",
    "validate_signals",
    "normalize_material_name",
    "format_analysis_summary",
    "extract_materials_from_profile",
    "extract_materials_from_forecasts",
    "extract_materials_from_signals",
    "truncate_for_logging",
    "get_data_summary",
]

