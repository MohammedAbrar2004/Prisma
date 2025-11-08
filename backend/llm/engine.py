"""
PRISMA LLM Reasoning Engine

Framework-agnostic LLM client for PRISMA demand forecasting analysis.

This module provides the core LLM reasoning layer that:
1. Consumes company profiles, forecasts, and external signals
2. Generates human-readable summaries and structured recommendations
3. Uses local Ollama (llama3) for inference

Design principles:
- Framework-agnostic: No FastAPI/DB dependencies
- Robust error handling
- Clear prompt engineering with schema enforcement
- Deterministic output structure

Integration:
- Forecasts: from backend/data/mock_forecasts.json (or future ML models)
- External signals: from external_signals.engine.build_signals()
- Output: feeds into /analyze API route
"""

import json
import re
import requests
from typing import Any, Dict, List, Optional

from .config import LLMConfig


# ============================================================================
# Core LLM Functions
# ============================================================================

def build_prisma_prompt(
    company_profile: Dict[str, Any],
    forecasts: Dict[str, Any],
    signals: Dict[str, Any],
    question: Optional[str] = None
) -> str:
    """
    Build a deterministic system + user prompt for PRISMA analysis.
    
    This function constructs a comprehensive prompt that:
    - Explains the assistant's role as a supply chain advisor
    - Provides all relevant data (company, forecasts, signals)
    - Instructs the model to use ONLY provided data (no hallucinations)
    - Specifies the expected JSON output format
    - Optionally includes a specific question from the user
    
    Args:
        company_profile: Company information and material requirements
        forecasts: Demand forecasts for materials
        signals: External demand risk signals
        question: Optional specific question to answer
    
    Returns:
        Formatted prompt string ready for LLM
    
    Example:
        >>> prompt = build_prisma_prompt(company_data, forecast_data, signal_data)
        >>> response = call_ollama(prompt)
    """
    
    # Build the system context
    system_context = """You are PRISMA - an AI advisor for supply chain planning and materials procurement.

Your role is to analyze material demand forecasts and external market signals to provide actionable recommendations for procurement teams.

CRITICAL RULES:
1. USE ONLY THE DATA PROVIDED BELOW - Do not make up prices, statistics, or events
2. If data is missing or insufficient, explicitly state "insufficient data for [specific aspect]"
3. Do not hallucinate vendor names, specific contracts, or fake regulations
4. Base ALL recommendations on the provided forecasts and signals
5. You MUST output valid JSON in the exact format specified

Your analysis should help procurement managers:
- Understand demand trends and risks
- Prioritize materials that need attention
- Make informed sourcing decisions
- Anticipate supply chain disruptions
"""

    # Add the data sections
    company_section = f"""
=== COMPANY PROFILE ===
{json.dumps(company_profile, indent=2)}
"""

    forecasts_section = f"""
=== DEMAND FORECASTS ===
{json.dumps(forecasts, indent=2)}
"""

    signals_section = f"""
=== EXTERNAL MARKET SIGNALS ===
{json.dumps(signals, indent=2)}
"""

    # Define the expected output schema
    output_schema = """
=== REQUIRED OUTPUT FORMAT ===

You MUST respond with ONLY valid JSON in this exact structure:

{
  "answer": "Direct answer to the question (if question provided, otherwise 'N/A')",
  "summary": "A concise 2-3 sentence summary of the overall procurement situation and key insights",
  "recommended_actions": [
    {
      "material": "Material name (e.g., Steel, Copper)",
      "action": "Specific action to take (e.g., 'Increase inventory', 'Accelerate procurement', 'Monitor closely')",
      "reason": "Clear explanation based on forecasts and signals"
    }
  ],
  "risks": [
    {
      "material": "Material name",
      "risk_level": "low|medium|high",
      "drivers": ["List of specific risk factors from the signals"]
    }
  ],
  "watchlist_materials": [
    {
      "material": "Material name",
      "reason": "Why this material needs monitoring"
    }
  ]
}

IMPORTANT:
- If a question is provided, "answer" field MUST directly answer that question first
- "answer" should be concise (1-2 sentences) and reference specific data
- Include AT LEAST one item in recommended_actions
- Include AT LEAST one item in risks
- watchlist_materials can be empty if no materials need special monitoring
- Do NOT include any text outside the JSON object
- Do NOT use markdown code blocks - just output raw JSON
"""

    # Add optional question section
    question_section = ""
    if question:
        question_section = f"""
=== SPECIFIC QUESTION TO ANSWER ===
{question}

CRITICAL: You MUST directly answer this question first, before providing general analysis.
- If asking about company name: Answer with the exact company name from company_profile
- If asking about specific materials: Reference the exact data from forecasts/signals
- If asking about risks: List specific risks from the signals data
- Be precise and direct - answer the question explicitly, then provide supporting analysis
"""

    # Construct final prompt - put question BEFORE output schema if provided
    if question:
        prompt = f"""{system_context}

{company_section}

{forecasts_section}

{signals_section}

{question_section}

{output_schema}

Now, analyze the above data and DIRECTLY ANSWER THE QUESTION FIRST, then provide your response in the required JSON format:"""
    else:
        prompt = f"""{system_context}

{company_section}

{forecasts_section}

{signals_section}

{output_schema}

Now, analyze the above data and provide your response in the required JSON format:"""

    return prompt


def call_ollama(
    prompt: str,
    model: Optional[str] = None,
    base_url: Optional[str] = None,
) -> str:
    """
    Call local Ollama API to generate a response.
    
    This function makes a synchronous HTTP POST request to the Ollama
    generate endpoint and returns the raw text response.
    
    Args:
        prompt: The complete prompt to send to the model
        model: Model name (default: from LLMConfig.LLM_MODEL_NAME)
        base_url: Ollama base URL (default: from LLMConfig.OLLAMA_BASE_URL)
    
    Returns:
        Raw text response from the model
    
    Raises:
        ConnectionError: If Ollama service is not reachable
        requests.Timeout: If request times out
        requests.RequestException: For other HTTP errors
        ValueError: If response format is invalid
    
    Example:
        >>> response = call_ollama("What is the capital of France?")
        >>> print(response)
        "Paris is the capital of France."
    """
    
    # Use provided values or fall back to config
    model_name = model or LLMConfig.get_model_name()
    ollama_url = f"{base_url or LLMConfig.OLLAMA_BASE_URL}/api/generate"
    
    # Prepare the request payload
    payload = {
        "model": model_name,
        "prompt": prompt,
        "stream": False,  # We want complete response, not streaming
        "options": {
            "temperature": LLMConfig.LLM_TEMPERATURE,
            "num_predict": LLMConfig.LLM_MAX_TOKENS,
        }
    }
    
    try:
        # Make the request
        response = requests.post(
            ollama_url,
            json=payload,
            timeout=LLMConfig.REQUEST_TIMEOUT
        )
        
        # Check for HTTP errors
        response.raise_for_status()
        
        # Parse the response
        response_data = response.json()
        
        # Ollama returns response in 'response' field
        if 'response' not in response_data:
            raise ValueError(f"Invalid Ollama response format: {response_data}")
        
        return response_data['response']
    
    except requests.ConnectionError as e:
        raise ConnectionError(
            f"LLM service unavailable; ensure Ollama is running at {ollama_url}. "
            f"Start Ollama with: 'ollama serve' or check if it's running on a different port. "
            f"Error: {str(e)}"
        )
    
    except requests.Timeout as e:
        raise requests.Timeout(
            f"LLM request timed out after {LLMConfig.REQUEST_TIMEOUT} seconds. "
            f"The model might be processing a complex prompt or the service is overloaded. "
            f"Error: {str(e)}"
        )
    
    except requests.RequestException as e:
        raise requests.RequestException(
            f"Error calling Ollama API at {ollama_url}: {str(e)}"
        )
    
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Invalid JSON response from Ollama: {str(e)}"
        )


def extract_json_block(raw_response: str) -> Dict[str, Any]:
    """
    Robustly extract JSON object from the model's raw response.
    
    LLMs sometimes include explanatory text before/after the JSON.
    This function finds and extracts the JSON object.
    
    Strategy:
    1. Find the first '{' and last '}' in the response
    2. Extract that substring
    3. Parse as JSON
    4. Validate basic structure
    
    Args:
        raw_response: Raw text response from the LLM
    
    Returns:
        Parsed JSON object as a dictionary
    
    Raises:
        ValueError: If no valid JSON found or parsing fails
    
    Example:
        >>> raw = "Here's my analysis: {\"summary\": \"...\", \"risks\": []} Hope this helps!"
        >>> result = extract_json_block(raw)
        >>> print(result['summary'])
        "..."
    """
    
    if not raw_response or not raw_response.strip():
        raise ValueError("Empty response from LLM - cannot extract JSON")
    
    # Remove markdown code blocks if present
    # Some models might return: ```json\n{...}\n```
    cleaned = re.sub(r'```json\s*', '', raw_response)
    cleaned = re.sub(r'```\s*$', '', cleaned)
    
    # Find the first '{' and last '}'
    first_brace = cleaned.find('{')
    last_brace = cleaned.rfind('}')
    
    if first_brace == -1 or last_brace == -1 or first_brace >= last_brace:
        raise ValueError(
            f"No valid JSON object found in response. "
            f"Response: {raw_response[:200]}..."
        )
    
    # Extract the JSON substring
    json_str = cleaned[first_brace:last_brace + 1]
    
    try:
        # Parse the JSON
        parsed = json.loads(json_str)
        
        # Validate basic structure
        if not isinstance(parsed, dict):
            raise ValueError("Extracted JSON is not an object/dictionary")
        
        # Check for required fields (at minimum should have summary)
        if 'summary' not in parsed:
            raise ValueError(
                "JSON missing required 'summary' field. "
                "LLM may not have followed the output schema."
            )
        
        # Ensure answer field exists if question was provided
        if 'answer' not in parsed:
            parsed['answer'] = parsed.get('summary', 'N/A')
        
        return parsed
    
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Failed to parse JSON from response. "
            f"JSON string: {json_str[:200]}... "
            f"Error: {str(e)}"
        )


def analyze_prisma(
    company_profile: Dict[str, Any],
    forecasts: Dict[str, Any],
    signals: Dict[str, Any],
    question: Optional[str] = None
) -> Dict[str, Any]:
    """
    Main orchestration function for PRISMA analysis.
    
    This is the primary entrypoint used by API routes. It coordinates
    the entire LLM reasoning pipeline:
    
    1. Build prompt with company data, forecasts, and signals
    2. Call Ollama to generate analysis
    3. Extract and validate JSON response
    4. Return structured recommendations
    
    Args:
        company_profile: Company information and material requirements
        forecasts: Demand forecasts for materials
        signals: External demand risk signals from external_signals.engine
        question: Optional specific question to answer
    
    Returns:
        Dictionary with structure:
        {
            "summary": str,
            "recommended_actions": List[Dict],
            "risks": List[Dict],
            "watchlist_materials": List[Dict]
        }
    
    Raises:
        ConnectionError: If Ollama is not available
        ValueError: If LLM response is invalid
        Exception: For other errors during analysis
    
    Example:
        >>> result = analyze_prisma(company_data, forecast_data, signal_data)
        >>> print(result['summary'])
        "Steel demand expected to increase 15% with high price volatility..."
        >>> for action in result['recommended_actions']:
        ...     print(f"{action['material']}: {action['action']}")
    """
    
    try:
        # Step 1: Build the prompt
        prompt = build_prisma_prompt(
            company_profile=company_profile,
            forecasts=forecasts,
            signals=signals,
            question=question
        )
        
        # Step 2: Call Ollama
        raw_response = call_ollama(prompt)
        
        # Step 3: Extract JSON
        result = extract_json_block(raw_response)
        
        # Step 4: Ensure all expected keys exist (with defaults if missing)
        result.setdefault('answer', 'N/A' if not question else 'Analysis provided')
        result.setdefault('summary', 'Analysis completed')
        result.setdefault('recommended_actions', [])
        result.setdefault('risks', [])
        result.setdefault('watchlist_materials', [])
        
        return result
    
    except ConnectionError:
        # Re-raise connection errors with clear message
        raise
    
    except ValueError as e:
        # Re-raise value errors (JSON parsing issues)
        raise ValueError(f"LLM analysis failed: {str(e)}")
    
    except Exception as e:
        # Catch-all for unexpected errors
        raise Exception(f"Unexpected error during PRISMA analysis: {str(e)}")


# ============================================================================
# Utility Functions
# ============================================================================

def test_ollama_connection() -> Dict[str, Any]:
    """
    Test connectivity to Ollama service.
    
    Returns:
        Dictionary with connection status and details
    
    Example:
        >>> status = test_ollama_connection()
        >>> print(status['status'])
        'connected'
    """
    
    try:
        # Try a simple prompt
        response = call_ollama("Hello", model=LLMConfig.LLM_MODEL_NAME)
        
        return {
            "status": "connected",
            "model": LLMConfig.LLM_MODEL_NAME,
            "base_url": LLMConfig.OLLAMA_BASE_URL,
            "message": "Ollama is reachable and responding"
        }
    
    except ConnectionError as e:
        return {
            "status": "disconnected",
            "model": LLMConfig.LLM_MODEL_NAME,
            "base_url": LLMConfig.OLLAMA_BASE_URL,
            "error": str(e),
            "message": "Ollama is not reachable. Ensure it's running: 'ollama serve'"
        }
    
    except Exception as e:
        return {
            "status": "error",
            "model": LLMConfig.LLM_MODEL_NAME,
            "base_url": LLMConfig.OLLAMA_BASE_URL,
            "error": str(e),
            "message": "Unexpected error testing Ollama connection"
        }


# ============================================================================
# Module Exports
# ============================================================================

__all__ = [
    "build_prisma_prompt",
    "call_ollama",
    "extract_json_block",
    "analyze_prisma",
    "test_ollama_connection",
]

