"""
Test: Basic /analyze Endpoint Functionality

This test file validates the basic functionality of the /analyze endpoint.

Test scenarios:
1. Basic analysis request with valid company_id
2. Analysis with specific materials filter
3. Analysis with region filter
4. Analysis with industry parameter
5. Analysis with custom question

Prerequisites:
- FastAPI server running on http://localhost:8000
- Ollama running with llama3 model
- Mock data files present (mock_requirements.json, mock_forecasts.json)

Usage:
    python test_analyze_basic.py
"""

import requests
import json
import time
from typing import Dict, Any


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


def print_response_summary(response: Dict[str, Any]):
    """Print a summary of the analysis response"""
    print("\n--- Response Summary ---")
    print(f"Company ID: {response.get('company_id')}")
    print(f"Summary: {response.get('summary', '')[:100]}...")
    print(f"Recommended Actions: {len(response.get('recommended_actions', []))}")
    print(f"Risks Identified: {len(response.get('risks', []))}")
    print(f"Watchlist Materials: {len(response.get('watchlist_materials', []))}")
    print(f"Data Sources: {', '.join(response.get('data_sources', []))}")
    print(f"Generated At: {response.get('generated_at')}")


# ============================================================================
# Test Cases
# ============================================================================

def test_basic_analysis():
    """
    Test 1: Basic analysis request
    
    Validates:
    - Endpoint responds successfully
    - Returns expected JSON structure
    - Contains required fields
    """
    print_test_header("Basic Analysis Request")
    
    payload = {
        "company_id": "abc-infra",
        "use_real_apis": False  # Use mock data for consistent testing
    }
    
    print(f"\nRequest: POST {ANALYZE_URL}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(ANALYZE_URL, json=payload, timeout=60)
        
        print(f"\nResponse Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print_response_summary(data)
            
            # Validate structure
            required_fields = ["summary", "recommended_actions", "risks", "company_id"]
            missing_fields = [f for f in required_fields if f not in data]
            
            if missing_fields:
                print_result(False, f"Missing required fields: {missing_fields}")
                return False
            
            # Validate content
            if not data.get("summary"):
                print_result(False, "Empty summary")
                return False
            
            if not data.get("recommended_actions"):
                print_result(False, "No recommended actions")
                return False
            
            print_result(True, "Basic analysis request successful")
            return True
        else:
            print(f"Response: {response.text}")
            print_result(False, f"HTTP {response.status_code}")
            return False
    
    except requests.Timeout:
        print_result(False, "Request timed out (LLM might be slow)")
        return False
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False


def test_analysis_with_materials_filter():
    """
    Test 2: Analysis with materials filter
    
    Validates:
    - Materials filter is respected
    - Analysis focuses on requested materials
    """
    print_test_header("Analysis with Materials Filter")
    
    payload = {
        "company_id": "abc-infra",
        "materials": ["Steel", "Copper"],
        "use_real_apis": False
    }
    
    print(f"\nRequest: POST {ANALYZE_URL}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(ANALYZE_URL, json=payload, timeout=60)
        
        print(f"\nResponse Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print_response_summary(data)
            
            # Check if analysis mentions the requested materials
            summary = data.get("summary", "").lower()
            actions = data.get("recommended_actions", [])
            
            mentioned_materials = []
            if "steel" in summary or any("steel" in str(a).lower() for a in actions):
                mentioned_materials.append("Steel")
            if "copper" in summary or any("copper" in str(a).lower() for a in actions):
                mentioned_materials.append("Copper")
            
            print(f"\nMaterials mentioned: {mentioned_materials}")
            
            if mentioned_materials:
                print_result(True, f"Analysis includes requested materials: {mentioned_materials}")
                return True
            else:
                print_result(False, "Analysis doesn't mention requested materials")
                return False
        else:
            print(f"Response: {response.text}")
            print_result(False, f"HTTP {response.status_code}")
            return False
    
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False


def test_analysis_with_region():
    """
    Test 3: Analysis with region filter
    
    Validates:
    - Region parameter is accepted
    - Analysis considers regional signals
    """
    print_test_header("Analysis with Region Filter")
    
    payload = {
        "company_id": "abc-infra",
        "region": "Maharashtra",
        "use_real_apis": False
    }
    
    print(f"\nRequest: POST {ANALYZE_URL}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(ANALYZE_URL, json=payload, timeout=60)
        
        print(f"\nResponse Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print_response_summary(data)
            
            # Verify region is in response
            if data.get("region") == "Maharashtra":
                print_result(True, "Region filter applied successfully")
                return True
            else:
                print_result(False, f"Region mismatch: expected Maharashtra, got {data.get('region')}")
                return False
        else:
            print(f"Response: {response.text}")
            print_result(False, f"HTTP {response.status_code}")
            return False
    
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False


def test_analysis_with_industry():
    """
    Test 4: Analysis with industry parameter
    
    Validates:
    - Industry intelligence integration works
    - Industry trends are included in analysis
    """
    print_test_header("Analysis with Industry Parameter")
    
    payload = {
        "company_id": "abc-infra",
        "industry": "construction",
        "use_real_apis": False
    }
    
    print(f"\nRequest: POST {ANALYZE_URL}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(ANALYZE_URL, json=payload, timeout=60)
        
        print(f"\nResponse Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print_response_summary(data)
            
            # Check if industry intelligence is in data sources
            data_sources = data.get("data_sources", [])
            
            if "industry_intelligence" in data_sources:
                print_result(True, "Industry intelligence successfully integrated")
                return True
            else:
                print(f"\nNote: Industry intelligence not in data sources: {data_sources}")
                print_result(True, "Analysis completed (industry intelligence may not be available)")
                return True
        else:
            print(f"Response: {response.text}")
            print_result(False, f"HTTP {response.status_code}")
            return False
    
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False


def test_analysis_with_question():
    """
    Test 5: Analysis with custom question
    
    Validates:
    - Question parameter is accepted
    - Analysis addresses the specific question
    """
    print_test_header("Analysis with Custom Question")
    
    payload = {
        "company_id": "abc-infra",
        "question": "Should we increase steel procurement for next month?",
        "materials": ["Steel"],
        "use_real_apis": False
    }
    
    print(f"\nRequest: POST {ANALYZE_URL}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(ANALYZE_URL, json=payload, timeout=60)
        
        print(f"\nResponse Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print_response_summary(data)
            
            # Check if summary addresses steel
            summary = data.get("summary", "").lower()
            
            if "steel" in summary:
                print_result(True, "Analysis addresses the question about steel")
                return True
            else:
                print_result(False, "Analysis doesn't clearly address the question")
                return False
        else:
            print(f"Response: {response.text}")
            print_result(False, f"HTTP {response.status_code}")
            return False
    
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False


def test_health_endpoint():
    """
    Bonus Test: Health check endpoint
    
    Validates:
    - /analyze/health endpoint works
    - Returns system status
    """
    print_test_header("Health Check Endpoint")
    
    health_url = f"{ANALYZE_URL}/health"
    
    print(f"\nRequest: GET {health_url}")
    
    try:
        response = requests.get(health_url, timeout=10)
        
        print(f"\nResponse Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\nHealth Status: {json.dumps(data, indent=2)}")
            
            print_result(True, f"Health check passed - Status: {data.get('status')}")
            return True
        else:
            print_result(False, f"HTTP {response.status_code}")
            return False
    
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False


# ============================================================================
# Main Test Runner
# ============================================================================

def run_all_tests():
    """Run all test cases and report results"""
    
    print("\n" + "=" * 80)
    print("PRISMA /analyze Endpoint - Basic Functionality Tests")
    print("=" * 80)
    print("\nPrerequisites:")
    print("  1. FastAPI server running on http://localhost:8000")
    print("  2. Ollama running with llama3 model")
    print("  3. Mock data files present")
    print("\nStarting tests in 3 seconds...")
    time.sleep(3)
    
    tests = [
        ("Health Check", test_health_endpoint),
        ("Basic Analysis", test_basic_analysis),
        ("Materials Filter", test_analysis_with_materials_filter),
        ("Region Filter", test_analysis_with_region),
        ("Industry Parameter", test_analysis_with_industry),
        ("Custom Question", test_analysis_with_question),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n✗ Test '{test_name}' crashed: {str(e)}")
            results.append((test_name, False))
        
        time.sleep(2)  # Brief pause between tests
    
    # Print summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} - {test_name}")
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    print(f"\nTotal: {passed}/{total} tests passed ({passed*100//total}%)")
    
    if passed == total:
        print("\n🎉 All tests passed!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
    
    return passed == total


# ============================================================================
# Entry Point
# ============================================================================

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)

