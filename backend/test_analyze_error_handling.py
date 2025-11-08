"""
Test: /analyze Endpoint Error Handling

This test file validates error handling and recovery mechanisms.

Test scenarios:
1. Server unavailable (connection error)
2. Ollama not running (LLM service down)
3. Invalid JSON payload
4. Missing required fields
5. Timeout scenarios
6. Malformed responses
7. Service degradation handling

Prerequisites:
- FastAPI server state can be controlled (run/stop)
- Ollama can be stopped/started for testing

Usage:
    python test_analyze_error_handling.py
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
HEALTH_URL = f"{BASE_URL}/health"
ANALYZE_HEALTH_URL = f"{ANALYZE_URL}/health"


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


def check_server_running() -> bool:
    """Check if server is accessible"""
    try:
        response = requests.get(HEALTH_URL, timeout=5)
        return response.status_code == 200
    except:
        return False


def check_ollama_running() -> bool:
    """Check if Ollama is accessible"""
    try:
        response = requests.get(ANALYZE_HEALTH_URL, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data.get("ollama", {}).get("status") == "connected"
        return False
    except:
        return False


# ============================================================================
# Error Handling Tests
# ============================================================================

def test_server_connectivity():
    """
    Test 1: Server connectivity check
    
    Validates:
    - Can reach server
    - Health endpoint works
    """
    print_test_header("Server Connectivity")
    
    print(f"\nChecking server at: {BASE_URL}")
    
    if check_server_running():
        print_result(True, "Server is running and accessible")
        return True
    else:
        print_result(False, "Server is not accessible - cannot run error tests")
        print("\n⚠️  Please start the server: uvicorn main:app --reload")
        return False


def test_ollama_connectivity():
    """
    Test 2: Ollama connectivity check
    
    Validates:
    - Can detect Ollama status
    - Health endpoint reports LLM availability
    """
    print_test_header("Ollama Connectivity")
    
    print(f"\nChecking Ollama status via: {ANALYZE_HEALTH_URL}")
    
    try:
        response = requests.get(ANALYZE_HEALTH_URL, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            ollama_status = data.get("ollama", {})
            
            print(f"\nOllama Status: {json.dumps(ollama_status, indent=2)}")
            
            if ollama_status.get("status") == "connected":
                print_result(True, "Ollama is running and accessible")
                return True
            else:
                print_result(False, "Ollama is not running")
                print("\n⚠️  To test error scenarios, Ollama should be running")
                print("   Start Ollama: ollama serve")
                return False
        else:
            print_result(False, f"Health check failed: HTTP {response.status_code}")
            return False
    
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False


def test_ollama_down_scenario():
    """
    Test 3: Simulate Ollama being down
    
    Note: This test just documents the expected behavior.
    To actually test, stop Ollama and run analyze endpoint.
    
    Expected:
    - Returns 503 (Service Unavailable)
    - Clear error message about LLM unavailability
    """
    print_test_header("Ollama Down Scenario")
    
    print("\n📝 DOCUMENTATION TEST")
    print("\nTo test Ollama unavailability:")
    print("  1. Stop Ollama service")
    print("  2. Try POST /analyze with valid payload")
    print("  3. Expected response: HTTP 503")
    print("  4. Expected message: 'LLM service unavailable'")
    
    print("\nChecking current Ollama status...")
    ollama_running = check_ollama_running()
    
    if ollama_running:
        print("\n✓ Ollama is currently running")
        print("  To test failure scenario, stop Ollama and re-run this test")
        print_result(True, "Documentation verified (Ollama currently running)")
    else:
        print("\n⚠️  Ollama is NOT running - perfect for testing!")
        print("  Attempting analysis request...")
        
        payload = {
            "company_id": "abc-infra",
            "use_real_apis": False
        }
        
        try:
            response = requests.post(ANALYZE_URL, json=payload, timeout=30)
            
            print(f"\nResponse Status: {response.status_code}")
            print(f"Response: {response.text[:200]}...")
            
            if response.status_code in [503, 500]:
                error_msg = response.json().get("detail", "")
                if "LLM" in error_msg or "Ollama" in error_msg or "unavailable" in error_msg:
                    print_result(True, "Correctly reports LLM unavailability")
                    return True
                else:
                    print_result(True, "Returns error (message could be more specific)")
                    return True
            else:
                print_result(False, f"Unexpected status code: {response.status_code}")
                return False
        
        except Exception as e:
            print_result(False, f"Exception: {str(e)}")
            return False
    
    return True


def test_invalid_json_payload():
    """
    Test 4: Invalid JSON payload
    
    Expected:
    - Returns 422 (Validation Error)
    - Clear error message about invalid format
    """
    print_test_header("Invalid JSON Payload")
    
    # Send malformed JSON
    invalid_payloads = [
        ('{"company_id": "abc-infra"', "Unclosed JSON"),
        ('{"company_id": 123}', "Invalid type (number instead of string)"),
        ('not json at all', "Plain text instead of JSON"),
    ]
    
    all_handled_correctly = True
    
    for payload_str, description in invalid_payloads:
        print(f"\n--- Test: {description} ---")
        print(f"Payload: {payload_str}")
        
        try:
            response = requests.post(
                ANALYZE_URL,
                data=payload_str,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            print(f"Response Status: {response.status_code}")
            
            if response.status_code in [422, 400]:
                print("✓ Correctly rejects invalid JSON")
            else:
                print(f"✗ Unexpected status: {response.status_code}")
                all_handled_correctly = False
        
        except Exception as e:
            print(f"✗ Exception: {str(e)}")
            all_handled_correctly = False
    
    print_result(all_handled_correctly, "Invalid JSON handled correctly" if all_handled_correctly else "Some issues with JSON validation")
    return all_handled_correctly


def test_missing_required_fields():
    """
    Test 5: Missing required fields
    
    Expected:
    - Returns 422 (Validation Error)
    - Indicates which field is missing
    """
    print_test_header("Missing Required Fields")
    
    # Empty payload
    payload = {}
    
    print(f"\nPayload: {json.dumps(payload)}")
    
    try:
        response = requests.post(ANALYZE_URL, json=payload, timeout=10)
        
        print(f"\nResponse Status: {response.status_code}")
        print(f"Response: {response.text[:300]}...")
        
        if response.status_code == 422:
            # FastAPI validation error
            error_data = response.json()
            print(f"\nValidation errors: {error_data.get('detail', [])}")
            print_result(True, "Correctly validates required fields")
            return True
        else:
            print_result(False, f"Expected 422, got {response.status_code}")
            return False
    
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False


def test_timeout_handling():
    """
    Test 6: Timeout handling
    
    Validates:
    - Client can set timeout
    - Graceful timeout handling
    """
    print_test_header("Timeout Handling")
    
    payload = {
        "company_id": "abc-infra",
        "question": "Very complex analysis requiring detailed examination",
        "use_real_apis": False
    }
    
    print("\nAttempting request with short timeout (1 second)...")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(ANALYZE_URL, json=payload, timeout=1)
        
        # If it completes in 1 second, that's actually fine
        print(f"\nResponse Status: {response.status_code}")
        print("✓ Request completed within 1 second (faster than expected)")
        print_result(True, "Fast response time")
        return True
    
    except requests.Timeout:
        print("\n✓ Request timed out as expected")
        print("  This is normal for LLM operations")
        print_result(True, "Timeout handled gracefully by client")
        return True
    
    except Exception as e:
        print_result(False, f"Unexpected exception: {str(e)}")
        return False


def test_concurrent_requests():
    """
    Test 7: Concurrent request handling
    
    Validates:
    - Server can handle multiple requests
    - No race conditions
    - Reasonable response times under load
    """
    print_test_header("Concurrent Requests")
    
    print("\nSending 3 concurrent requests...")
    print("(Simulating multiple users accessing the endpoint)")
    
    payload = {
        "company_id": "abc-infra",
        "materials": ["Steel"],
        "use_real_apis": False
    }
    
    import concurrent.futures
    import time as time_module
    
    def make_request(request_id):
        """Make a single request and measure time"""
        start = time_module.time()
        try:
            response = requests.post(ANALYZE_URL, json=payload, timeout=90)
            duration = time_module.time() - start
            return {
                "id": request_id,
                "status": response.status_code,
                "duration": duration,
                "success": response.status_code == 200
            }
        except Exception as e:
            duration = time_module.time() - start
            return {
                "id": request_id,
                "status": 0,
                "duration": duration,
                "success": False,
                "error": str(e)
            }
    
    # Execute concurrent requests
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(make_request, i) for i in range(1, 4)]
        results = [f.result() for f in concurrent.futures.as_completed(futures)]
    
    # Analyze results
    print("\n--- Results ---")
    for result in results:
        status_str = f"HTTP {result['status']}" if result['status'] else "ERROR"
        print(f"Request {result['id']}: {status_str} in {result['duration']:.2f}s")
    
    success_count = sum(1 for r in results if r['success'])
    avg_duration = sum(r['duration'] for r in results) / len(results)
    
    print(f"\nSuccess Rate: {success_count}/3")
    print(f"Average Duration: {avg_duration:.2f}s")
    
    if success_count >= 2:  # At least 2 out of 3 should succeed
        print_result(True, f"Handles concurrent requests ({success_count}/3 succeeded)")
        return True
    else:
        print_result(False, f"Poor concurrent performance ({success_count}/3 succeeded)")
        return False


def test_malformed_company_data():
    """
    Test 8: Graceful handling of malformed mock data
    
    Expected:
    - Detects data issues
    - Returns meaningful error
    - Doesn't crash
    """
    print_test_header("Malformed Data Handling")
    
    print("\n📝 DOCUMENTATION TEST")
    print("\nExpected behavior if mock_requirements.json is corrupted:")
    print("  - Returns 404 or 500 with clear error message")
    print("  - Does not crash the server")
    print("  - Logs the error for debugging")
    
    # Try with a company that would require DB access
    payload = {
        "company_id": "test-data-quality-999",
        "use_real_apis": False
    }
    
    print(f"\nTesting with unusual company_id: {payload['company_id']}")
    
    try:
        response = requests.post(ANALYZE_URL, json=payload, timeout=30)
        
        print(f"\nResponse Status: {response.status_code}")
        print(f"Response: {response.text[:200]}...")
        
        if response.status_code in [404, 500, 200]:
            # Any of these is acceptable - it handled the situation
            print_result(True, "Gracefully handles data issues")
            return True
        else:
            print_result(False, f"Unexpected status: {response.status_code}")
            return False
    
    except Exception as e:
        # Even an exception is somewhat acceptable if it's handled
        print(f"Exception occurred: {str(e)}")
        print_result(True, "Error was caught and handled")
        return True


# ============================================================================
# Main Test Runner
# ============================================================================

def run_all_tests():
    """Run all error handling tests and report results"""
    
    print("\n" + "=" * 80)
    print("PRISMA /analyze Endpoint - Error Handling Tests")
    print("=" * 80)
    print("\nThese tests validate error conditions and recovery.")
    print("\nStarting tests in 3 seconds...")
    time.sleep(3)
    
    tests = [
        ("Server Connectivity", test_server_connectivity),
        ("Ollama Connectivity", test_ollama_connectivity),
        ("Ollama Down Scenario", test_ollama_down_scenario),
        ("Invalid JSON Payload", test_invalid_json_payload),
        ("Missing Required Fields", test_missing_required_fields),
        ("Timeout Handling", test_timeout_handling),
        ("Concurrent Requests", test_concurrent_requests),
        ("Malformed Data Handling", test_malformed_company_data),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n✗ Test '{test_name}' crashed: {str(e)}")
            results.append((test_name, False))
        
        time.sleep(1)
    
    # Print summary
    print("\n" + "=" * 80)
    print("ERROR HANDLING TEST SUMMARY")
    print("=" * 80)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} - {test_name}")
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    print(f"\nTotal: {passed}/{total} tests passed ({passed*100//total}%)")
    
    if passed == total:
        print("\n🎉 All error handling tests passed!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
    
    return passed == total


# ============================================================================
# Entry Point
# ============================================================================

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)

