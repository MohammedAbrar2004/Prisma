# PRISMA Quick Reference Card

## 🚀 Getting Started (30 seconds)

```bash
cd backend
pip install -r requirements.txt
python test_setup.py
uvicorn main:app --reload
```

Visit: http://localhost:8000/docs

---

## 📡 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Basic health check |
| `/signals/{company_id}` | GET | Get demand signals |
| `/signals/health/check` | GET | Check API connectivity |
| `/signals/debug/mock/{company_id}` | GET | Get mock data only |
| `/docs` | GET | Interactive API docs |

---

## 💡 Common Commands

### Setup
```bash
# Install
pip install -r requirements.txt

# Configure (optional)
cp env.example .env

# Test
python test_setup.py
```

### Run
```bash
# Development (with auto-reload)
uvicorn main:app --reload

# Production
uvicorn main:app --host 0.0.0.0 --port 8000

# With specific port
uvicorn main:app --reload --port 8001
```

### Test
```bash
# Health check
curl http://localhost:8000/health

# Get signals
curl http://localhost:8000/signals/test-company

# With filters
curl "http://localhost:8000/signals/test-company?region=Maharashtra&materials=Steel,Copper"

# API health
curl http://localhost:8000/signals/health/check
```

---

## 🔑 Environment Variables

```env
# API Keys (optional)
METALPRICE_API_KEY=your_key
COMMODITY_API_KEY=your_key
WEATHER_API_KEY=your_key

# Server
HOST=0.0.0.0
PORT=8000
ENVIRONMENT=development

# Features
USE_REAL_APIS=true
```

---

## 📊 Signal Response Format

```json
{
  "company_id": "string",
  "horizon": "next_month",
  "signals": [
    {
      "region": "string",
      "material": "string",
      "demand_direction": "increase|decrease|stable",
      "demand_score": 0.82,        // 0.0 to 1.0
      "confidence": 0.85,           // 0.0 to 1.0
      "drivers": ["reason1", "..."]
    }
  ],
  "data_sources": ["mock", "commodity_api", ...]
}
```

---

## 🎯 Demand Score Interpretation

| Score | Risk Level | Action |
|-------|-----------|--------|
| 0.0-0.3 | Low | Normal |
| 0.3-0.5 | Moderate | Monitor |
| 0.5-0.7 | Elevated | Consider action |
| 0.7-0.9 | High | Take action |
| 0.9-1.0 | Critical | Urgent |

---

## 🔧 Troubleshooting

### Port Already in Use
```bash
# Use different port
uvicorn main:app --reload --port 8001

# Or kill process (Linux/Mac)
lsof -ti:8000 | xargs kill
```

### Import Errors
```bash
# Run from backend directory
cd backend
python main.py
```

### API Keys Not Working
```bash
# Test API connections
python external_signals/engine.py

# Or check via API
curl http://localhost:8000/signals/health/check
```

### Module Not Found
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Or use virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

---

## 🐍 Python Client Example

```python
import requests

class PrismaClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
    
    def get_signals(self, company_id, region=None, materials=None):
        params = {}
        if region:
            params['region'] = region
        if materials:
            params['materials'] = ','.join(materials)
        
        response = requests.get(
            f"{self.base_url}/signals/{company_id}",
            params=params
        )
        return response.json()

# Usage
client = PrismaClient()
signals = client.get_signals(
    "my-company",
    region="Maharashtra",
    materials=["Steel", "Copper"]
)
```

---

## 🌐 JavaScript Client Example

```javascript
async function getPrismaSignals(companyId, options = {}) {
  const params = new URLSearchParams(options);
  const response = await fetch(
    `http://localhost:8000/signals/${companyId}?${params}`
  );
  return response.json();
}

// Usage
const signals = await getPrismaSignals('my-company', {
  region: 'Maharashtra',
  materials: 'Steel,Copper'
});
```

---

## 📁 File Locations

| File | Location | Purpose |
|------|----------|---------|
| Main app | `backend/main.py` | FastAPI entry |
| Engine | `backend/external_signals/engine.py` | Core logic |
| Routes | `backend/routes/signals.py` | API endpoints |
| Config | `backend/.env` | Environment vars |
| Docs | `backend/README.md` | Full docs |

---

## 🔍 Useful Commands

```bash
# Test engine directly
python backend/external_signals/engine.py

# Run setup test
python backend/test_setup.py

# Format code
black backend/

# Type check
mypy backend/

# View logs with more detail
uvicorn main:app --reload --log-level debug
```

---

## 📞 Quick Links

- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health
- **API Health**: http://localhost:8000/signals/health/check

---

## 🎓 Documentation

| Doc | Link |
|-----|------|
| Main README | [README.md](README.md) |
| Setup Guide | [backend/SETUP.md](backend/SETUP.md) |
| API Guide | [backend/API_GUIDE.md](backend/API_GUIDE.md) |
| Backend Docs | [backend/README.md](backend/README.md) |
| Architecture | [functioning/Architecture read me](functioning/Architecture%20read%20me) |
| Summary | [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) |

---

## 🐛 Common Issues

**Issue**: `ModuleNotFoundError`
**Fix**: `pip install -r requirements.txt`

**Issue**: Port in use
**Fix**: Use `--port 8001` or kill process

**Issue**: API not configured
**Fix**: APIs are optional! System works with mock data

**Issue**: Import errors in routes
**Fix**: Run from `backend/` directory

**Issue**: Slow response
**Fix**: Use `?use_real_apis=false` for mock data

---

## ⚡ Quick Tips

1. **No API keys?** System works with mock data!
2. **Testing?** Use `/signals/debug/mock/{id}`
3. **Development?** Use `--reload` flag
4. **Production?** See DEPLOYMENT_CHECKLIST.md
5. **Debugging?** Check `/signals/health/check`
6. **Learning?** Visit `/docs` for interactive examples

---

## 🎯 Next Steps

1. ✅ Setup complete? → Start server
2. ✅ Server running? → Visit `/docs`
3. ✅ API working? → Try sample requests
4. ✅ Ready for more? → Add real API keys
5. 🚧 Want to extend? → Check PROJECT_SUMMARY.md

---

**Print this page for quick reference during development!** 📄

For detailed information, see [Full Documentation](README.md)

