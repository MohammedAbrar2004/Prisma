# PRISMA - Predictive Resource Intelligence & Supply-chain Management using AI

<div align="center">

**An intelligent decision-support platform for material demand forecasting and procurement optimization**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

[Features](#-features) • [Quick Start](#-quick-start) • [Documentation](#-documentation) • [Architecture](#-architecture) • [Contributing](#-contributing)

</div>

---

## 🎯 Problem Statement

Large-scale, project-based organizations (infrastructure, power, construction, manufacturing) face critical challenges:

- **Uncertain material demand** - Dynamic project requirements
- **Fragmented data** - Silos across departments
- **Volatile external factors** - Price swings, weather, logistics disruptions
- **Limited visibility** - Why are we short on materials? Why overstocked?

Traditional ERP systems:
- ❌ Rely on historical averages
- ❌ Don't adapt to external signals
- ❌ Offer no transparency into recommendations

**Result:** Project delays, capital locked in inventory, reactive decision-making

---

## 💡 PRISMA Solution

PRISMA combines **traditional forecasting**, **external intelligence**, and **AI reasoning** to provide:

✅ **Demand Forecasting** - ML-powered predictions
✅ **External Signal Analysis** - Real-time price, weather, infrastructure data
✅ **Smart Recommendations** - AI-explained procurement suggestions
✅ **Risk Assessment** - Proactive identification of supply chain risks
✅ **Explainability** - Clear reasoning behind every recommendation

---

## 🏗️ Architecture

PRISMA follows a clean, modular architecture:

```
┌─────────────────┐
│  Frontend UI    │  ← Dashboard, visualizations
│  (Dashboard)    │
└────────┬────────┘
         │
         ↓
┌────────────────────────────────────────────┐
│         FastAPI Backend (REST API)         │
├────────────────────────────────────────────┤
│                                            │
│  ┌──────────────┐  ┌──────────────┐       │
│  │ Requirements │  │   Forecast   │       │
│  │    Parser    │→ │    Engine    │       │
│  └──────────────┘  └──────┬───────┘       │
│                           │               │
│                           ↓               │
│                  ┌──────────────┐         │
│                  │   External   │         │
│                  │   Signals    │  ← 🔥 IMPLEMENTED
│                  │    Engine    │         │
│                  └──────┬───────┘         │
│                         │                 │
│     Requirements + Forecasts + Signals    │
│                         │                 │
│                         ↓                 │
│                  ┌──────────────┐         │
│                  │     LLM      │         │
│                  │  Reasoning   │         │
│                  │   (Ollama)   │         │
│                  └──────────────┘         │
│                                            │
└────────────────────────────────────────────┘
```

### Data Sources

PRISMA integrates with multiple external APIs:

- **MetalpriceAPI** - Metal/commodity prices
- **CommodityAPI** - Broader commodity tracking
- **WeatherAPI** - Regional weather forecasts
- **World Bank API** - Economic indicators

---

## 🚀 Features

### ✅ Implemented (v0.1.0)

#### External Signals Engine
- ✅ Real-time commodity price tracking
- ✅ Weather impact analysis
- ✅ Infrastructure activity monitoring
- ✅ Multi-source signal aggregation
- ✅ Mock data fallback (works without API keys)
- ✅ RESTful API with FastAPI
- ✅ Interactive API documentation
- ✅ Region and material filtering
- ✅ Health check endpoints

### 🚧 Coming Soon

- [ ] **Forecast Engine** - ML-powered demand predictions
- [ ] **LLM Reasoning** - AI recommendations via Ollama
- [ ] **Requirements Upload** - CSV/Excel parsing
- [ ] **Frontend Dashboard** - React/Next.js UI
- [ ] **Authentication** - API keys / JWT
- [ ] **Database** - PostgreSQL integration
- [ ] **Caching** - Redis for performance

---

## 📦 Quick Start

### Prerequisites

- Python 3.10+
- pip

### Installation

```bash
# Clone the repository
git clone <repo-url>
cd prisma

# Navigate to backend
cd backend

# Install dependencies
pip install -r requirements.txt

# Configure environment (optional - works without API keys)
cp env.example .env
# Edit .env and add your API keys

# Test the setup
python test_setup.py
```

### Run the Server

```bash
# Start the FastAPI server
uvicorn main:app --reload --port 8000
```

Server will be available at: **http://localhost:8000**

### Test the API

**Option 1: Interactive Docs**
- Visit: http://localhost:8000/docs
- Try the `/signals/{company_id}` endpoint

**Option 2: curl**
```bash
# Get signals for a company
curl http://localhost:8000/signals/test-company

# Filter by region
curl "http://localhost:8000/signals/test-company?region=Maharashtra"

# Check API health
curl http://localhost:8000/signals/health/check
```

**Option 3: Python**
```python
import requests

response = requests.get("http://localhost:8000/signals/test-company")
data = response.json()

print(f"Got {len(data['signals'])} signals")
for signal in data['signals']:
    print(f"{signal['material']}: {signal['demand_direction']} "
          f"(risk: {signal['demand_score']:.2f})")
```

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [Backend README](backend/README.md) | Complete backend documentation |
| [Setup Guide](backend/SETUP.md) | Step-by-step setup instructions |
| [API Guide](backend/API_GUIDE.md) | API usage with examples |
| [Architecture](functioning/Architecture%20read%20me) | System design details |
| [Project Summary](PROJECT_SUMMARY.md) | Implementation overview |
| [Deployment Checklist](backend/DEPLOYMENT_CHECKLIST.md) | Production deployment guide |

---

## 🔌 API Overview

### Get External Signals

**Endpoint:** `GET /signals/{company_id}`

Returns demand risk signals based on external data sources.

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

### Check API Health

**Endpoint:** `GET /signals/health/check`

Returns connectivity status for all external APIs.

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

---

## 🗂️ Project Structure

```
prisma/
├── README.md                        # This file
├── PROJECT_SUMMARY.md              # Implementation details
│
├── functioning/                     # Design documents
│   ├── musi                        # Main PRISMA overview
│   └── Architecture read me        # Architecture guide
│
└── backend/                         # Backend implementation
    ├── main.py                     # FastAPI entry point
    ├── requirements.txt            # Python dependencies
    ├── env.example                 # Configuration template
    ├── test_setup.py              # Setup validation script
    │
    ├── README.md                   # Backend docs
    ├── SETUP.md                    # Setup guide
    ├── API_GUIDE.md               # API documentation
    ├── DEPLOYMENT_CHECKLIST.md    # Deployment guide
    │
    ├── external_signals/           # 🔥 External Signals Engine
    │   ├── __init__.py
    │   └── engine.py              # Core logic (706 lines)
    │
    ├── routes/                     # API endpoints
    │   ├── __init__.py
    │   └── signals.py             # Signals API
    │
    ├── data/                       # Sample/mock data
    │   ├── mock_requirements.json
    │   └── mock_forecasts.json
    │
    └── [future]
        ├── forecast/               # Forecasting engine
        ├── llm/                   # LLM reasoning
        └── models/                # Shared schemas
```

---

## 🔑 API Keys (Optional)

PRISMA works with mock data out of the box. For real-time signals, get these free API keys:

1. **MetalpriceAPI** - https://metalpriceapi.com/
   - Free: 100 requests/month
   - Tracks metal prices

2. **CommodityAPI** - https://commodityapi.com/
   - Free trial available
   - 130+ commodities

3. **WeatherAPI** - https://www.weatherapi.com/
   - Free: 1M requests/month
   - Regional weather data

4. **World Bank API** - No key needed (public API)
   - Economic indicators

Add keys to `.env` file:
```env
METALPRICE_API_KEY=your_key_here
COMMODITY_API_KEY=your_key_here
WEATHER_API_KEY=your_key_here
```

---

## 🎨 Frontend (Coming Soon)

The frontend dashboard will provide:

- 📊 **Signal Visualization** - Charts and risk indicators
- 📈 **Forecast Display** - Material demand predictions
- 💡 **Recommendations** - AI-powered procurement suggestions
- 🔍 **Drill-down Analysis** - Detailed signal drivers
- 📱 **Responsive Design** - Mobile-friendly

Planned tech stack: React/Next.js + TailwindCSS

---

## 🧪 Testing

### Automated Setup Test
```bash
cd backend
python test_setup.py
```

### Manual Testing
```bash
# Test engine directly
python external_signals/engine.py

# Start server and test
uvicorn main:app --reload
curl http://localhost:8000/signals/test-company
```

### Interactive Testing
Visit http://localhost:8000/docs for Swagger UI

---

## 🛠️ Development

### Install Development Dependencies
```bash
pip install -r requirements.txt
```

### Code Quality Tools
```bash
# Format code
black .

# Lint
flake8 .

# Type check
mypy .
```

### Running with Auto-reload
```bash
uvicorn main:app --reload --log-level debug
```

---

## 🤝 Contributing

We welcome contributions! Here's how:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Contribution Guidelines

- Follow existing code style
- Add tests for new features
- Update documentation
- Keep commits atomic and well-described

---

## 📊 Performance

### Current Performance (v0.1.0)

- **Mock Data Mode**: < 50ms response time
- **With APIs**: 1-3 seconds (parallel requests)
- **Throughput**: Limited by external API rate limits

### Optimization Roadmap

- [ ] Implement Redis caching (target: < 100ms with cache)
- [ ] Async API calls
- [ ] Database for historical signals
- [ ] CDN for static assets

---

## 🔐 Security

- ✅ Environment-based configuration
- ✅ No secrets in code
- ✅ Input validation via Pydantic
- 🚧 Authentication (coming soon)
- 🚧 Rate limiting (coming soon)
- 🚧 HTTPS in production (deployment)

---

## 📱 Deployment

See [DEPLOYMENT_CHECKLIST.md](backend/DEPLOYMENT_CHECKLIST.md) for production deployment guide.

### Quick Deploy Options

**Docker** (coming soon)
```bash
docker-compose up
```

**Heroku** (coming soon)
```bash
git push heroku main
```

**AWS/GCP/Azure** - See deployment docs

---

## 🎓 Learn More

### Documentation
- [Architecture Overview](functioning/Architecture%20read%20me)
- [API Documentation](backend/API_GUIDE.md)
- [Implementation Details](PROJECT_SUMMARY.md)

### External Resources
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Pydantic Docs](https://docs.pydantic.dev/)
- [Ollama](https://ollama.ai/) (for LLM integration)

---

## 🗺️ Roadmap

### v0.1.0 (Current) ✅
- External Signals Engine
- REST API
- Basic documentation

### v0.2.0 (Next)
- Forecast Engine
- Requirements Upload
- Database integration

### v0.3.0
- LLM Reasoning Layer
- Ollama integration
- Recommendation engine

### v0.4.0
- Frontend Dashboard
- Authentication
- Production deployment

### v1.0.0
- Full feature set
- Production-ready
- Comprehensive testing

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- FastAPI team for the amazing framework
- MetalpriceAPI, CommodityAPI, WeatherAPI for data access
- World Bank for open data
- Ollama for local LLM support

---

## 📞 Support

- 📧 Email: [your-email]
- 🐛 Issues: [GitHub Issues](issues)
- 💬 Discussions: [GitHub Discussions](discussions)
- 📚 Docs: [Documentation](backend/README.md)

---

## 🌟 Star History

If you find PRISMA useful, please consider giving it a star! ⭐

---

<div align="center">

**Built with ❤️ for smarter supply chain management**

[Get Started](#-quick-start) • [Read Docs](#-documentation) • [View Demo](#) • [Report Bug](#)

</div>

