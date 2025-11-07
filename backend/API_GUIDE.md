# PRISMA API Usage Guide

Complete guide to using the PRISMA External Signals API.

## Base URL

```
http://localhost:8000
```

## Authentication

Currently no authentication required (MVP phase). 

Production version will support:
- API Keys
- JWT tokens
- OAuth 2.0

---

## Endpoints

### 1. Health Check

Check if the API is running.

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "healthy",
  "service": "PRISMA Backend",
  "version": "0.1.0"
}
```

**Example:**
```bash
curl http://localhost:8000/health
```

---

### 2. Get External Signals

Get demand risk signals for a company based on external data sources.

**Endpoint:** `GET /signals/{company_id}`

**Path Parameters:**
- `company_id` (required) - Your company identifier

**Query Parameters:**
- `region` (optional) - Filter by region (e.g., "Maharashtra", "Gujarat")
- `materials` (optional) - Comma-separated materials (e.g., "Steel,Copper,Aluminum")
- `horizon` (optional) - Time horizon. Default: "next_month"
- `use_real_apis` (optional) - Boolean. Use real APIs if configured. Default: true

**Response:**
```json
{
  "company_id": "abc-infra",
  "horizon": "next_month",
  "region_filter": "Maharashtra",
  "signals": [
    {
      "company_id": "abc-infra",
      "region": "Maharashtra",
      "material": "Steel",
      "material_category": "Metals",
      "horizon": "next_month",
      "demand_direction": "increase",
      "demand_score": 0.82,
      "confidence": 0.85,
      "drivers": [
        "Steel price increased by 9.2% in last 30 days",
        "Multiple large infrastructure tenders announced in region",
        "Monsoon season approaching - pre-stocking expected"
      ],
      "last_updated": "2025-11-07T19:00:00.123456"
    }
  ],
  "data_sources": ["mock", "commodity_api", "weather_api"],
  "generated_at": "2025-11-07T19:00:00.123456"
}
```

**Signal Object Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `company_id` | string | Company identifier |
| `region` | string | Geographic region |
| `material` | string | Material name (Steel, Copper, etc.) |
| `material_category` | string | Category (Metals, Construction Materials, etc.) |
| `horizon` | string | Time horizon for this signal |
| `demand_direction` | string | "increase", "decrease", or "stable" |
| `demand_score` | float | Risk score 0.0 (low) to 1.0 (high) |
| `confidence` | float | Confidence in signal 0.0 to 1.0 |
| `drivers` | array[string] | Human-readable reasons for this signal |
| `last_updated` | string (ISO 8601) | When signal was generated |

**Examples:**

```bash
# Basic usage - get all signals
curl http://localhost:8000/signals/my-company

# Filter by region
curl "http://localhost:8000/signals/my-company?region=Maharashtra"

# Filter by materials
curl "http://localhost:8000/signals/my-company?materials=Steel,Copper"

# Both filters
curl "http://localhost:8000/signals/my-company?region=Gujarat&materials=Steel"

# Use only mock data (no API calls)
curl "http://localhost:8000/signals/my-company?use_real_apis=false"

# Different time horizon
curl "http://localhost:8000/signals/my-company?horizon=next_quarter"
```

**Python Example:**
```python
import requests

response = requests.get(
    "http://localhost:8000/signals/my-company",
    params={
        "region": "Maharashtra",
        "materials": "Steel,Copper",
        "horizon": "next_month"
    }
)

data = response.json()

print(f"Company: {data['company_id']}")
print(f"Data sources: {', '.join(data['data_sources'])}")
print(f"\nFound {len(data['signals'])} signals:")

for signal in data['signals']:
    print(f"\n{signal['material']} ({signal['region']})")
    print(f"  Direction: {signal['demand_direction']}")
    print(f"  Risk Score: {signal['demand_score']:.2f}")
    print(f"  Confidence: {signal['confidence']:.2f}")
    print(f"  Drivers:")
    for driver in signal['drivers']:
        print(f"    - {driver}")
```

---

### 3. API Health Check

Check connectivity to all external APIs.

**Endpoint:** `GET /signals/health/check`

**Response:**
```json
{
  "status": "healthy",
  "apis": {
    "metalprice": "connected",
    "commodity": "not_configured",
    "weather": "connected",
    "worldbank": "connected"
  },
  "summary": "3/3 configured APIs responding"
}
```

**API Status Values:**
- `"connected"` - API is configured and responding
- `"not_configured"` - No API key provided
- `"error_XXX"` - Error occurred (XXX = HTTP status code)
- `"error: message"` - Error with description

**Example:**
```bash
curl http://localhost:8000/signals/health/check
```

**Use Cases:**
- Monitoring API health
- Debugging API configuration
- Validating API keys
- CI/CD health checks

---

### 4. Debug Mock Signals

Get mock signals without any external API calls. Useful for testing.

**Endpoint:** `GET /signals/debug/mock/{company_id}`

**Path Parameters:**
- `company_id` (required) - Your company identifier

**Response:**
```json
{
  "company_id": "test-company",
  "signals": [
    {
      "company_id": "test-company",
      "region": "Maharashtra",
      "material": "Steel",
      "demand_direction": "increase",
      "demand_score": 0.82,
      "confidence": 0.85,
      "drivers": [
        "Steel price increased by 9.2% in last 30 days",
        "Multiple large infrastructure tenders announced in region"
      ],
      "last_updated": "2025-11-07T19:00:00"
    }
  ]
}
```

**Example:**
```bash
curl http://localhost:8000/signals/debug/mock/test-company
```

**Use Cases:**
- Testing without API keys
- Demo/presentation mode
- Understanding signal format
- Development without API costs

---

## Understanding Signals

### Demand Direction

Indicates the expected trend in material demand:

- **`increase`** - Demand is rising
  - Price increases
  - New projects in region
  - Supply constraints
  - Pre-stocking behavior

- **`decrease`** - Demand is falling
  - Price drops
  - Project delays/cancellations
  - Oversupply
  - Seasonal downturn

- **`stable`** - Demand is steady
  - Normal market conditions
  - No significant changes
  - Predictable patterns

### Demand Score

Numerical risk indicator (0.0 to 1.0):

| Range | Interpretation | Action |
|-------|---------------|--------|
| 0.0 - 0.3 | Low risk | Normal procurement |
| 0.3 - 0.5 | Moderate risk | Monitor closely |
| 0.5 - 0.7 | Elevated risk | Consider increasing orders |
| 0.7 - 0.9 | High risk | Increase orders, secure suppliers |
| 0.9 - 1.0 | Critical risk | Urgent action needed |

### Confidence

How confident PRISMA is in this signal:

| Range | Meaning |
|-------|---------|
| 0.7 - 1.0 | High confidence - multiple data sources agree |
| 0.5 - 0.7 | Moderate confidence - limited data |
| 0.0 - 0.5 | Low confidence - use with caution |

### Data Sources

The `data_sources` array shows which systems contributed to the signals:

- `mock` - Mock/sample data
- `commodity_api` - Real commodity price data
- `weather_api` - Weather forecasts and alerts
- `worldbank_api` - Economic/infrastructure indicators

---

## Integration Examples

### JavaScript/Node.js

```javascript
const axios = require('axios');

async function getPrismaSignals(companyId, options = {}) {
  try {
    const response = await axios.get(
      `http://localhost:8000/signals/${companyId}`,
      { params: options }
    );
    
    return response.data;
  } catch (error) {
    console.error('Error fetching signals:', error.message);
    throw error;
  }
}

// Usage
const signals = await getPrismaSignals('my-company', {
  region: 'Maharashtra',
  materials: 'Steel,Copper'
});

console.log(`Got ${signals.signals.length} signals`);
signals.signals.forEach(signal => {
  console.log(`${signal.material}: ${signal.demand_direction} (${signal.demand_score})`);
});
```

### Python

```python
import requests
from typing import Optional, List

class PrismaClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
    
    def get_signals(
        self,
        company_id: str,
        region: Optional[str] = None,
        materials: Optional[List[str]] = None,
        horizon: str = "next_month",
        use_real_apis: bool = True
    ):
        params = {
            "horizon": horizon,
            "use_real_apis": use_real_apis
        }
        
        if region:
            params["region"] = region
        
        if materials:
            params["materials"] = ",".join(materials)
        
        response = requests.get(
            f"{self.base_url}/signals/{company_id}",
            params=params
        )
        response.raise_for_status()
        return response.json()
    
    def check_health(self):
        response = requests.get(f"{self.base_url}/signals/health/check")
        response.raise_for_status()
        return response.json()

# Usage
client = PrismaClient()

# Check health
health = client.check_health()
print(f"API Status: {health['status']}")

# Get signals
signals = client.get_signals(
    company_id="my-company",
    region="Maharashtra",
    materials=["Steel", "Copper"]
)

print(f"Got {len(signals['signals'])} signals")
for signal in signals['signals']:
    print(f"{signal['material']}: {signal['demand_direction']} "
          f"(score: {signal['demand_score']:.2f})")
```

### React/Frontend

```javascript
import { useState, useEffect } from 'react';

function SignalsDashboard({ companyId }) {
  const [signals, setSignals] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchSignals() {
      try {
        const response = await fetch(
          `http://localhost:8000/signals/${companyId}?region=Maharashtra`
        );
        const data = await response.json();
        setSignals(data.signals);
      } catch (error) {
        console.error('Failed to fetch signals:', error);
      } finally {
        setLoading(false);
      }
    }

    fetchSignals();
  }, [companyId]);

  if (loading) return <div>Loading signals...</div>;

  return (
    <div>
      <h2>Demand Signals</h2>
      {signals.map((signal, idx) => (
        <div key={idx} className="signal-card">
          <h3>{signal.material} - {signal.region}</h3>
          <p>Direction: {signal.demand_direction}</p>
          <p>Risk Score: {(signal.demand_score * 100).toFixed(0)}%</p>
          <ul>
            {signal.drivers.map((driver, i) => (
              <li key={i}>{driver}</li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  );
}
```

---

## Rate Limits

Currently no rate limits in MVP phase.

Production considerations:
- MetalpriceAPI: 100 requests/month (free tier)
- CommodityAPI: Varies by plan
- WeatherAPI: 1M requests/month (free tier)
- World Bank API: No official limits

**Best Practices:**
- Cache responses when possible
- Don't poll more than once per hour for same company
- Use `use_real_apis=false` for testing

---

## Error Handling

### HTTP Status Codes

| Code | Meaning | Cause |
|------|---------|-------|
| 200 | Success | Request succeeded |
| 404 | Not Found | Invalid endpoint |
| 422 | Validation Error | Invalid parameters |
| 500 | Internal Error | Server error (check logs) |

### Error Response Format

```json
{
  "detail": "Error generating signals: Connection timeout"
}
```

### Handling Errors

```python
import requests

try:
    response = requests.get("http://localhost:8000/signals/my-company")
    response.raise_for_status()  # Raises exception for 4xx/5xx
    data = response.json()
except requests.exceptions.HTTPError as e:
    print(f"HTTP Error: {e.response.status_code}")
    print(f"Detail: {e.response.json()['detail']}")
except requests.exceptions.ConnectionError:
    print("Cannot connect to PRISMA API - is it running?")
except requests.exceptions.Timeout:
    print("Request timed out")
```

---

## Interactive Documentation

PRISMA includes automatic interactive API documentation:

### Swagger UI
Visit: http://localhost:8000/docs

Features:
- Try all endpoints directly in browser
- See request/response schemas
- Generate code samples
- No setup required

### ReDoc
Visit: http://localhost:8000/redoc

Features:
- Clean, readable documentation
- Better for printing/sharing
- Search functionality

---

## Tips & Best Practices

### 1. Start with Mock Data

Test your integration without API keys:

```bash
curl "http://localhost:8000/signals/my-company?use_real_apis=false"
```

### 2. Filter Strategically

Don't fetch all signals if you only need specific ones:

```bash
# Instead of getting all signals and filtering client-side
curl http://localhost:8000/signals/my-company

# Do this - filter server-side
curl "http://localhost:8000/signals/my-company?region=Maharashtra&materials=Steel"
```

### 3. Cache Responses

Signals don't change every second. Cache for at least 1 hour:

```python
from functools import lru_cache
from datetime import datetime, timedelta

# Simple in-memory cache
_cache = {}
CACHE_TTL = timedelta(hours=1)

def get_cached_signals(company_id):
    if company_id in _cache:
        cached_time, data = _cache[company_id]
        if datetime.now() - cached_time < CACHE_TTL:
            return data
    
    # Fetch fresh data
    data = requests.get(f"http://localhost:8000/signals/{company_id}").json()
    _cache[company_id] = (datetime.now(), data)
    return data
```

### 4. Monitor API Health

Set up automated health checks:

```python
import requests
import time

def monitor_prisma():
    while True:
        try:
            response = requests.get("http://localhost:8000/signals/health/check")
            health = response.json()
            
            if health['status'] != 'healthy':
                print(f"⚠️  PRISMA health degraded: {health['summary']}")
            else:
                print(f"✅ PRISMA healthy: {health['summary']}")
        
        except Exception as e:
            print(f"❌ PRISMA unreachable: {e}")
        
        time.sleep(300)  # Check every 5 minutes
```

### 5. Handle Missing Data Gracefully

Not all fields may be present:

```python
for signal in signals['signals']:
    material = signal.get('material', 'Unknown')
    category = signal.get('material_category', 'General')
    drivers = signal.get('drivers', ['No specific drivers available'])
```

---

## Coming Soon

These endpoints are planned for future releases:

- `POST /upload-requirements` - Upload company requirements
- `GET /forecasts/{company_id}` - Get demand forecasts
- `POST /analyze` - Get LLM-powered recommendations
- `GET /recommendations/{company_id}` - Procurement suggestions
- `POST /auth/login` - Authentication

---

## Support

For issues or questions:
1. Check server logs
2. Test with mock data: `?use_real_apis=false`
3. Verify API health: `/signals/health/check`
4. Check interactive docs: `/docs`

Happy integrating! 🚀

