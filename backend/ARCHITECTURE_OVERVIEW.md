# PRISMA Architecture Overview

## System Purpose

PRISMA is an AI-powered supply chain intelligence platform that helps procurement teams forecast material demand, identify supply risks, and make data-driven sourcing decisions.

The system combines:
- **Demand Forecasting** - Predicts future material requirements
- **External Signals** - Real-time market intelligence (prices, weather, industry trends)
- **LLM Reasoning** - AI-powered analysis and recommendations
- **Custom Search** - Industry intelligence from Google Programmable Search

---

## High-Level Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│                          PRISMA SYSTEM                               │
└──────────────────────────────────────────────────────────────────────┘

┌─────────────────┐
│   User / UI     │ ← Simple chat interface (index.html)
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         FastAPI Backend                              │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────┐                │
│  │  /signals   │  │   /analyze   │  │  /forecast  │                │
│  └─────────────┘  └──────────────┘  └─────────────┘                │
└───────┬──────────────────┬─────────────────┬────────────────────────┘
        │                  │                 │
        ▼                  ▼                 ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│  External    │   │  Forecast    │   │   Search     │
│  Signals     │   │  Engine      │   │   Engine     │
│  Engine      │   │              │   │              │
└──────┬───────┘   └──────┬───────┘   └──────┬───────┘
       │                  │                  │
       ▼                  ▼                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      Cache Manager                                   │
│         (Rate-limit protection & performance optimization)          │
└─────────────────────────────────────────────────────────────────────┘
       │                  │                  │
       ▼                  ▼                  ▼
┌────────────┐   ┌────────────┐   ┌──────────────────┐
│ Commodity  │   │   World    │   │  Google Search   │
│ APIs       │   │   Bank     │   │  API (optional)  │
└────────────┘   └────────────┘   └──────────────────┘

                         │
                         ▼
             ┌───────────────────────┐
             │    LLM Reasoning      │
             │   (Ollama/llama3)     │
             └───────────────────────┘
                         │
                         ▼
             ┌───────────────────────┐
             │  JSON Response        │
             │  • Summary            │
             │  • Actions            │
             │  • Risks              │
             │  • Watchlist          │
             └───────────────────────┘
```

---

## Data Flow

### End-to-End Request Flow

```
1. User Input
   ├─ Company requirements (JSON)
   ├─ Optional: Specific question
   └─ Optional: Filters (region, materials, industry)
           │
           ▼
2. Load Company Profile
   └─ From mock_requirements.json (MVP)
      or database (production)
           │
           ▼
3. Generate Forecasts
   ├─ Rule-based: Apply growth rate to current usage
   ├─ Output: Predicted demand per material
   └─ Future: ML models
           │
           ▼
4. Fetch External Signals
   ├─ MetalpriceAPI → Metal prices
   ├─ CommodityAPI → Commodity prices
   ├─ WeatherAPI → Climate risks
   ├─ World Bank → Economic indicators
   ├─ Custom Search → Industry trends (Google Search)
   └─ Cache Manager → Avoid rate limits
           │
           ▼
5. LLM Analysis
   ├─ Build prompt with all data
   ├─ Call Ollama (llama3)
   ├─ Extract & parse JSON response
   └─ Validate structure
           │
           ▼
6. Return Results
   ├─ Direct answer (if question asked)
   ├─ Summary of situation
   ├─ Recommended actions per material
   ├─ Risk assessment
   └─ Watchlist items
```

---

## Module Responsibilities

### 1. **FastAPI Routes** (`backend/routes/`)

#### `routes/signals.py`
- **Purpose**: Expose external signals API
- **Endpoint**: `GET /signals`
- **Dependencies**: `external_signals.engine`
- **Output**: Raw signal data (JSON)

#### `routes/analyze.py`
- **Purpose**: Main analysis endpoint - orchestrates full pipeline
- **Endpoints**:
  - `POST /analyze` - Full analysis with data loading
  - `POST /analyze/ask` - Alias emphasizing Q&A
  - `POST /analyze/direct` - Direct analysis with custom data (for UI)
  - `GET /analyze/health` - Health check
- **Dependencies**: `forecast.engine`, `external_signals.engine`, `llm.engine`
- **Flow**:
  1. Load company profile
  2. Generate forecasts
  3. Fetch signals
  4. Call LLM
  5. Return enriched response

#### `routes/forecast.py`
- **Purpose**: Standalone forecast generation
- **Endpoint**: `POST /forecast/generate`
- **Dependencies**: `forecast.engine`
- **Output**: Forecasts JSON

---

### 2. **Forecast Engine** (`backend/forecast/`)

#### `forecast/engine.py`
- **Purpose**: Generate demand predictions
- **Function**: `generate_forecasts(company_profile, horizon, growth_rate)`
- **MVP Strategy**: Simple rule-based (10% growth)
- **Future Strategy**: ML models, time-series analysis
- **Output**:
  ```json
  {
    "company_id": "abc-infra",
    "forecasts": [
      {
        "project_id": "proj-001",
        "material": "Steel",
        "current_usage": 1500,
        "predicted_demand": 1650,
        "unit": "MT",
        "confidence": 0.75,
        "month": "2025-12"
      }
    ]
  }
  ```

---

### 3. **External Signals Engine** (`backend/external_signals/`)

#### `external_signals/engine.py`
- **Purpose**: Aggregate demand risk signals from multiple APIs
- **Function**: `build_signals(company_id, region, materials, horizon, industry)`
- **Data Sources**:
  - **MetalpriceAPI** - Real-time metal prices
  - **CommodityAPI** - Commodity market data
  - **WeatherAPI** - Climate and weather patterns
  - **World Bank API** - Economic indicators
  - **Industry Intelligence** - From `search.industry` module
- **Features**:
  - Graceful fallbacks to mock data if APIs unavailable
  - Rate-limit handling via cache
  - Signal normalization (demand_score, confidence)
- **Output**:
  ```json
  {
    "company_id": "abc-infra",
    "signals": [
      {
        "material": "Steel",
        "demand_direction": "increase",
        "demand_score": 0.75,
        "confidence": 0.80,
        "drivers": ["Price rising 12%", "High demand in Asia"],
        "source": "metalpriceapi"
      }
    ],
    "data_sources": ["metalpriceapi", "world_bank", "industry_intelligence"]
  }
  ```

---

### 4. **Custom Search Engine** (`backend/search/`)

#### `search/industry.py`
- **Purpose**: Industry intelligence and trend analysis
- **Features**:
  - Google Programmable Search integration (optional)
  - Hardcoded industry trends (MVP fallback)
  - Caching for rate-limit protection
  - Standardized output format
- **Functions**:
  - `get_industry_trends(industry, materials)` - Raw trends
  - `get_standardized_trends(industry, materials, region)` - Standardized format
  - `search_google(query, num_results)` - Google Search API
- **Standardized Output**:
  ```json
  {
    "type": "industry_trend",
    "industry": "construction",
    "region": "Global",
    "summary": "Infrastructure spending increase...",
    "impact_on_materials": [
      {"material": "Steel", "effect": "demand_increase"}
    ],
    "source": "https://example.com/article",
    "confidence": 0.85
  }
  ```

---

### 5. **LLM Reasoning Engine** (`backend/llm/`)

#### `llm/config.py`
- **Purpose**: Centralized LLM configuration
- **Settings**:
  - `OLLAMA_BASE_URL` - Ollama server URL (default: localhost:11434)
  - `LLM_MODEL_NAME` - Model to use (default: llama3)
  - `LLM_TEMPERATURE` - Generation temperature (default: 0.7)
  - `LLM_MAX_TOKENS` - Max tokens to generate (default: 2000)

#### `llm/engine.py`
- **Purpose**: AI-powered analysis and recommendations
- **Functions**:
  - `build_prisma_prompt()` - Construct prompt with data + schema
  - `call_ollama()` - HTTP call to Ollama API
  - `extract_json_block()` - Robust JSON extraction from LLM response
  - `analyze_prisma()` - Orchestrate full LLM analysis
- **Prompt Engineering**:
  - Role definition (supply chain advisor)
  - Strict "no hallucination" rules
  - Comprehensive data injection (company, forecasts, signals)
  - JSON schema enforcement
  - Optional question handling
- **Error Handling**:
  - Connection errors (Ollama not running)
  - Timeout handling
  - JSON parsing fallbacks
  - Malformed response recovery
- **Output**:
  ```json
  {
    "answer": "Direct answer to question (if asked)",
    "summary": "2-3 sentence overview",
    "recommended_actions": [
      {
        "material": "Steel",
        "action": "Increase inventory by 20%",
        "reason": "Price trending up with strong demand"
      }
    ],
    "risks": [
      {
        "material": "Steel",
        "risk_level": "medium",
        "drivers": ["Price volatility", "Supply constraints"]
      }
    ],
    "watchlist_materials": [
      {
        "material": "Copper",
        "reason": "Moderate demand increase expected"
      }
    ]
  }
  ```

---

### 6. **Cache Manager** (`backend/utils/`)

#### `utils/cache_manager.py`
- **Purpose**: Rate-limit protection and performance optimization
- **Features**:
  - File-based JSON cache (stored in `.cache/`)
  - TTL-based expiration (configurable)
  - Automatic cache invalidation
  - Cache statistics
- **Usage**:
  ```python
  from utils.cache_manager import CacheManager
  
  cache = CacheManager()
  
  # Check cache
  data = cache.get("api_key")
  if data is None:
      data = fetch_from_api()
      cache.set("api_key", data, ttl=3600)  # 1 hour
  ```
- **TTL Defaults**:
  - `SHORT_TTL` = 1 hour (for volatile data)
  - `DEFAULT_TTL` = 24 hours (for stable data)
  - `LONG_TTL` = 7 days (for rarely changing data)

---

## Key Design Patterns

### 1. **Graceful Degradation**
- All external API calls have mock fallbacks
- System works offline with reduced accuracy
- Cache provides continuity during API outages

### 2. **Modular Architecture**
- Each engine is independent and testable
- Clear interfaces between modules
- Easy to swap implementations (e.g., switch LLM provider)

### 3. **Configuration-Driven**
- Environment variables for all external services
- No hard-coded credentials
- Easy to configure for different environments

### 4. **Error Transparency**
- Detailed error messages for debugging
- Graceful error handling (don't crash the pipeline)
- Health check endpoints for monitoring

### 5. **Caching Strategy**
- Transparent caching at the API level
- Reduces external API costs
- Improves response time
- Rate-limit protection

---

## External Dependencies

### Required
- **Python 3.11+**
- **FastAPI** - Web framework
- **Ollama** - Local LLM server
- **llama3** - LLM model

### Optional (with fallbacks)
- **MetalpriceAPI** - Metal price data
- **CommodityAPI** - Commodity prices
- **WeatherAPI** - Weather data
- **World Bank API** - Economic indicators
- **Google Programmable Search** - Industry intelligence

### Python Libraries
- `fastapi` - API framework
- `uvicorn` - ASGI server
- `requests` - HTTP client
- `pydantic` - Data validation
- `python-dotenv` - Environment management

---

## Configuration

### Environment Variables

```bash
# LLM Configuration
OLLAMA_BASE_URL=http://localhost:11434
LLM_MODEL_NAME=llama3
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=2000
LLM_REQUEST_TIMEOUT=120

# External APIs (Optional)
METALPRICEAPI_KEY=your_key_here
COMMODITYAPI_KEY=your_key_here
WEATHERAPI_KEY=your_key_here
GOOGLE_SEARCH_API_KEY=your_key_here
GOOGLE_SEARCH_ENGINE_ID=your_cx_here

# Cache Configuration
CACHE_ENABLED=true

# Feature Flags
USE_REAL_APIS=true
```

---

## Testing Strategy

### Test Files
1. **`test_pipeline_validation.py`** - End-to-end architecture validation
2. **`test_analyze_basic.py`** - `/analyze` endpoint tests
3. **`test_analyze_edge_cases.py`** - Edge case handling
4. **`test_analyze_error_handling.py`** - Error scenarios
5. **`test_llm_mock_vs_real.py`** - LLM integration tests
6. **`test_industry_search.py`** - Search engine tests

### Running Tests
```bash
cd backend

# Full pipeline validation
python test_pipeline_validation.py

# Specific endpoint tests
python test_analyze_basic.py

# All tests
python -m pytest
```

---

## Deployment

### Local Development
```bash
# 1. Start Ollama
ollama serve

# 2. Pull model (first time only)
ollama pull llama3

# 3. Start backend
cd backend
python -m uvicorn main:app --reload --port 8000

# 4. Access UI
# Open http://localhost:8000
```

### Production Considerations
- **Ollama**: Run as a service, consider GPU acceleration
- **Cache**: Use Redis instead of file-based cache
- **Database**: Replace mock JSON with PostgreSQL/MongoDB
- **API Keys**: Use secret management (AWS Secrets Manager, etc.)
- **Monitoring**: Add logging, metrics, alerting
- **Rate Limiting**: Implement per-user rate limits
- **Authentication**: Add JWT/OAuth for API access

---

## Performance Characteristics

### Response Times (Typical)
- **Forecast Generation**: < 100ms
- **External Signals (cached)**: < 200ms
- **External Signals (fresh)**: 2-5 seconds
- **LLM Analysis**: 5-15 seconds (depends on model, hardware)
- **Total `/analyze` request**: 6-20 seconds

### Optimization Opportunities
1. **Cache aggressively** - Most external data doesn't change hourly
2. **Parallelize API calls** - Fetch signals concurrently
3. **Smaller prompts** - Reduce LLM processing time
4. **Model tuning** - Fine-tune llama3 for faster responses
5. **GPU acceleration** - For Ollama inference

---

## Security Considerations

### Current (MVP)
- No authentication (local use only)
- API keys in `.env` (not committed)
- No input validation beyond Pydantic

### Production Requirements
- **Authentication**: JWT tokens, OAuth
- **Authorization**: Role-based access control
- **Input Validation**: Sanitize all user inputs
- **Rate Limiting**: Prevent abuse
- **API Key Management**: Rotate keys, use secret manager
- **HTTPS**: Enforce encrypted communication
- **Logging**: Audit trail for compliance

---

## Future Enhancements

### Near-Term (Next Milestone)
- [ ] Frontend file upload for custom requirements
- [ ] Database persistence (replace mock JSON)
- [ ] User authentication
- [ ] Docker containerization
- [ ] API documentation (Swagger improvements)

### Medium-Term
- [ ] ML-based forecasting models
- [ ] RAG (Retrieval Augmented Generation) for deeper analysis
- [ ] Real-time signal streaming (WebSockets)
- [ ] Multi-tenant support
- [ ] Export to PDF/Excel

### Long-Term
- [ ] Mobile app
- [ ] Advanced analytics dashboard
- [ ] Integration with ERP systems (SAP, Oracle)
- [ ] Automated procurement workflows
- [ ] Predictive maintenance signals

---

## Troubleshooting

### Common Issues

#### 1. Ollama Connection Error
```
Error: LLM service unavailable; ensure Ollama is running
```
**Solution**: Start Ollama with `ollama serve`

#### 2. Model Not Found
```
Error: Model 'llama3' not found
```
**Solution**: Pull model with `ollama pull llama3`

#### 3. JSON Parsing Errors
```
Error: Failed to parse JSON from response
```
**Solution**: Check LLM prompt formatting, increase temperature, or retry

#### 4. API Rate Limits
```
Error: API rate limit exceeded
```
**Solution**: Cache is automatically used. Wait and retry.

#### 5. Indentation Errors (Python)
**Solution**: Ensure consistent indentation (4 spaces, no tabs)

---

## Contact & Contribution

For questions, issues, or contributions:
- Check existing test files for usage examples
- Review `CURRENT_STATUS.md` for quick reference
- See `NEXT_MILESTONE.md` for planned features

---

**Last Updated**: November 8, 2025  
**Version**: MVP 0.1.0  
**Status**: ✅ Stable - Ready for demo and enhancement

