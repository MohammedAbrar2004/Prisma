"""
PRISMA LLM Configuration

Central configuration for LLM integration with Ollama.

This module provides environment-based configuration for:
- Ollama connection settings
- Model selection
- LLM parameters

Design:
- Load from environment variables with sensible defaults
- No hard-coded secrets
- Easy to override for testing
"""

import os
from typing import Optional


# ============================================================================
# Ollama Configuration
# ============================================================================

class LLMConfig:
    """
    Central configuration class for LLM integration.
    
    Environment Variables:
    - OLLAMA_BASE_URL: Base URL for Ollama API (default: http://localhost:11434)
    - LLM_MODEL_NAME: Model name to use (default: llama3)
    - LLM_TEMPERATURE: Temperature for generation (default: 0.7)
    - LLM_MAX_TOKENS: Maximum tokens to generate (default: 2000)
    """
    
    # Ollama Connection
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    
    # Model Selection
    LLM_MODEL_NAME: str = os.getenv("LLM_MODEL_NAME", "llama3")
    
    # Generation Parameters
    LLM_TEMPERATURE: float = float(os.getenv("LLM_TEMPERATURE", "0.7"))
    LLM_MAX_TOKENS: int = int(os.getenv("LLM_MAX_TOKENS", "2000"))
    
    # Timeout Configuration
    REQUEST_TIMEOUT: int = int(os.getenv("LLM_REQUEST_TIMEOUT", "120"))  # 2 minutes for LLM calls
    
    @classmethod
    def get_ollama_url(cls) -> str:
        """Get the full Ollama API URL for generate endpoint"""
        return f"{cls.OLLAMA_BASE_URL}/api/generate"
    
    @classmethod
    def get_model_name(cls) -> str:
        """Get the configured model name"""
        return cls.LLM_MODEL_NAME
    
    @classmethod
    def is_configured(cls) -> bool:
        """
        Check if LLM is properly configured.
        
        For Ollama, we just need a valid base URL.
        No API keys required since it's local.
        """
        return bool(cls.OLLAMA_BASE_URL)
    
    @classmethod
    def get_config_summary(cls) -> dict:
        """
        Get a summary of current configuration.
        
        Useful for debugging and logging.
        """
        return {
            "ollama_base_url": cls.OLLAMA_BASE_URL,
            "model_name": cls.LLM_MODEL_NAME,
            "temperature": cls.LLM_TEMPERATURE,
            "max_tokens": cls.LLM_MAX_TOKENS,
            "timeout": cls.REQUEST_TIMEOUT,
            "configured": cls.is_configured()
        }


# ============================================================================
# Convenience Exports
# ============================================================================

# Export commonly used values for convenience
OLLAMA_BASE_URL = LLMConfig.OLLAMA_BASE_URL
LLM_MODEL_NAME = LLMConfig.LLM_MODEL_NAME
LLM_TEMPERATURE = LLMConfig.LLM_TEMPERATURE
LLM_MAX_TOKENS = LLMConfig.LLM_MAX_TOKENS

# Export the config class
__all__ = [
    "LLMConfig",
    "OLLAMA_BASE_URL",
    "LLM_MODEL_NAME",
    "LLM_TEMPERATURE",
    "LLM_MAX_TOKENS",
]

