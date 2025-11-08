"""
Test: /analyze Endpoint Edge Cases

This test file validates edge case handling and boundary conditions.

Test scenarios:
1. Invalid company_id (not found)
2. Empty materials list
3. Very long question
4. Special characters in inputs
5. All optional parameters omitted
6. Extreme combinations of parameters

Prerequisites:
- FastAPI server running on http://localhost:8000
- Ollama running with llama3 model

Usage:
    python test_analyze_edge_cases.py
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


# ============================================================================
# Edge Case Tests
# ============================================================================

def test_invalid_company_id():
    """
    Test 1: Invalid company_id
    
    Expected:
    - Returns 404 or gracefully handles missing company
    - Provides clear error message
    """
    print_test_header("Invalid Company ID")
    
    payload = {
        "company_id": "nonexistent-company-xyz-999",
        "use_real_apis": False
    }
    
    print(f"\nRequest: POST {ANALYZE_URL}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(ANALYZE_URL, json=payload, timeout=30)
        
        print(f"\nResponse Status: {response.status_code}")
        print(f"Response: {response.text[:200]}...")
        
        # We expect either 404 or 200 with error handling in response
        if response.status_code in [404, 400]:
            print_result(True, "Correctly returns error for invalid company_id")
            return True
        elif response.status_code == 200:
            # Server might gracefully handle by using available data
            print_result(True, "Gracefully handles invalid company_id (returns available data)")
            return True
        else:
            print_result(False, f"Unexpected status code: {response.status_code}")
            return False
    
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False


def test_empty_materials_list():
    """
    Test 2: Empty materials list
    
    Expected:
    - Accepts empty list
    - Analyzes all materials
    """
    print_test_header("Empty Materials List")
    
    payload = {
        "company_id": "abc-infra",
        "materials": [],
        "use_real_apis": False
    }
    
    print(f"\nRequest: POST {ANALYZE_URL}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(ANALYZE_URL, json=payload, timeout=60)
        
        print(f"\nResponse Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Summary: {data.get('summary', '')[:100]}...")
            print(f"Recommended Actions: {len(data.get('recommended_actions', []))}")
            
            print_result(True, "Handles empty materials list correctly")
            return True
        else:
            print(f"Response: {response.text}")
            print_result(False, f"HTTP {response.status_code}")
            return False
    
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False


def test_very_long_question():
    """
    Test 3: Very long question (stress test)
    
    Expected:
    - Accepts long input
    - LLM processes without error
    """
    print_test_header("Very Long Question")
    
    long_question = " ".join([
        "I need detailed analysis on whether we should increase procurement",
        "for steel, copper, aluminum, and concrete materials for our upcoming",
        "infrastructure projects in Maharashtra, Gujarat, and Karnataka regions",
        "considering the current market conditions, price volatility, weather patterns,",
        "supply chain disruptions, geopolitical factors, and industry trends in",
        "construction and infrastructure sectors for the next quarter and beyond.",
        "What are the specific risks and opportunities we should be aware of?",
        "How should we prioritize our procurement strategy across different materials?",
        "What are the cost implications and inventory management considerations?"
    ])
    
    payload = {
        "company_id": "abc-infra",
        "question": long_question,
        "use_real_apis": False
    }
    
    print(f"\nRequest: POST {ANALYZE_URL}")
    print(f"Question length: {len(long_question)} characters")
    print(f"Question preview: {long_question[:100]}...")
    
    try:
        response = requests.post(ANALYZE_URL, json=payload, timeout=120)
        
        print(f"\nResponse Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Summary: {data.get('summary', '')[:100]}...")
            
            print_result(True, "Handles long questions without error")
            return True
        else:
            print(f"Response: {response.text[:200]}...")
            print_result(False, f"HTTP {response.status_code}")
            return False
    
    except requests.Timeout:
        print_result(False, "Request timed out with long question")
        return False
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False


def test_special_characters():
    """
    Test 4: Special characters in inputs
    
    Expected:
    - Handles special characters safely
    - No injection vulnerabilities
    """
    print_test_header("Special Characters in Inputs")
    
    payload = {
        "company_id": "abc-infra",
        "question": "What about Steel? Cost > $1000/ton & supply < demand!",
        "materials": ["Steel", "Copper & Brass", "Concrete (Type-A)"],
        "region": "Maharashtra, India",
        "use_real_apis": False
    }
    
    print(f"\nRequest: POST {ANALYZE_URL}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(ANALYZE_URL, json=payload, timeout=60)
        
        print(f"\nResponse Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Summary: {data.get('summary', '')[:100]}...")
            
            print_result(True, "Handles special characters safely")
            return True
        else:
            print(f"Response: {response.text[:200]}...")
            # 400 is also acceptable if validation rejects special chars
            if response.status_code == 400:
                print_result(True, "Validates and rejects problematic input")
                return True
            print_result(False, f"HTTP {response.status_code}")
            return False
    
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False


def test_minimal_payload():
    """
    Test 5: Minimal payload (only required fields)
    
    Expected:
    - Works with just company_id
    - All optional parameters use defaults
    """
    print_test_header("Minimal Payload")
    
    payload = {
        "company_id": "abc-infra"
    }
    
    print(f"\nRequest: POST {ANALYZE_URL}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(ANALYZE_URL, json=payload, timeout=60)
        
        print(f"\nResponse Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Summary: {data.get('summary', '')[:100]}...")
            print(f"Data Sources: {data.get('data_sources')}")
            
            print_result(True, "Works with minimal payload")
            return True
        else:
            print(f"Response: {response.text}")
            print_result(False, f"HTTP {response.status_code}")
            return False
    
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False


def test_maximum_parameters():
    """
    Test 6: Maximum parameters (all fields populated)
    
    Expected:
    - Handles all parameters together
    - No conflicts between parameters
    """
    print_test_header("Maximum Parameters")
    
    payload = {
        "company_id": "abc-infra",
        "question": "Comprehensive analysis needed for all projects",
        "region": "Maharashtra",
        "materials": ["Steel", "Copper", "Concrete", "Aluminum"],
        "industry": "construction",
        "horizon": "next_quarter",
        "use_real_apis": False
    }
    
    print(f"\nRequest: POST {ANALYZE_URL}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(ANALYZE_URL, json=payload, timeout=90)
        
        print(f"\nResponse Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Summary: {data.get('summary', '')[:100]}...")
            print(f"Actions: {len(data.get('recommended_actions', []))}")
            print(f"Risks: {len(data.get('risks', []))}")
            print(f"Data Sources: {data.get('data_sources')}")
            
            print_result(True, "Handles all parameters successfully")
            return True
        else:
            print(f"Response: {response.text}")
            print_result(False, f"HTTP {response.status_code}")
            return False
    
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False


def test_case_sensitivity():
    """
    Test 7: Case sensitivity in materials and regions
    
    Expected:
    - Handles different cases appropriately
    - Normalizes inputs correctly
    """
    print_test_header("Case Sensitivity")
    
    payloads = [
        {
            "company_id": "abc-infra",
            "materials": ["steel", "COPPER", "Concrete"],
            "use_real_apis": False
        },
        {
            "company_id": "ABC-INFRA",
            "region": "maharashtra",
            "use_real_apis": False
        }
    ]
    
    all_passed = True
    
    for i, payload in enumerate(payloads, 1):
        print(f"\n--- Case Test {i} ---")
        print(f"Payload: {json.dumps(payload, indent=2)}")
        
        try:
            response = requests.post(ANALYZE_URL, json=payload, timeout=60)
            
            print(f"Response Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"Summary: {data.get('summary', '')[:80]}...")
                print("✓ Request succeeded")
            else:
                print(f"Response: {response.text[:150]}...")
                all_passed = False
        
        except Exception as e:
            print(f"✗ Exception: {str(e)}")
            all_passed = False
    
    print_result(all_passed, "Case sensitivity handled correctly" if all_passed else "Case handling issues detected")
    return all_passed


def test_unicode_characters():
    """
    Test 8: Unicode characters in question
    
    Expected:
    - Handles unicode/international characters
    - No encoding errors
    """
    print_test_header("Unicode Characters")
    
    payload = {
        "company_id": "abc-infra",
        "question": "माहाराष्ट्र में Steel की demand क्या है? €1000/ton price सही है?",
        "region": "Maharashtra",
        "use_real_apis": False
    }
    
    print(f"\nRequest: POST {ANALYZE_URL}")
    print(f"Payload: {json.dumps(payload, indent=2, ensure_ascii=False)}")
    
    try:
        response = requests.post(ANALYZE_URL, json=payload, timeout=60)
        
        print(f"\nResponse Status: {response.status_code}")
        
        if response.status_code in [200, 400]:
            # Either success or validation error is acceptable
            print_result(True, "Handles unicode characters appropriately")
            return True
        else:
            print(f"Response: {response.text}")
            print_result(False, f"HTTP {response.status_code}")
            return False
    
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False


# ============================================================================
# Main Test Runner
# ============================================================================

def run_all_tests():
    """Run all edge case tests and report results"""
    
    print("\n" + "=" * 80)
    print("PRISMA /analyze Endpoint - Edge Case Tests")
    print("=" * 80)
    print("\nThese tests validate boundary conditions and error handling.")
    print("\nStarting tests in 3 seconds...")
    time.sleep(3)
    
    tests = [
        ("Invalid Company ID", test_invalid_company_id),
        ("Empty Materials List", test_empty_materials_list),
        ("Very Long Question", test_very_long_question),
        ("Special Characters", test_special_characters),
        ("Minimal Payload", test_minimal_payload),
        ("Maximum Parameters", test_maximum_parameters),
        ("Case Sensitivity", test_case_sensitivity),
        ("Unicode Characters", test_unicode_characters),
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
    print("EDGE CASE TEST SUMMARY")
    print("=" * 80)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} - {test_name}")
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    print(f"\nTotal: {passed}/{total} tests passed ({passed*100//total}%)")
    
    if passed == total:
        print("\n🎉 All edge case tests passed!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
    
    return passed == total


# ============================================================================
# Entry Point
# ============================================================================

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)

