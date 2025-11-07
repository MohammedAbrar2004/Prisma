#!/usr/bin/env python3
"""
PRISMA Backend Setup Test Script

This script tests that your PRISMA installation is working correctly.

Usage:
    python test_setup.py
"""

import sys
import os

print("=" * 70)
print("🔍 PRISMA Backend Setup Test")
print("=" * 70)
print()

# Test 1: Python version
print("1️⃣  Checking Python version...")
if sys.version_info < (3, 10):
    print("   ❌ Python 3.10+ required. You have:", sys.version)
    print("   Please upgrade Python and try again.")
    sys.exit(1)
else:
    print(f"   ✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
print()

# Test 2: Required packages
print("2️⃣  Checking required packages...")
required_packages = {
    'fastapi': 'FastAPI',
    'uvicorn': 'Uvicorn',
    'requests': 'Requests',
    'pydantic': 'Pydantic',
    'dotenv': 'python-dotenv'
}

missing_packages = []
for package, display_name in required_packages.items():
    try:
        __import__(package)
        print(f"   ✅ {display_name}")
    except ImportError:
        print(f"   ❌ {display_name} - NOT INSTALLED")
        missing_packages.append(display_name)

if missing_packages:
    print()
    print(f"   ⚠️  Missing packages: {', '.join(missing_packages)}")
    print("   Run: pip install -r requirements.txt")
    sys.exit(1)
print()

# Test 3: File structure
print("3️⃣  Checking file structure...")
required_files = [
    'main.py',
    'requirements.txt',
    'external_signals/__init__.py',
    'external_signals/engine.py',
    'routes/__init__.py',
    'routes/signals.py',
]

missing_files = []
for file_path in required_files:
    if os.path.exists(file_path):
        print(f"   ✅ {file_path}")
    else:
        print(f"   ❌ {file_path} - MISSING")
        missing_files.append(file_path)

if missing_files:
    print()
    print(f"   ⚠️  Missing files. Please ensure all files are in place.")
    sys.exit(1)
print()

# Test 4: Environment configuration
print("4️⃣  Checking environment configuration...")
if os.path.exists('.env'):
    print("   ✅ .env file found")
    from dotenv import load_dotenv
    load_dotenv()
    
    api_keys = {
        'METALPRICE_API_KEY': 'MetalpriceAPI',
        'COMMODITY_API_KEY': 'CommodityAPI',
        'WEATHER_API_KEY': 'WeatherAPI'
    }
    
    configured_count = 0
    for key, name in api_keys.items():
        value = os.getenv(key, '')
        if value and value != f'your_{key.lower()}_here' and 'your_' not in value:
            print(f"   ✅ {name} configured")
            configured_count += 1
        else:
            print(f"   ⚠️  {name} not configured (will use mock data)")
    
    if configured_count == 0:
        print()
        print("   ℹ️  No API keys configured. PRISMA will use mock data.")
        print("   This is fine for testing! See SETUP.md for API key setup.")
else:
    print("   ⚠️  .env file not found")
    print("   Run: cp env.example .env")
    print("   PRISMA will work with mock data, but API features won't be available.")
print()

# Test 5: Import external_signals engine
print("5️⃣  Testing external_signals engine...")
try:
    from external_signals import build_signals, test_api_connections, get_mock_signals
    print("   ✅ Engine imported successfully")
    
    # Test mock signals
    print("   Testing mock signal generation...")
    mock_result = get_mock_signals("test-company")
    if 'signals' in mock_result and len(mock_result['signals']) > 0:
        print(f"   ✅ Generated {len(mock_result['signals'])} mock signals")
    else:
        print("   ❌ Failed to generate mock signals")
        sys.exit(1)
    
    # Test API connections
    print("   Testing API connections...")
    api_status = test_api_connections()
    connected_count = sum(1 for v in api_status.values() if v == "connected")
    total_configured = sum(1 for v in api_status.values() if v != "not_configured")
    
    if total_configured > 0:
        print(f"   ℹ️  {connected_count}/{total_configured} APIs responding")
    else:
        print("   ℹ️  No APIs configured (using mock data)")
    
except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
print()

# Test 6: Test FastAPI app
print("6️⃣  Testing FastAPI app initialization...")
try:
    from main import app
    print("   ✅ FastAPI app loaded successfully")
    print(f"   ℹ️  Title: {app.title}")
    print(f"   ℹ️  Version: {app.version}")
except Exception as e:
    print(f"   ❌ Error loading FastAPI app: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
print()

# Test 7: Test signals router
print("7️⃣  Testing signals router...")
try:
    from routes.signals import router
    route_count = len(router.routes)
    print(f"   ✅ Router loaded with {route_count} routes")
    for route in router.routes:
        if hasattr(route, 'path') and hasattr(route, 'methods'):
            methods = ','.join(route.methods)
            print(f"      • {methods} {route.path}")
except Exception as e:
    print(f"   ❌ Error loading router: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
print()

# Final summary
print("=" * 70)
print("✅ All tests passed!")
print("=" * 70)
print()
print("🚀 Next steps:")
print()
print("1. Start the server:")
print("   uvicorn main:app --reload --port 8000")
print()
print("2. Open in browser:")
print("   http://localhost:8000/docs")
print()
print("3. Test the API:")
print("   curl http://localhost:8000/signals/test-company")
print()
print("4. Check API health:")
print("   curl http://localhost:8000/signals/health/check")
print()
print("For detailed setup instructions, see SETUP.md")
print("For API usage examples, see API_GUIDE.md")
print()
print("Happy coding! 🎉")
print("=" * 70)

