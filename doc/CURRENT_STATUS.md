# PRISMA Current Status (MVP - Enhanced)

## What Works Today
- ✅ Backend runs on FastAPI (http://localhost:8000)
- ✅ Frontend chat UI served by FastAPI (same URL)
- ✅ Ollama (llama3) provides local reasoning
- ✅ Forecast engine auto-generates demand from requirements
- ✅ External signals combine mock data and optional Google search trends
- ✅ LLM outputs direct answers + summary + actions + risks
- ✅ **NEW:** Cache manager for rate-limit protection (file-based)
- ✅ **NEW:** Standardized output format for industry intelligence
- ✅ **NEW:** Admin endpoints for cache management and diagnostics
- ✅ **NEW:** Enhanced health check with component status
- ✅ **NEW:** Comprehensive architecture documentation
- ✅ Validation script test_pipeline_validation.py checks end-to-end flow

## Typical Flow
1. Load requirements (mock or custom)
2. Forecasts and signals auto-generate
3. LLM analyzes and answers questions

## Key Endpoints
- `POST /analyze` - Full analysis with data loading
- `POST /analyze/direct` - Direct analysis with custom data (for UI)
- `GET /analyze/health` - Health check for analysis service
- `POST /forecast/generate` - Generate demand forecasts
- `GET /signals` - Fetch external signals
- `GET /admin/cache/stats` - Cache statistics
- `DELETE /admin/cache/clear` - Clear all cache
- `GET /admin/diagnostics` - Comprehensive system diagnostics
- `GET /health` - Global health check
- Full docs at: http://localhost:8000/docs

## Usage
`
python -m uvicorn main:app --reload --port 8000
# open http://localhost:8000
# load default data → run analysis → ask questions
`

## Requirements
- Ollama running locally (ollama serve)
- Optional: Google search API keys in .env

## Tests
`
python test_pipeline_validation.py
python test_analyze_basic.py
`

