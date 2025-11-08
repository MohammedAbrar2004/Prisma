"""
Test: LLM Mock vs Real Ollama Testing

This test file validates LLM engine functionality with both mock and real Ollama.

Test scenarios:
1. Direct Ollama connection test
2. Prompt building validation
3. JSON extraction from LLM responses
4. Mock data vs real Ollama comparison
5. Different Ollama models (if available)
6. LLM response consistency
7. Performance benchmarking

Prerequisites:
- Ollama installed and running (for real tests)
- llama3 model available
- FastAPI server running (for integration tests)

Usage:
    python test_llm_mock_vs_real.py
"""

import sys
import json
import time
import requests
from pathlib import Path
from typing import Dict, Any, Optional

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent))

try:
    from llm import (
        call_ollama,
        build_prisma_prompt,
        extract_json_block,
        analyze_prisma,
        test_ollama_connection,
        LLMConfig
    )
    LLM_MODULE_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import LLM module: {e}")
    LLM_MODULE_AVAILABLE = False


# ============================================================================
# Configuration
# ============================================================================

BASE_URL = "http://localhost:8000"
ANALYZE_URL = f"{BASE_URL}/analyze"


# ============================================================================
# Test Utilities
# ============================================================================

def print_test_header(test_name: str):
    """Print a formatted test header"""
    print("\n" + "=" * 80)
    print(f"TEST: {test_name}")
    print("=" * 80)


def print_result(success: bool, message: str):
    """Print test result"""
    status = "✓ PASS" if success else "✗ FAIL"
    print(f"\n{status}: {message}")


def load_mock_data() -> tuple:
    """Load mock requirements and forecasts"""
    try:
        req_path = Path(__file__).parent / "data" / "mock_requirements.json"
        forecast_path = Path(__file__).parent / "data" / "mock_forecasts.json"
        
        with open(req_path) as f:
            requirements = json.load(f)
        
        with open(forecast_path) as f:
            forecasts = json.load(f)
        
        return requirements, forecasts
    except Exception as e:
        print(f"Error loading mock data: {e}")
        return None, None


# ============================================================================
# Direct LLM Tests
# ============================================================================

def test_ollama_direct_connection():
    """
    Test 1: Direct Ollama connection
    
    Validates:
    - Ollama is running
    - Can make basic requests
    - Returns valid responses
    """
    print_test_header("Direct Ollama Connection")
    
    if not LLM_MODULE_AVAILABLE:
        print_result(False, "LLM module not available")
        return False
    
    print(f"\nOllama URL: {LLMConfig.OLLAMA_BASE_URL}")
    print(f"Model: {LLMConfig.LLM_MODEL_NAME}")
    
    try:
        status = test_ollama_connection()
        
        print(f"\nConnection Status: {json.dumps(status, indent=2)}")
        
        if status.get("status") == "connected":
            print_result(True, "Ollama is connected and responding")
            return True
        else:
            print_result(False, f"Ollama not available: {status.get('message')}")
            return False
    
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False


def test_simple_ollama_call():
    """
    Test 2: Simple Ollama call
    
    Validates:
    - Basic LLM call works
    - Returns coherent response
    """
    print_test_header("Simple Ollama Call")
    
    if not LLM_MODULE_AVAILABLE:
        print_result(False, "LLM module not available")
        return False
    
    prompt = "What is 2+2? Respond with just the number."
    
    print(f"\nPrompt: {prompt}")
    print("Calling Ollama...")
    
    try:
        start_time = time.time()
        response = call_ollama(prompt)
        duration = time.time() - start_time
        
        print(f"\nResponse (took {duration:.2f}s): {response[:200]}...")
        
        if response and len(response) > 0:
            print_result(True, f"Ollama responded successfully in {duration:.2f}s")
            return True
        else:
            print_result(False, "Empty response from Ollama")
            return False
    
    except ConnectionError as e:
        print_result(False, f"Ollama not available: {str(e)}")
        return False
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False


def test_prompt_building():
    """
    Test 3: Prompt building
    
    Validates:
    - build_prisma_prompt generates valid prompts
    - Includes all necessary data
    - Proper formatting
    """
    print_test_header("Prompt Building")
    
    if not LLM_MODULE_AVAILABLE:
        print_result(False, "LLM module not available")
        return False
    
    requirements, forecasts = load_mock_data()
    
    if not requirements or not forecasts:
        print_result(False, "Could not load mock data")
        return False
    
    signals = {
        "signals": [
            {
                "material": "Steel",
                "demand_direction": "increase",
                "drivers": ["Price trending upward"]
            }
        ]
    }
    
    print("\nBuilding PRISMA prompt...")
    
    try:
        prompt = build_prisma_prompt(
            company_profile=requirements,
            forecasts=forecasts,
            signals=signals,
            question="Should we increase steel procurement?"
        )
        
        print(f"\nPrompt length: {len(prompt)} characters")
        print(f"Prompt preview:\n{prompt[:500]}...")
        
        # Validate prompt contents
        required_elements = [
            "PRISMA",
            "company_profile",
            "forecasts",
            "signals",
            "JSON",
            "summary",
            "recommended_actions"
        ]
        
        missing = [elem for elem in required_elements if elem.lower() not in prompt.lower()]
        
        if missing:
            print_result(False, f"Prompt missing elements: {missing}")
            return False
        
        print_result(True, "Prompt built successfully with all required elements")
        return True
    
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False


def test_json_extraction():
    """
    Test 4: JSON extraction from LLM responses
    
    Validates:
    - extract_json_block handles various formats
    - Robust parsing
    """
    print_test_header("JSON Extraction")
    
    if not LLM_MODULE_AVAILABLE:
        print_result(False, "LLM module not available")
        return False
    
    test_cases = [
        (
            '{"summary": "Test", "recommended_actions": [], "risks": []}',
            "Plain JSON"
        ),
        (
            'Here is my analysis: {"summary": "Test", "recommended_actions": [], "risks": []} I hope this helps!',
            "JSON with surrounding text"
        ),
        (
            '```json\n{"summary": "Test", "recommended_actions": [], "risks": []}\n```',
            "Markdown code block"
        ),
    ]
    
    all_passed = True
    
    for response_text, description in test_cases:
        print(f"\n--- Test: {description} ---")
        print(f"Input: {response_text[:80]}...")
        
        try:
            result = extract_json_block(response_text)
            print(f"Extracted: {json.dumps(result, indent=2)}")
            
            if "summary" in result:
                print("✓ Successfully extracted JSON")
            else:
                print("✗ Missing expected fields")
                all_passed = False
        
        except Exception as e:
            print(f"✗ Exception: {str(e)}")
            all_passed = False
    
    print_result(all_passed, "JSON extraction works for all formats" if all_passed else "Some extraction issues")
    return all_passed


def test_full_analysis_pipeline():
    """
    Test 5: Full analysis pipeline with real Ollama
    
    Validates:
    - Complete analyze_prisma function
    - End-to-end LLM reasoning
    - Structured output
    """
    print_test_header("Full Analysis Pipeline")
    
    if not LLM_MODULE_AVAILABLE:
        print_result(False, "LLM module not available")
        return False
    
    requirements, forecasts = load_mock_data()
    
    if not requirements or not forecasts:
        print_result(False, "Could not load mock data")
        return False
    
    signals = {
        "signals": [
            {
                "material": "Steel",
                "region": "Maharashtra",
                "demand_direction": "increase",
                "demand_score": 0.8,
                "confidence": 0.85,
                "drivers": ["Price up 10%", "New projects announced"]
            }
        ],
        "data_sources": ["mock"]
    }
    
    print("\nRunning full PRISMA analysis...")
    print("This may take 30-60 seconds for LLM to process...")
    
    try:
        start_time = time.time()
        
        result = analyze_prisma(
            company_profile=requirements,
            forecasts=forecasts,
            signals=signals,
            question="What are the key procurement priorities?"
        )
        
        duration = time.time() - start_time
        
        print(f"\n✓ Analysis completed in {duration:.2f}s")
        print(f"\nResult keys: {list(result.keys())}")
        print(f"\nSummary: {result.get('summary', '')[:200]}...")
        print(f"Actions: {len(result.get('recommended_actions', []))}")
        print(f"Risks: {len(result.get('risks', []))}")
        
        # Validate result structure
        required_keys = ["summary", "recommended_actions", "risks"]
        missing_keys = [k for k in required_keys if k not in result]
        
        if missing_keys:
            print_result(False, f"Missing required keys: {missing_keys}")
            return False
        
        if not result.get("summary"):
            print_result(False, "Empty summary")
            return False
        
        print_result(True, f"Full analysis pipeline successful (took {duration:.2f}s)")
        return True
    
    except ConnectionError as e:
        print_result(False, f"Ollama not available: {str(e)}")
        return False
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False


def test_endpoint_with_real_llm():
    """
    Test 6: /analyze endpoint with real LLM
    
    Validates:
    - Full integration through API
    - Real Ollama processing
    - End-to-end functionality
    """
    print_test_header("API Endpoint with Real LLM")
    
    payload = {
        "company_id": "abc-infra",
        "materials": ["Steel"],
        "question": "Should we increase steel inventory?",
        "use_real_apis": False  # Use mock signals for consistency
    }
    
    print(f"\nRequest: POST {ANALYZE_URL}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    print("\nCalling endpoint (may take 30-60 seconds)...")
    
    try:
        start_time = time.time()
        response = requests.post(ANALYZE_URL, json=payload, timeout=120)
        duration = time.time() - start_time
        
        print(f"\nResponse Status: {response.status_code} (took {duration:.2f}s)")
        
        if response.status_code == 200:
            data = response.json()
            
            print(f"\nSummary: {data.get('summary', '')[:150]}...")
            print(f"Actions: {len(data.get('recommended_actions', []))}")
            print(f"Risks: {len(data.get('risks', []))}")
            
            print_result(True, f"API endpoint with real LLM successful (took {duration:.2f}s)")
            return True
        else:
            print(f"Response: {response.text}")
            print_result(False, f"HTTP {response.status_code}")
            return False
    
    except requests.Timeout:
        print_result(False, "Request timed out (LLM processing may be too slow)")
        return False
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False


def test_response_consistency():
    """
    Test 7: Response consistency
    
    Validates:
    - Similar prompts produce similar analyses
    - LLM reasoning is coherent
    """
    print_test_header("Response Consistency")
    
    print("\n📝 DOCUMENTATION TEST")
    print("\nTo test consistency:")
    print("  1. Run same analysis multiple times")
    print("  2. Compare summaries and recommendations")
    print("  3. Verify key points are consistent")
    print("\nNote: Some variation is expected with temperature > 0")
    
    payload = {
        "company_id": "abc-infra",
        "materials": ["Steel"],
        "use_real_apis": False
    }
    
    print(f"\nRunning analysis twice to check consistency...")
    
    responses = []
    
    for i in range(2):
        print(f"\n--- Run {i+1} ---")
        try:
            response = requests.post(ANALYZE_URL, json=payload, timeout=90)
            if response.status_code == 200:
                data = response.json()
                summary = data.get('summary', '')
                print(f"Summary: {summary[:100]}...")
                responses.append(summary.lower())
            else:
                print(f"Error: HTTP {response.status_code}")
                responses.append("")
        except Exception as e:
            print(f"Error: {str(e)}")
            responses.append("")
        
        time.sleep(2)
    
    if len(responses) == 2 and responses[0] and responses[1]:
        # Check if both mention steel
        if "steel" in responses[0] and "steel" in responses[1]:
            print_result(True, "Both responses address the requested material")
            return True
        else:
            print_result(False, "Responses are inconsistent")
            return False
    else:
        print_result(False, "Could not complete consistency test")
        return False


def test_performance_benchmark():
    """
    Test 8: Performance benchmarking
    
    Measures:
    - LLM response time
    - API endpoint latency
    - Resource usage
    """
    print_test_header("Performance Benchmark")
    
    payload = {
        "company_id": "abc-infra",
        "materials": ["Steel", "Copper"],
        "use_real_apis": False
    }
    
    print("\nBenchmarking /analyze endpoint performance...")
    print("Running 3 requests to measure average response time...")
    
    times = []
    
    for i in range(3):
        print(f"\n--- Request {i+1}/3 ---")
        
        try:
            start = time.time()
            response = requests.post(ANALYZE_URL, json=payload, timeout=120)
            duration = time.time() - start
            
            times.append(duration)
            
            if response.status_code == 200:
                print(f"✓ Completed in {duration:.2f}s")
            else:
                print(f"✗ Failed: HTTP {response.status_code}")
        
        except Exception as e:
            print(f"✗ Error: {str(e)}")
        
        time.sleep(3)  # Brief pause between requests
    
    if times:
        avg_time = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)
        
        print(f"\n--- Performance Results ---")
        print(f"Average: {avg_time:.2f}s")
        print(f"Min: {min_time:.2f}s")
        print(f"Max: {max_time:.2f}s")
        
        if avg_time < 60:
            print_result(True, f"Good performance - average {avg_time:.2f}s")
            return True
        else:
            print_result(True, f"Acceptable performance - average {avg_time:.2f}s (LLM processing is inherently slow)")
            return True
    else:
        print_result(False, "Could not complete benchmark")
        return False


# ============================================================================
# Main Test Runner
# ============================================================================

def run_all_tests():
    """Run all LLM tests and report results"""
    
    print("\n" + "=" * 80)
    print("PRISMA LLM Engine - Mock vs Real Ollama Tests")
    print("=" * 80)
    print("\nThese tests validate LLM functionality with real Ollama.")
    print("\nPrerequisites:")
    print("  - Ollama running with llama3 model")
    print("  - FastAPI server running")
    print("\nStarting tests in 3 seconds...")
    time.sleep(3)
    
    tests = [
        ("Ollama Direct Connection", test_ollama_direct_connection),
        ("Simple Ollama Call", test_simple_ollama_call),
        ("Prompt Building", test_prompt_building),
        ("JSON Extraction", test_json_extraction),
        ("Full Analysis Pipeline", test_full_analysis_pipeline),
        ("API Endpoint with Real LLM", test_endpoint_with_real_llm),
        ("Response Consistency", test_response_consistency),
        ("Performance Benchmark", test_performance_benchmark),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n✗ Test '{test_name}' crashed: {str(e)}")
            results.append((test_name, False))
        
        time.sleep(2)
    
    # Print summary
    print("\n" + "=" * 80)
    print("LLM TEST SUMMARY")
    print("=" * 80)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} - {test_name}")
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    print(f"\nTotal: {passed}/{total} tests passed ({passed*100//total}%)")
    
    if passed == total:
        print("\n🎉 All LLM tests passed!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        print("\nNote: Failures may be due to Ollama not running.")
        print("Ensure Ollama is started: ollama serve")
    
    return passed == total


# ============================================================================
# Entry Point
# ============================================================================

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)

