# PRISMA Quick Reference Guide

## 🚀 Quick Start (3 Steps)

```bash
# 1. Start Ollama
ollama serve

# 2. Start Backend
cd backend
python -m uvicorn main:app --reload --port 8000

# 3. Open Browser
# Navigate to: http://localhost:8000
```

---

## 📌 Essential Endpoints

### Analysis & Forecasting
```bash
# Get full analysis
POST http://localhost:8000/analyze
{
  "company_id": "abc-infra",
  "question": "Should we increase steel inventory?"
}

# Generate forecasts
POST http://localhost:8000/forecast/generate
{
  "company_id": "abc-infra",
  "horizon": "next_month"
}

# Get external signals
GET http://localhost:8000/signals?company_id=abc-infra
```

### Admin & Monitoring
```bash
# System health
GET http://localhost:8000/health

# Cache statistics
GET http://localhost:8000/admin/cache/stats

# System diagnostics
GET http://localhost:8000/admin/diagnostics

# Clear cache
DELETE http://localhost:8000/admin/cache/clear
```

---

## 🔧 Configuration Cheat Sheet

### Environment Variables (.env)
```bash
# LLM Configuration
OLLAMA_BASE_URL=http://localhost:11434
LLM_MODEL_NAME=llama3
LLM_TEMPERATURE=0.7

# Cache
CACHE_ENABLED=true

# External APIs (Optional)
GOOGLE_SEARCH_API_KEY=your_key_here
GOOGLE_SEARCH_ENGINE_ID=your_cx_here
METALPRICEAPI_KEY=your_key_here
```

---

## 📂 Project Structure

```
backend/
├── main.py              # FastAPI entry point
├── routes/              # API endpoints
│   ├── analyze.py       # Main analysis endpoint
│   ├── forecast.py      # Forecast generation
│   ├── signals.py       # External signals
│   └── admin.py         # Admin & monitoring
├── llm/                 # LLM reasoning engine
│   ├── config.py        # LLM configuration
│   └── engine.py        # Ollama integration
├── forecast/            # Demand forecasting
│   └── engine.py        # Forecast generation
├── external_signals/    # Market intelligence
│   └── engine.py        # Signal aggregation
├── search/              # Industry intelligence
│   └── industry.py      # Google Search + trends
├── utils/               # Shared utilities
│   └── cache_manager.py # Caching system
├── data/                # Mock data
│   ├── mock_requirements.json
│   └── mock_forecasts.json
└── static/              # Frontend UI
    └── index.html
```

---

## 🧪 Testing Commands

```bash
# Full pipeline validation
python test_pipeline_validation.py

# Basic endpoint tests
python test_analyze_basic.py

# Industry search tests
python test_industry_search.py

# Run all tests
python -m pytest
```

---

## 🐛 Common Issues & Solutions

### Issue: "Ollama connection error"
```bash
# Solution: Start Ollama
ollama serve

# Verify Ollama is running
curl http://localhost:11434/api/tags
```

### Issue: "Model 'llama3' not found"
```bash
# Solution: Pull the model
ollama pull llama3
```

### Issue: "Cache not working"
```bash
# Check cache status
curl http://localhost:8000/admin/cache/stats

# Clear cache if needed
curl -X DELETE http://localhost:8000/admin/cache/clear
```

### Issue: "Import errors"
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

---

## 💡 Usage Examples

### Example 1: Basic Analysis
```python
import requests

response = requests.post(
    "http://localhost:8000/analyze",
    json={
        "company_id": "abc-infra",
        "horizon": "next_month",
        "industry": "construction"
    }
)
print(response.json())
```

### Example 2: Ask a Question
```python
response = requests.post(
    "http://localhost:8000/analyze",
    json={
        "company_id": "abc-infra",
        "question": "What are the biggest risks to our steel supply?"
    }
)
print(response.json()["answer"])
```

### Example 3: Get Cache Stats
```python
response = requests.get("http://localhost:8000/admin/cache/stats")
stats = response.json()
print(f"Cache has {stats['total_entries']} entries")
print(f"Total size: {stats['total_size_mb']} MB")
```

### Example 4: Industry Trends
```python
from search.industry import get_standardized_trends

trends = get_standardized_trends(
    industry="construction",
    materials=["Steel", "Concrete"],
    region="Global"
)

for trend in trends:
    print(trend["summary"])
    print(trend["impact_on_materials"])
```

---

## 📊 API Response Formats

### Analysis Response
```json
{
  "answer": "Direct answer to your question",
  "summary": "2-3 sentence overview of the situation",
  "recommended_actions": [
    {
      "material": "Steel",
      "action": "Increase inventory by 20%",
      "reason": "Price trending upward with strong demand"
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

### Forecast Response
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

### Signals Response
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
  ]
}
```

---

## 🎯 Performance Tips

1. **Use caching** - Automatically enabled, saves time and API costs
2. **Batch requests** - Analyze multiple materials at once
3. **Set appropriate TTL** - Balance freshness vs performance
4. **Monitor cache** - Check `/admin/cache/stats` regularly
5. **Clear cache after config changes** - Use `/admin/cache/clear`

---

## 📚 Documentation Links

- **Full Architecture**: `ARCHITECTURE_OVERVIEW.md`
- **Next Features**: `NEXT_MILESTONE.md`
- **Current Status**: `CURRENT_STATUS.md`
- **Recent Improvements**: `MILESTONE_IMPROVEMENTS.md`
- **API Docs**: http://localhost:8000/docs

---

## 🆘 Need Help?

1. **Check logs** - Backend prints detailed error messages
2. **Run diagnostics** - `GET /admin/diagnostics`
3. **Check health** - `GET /health`
4. **Clear cache** - Often fixes weird issues
5. **Restart Ollama** - Sometimes Ollama needs a restart

---

## 🔐 Security Notes (MVP)

⚠️ **Current State**: MVP - Not production-ready
- No authentication on admin endpoints
- API keys in `.env` file
- No rate limiting
- No input sanitization

✅ **Before Production**:
- Add JWT authentication
- Use secret manager for API keys
- Implement rate limiting
- Add input validation
- Enable HTTPS
- Add audit logging

---

## 📈 Monitoring Checklist

Daily:
- [ ] Check `/health` endpoint
- [ ] Review error logs
- [ ] Monitor cache hit rate

Weekly:
- [ ] Clear cache and rebuild
- [ ] Review performance metrics
- [ ] Update API keys if needed

Monthly:
- [ ] Review and update dependencies
- [ ] Check for security updates
- [ ] Optimize cache TTL settings

---

**Version**: 0.1.0 (MVP Enhanced)  
**Last Updated**: November 8, 2025  
**Status**: ✅ Stable & Ready

