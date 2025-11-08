"""
PRISMA Comprehensive Integration Test

This script validates that:
1. Mock company data and forecasts are well-formed
2. External signals engines provide relevant context for the materials
3. Industry search engine returns appropriate trends
4. All signals integrate properly to give LLM good context
5. The complete pipeline works end-to-end

Run this to verify the system is providing quality data for LLM reasoning.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Import PRISMA modules
from external_signals import build_signals
from search.industry import get_industry_trends, get_standardized_trends
from forecast import generate_forecasts


# ============================================================================
# Color output for terminal
# ============================================================================

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    END = '\033[0m'
    BOLD = '\033[1m'


def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'=' * 80}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text.center(80)}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'=' * 80}{Colors.END}\n")


def print_success(text):
    print(f"{Colors.GREEN}[PASS] {text}{Colors.END}")


def print_warning(text):
    print(f"{Colors.YELLOW}[WARN] {text}{Colors.END}")


def print_error(text):
    print(f"{Colors.RED}[FAIL] {text}{Colors.END}")


def print_info(text):
    print(f"{Colors.BLUE}[INFO] {text}{Colors.END}")


# ============================================================================
# Test Functions
# ============================================================================

def load_mock_data():
    """Load mock requirements and forecasts"""
    print_header("STEP 1: Loading Mock Data")
    
    data_dir = Path(__file__).parent / "data"
    
    # Load requirements
    req_path = data_dir / "mock_requirements.json"
    with open(req_path) as f:
        requirements = json.load(f)
    
    print_success(f"Loaded company data: {requirements['company_name']}")
    print_info(f"  Company ID: {requirements['company_id']}")
    print_info(f"  Industry: {requirements['industry']}")
    print_info(f"  Active Projects: {len(requirements['projects'])}")
    
    # Extract unique materials
    materials = set()
    for project in requirements['projects']:
        for material in project['materials']:
            materials.add(material['name'])
    
    print_info(f"  Unique Materials: {', '.join(sorted(materials))}")
    
    # Load forecasts
    forecast_path = data_dir / "mock_forecasts.json"
    with open(forecast_path) as f:
        forecasts = json.load(f)
    
    print_success(f"Loaded forecasts: {len(forecasts['forecasts'])} predictions")
    print_info(f"  Forecast Date: {forecasts['forecast_date']}")
    print_info(f"  Method: {forecasts['method']}")
    print_info(f"  Confidence: {forecasts['confidence_level']:.1%}")
    
    return requirements, forecasts, list(materials)


def validate_forecast_alignment(requirements, forecasts):
    """Verify forecasts align with requirements"""
    print_header("STEP 2: Validating Forecast Alignment")
    
    # Get materials from requirements
    req_materials = {}
    for project in requirements['projects']:
        proj_id = project['id']
        for material in project['materials']:
            key = (proj_id, material['name'])
            req_materials[key] = material['current_month_usage']
    
    # Check if forecasts cover all materials
    forecast_materials = {}
    for forecast in forecasts['forecasts']:
        key = (forecast['project_id'], forecast['material'])
        forecast_materials[key] = forecast['current_usage']
    
    # Validation
    matches = 0
    mismatches = []
    
    for key, req_usage in req_materials.items():
        if key in forecast_materials:
            forecast_usage = forecast_materials[key]
            if req_usage == forecast_usage:
                matches += 1
            else:
                mismatches.append(f"{key}: Req={req_usage}, Forecast={forecast_usage}")
    
    print_success(f"Forecast-Requirement alignment: {matches}/{len(req_materials)} matches")
    
    if mismatches:
        print_warning(f"Found {len(mismatches)} mismatches:")
        for mm in mismatches[:5]:  # Show first 5
            print(f"    {mm}")
    
    return matches == len(req_materials)


def test_external_signals(company_id, materials):
    """Test external signals engine with mock data materials"""
    print_header("STEP 3: Testing External Signals Engine")
    
    print_info("Building signals for all materials...")
    
    signals = build_signals(
        company_id=company_id,
        materials=materials,
        region="India",
        horizon="next_month",
        use_real_apis=False,  # Use mock data for testing
        industry="infrastructure"
    )
    
    print_success(f"Generated {len(signals['signals'])} signals")
    print_info(f"  Data Sources: {', '.join(signals['data_sources'])}")
    
    # Check coverage
    signal_materials = set(s['material'] for s in signals['signals'])
    coverage = len(signal_materials) / len(materials) if materials else 0
    
    print_info(f"  Material Coverage: {len(signal_materials)}/{len(materials)} ({coverage:.0%})")
    
    # Analyze signal quality
    print("\n" + Colors.BOLD + "Signal Quality Analysis:" + Colors.END)
    
    material_signals = {}
    for signal in signals['signals']:
        mat = signal['material']
        if mat not in material_signals:
            material_signals[mat] = []
        material_signals[mat].append(signal)
    
    for material in sorted(material_signals.keys()):
        sigs = material_signals[material]
        avg_confidence = sum(s['confidence'] for s in sigs) / len(sigs)
        demand_directions = [s['demand_direction'] for s in sigs]
        
        print(f"\n  {Colors.BOLD}{material}{Colors.END}:")
        print(f"    Signals: {len(sigs)}")
        print(f"    Avg Confidence: {avg_confidence:.2f}")
        print(f"    Demand Directions: {', '.join(set(demand_directions))}")
        
        # Show sample drivers
        if sigs[0].get('drivers'):
            print(f"    Sample Drivers:")
            for driver in sigs[0]['drivers'][:2]:
                print(f"      - {driver}")
    
    return signals, coverage >= 0.8  # Pass if 80%+ coverage


def test_industry_intelligence(industry, materials):
    """Test industry search engine relevance"""
    print_header("STEP 4: Testing Industry Intelligence / Search Engine")
    
    print_info(f"Searching for industry trends: {industry}")
    print_info(f"  Materials filter: {', '.join(materials[:3])}...")
    
    # Get raw trends
    trends = get_industry_trends(
        industry=industry,
        materials=materials,
        use_google_search=False  # Use hardcoded for testing
    )
    
    print_success(f"Retrieved {len(trends)} industry trends")
    
    # Get standardized format
    standardized = get_standardized_trends(
        industry=industry,
        materials=materials[:3],  # Test with first 3 materials
        region="Global"
    )
    
    print_success(f"Converted to {len(standardized)} standardized trends")
    
    # Analyze relevance
    print("\n" + Colors.BOLD + "Trend Relevance Analysis:" + Colors.END)
    
    relevant_count = 0
    for i, trend in enumerate(standardized[:3], 1):  # Show first 3
        print(f"\n  {Colors.BOLD}Trend {i}: {trend['trend_id']}{Colors.END}")
        print(f"    Type: {trend['type']}")
        print(f"    Industry: {trend['industry']}")
        print(f"    Summary: {trend['summary'][:100]}...")
        print(f"    Confidence: {trend['confidence']:.2f}")
        
        # Check if materials are mentioned
        materials_mentioned = [
            m['material'] for m in trend['impact_on_materials']
            if m['material'] in materials
        ]
        
        if materials_mentioned:
            relevant_count += 1
            print_success(f"    Relevant Materials: {', '.join(materials_mentioned)}")
            
            # Show effects
            for impact in trend['impact_on_materials']:
                if impact['material'] in materials:
                    print(f"      {impact['material']}: {impact['effect']}")
        else:
            print_warning("    No direct material matches found")
    
    relevance_score = relevant_count / len(standardized) if standardized else 0
    print(f"\n  {Colors.BOLD}Relevance Score: {relevance_score:.0%}{Colors.END}")
    
    return standardized, relevance_score >= 0.5


def test_llm_context_quality(requirements, forecasts, signals, trends):
    """Validate that LLM receives high-quality context"""
    print_header("STEP 5: Validating LLM Context Quality")
    
    # Check data completeness
    checks = {
        "Company Profile": requirements is not None,
        "Forecasts": forecasts is not None and len(forecasts.get('forecasts', [])) > 0,
        "External Signals": signals is not None and len(signals.get('signals', [])) > 0,
        "Industry Trends": trends is not None and len(trends) > 0,
    }
    
    print_info("Context Completeness Checks:")
    for check, passed in checks.items():
        if passed:
            print_success(f"  {check}: Available")
        else:
            print_error(f"  {check}: Missing")
    
    all_passed = all(checks.values())
    
    # Check data richness
    print("\n" + Colors.BOLD + "Data Richness Analysis:" + Colors.END)
    
    # Materials diversity
    materials_in_reqs = set()
    for project in requirements['projects']:
        for material in project['materials']:
            materials_in_reqs.add(material['name'])
    
    materials_in_forecasts = set(f['material'] for f in forecasts['forecasts'])
    materials_in_signals = set(s['material'] for s in signals['signals'])
    
    print_info(f"  Materials in Requirements: {len(materials_in_reqs)}")
    print_info(f"  Materials in Forecasts: {len(materials_in_forecasts)}")
    print_info(f"  Materials in Signals: {len(materials_in_signals)}")
    
    # Context diversity
    signal_sources = set(signals.get('data_sources', []))
    print_info(f"  Signal Data Sources: {len(signal_sources)} ({', '.join(signal_sources)})")
    
    # Check for critical materials
    critical_materials = [
        m['name'] for p in requirements['projects']
        for m in p['materials'] if m.get('critical', False)
    ]
    
    if critical_materials:
        print_info(f"  Critical Materials Identified: {len(critical_materials)}")
        print(f"    {', '.join(set(critical_materials))}")
    
    # Driver quality (check if signals have meaningful drivers)
    signals_with_drivers = sum(1 for s in signals['signals'] if s.get('drivers') and len(s['drivers']) > 0)
    driver_coverage = signals_with_drivers / len(signals['signals']) if signals['signals'] else 0
    
    print_info(f"  Signals with Drivers: {signals_with_drivers}/{len(signals['signals'])} ({driver_coverage:.0%})")
    
    return all_passed and driver_coverage >= 0.5


def test_end_to_end_pipeline():
    """Test complete pipeline from requirements to LLM-ready context"""
    print_header("STEP 6: End-to-End Pipeline Test")
    
    print_info("Simulating complete analysis flow...")
    
    try:
        # Load mock data
        data_dir = Path(__file__).parent / "data"
        req_path = data_dir / "mock_requirements.json"
        with open(req_path) as f:
            company_profile = json.load(f)
        
        company_id = company_profile['company_id']
        industry = company_profile['industry']
        
        # Extract materials
        materials = list(set(
            m['name'] for p in company_profile['projects']
            for m in p['materials']
        ))
        
        print_success("Step 1: Loaded company profile")
        
        # Generate forecasts
        forecasts = generate_forecasts(
            company_profile=company_profile,
            horizon="next_month"
        )
        print_success(f"Step 2: Generated {len(forecasts['forecasts'])} forecasts")
        
        # Build signals
        signals = build_signals(
            company_id=company_id,
            materials=materials,
            region="India",
            horizon="next_month",
            use_real_apis=False,
            industry=industry
        )
        print_success(f"Step 3: Built {len(signals['signals'])} signals")
        
        # Get industry trends
        trends = get_standardized_trends(
            industry=industry,
            materials=materials[:3]
        )
        print_success(f"Step 4: Retrieved {len(trends)} industry trends")
        
        # Verify LLM would receive complete context
        context_complete = all([
            company_profile,
            forecasts and forecasts.get('forecasts'),
            signals and signals.get('signals'),
            trends
        ])
        
        if context_complete:
            print_success("\nPipeline Complete: LLM would receive full context")
            
            # Show what LLM would see
            print("\n" + Colors.BOLD + "LLM Context Summary:" + Colors.END)
            print(f"  Company: {company_profile['company_name']}")
            print(f"  Projects: {len(company_profile['projects'])}")
            print(f"  Materials Tracked: {len(materials)}")
            print(f"  Forecast Points: {len(forecasts['forecasts'])}")
            print(f"  Signal Points: {len(signals['signals'])}")
            print(f"  Industry Trends: {len(trends)}")
            print(f"  Data Sources: {', '.join(signals['data_sources'])}")
            
            return True
        else:
            print_error("Pipeline Incomplete: Missing data")
            return False
            
    except Exception as e:
        print_error(f"Pipeline Failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


# ============================================================================
# Main Test Runner
# ============================================================================

def run_all_tests():
    """Run all integration tests"""
    print("\n")
    print(f"{Colors.BOLD}{Colors.GREEN}")
    print("="*80)
    print("=                                                                              =")
    print("=            PRISMA COMPREHENSIVE INTEGRATION TEST SUITE                       =")
    print("=                                                                              =")
    print("="*80)
    print(Colors.END)
    
    start_time = datetime.now()
    
    results = {}
    
    try:
        # Test 1: Load and validate mock data
        requirements, forecasts, materials = load_mock_data()
        results['data_loading'] = True
        
        # Test 2: Forecast alignment
        results['forecast_alignment'] = validate_forecast_alignment(requirements, forecasts)
        
        # Test 3: External signals
        signals, signals_pass = test_external_signals(
            requirements['company_id'],
            materials
        )
        results['external_signals'] = signals_pass
        
        # Test 4: Industry intelligence
        trends, trends_pass = test_industry_intelligence(
            requirements['industry'],
            materials
        )
        results['industry_intelligence'] = trends_pass
        
        # Test 5: LLM context quality
        results['llm_context'] = test_llm_context_quality(
            requirements, forecasts, signals, trends
        )
        
        # Test 6: End-to-end pipeline
        results['end_to_end'] = test_end_to_end_pipeline()
        
    except Exception as e:
        print_error(f"\nFatal Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    # Summary
    print_header("TEST SUMMARY")
    
    total_tests = len(results)
    passed_tests = sum(1 for v in results.values() if v)
    
    for test_name, passed in results.items():
        status = "PASS" if passed else "FAIL"
        color = Colors.GREEN if passed else Colors.RED
        print(f"  {color}{status}{Colors.END} - {test_name.replace('_', ' ').title()}")
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print(f"\n{Colors.BOLD}Results: {passed_tests}/{total_tests} tests passed{Colors.END}")
    print(f"Duration: {duration:.2f} seconds")
    
    if passed_tests == total_tests:
        print(f"\n{Colors.GREEN}{Colors.BOLD}[SUCCESS] ALL TESTS PASSED - System Ready!{Colors.END}")
        return True
    else:
        print(f"\n{Colors.YELLOW}[WARNING] Some tests failed - Review output above{Colors.END}")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

