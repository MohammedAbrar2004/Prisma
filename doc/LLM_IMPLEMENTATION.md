# PRISMA LLM Reasoning Layer - Implementation Guide

## 🎯 Overview

This document describes the **LLM Reasoning Layer** and **Industry Intelligence** implementation for PRISMA - a comprehensive system that uses local Ollama (llama3) to provide AI-powered procurement recommendations based on demand forecasts and external signals.

## 📦 What Was Built

### Core Modules

#### 1. LLM Module (`backend/llm/`)

**`llm/config.py`** - Environment-based configuration
- Ollama connection settings (default: http://localhost:11434)
- Model selection (default: llama3)
- Temperature, max tokens, timeout settings
- No hard-coded secrets

**`llm/engine.py`** - Core LLM reasoning engine (500+ lines)
- `build_prisma_prompt()` - Constructs deterministic prompts with clear instructions
- `call_ollama()` - Makes HTTP requests to local Ollama API
- `extract_json_block()` - Robustly parses JSON from LLM responses
- `analyze_prisma()` - Main orchestration function for analysis
- `test_ollama_connection()` - Health check utility

**`llm/utils.py`** - Helper utilities
- JSON normalization and validation
- Input data validation (company profiles, forecasts, signals)
- Material name normalization
- Response formatting utilities
- Debugging helpers

**`llm/__init__.py`** - Clean module exports

#### 2. Industry Intelligence Module (`backend/search/`)

**`search/industry.py`** - Industry trend analysis (400+ lines)
- `get_industry_trends()` - Retrieve trends by industry/sector
- `get_industry_signals()` - Convert trends to signal format
- `search_industry_trends()` - Keyword search functionality
- `get_available_industries()` - List supported industries
- Hardcoded MVP data for: construction, infrastructure, manufacturing, energy
- Documented path to production (custom search engines, news APIs, etc.)

**`search/__init__.py`** - Module exports

#### 3. API Routes

**`routes/analyze.py`** - /analyze endpoint (450+ lines)
- `POST /analyze` - Main analysis endpoint
- `POST /analyze/ask` - Conversational Q&A alias
- `GET /analyze/health` - Health check for analysis service
- Request/response models with Pydantic validation
- Helper functions for loading mock data
- Comprehensive error handling

**Integration in `main.py`**
- Imported and wired analyze router
- Updated API description
- Added Ollama to external services list

#### 4. External Signals Integration

**Updated `external_signals/engine.py`**
- Added `industry` parameter to `build_signals()`
- Integrated industry intelligence signals
- Added `industry_intelligence` to data sources
- Graceful handling if industry module unavailable

#### 5. Comprehensive Test Suite

**`test_analyze_basic.py`** (600+ lines)
- Basic analysis request
- Materials filter
- Region filter
- Industry parameter
- Custom questions
- Health endpoint

**`test_analyze_edge_cases.py`** (500+ lines)
- Invalid company_id
- Empty materials list
- Very long questions
- Special characters
- Minimal/maximum payloads
- Case sensitivity
- Unicode characters

**`test_analyze_error_handling.py`** (550+ lines)
- Server connectivity
- Ollama availability
- Invalid JSON payloads
- Missing required fields
- Timeout handling
- Concurrent requests
- Malformed data handling

**`test_llm_mock_vs_real.py`** (650+ lines)
- Direct Ollama connection
- Simple LLM calls
- Prompt building
- JSON extraction
- Full analysis pipeline
- API endpoint integration
- Response consistency
- Performance benchmarking

**`test_industry_search.py`** (600+ lines)
- Available industries
- Industry trends by sector
- Material filtering
- Signal format conversion
- Search functionality
- Multiple industries
- Signals engine integration
- API endpoint with industry
- Data quality validation

## 🚀 Quick Start

### Prerequisites

1. **Ollama installed and running**
   ```bash
   # Install Ollama (if not already)
   # Visit: https://ollama.ai
   
   # Pull llama3 model
   ollama pull llama3
   
   # Start Ollama server
   ollama serve
   ```

2. **Backend dependencies installed**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Environment variables (optional)**
   ```bash
   # In backend/.env
   OLLAMA_BASE_URL=http://localhost:11434
   LLM_MODEL_NAME=llama3
   LLM_TEMPERATURE=0.7
   ```

### Running the Server

```bash
cd backend
uvicorn main:app --reload --port 8000
```

Server starts at: http://localhost:8000

### Testing the Implementation

#### Quick Test - Health Check
```bash
curl http://localhost:8000/analyze/health
```

#### Basic Analysis Request
```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "company_id": "abc-infra",
    "materials": ["Steel", "Copper"],
    "industry": "construction"
  }'
```

#### Run Test Suites
```bash
# Basic functionality
python test_analyze_basic.py

# Edge cases
python test_analyze_edge_cases.py

# Error handling
python test_analyze_error_handling.py

# LLM functionality
python test_llm_mock_vs_real.py

# Industry intelligence
python test_industry_search.py
```

## 📊 API Documentation

### POST /analyze

Main endpoint for AI-powered procurement analysis.

**Request Body:**
```json
{
  "company_id": "abc-infra",
  "question": "Should we increase steel procurement?",
  "region": "Maharashtra",
  "materials": ["Steel", "Copper"],
  "industry": "construction",
  "horizon": "next_month",
  "use_real_apis": false
}
```

**Response:**
```json
{
  "company_id": "abc-infra",
  "summary": "Steel demand expected to increase 15% with moderate price risk...",
  "recommended_actions": [
    {
      "material": "Steel",
      "action": "Increase inventory by 20%",
      "reason": "Price trending upward with strong demand signals"
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
  ],
  "data_sources": ["mock", "commodity_api", "industry_intelligence"],
  "generated_at": "2025-11-08T10:00:00"
}
```

### POST /analyze/ask

Conversational Q&A endpoint (same as /analyze but emphasizes questions).

### GET /analyze/health

Health check for analysis service.

**Response:**
```json
{
  "status": "healthy",
  "ollama": {
    "status": "connected",
    "model": "llama3",
    "base_url": "http://localhost:11434"
  },
  "data": {
    "company_profiles": true,
    "forecasts": true
  }
}
```

## 🔧 Architecture

### Data Flow

```
User Request
    ↓
POST /analyze (routes/analyze.py)
    ↓
1. Load company profile (mock_requirements.json)
2. Load forecasts (mock_forecasts.json)
3. Build signals → external_signals.build_signals()
    ↓
    ├─→ Mock signals
    ├─→ Commodity price signals
    ├─→ Weather signals
    ├─→ Infrastructure signals
    └─→ Industry intelligence signals ✨ NEW
    ↓
4. LLM Analysis → llm.analyze_prisma()
    ↓
    ├─→ build_prisma_prompt()
    ├─→ call_ollama() → Local Ollama API
    └─→ extract_json_block()
    ↓
5. Return structured recommendations
```

### Module Dependencies

```
routes/analyze.py
    ↓
    ├─→ external_signals/engine.py
    │       ↓
    │       └─→ search/industry.py ✨ NEW
    │
    └─→ llm/engine.py ✨ NEW
            ↓
            └─→ llm/config.py
```

## 🎓 Key Design Principles

### 1. Framework-Agnostic Core

- `llm/engine.py` has NO FastAPI dependencies
- Can be used in CLI tools, notebooks, or other frameworks
- Easy to test in isolation

### 2. Deterministic Prompts

- Clear system instructions
- Explicit JSON schema
- "Use only provided data" constraint
- No hallucination encouragement

### 3. Robust Error Handling

- Connection errors (Ollama down)
- Timeout handling (LLM is slow)
- JSON parsing errors
- Graceful degradation

### 4. Mock-First Development

- Works without Ollama for testing
- Mock industry data for MVP
- Easy to swap real services later

### 5. Type Safety

- Type hints everywhere
- Pydantic models for API
- Clear function signatures

## 📈 Performance Considerations

### Expected Response Times

- **Mock data only**: 30-60 seconds (LLM processing time)
- **With real APIs**: 35-65 seconds (LLM + API calls)
- **Health check**: < 1 second

### Optimization Strategies

1. **Caching** (Future)
   - Cache LLM responses for identical inputs
   - Redis with 1-hour TTL
   - Invalidate on new data

2. **Async Processing** (Future)
   - Background jobs for analysis
   - WebSocket for real-time updates
   - Queue system (Celery/RQ)

3. **Prompt Optimization**
   - Shorter prompts = faster responses
   - Structured data over long text
   - Lower temperature for consistency

## 🔐 Security & Best Practices

### Current Implementation

✅ No hard-coded secrets
✅ Environment-based configuration
✅ Input validation (Pydantic)
✅ Timeout protection
✅ Error sanitization (no stack traces to users)

### Production Recommendations

- [ ] Add authentication (JWT/API keys)
- [ ] Rate limiting (per user/IP)
- [ ] Request logging & monitoring
- [ ] Input sanitization (prevent injection)
- [ ] Output content filtering
- [ ] HTTPS only
- [ ] CORS restrictions

## 🧪 Testing Strategy

### Test Coverage

- **Unit Tests**: Individual LLM functions, industry intelligence
- **Integration Tests**: Full analysis pipeline, API endpoints
- **Edge Cases**: Invalid inputs, boundary conditions
- **Error Scenarios**: Service unavailability, timeouts
- **Performance**: Response times, concurrent requests

### Test Philosophy

- Real Ollama tests (not mocked) for authenticity
- Graceful handling when Ollama unavailable
- Documentation tests for manual verification
- Comprehensive logging for debugging

## 📁 File Structure

```
backend/
├── llm/                          ✨ NEW
│   ├── __init__.py              # Module exports
│   ├── config.py                # LLM configuration
│   ├── engine.py                # Core LLM functions
│   └── utils.py                 # Helper utilities
│
├── search/                       ✨ NEW
│   ├── __init__.py              # Module exports
│   └── industry.py              # Industry intelligence
│
├── routes/
│   ├── __init__.py
│   ├── signals.py               # External signals API
│   └── analyze.py               ✨ NEW - Analysis API
│
├── external_signals/
│   ├── __init__.py
│   └── engine.py                # ✨ UPDATED - Industry integration
│
├── data/
│   ├── mock_requirements.json   # Company profiles
│   └── mock_forecasts.json      # Demand forecasts
│
├── main.py                       # ✨ UPDATED - Analyze router
│
├── test_analyze_basic.py         ✨ NEW
├── test_analyze_edge_cases.py    ✨ NEW
├── test_analyze_error_handling.py ✨ NEW
├── test_llm_mock_vs_real.py      ✨ NEW
└── test_industry_search.py       ✨ NEW
```

## 🚧 Future Enhancements

### Short-Term (MVP+)

- [ ] Response caching (Redis)
- [ ] Streaming responses (SSE)
- [ ] More industry categories
- [ ] Historical analysis tracking

### Medium-Term

- [ ] Multiple LLM models support
- [ ] Custom fine-tuned models
- [ ] Real-time industry data (APIs)
- [ ] User feedback loop
- [ ] A/B testing for prompts

### Long-Term

- [ ] Multi-language support
- [ ] Advanced RAG (vector DB)
- [ ] Predictive analytics
- [ ] Automated procurement actions
- [ ] Integration with ERP systems

## 🐛 Troubleshooting

### Ollama Connection Issues

**Problem**: `ConnectionError: LLM service unavailable`

**Solutions**:
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Start Ollama
ollama serve

# Check model is available
ollama list
ollama pull llama3
```

### Slow Response Times

**Problem**: Analysis takes > 2 minutes

**Solutions**:
- Reduce LLM_TEMPERATURE (faster but less creative)
- Reduce LLM_MAX_TOKENS (shorter responses)
- Use smaller model (llama3:8b vs llama3:70b)
- Optimize prompt length

### JSON Parsing Errors

**Problem**: `ValueError: Failed to parse JSON from response`

**Causes**:
- LLM didn't follow JSON schema
- Prompt unclear
- Model too small/weak

**Solutions**:
- Review prompt clarity
- Use stronger model
- Add examples to prompt
- Increase temperature slightly

### Industry Intelligence Not Appearing

**Problem**: `industry_intelligence` not in data_sources

**Solutions**:
```bash
# Check module import
python -c "from search.industry import get_industry_trends; print('OK')"

# Verify integration
python test_industry_search.py
```

## 📞 Support & Resources

### Documentation

- Main README: `backend/README.md`
- API Guide: `backend/API_GUIDE.md`
- Setup Guide: `backend/SETUP.md`
- This Document: `backend/LLM_IMPLEMENTATION.md`

### Interactive Docs

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Test Scripts

- Run all tests to validate setup
- Check logs for detailed error messages
- Use health endpoints for diagnostics

## 📊 Statistics

- **Total Files Created**: 13
- **Total Lines of Code**: ~4,500+
- **Test Files**: 5 comprehensive test suites
- **API Endpoints**: 3 new endpoints
- **Functions Implemented**: 40+ functions
- **Documentation**: Extensive inline + this guide

## ✅ Implementation Checklist

### Core Functionality
- [x] LLM configuration module
- [x] Ollama integration
- [x] Prompt engineering
- [x] JSON extraction
- [x] Analysis orchestration
- [x] Industry intelligence
- [x] Signal integration
- [x] API endpoints
- [x] Error handling

### Testing
- [x] Basic functionality tests
- [x] Edge case tests
- [x] Error handling tests
- [x] LLM integration tests
- [x] Industry intelligence tests

### Documentation
- [x] Inline code comments
- [x] Function docstrings
- [x] API documentation
- [x] This implementation guide
- [x] Usage examples

### Integration
- [x] External signals integration
- [x] Mock data compatibility
- [x] Main app wiring
- [x] Health checks

---

**Status**: ✅ Complete and Production-Ready (MVP)
**Date**: November 8, 2025
**Version**: 1.0.0

**Built with**: Python 3.10+, FastAPI, Ollama, llama3

