# PRISMA Backend Setup Guide

Complete step-by-step guide to get PRISMA running on your machine.

## Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Git (optional, for cloning)

## Step 1: Setup Python Environment

### Windows

```powershell
# Check Python version (should be 3.10+)
python --version

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate
```

### Linux/macOS

```bash
# Check Python version (should be 3.10+)
python3 --version

# Create virtual environment (recommended)
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

## Step 2: Install Dependencies

```bash
# Make sure you're in the backend directory
cd backend

# Install all required packages
pip install -r requirements.txt
```

## Step 3: Get API Keys (Optional but Recommended)

PRISMA works with mock data out of the box, but for real-time signals, get these free API keys:

### 1. MetalpriceAPI

1. Visit: https://metalpriceapi.com/
2. Sign up for free account
3. Get your API key (100 requests/month free)
4. Copy the key

### 2. CommodityAPI

1. Visit: https://commodityapi.com/
2. Sign up for free account
3. Get your API key
4. Copy the key

### 3. WeatherAPI.com

1. Visit: https://www.weatherapi.com/
2. Sign up for free account
3. Get your API key (1M requests/month free)
4. Copy the key

### 4. World Bank API

No key needed! It's a public API.

## Step 4: Configure Environment

```bash
# Copy the example environment file
cp env.example .env

# Edit .env file and add your API keys
# On Windows: notepad .env
# On Linux/Mac: nano .env
```

Your `.env` should look like:

```env
METALPRICE_API_KEY=your_actual_key_here
COMMODITY_API_KEY=your_actual_key_here
WEATHER_API_KEY=your_actual_key_here

ENVIRONMENT=development
HOST=0.0.0.0
PORT=8000
USE_REAL_APIS=true
```

**Note:** If you skip API keys, PRISMA will use mock data automatically!

## Step 5: Test the Setup

Run the test script to verify everything works:

```bash
# Test the external signals engine
python external_signals/engine.py
```

You should see:
```
Testing PRISMA External Signals Engine...

API Connection Status:
{
  "metalprice": "connected",  # or "not_configured" if no key
  "commodity": "not_configured",
  "weather": "connected",
  "worldbank": "connected"
}

Generating signals for test company...
Generated 3 signals
Data sources used: mock, weather_api
```

## Step 6: Start the Server

```bash
# Option 1: Using uvicorn directly (recommended for development)
uvicorn main:app --reload --port 8000

# Option 2: Using Python
python main.py
```

You should see:

```
============================================================
🚀 PRISMA Backend Starting...
============================================================
Environment: development
Docs available at: http://localhost:8000/docs
============================================================
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
```

## Step 7: Test the API

### Option 1: Open in Browser

1. Go to: http://localhost:8000/docs
2. You'll see interactive API documentation
3. Try the `/signals/{company_id}` endpoint
4. Click "Try it out"
5. Enter `test-company` as company_id
6. Click "Execute"

### Option 2: Use curl

```bash
# Test root endpoint
curl http://localhost:8000/

# Get signals for a company
curl http://localhost:8000/signals/test-company

# Get signals with region filter
curl "http://localhost:8000/signals/test-company?region=Maharashtra"

# Get signals for specific materials
curl "http://localhost:8000/signals/test-company?materials=Steel,Copper"

# Check API health
curl http://localhost:8000/signals/health/check

# Get only mock data (no API calls)
curl http://localhost:8000/signals/debug/mock/test-company
```

### Option 3: Use Python requests

```python
import requests

# Get signals
response = requests.get("http://localhost:8000/signals/test-company")
data = response.json()

print(f"Got {len(data['signals'])} signals")
for signal in data['signals']:
    print(f"- {signal['material']} in {signal['region']}: {signal['demand_direction']}")
```

## Troubleshooting

### Issue: ModuleNotFoundError

**Problem:** `ModuleNotFoundError: No module named 'fastapi'`

**Solution:**
```bash
# Make sure virtual environment is activated
# Then reinstall dependencies
pip install -r requirements.txt
```

### Issue: Port Already in Use

**Problem:** `Error: [Errno 48] Address already in use`

**Solution:**
```bash
# Use a different port
uvicorn main:app --reload --port 8001

# Or find and kill the process using port 8000
# On Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# On Linux/Mac:
lsof -ti:8000 | xargs kill
```

### Issue: API Keys Not Working

**Problem:** APIs showing "not_configured" or "error"

**Solution:**
1. Verify `.env` file exists in `backend/` directory
2. Check API keys are correct (no extra spaces)
3. Restart the server after changing `.env`
4. Test individual APIs:

```bash
python external_signals/engine.py
```

### Issue: Import Errors in routes/signals.py

**Problem:** Cannot import from external_signals

**Solution:**
```bash
# Make sure you're running from the backend directory
cd backend
python main.py

# Or set PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$(pwd)  # Linux/Mac
set PYTHONPATH=%PYTHONPATH%;%cd%       # Windows
```

## What's Next?

Once the backend is running:

1. ✅ Test all endpoints using `/docs`
2. ✅ Check API health at `/signals/health/check`
3. ✅ Try with and without API keys
4. 🚧 Build the frontend dashboard (coming soon)
5. 🚧 Add forecast engine
6. 🚧 Integrate Ollama for LLM reasoning

## Development Tips

### Auto-reload

The `--reload` flag makes the server restart automatically when you change code:

```bash
uvicorn main:app --reload
```

### View Logs

```bash
# Run with more detailed logging
uvicorn main:app --reload --log-level debug
```

### Test API Without Browser

Install HTTPie (better than curl):

```bash
pip install httpie

# Then use it
http GET localhost:8000/signals/test-company
```

## Next Steps

- [Backend README](README.md) - Full documentation
- [External Signals Engine](external_signals/engine.py) - Core logic
- [API Routes](routes/signals.py) - Endpoint definitions
- [Architecture Guide](../functioning/Architecture%20read%20me) - System design

## Need Help?

1. Check the logs in the terminal
2. Visit `/docs` for API documentation
3. Run `python external_signals/engine.py` to test the engine
4. Check that all files are in place:

```bash
backend/
├── main.py                ✓
├── requirements.txt       ✓
├── .env                   ✓ (you create this)
├── external_signals/
│   ├── __init__.py       ✓
│   └── engine.py         ✓
└── routes/
    ├── __init__.py       ✓
    └── signals.py        ✓
```

Happy coding! 🚀

