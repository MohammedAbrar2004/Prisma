# PRISMA Backend

Backend API server for PRISMA - Predictive Resource Intelligence & Supply-chain Management using AI.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure API Keys

Copy the example environment file and add your API keys:

```bash
cp env.example .env
```

Edit `.env` and add your API keys:

```env
METALPRICE_API_KEY=your_key_here
COMMODITY_API_KEY=your_key_here
WEATHER_API_KEY=your_key_here
```

**Get API Keys:**

- **MetalpriceAPI**: https://metalpriceapi.com/ (100 free requests/month)
- **CommodityAPI**: https://commodityapi.com/ (Free tier available)
- **WeatherAPI**: https://www.weatherapi.com/ (1M free requests/month)
- **World Bank API**: No key needed - public API

### 3. Run the Server

```bash
# Option 1: Using uvicorn
uvicorn main:app --reload --port 8000

# Option 2: Direct Python
python main.py
```

Server will start at: **http://localhost:8000**

### 4. Test the API

Visit the interactive documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

Or test with curl:

```bash
# Get signals for a company
curl http://localhost:8000/signals/test-company

# Get signals for specific region
curl "http://localhost:8000/signals/test-company?region=Maharashtra"

# Get signals for specific materials
curl "http://localhost:8000/signals/test-company?materials=Steel,Copper"

# Check API health
curl http://localhost:8000/signals/health/check

# Get mock data only (no API calls)
curl http://localhost:8000/signals/debug/mock/test-company
```

## 📁 Project Structure

```
backend/
├── main.py                      # FastAPI app entry point
├── requirements.txt             # Python dependencies
├── env.example                  # Environment variables template
│
├── routes/                      # API endpoints
│   ├── __init__.py
│   └── signals.py              # /signals endpoints
│
├── external_signals/            # External data collection
│   ├── __init__.py
│   └── engine.py               # Signal aggregation & API integrations
│
├── forecast/                    # Demand forecasting (future)
│   └── engine.py
│
├── llm/                         # LLM reasoning layer (future)
│   └── engine.py
│
├── models/                      # Shared data models (future)
│   └── schemas.py
│
└── data/                        # Mock/sample data
    ├── mock_requirements.json
    ├── mock_forecasts.json
    └── mock_signals.json
```

## 🔌 API Endpoints

### Signals API

#### `GET /signals/{company_id}`

Get external demand signals for a company.

**Parameters:**
- `company_id` (path) - Company identifier
- `region` (query, optional) - Filter by region (e.g., "Maharashtra")
- `materials` (query, optional) - Comma-separated materials (e.g., "Steel,Copper")
- `horizon` (query, optional) - Time horizon (default: "next_month")
- `use_real_apis` (query, optional) - Use real APIs if configured (default: true)

**Example Response:**
```json
{
  "company_id": "abc-corp",
  "horizon": "next_month",
  "signals": [
    {
      "region": "Maharashtra",
      "material": "Steel",
      "demand_direction": "increase",
      "demand_score": 0.82,
      "confidence": 0.85,
      "drivers": [
        "Steel price increased by 9.2% in last 30 days",
        "Multiple large infrastructure tenders announced"
      ],
      "last_updated": "2025-11-07T19:00:00"
    }
  ],
  "data_sources": ["mock", "commodity_api", "weather_api"]
}
```

#### `GET /signals/health/check`

Check connectivity to external APIs.

**Example Response:**
```json
{
  "status": "healthy",
  "apis": {
    "metalprice": "connected",
    "commodity": "not_configured",
    "weather": "connected",
    "worldbank": "connected"
  }
}
```

#### `GET /signals/debug/mock/{company_id}`

Get mock signals only (no API calls). Useful for testing.

## 🔧 Development

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black .
```

### Type Checking

```bash
mypy .
```

### Linting

```bash
flake8 .
```

## 🌐 External APIs Integration

### MetalpriceAPI

Tracks metal prices (steel, copper, aluminum, etc.)

- **Usage**: Price trend analysis → demand risk signals
- **Free tier**: 100 requests/month
- **Docs**: https://metalpriceapi.com/documentation

### CommodityAPI

Tracks 130+ commodities (metals, energy, agriculture)

- **Usage**: Broader commodity tracking, backup for metals
- **Free tier**: Available with limitations
- **Docs**: https://commodityapi.com/documentation

### WeatherAPI.com

Regional weather forecasts and alerts

- **Usage**: Weather impact on material demand and logistics
- **Free tier**: 1M requests/month
- **Docs**: https://www.weatherapi.com/docs/

### World Bank API

Economic and infrastructure indicators

- **Usage**: Infrastructure spending trends → demand signals
- **Free tier**: Unlimited (public API)
- **Docs**: https://datahelpdesk.worldbank.org/knowledgebase/articles/889392

## 🔐 Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `METALPRICE_API_KEY` | MetalpriceAPI key | No* | - |
| `COMMODITY_API_KEY` | CommodityAPI key | No* | - |
| `WEATHER_API_KEY` | WeatherAPI key | No* | - |
| `ENVIRONMENT` | Environment (dev/prod) | No | development |
| `HOST` | Server host | No | 0.0.0.0 |
| `PORT` | Server port | No | 8000 |
| `OLLAMA_BASE_URL` | Ollama server URL | No | http://localhost:11434 |
| `USE_REAL_APIS` | Enable real API calls | No | true |

\* APIs are optional - the system works with mock data if keys not provided.

## 🚧 Coming Soon

- [ ] **Requirements Upload** - `/upload-requirements` endpoint
- [ ] **Forecast Engine** - `/forecasts/{company_id}` endpoint
- [ ] **LLM Reasoning** - `/analyze` endpoint with Ollama integration
- [ ] **Authentication** - API key / JWT support
- [ ] **Database** - PostgreSQL integration for persistence
- [ ] **Caching** - Redis for API response caching
- [ ] **Rate Limiting** - Per-user API limits

## 📝 Notes

### Mock Data vs Real APIs

The system is designed to work seamlessly with or without API keys:

- **With API keys**: Real-time data from external sources
- **Without API keys**: Falls back to realistic mock data
- **Mixed mode**: Combines mock + real data

This makes it perfect for:
- Development without API costs
- Demos and presentations
- Testing and CI/CD pipelines

### API Rate Limits

Be mindful of free tier limits:

- MetalpriceAPI: 100 requests/month
- CommodityAPI: Varies by plan
- WeatherAPI: 1M requests/month

Consider implementing caching for production use.

## 🤝 Contributing

When adding new features:

1. Keep business logic in respective engines (`external_signals`, `forecast`, `llm`)
2. Keep routes thin - delegate to engines
3. Add tests for new functionality
4. Update this README

## 📄 License

(Add your license here)

