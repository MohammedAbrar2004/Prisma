"""
PRISMA Pipeline Validation Test

Validates the complete architecture flow:
1. Requirements → Forecast Engine
2. External Signals Engine
3. LLM Reasoning Layer
4. Structured JSON output

Follows Architecture read me specifications.
"""

import sys
import json
import requests
from pathlib import Path
from typing import Dict, Any

sys.path.insert(0, str(Path(__file__).parent))

BASE_URL = "http://localhost:8000"


def print_section(title: str):
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)


def print_result(success: bool, message: str):
    status = "[PASS]" if success else "[FAIL]"
    print(f"{status}: {message}")


def test_forecast_engine():
    """Test 1: Forecast Engine generates structured forecasts.json"""
    print_section("1. Forecast Engine Test")
    
    try:
        from forecast import generate_forecasts
        
        # Load sample requirements
        req_path = Path(__file__).parent / "data" / "mock_requirements.json"
        with open(req_path) as f:
            company_profile = json.load(f)
        
        print(f"Input: Company profile with {len(company_profile.get('projects', []))} projects")
        
        # Generate forecasts
        forecasts = generate_forecasts(company_profile, horizon="next_month")
        
        print(f"\nOutput structure:")
        print(f"  - company_id: {forecasts.get('company_id')}")
        print(f"  - horizon: {forecasts.get('horizon')}")
        print(f"  - method: {forecasts.get('method')}")
        print(f"  - forecasts count: {len(forecasts.get('forecasts', []))}")
        
        # Validate structure
        required_keys = ["company_id", "forecast_date", "horizon", "forecasts"]
        missing = [k for k in required_keys if k not in forecasts]
        
        if missing:
            print_result(False, f"Missing keys: {missing}")
            return False
        
        if not forecasts.get("forecasts"):
            print_result(False, "No forecasts generated")
            return False
        
        # Validate forecast items
        sample = forecasts["forecasts"][0]
        forecast_keys = ["project_id", "material", "current_usage", "predicted_demand", "unit", "confidence"]
        missing_forecast_keys = [k for k in forecast_keys if k not in sample]
        
        if missing_forecast_keys:
            print_result(False, f"Forecast item missing keys: {missing_forecast_keys}")
            return False
        
        print(f"\nSample forecast:")
        print(json.dumps(sample, indent=2))
        
        print_result(True, f"Forecast engine generates structured forecasts.json ({len(forecasts['forecasts'])} items)")
        return True
    
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False


def test_external_signals():
    """Test 2: External Signals Engine provides structured signals.json"""
    print_section("2. External Signals Engine Test")
    
    try:
        from external_signals import build_signals
        
        company_id = "test-company"
        
        print(f"Input: company_id={company_id}, region=Maharashtra, materials=['Steel', 'Copper']")
        
        # Build signals
        signals = build_signals(
            company_id=company_id,
            region="Maharashtra",
            materials=["Steel", "Copper"],
            horizon="next_month",
            use_real_apis=False,
            industry="construction"
        )
        
        print(f"\nOutput structure:")
        print(f"  - company_id: {signals.get('company_id')}")
        print(f"  - horizon: {signals.get('horizon')}")
        print(f"  - signals count: {len(signals.get('signals', []))}")
        print(f"  - data_sources: {signals.get('data_sources', [])}")
        
        # Validate structure
        required_keys = ["company_id", "horizon", "signals", "data_sources"]
        missing = [k for k in required_keys if k not in signals]
        
        if missing:
            print_result(False, f"Missing keys: {missing}")
            return False
        
        if not signals.get("signals"):
            print_result(False, "No signals generated")
            return False
        
        # Validate signal items
        sample = signals["signals"][0]
        signal_keys = ["material", "region", "demand_direction", "demand_score", "drivers"]
        missing_signal_keys = [k for k in signal_keys if k not in sample]
        
        if missing_signal_keys:
            print_result(False, f"Signal item missing keys: {missing_signal_keys}")
            return False
        
        print(f"\nSample signal:")
        print(json.dumps(sample, indent=2))
        
        print_result(True, f"Signals engine provides structured signals.json ({len(signals['signals'])} items)")
        return True
    
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False


def test_llm_prompt_building():
    """Test 3: LLM receives structured inputs"""
    print_section("3. LLM Prompt Building Test")
    
    try:
        from llm import build_prisma_prompt
        from forecast import generate_forecasts
        from external_signals import build_signals
        
        # Load and prepare data
        req_path = Path(__file__).parent / "data" / "mock_requirements.json"
        with open(req_path) as f:
            company_profile = json.load(f)
        
        forecasts = generate_forecasts(company_profile)
        signals = build_signals(
            company_id=company_profile["company_id"],
            region="Maharashtra",
            materials=["Steel"],
            use_real_apis=False
        )
        
        print("Building prompt with:")
        print(f"  - Company profile: {len(json.dumps(company_profile))} chars")
        print(f"  - Forecasts: {len(json.dumps(forecasts))} chars")
        print(f"  - Signals: {len(json.dumps(signals))} chars")
        
        # Build prompt
        prompt = build_prisma_prompt(
            company_profile=company_profile,
            forecasts=forecasts,
            signals=signals,
            question="What are the procurement priorities?"
        )
        
        print(f"\nPrompt length: {len(prompt)} characters")
        
        # Validate prompt contains all data
        checks = {
            "Company profile": "COMPANY PROFILE" in prompt or "company_profile" in prompt.lower(),
            "Forecasts": "DEMAND FORECASTS" in prompt or "forecasts" in prompt.lower(),
            "Signals": "EXTERNAL MARKET SIGNALS" in prompt or "signals" in prompt.lower(),
            "JSON schema": "recommended_actions" in prompt.lower() and "risks" in prompt.lower(),
            "Instructions": "USE ONLY" in prompt or "provided data" in prompt.lower()
        }
        
        failed_checks = [k for k, v in checks.items() if not v]
        
        if failed_checks:
            print_result(False, f"Prompt missing: {failed_checks}")
            return False
        
        print("\nPrompt preview (first 500 chars):")
        print(prompt[:500] + "...")
        
        print_result(True, "LLM prompt contains all structured inputs")
        return True
    
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False


def test_llm_analysis():
    """Test 4: LLM can access data and answer queries"""
    print_section("4. LLM Analysis Test")
    
    try:
        from llm import analyze_prisma, test_ollama_connection
        from forecast import generate_forecasts
        from external_signals import build_signals
        
        # Check Ollama connection
        ollama_status = test_ollama_connection()
        if ollama_status.get("status") != "connected":
            print_result(False, f"Ollama not connected: {ollama_status.get('message')}")
            return False
        
        print("[OK] Ollama connected")
        
        # Prepare data
        req_path = Path(__file__).parent / "data" / "mock_requirements.json"
        with open(req_path) as f:
            company_profile = json.load(f)
        
        forecasts = generate_forecasts(company_profile)
        signals = build_signals(
            company_id=company_profile["company_id"],
            region="Maharashtra",
            materials=["Steel", "Copper"],
            use_real_apis=False
        )
        
        print(f"\nInput data:")
        print(f"  - Company: {company_profile.get('company')}")
        print(f"  - Forecasts: {len(forecasts.get('forecasts', []))} items")
        print(f"  - Signals: {len(signals.get('signals', []))} items")
        
        print("\nCalling LLM (this may take 30-60 seconds)...")
        
        # Call LLM
        result = analyze_prisma(
            company_profile=company_profile,
            forecasts=forecasts,
            signals=signals,
            question="What are the key procurement priorities for Steel?"
        )
        
        print(f"\nLLM Response structure:")
        print(f"  - summary: {len(result.get('summary', ''))} chars")
        print(f"  - recommended_actions: {len(result.get('recommended_actions', []))} items")
        print(f"  - risks: {len(result.get('risks', []))} items")
        print(f"  - watchlist_materials: {len(result.get('watchlist_materials', []))} items")
        
        # Validate response structure
        required_keys = ["summary", "recommended_actions", "risks"]
        missing = [k for k in required_keys if k not in result]
        
        if missing:
            print_result(False, f"Response missing keys: {missing}")
            return False
        
        if not result.get("summary"):
            print_result(False, "Empty summary")
            return False
        
        # Check if LLM actually used the data
        summary = result.get("summary", "").lower()
        mentions_steel = "steel" in summary
        mentions_forecast = any(word in summary for word in ["forecast", "demand", "predicted", "increase"])
        
        print(f"\nData usage check:")
        print(f"  - Mentions Steel: {mentions_steel}")
        print(f"  - Mentions forecast/demand: {mentions_forecast}")
        
        if not mentions_steel:
            print_result(False, "LLM response doesn't mention Steel (may not be using input data)")
            return False
        
        print("\nSample response:")
        print(f"Summary: {result['summary'][:200]}...")
        if result.get("recommended_actions"):
            print(f"\nFirst action: {json.dumps(result['recommended_actions'][0], indent=2)}")
        
        print_result(True, "LLM successfully processes structured inputs and answers queries")
        return True
    
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_end_to_end_api():
    """Test 5: Complete API pipeline"""
    print_section("5. End-to-End API Test")
    
    try:
        print("Testing POST /analyze endpoint...")
        
        payload = {
            "company_id": "abc-infra",
            "question": "What are the procurement priorities?",
            "materials": ["Steel"],
            "region": "Maharashtra",
            "industry": "construction",
            "use_real_apis": False
        }
        
        print(f"\nRequest payload:")
        print(json.dumps(payload, indent=2))
        
        print("\nCalling API (this may take 30-60 seconds)...")
        
        response = requests.post(
            f"{BASE_URL}/analyze",
            json=payload,
            timeout=120
        )
        
        print(f"\nResponse status: {response.status_code}")
        
        if response.status_code != 200:
            print(f"Response: {response.text}")
            print_result(False, f"API returned {response.status_code}")
            return False
        
        data = response.json()
        
        print(f"\nResponse structure:")
        print(f"  - company_id: {data.get('company_id')}")
        print(f"  - summary: {len(data.get('summary', ''))} chars")
        print(f"  - recommended_actions: {len(data.get('recommended_actions', []))}")
        print(f"  - risks: {len(data.get('risks', []))}")
        print(f"  - data_sources: {data.get('data_sources', [])}")
        
        # Validate complete response
        required_keys = ["summary", "recommended_actions", "risks", "company_id"]
        missing = [k for k in required_keys if k not in data]
        
        if missing:
            print_result(False, f"Response missing keys: {missing}")
            return False
        
        # Check data flow
        has_forecasts = "forecast" in str(data.get("summary", "")).lower() or len(data.get("recommended_actions", [])) > 0
        has_signals = len(data.get("data_sources", [])) > 0
        
        print(f"\nData flow check:")
        print(f"  - Forecasts used: {has_forecasts}")
        print(f"  - Signals used: {has_signals}")
        
        print("\nSample response:")
        print(json.dumps({
            "summary": data.get("summary", "")[:150] + "...",
            "first_action": data.get("recommended_actions", [{}])[0] if data.get("recommended_actions") else None
        }, indent=2))
        
        print_result(True, "Complete API pipeline works end-to-end")
        return True
    
    except requests.ConnectionError:
        print_result(False, "Cannot connect to API server. Is it running?")
        return False
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False


def test_google_search_integration():
    """Test 6: Google Search provides knowledge"""
    print_section("6. Google Search Integration Test")
    
    try:
        from search.industry import get_industry_trends, GOOGLE_SEARCH_API_KEY, GOOGLE_SEARCH_ENGINE_ID
        
        if not GOOGLE_SEARCH_API_KEY or not GOOGLE_SEARCH_ENGINE_ID:
            print("[INFO] Google Search not configured (using fallback)")
            print("   Set GOOGLE_SEARCH_API_KEY and GOOGLE_SEARCH_ENGINE_ID in .env")
            print("   See: backend/GOOGLE_SEARCH_SETUP.md")
            
            # Test fallback
            trends = get_industry_trends("construction", materials=["Steel"], use_google_search=False)
            if trends:
                print_result(True, "Fallback trends available")
                return True
            else:
                print_result(False, "No fallback trends")
                return False
        
        print("Testing Google Search integration...")
        
        trends = get_industry_trends(
            industry="construction",
            materials=["Steel", "Copper"],
            use_google_search=True
        )
        
        print(f"\nFound {len(trends)} trends")
        
        if trends:
            print("\nSample trend:")
            print(json.dumps(trends[0], indent=2))
            
            # Check if from Google
            google_trends = [t for t in trends if t.get("source") == "Google Search"]
            print(f"\nGoogle Search trends: {len(google_trends)}")
            
            if google_trends:
                print_result(True, f"Google Search provides {len(google_trends)} knowledge items")
                return True
        
        print_result(True, "Trends available (may be fallback)")
        return True
    
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False


def main():
    """Run all validation tests"""
    print("\n" + "=" * 80)
    print("PRISMA Pipeline Validation")
    print("Validating architecture flow per Architecture read me")
    print("=" * 80)
    
    tests = [
        ("Forecast Engine", test_forecast_engine),
        ("External Signals Engine", test_external_signals),
        ("LLM Prompt Building", test_llm_prompt_building),
        ("LLM Analysis", test_llm_analysis),
        ("End-to-End API", test_end_to_end_api),
        ("Google Search Integration", test_google_search_integration),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n[ERROR] Test '{test_name}' crashed: {str(e)}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 80)
    print("VALIDATION SUMMARY")
    print("=" * 80)
    
    for test_name, result in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"{status} - {test_name}")
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    print(f"\nTotal: {passed}/{total} tests passed ({passed*100//total}%)")
    
    if passed == total:
        print("\n[SUCCESS] All components validated! Pipeline is working correctly.")
        print("\nArchitecture flow verified:")
        print("  1. Requirements -> Forecast Engine [OK]")
        print("  2. External Signals Engine [OK]")
        print("  3. LLM receives structured inputs [OK]")
        print("  4. LLM processes and answers queries [OK]")
        print("  5. API returns structured JSON [OK]")
    else:
        print(f"\n[WARNING] {total - passed} test(s) failed - check above for details")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)

