# PRISMA LLM - Quick Start Guide

## 🚀 Get Up and Running in 5 Minutes

This guide helps you quickly set up and test the LLM reasoning layer.

## Step 1: Install Ollama

### Windows
```powershell
# Download and run installer from:
https://ollama.ai/download/windows

# Or use winget
winget install Ollama.Ollama
```

### Mac/Linux
```bash
curl https://ollama.ai/install.sh | sh
```

## Step 2: Pull llama3 Model

```bash
# Pull the model (this may take a few minutes)
ollama pull llama3

# Verify it's available
ollama list
```

## Step 3: Start Ollama Server

```bash
# Start Ollama (keep this running in a terminal)
ollama serve
```

**Note**: On Windows, Ollama may start automatically as a service.

## Step 4: Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

## Step 5: Start FastAPI Server

```bash
# From the backend directory
uvicorn main:app --reload --port 8000
```

Server will be available at: http://localhost:8000

## Step 6: Test the Implementation

### Option A: Web Interface (Recommended)

1. Open browser: http://localhost:8000/docs
2. Find the `/analyze` endpoint
3. Click "Try it out"
4. Use this sample request:

```json
{
  "company_id": "abc-infra",
  "materials": ["Steel", "Copper"],
  "industry": "construction",
  "use_real_apis": false
}
```

5. Click "Execute"
6. Wait 30-60 seconds for LLM to process
7. View the AI-generated recommendations!

### Option B: Command Line

```bash
# Quick health check
curl http://localhost:8000/analyze/health

# Full analysis request
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "company_id": "abc-infra",
    "materials": ["Steel"],
    "question": "Should we increase steel procurement?",
    "industry": "construction"
  }'
```

### Option C: Run Test Suites

```bash
# Run all tests at once
python test_analyze_basic.py && \
python test_analyze_edge_cases.py && \
python test_analyze_error_handling.py && \
python test_llm_mock_vs_real.py && \
python test_industry_search.py

# Or run individually
python test_analyze_basic.py
```

## 🎯 Expected Results

### Successful Analysis Response

You should see output like this:

```json
{
  "company_id": "abc-infra",
  "summary": "Based on the forecasted demand and external signals, Steel shows the strongest indicators for procurement attention. Current forecasts predict a 10% increase in Steel demand for Maharashtra Power Plant Phase 2, while external signals indicate rising prices and increasing market demand. Copper demand is also growing but at a more moderate pace.",
  "recommended_actions": [
    {
      "material": "Steel",
      "action": "Increase procurement and inventory levels by 15-20%",
      "reason": "Strong demand growth forecast combined with upward price pressure and multiple infrastructure projects requiring steel"
    },
    {
      "material": "Copper",
      "action": "Monitor closely and consider forward contracts",
      "reason": "Moderate demand increase with stable pricing, but potential for supply tightness"
    }
  ],
  "risks": [
    {
      "material": "Steel",
      "risk_level": "medium",
      "drivers": [
        "Price volatility in commodity markets",
        "Supply chain constraints",
        "Weather disruptions in Maharashtra region"
      ]
    }
  ],
  "watchlist_materials": [
    {
      "material": "Concrete",
      "reason": "Steady demand across multiple projects, monitor for capacity constraints"
    }
  ],
  "data_sources": ["mock", "industry_intelligence"],
  "generated_at": "2025-11-08T10:30:00",
  "horizon": "next_month",
  "region": null,
  "industry": "construction"
}
```

## 🔍 Verify Everything is Working

### 1. Check Ollama
```bash
curl http://localhost:11434/api/tags
# Should return list of models including llama3
```

### 2. Check FastAPI Server
```bash
curl http://localhost:8000/health
# Should return: {"status": "healthy", ...}
```

### 3. Check LLM Integration
```bash
curl http://localhost:8000/analyze/health
# Should show ollama status: "connected"
```

### 4. Check Industry Intelligence
```bash
python -c "from search.industry import get_available_industries; print(get_available_industries())"
# Should return: ['construction', 'infrastructure', 'manufacturing', 'energy', 'general']
```

## 🐛 Common Issues & Fixes

### Issue 1: Ollama Not Found

**Error**: `ConnectionError: LLM service unavailable`

**Fix**:
```bash
# Verify Ollama is running
curl http://localhost:11434/api/tags

# If not running, start it
ollama serve
```

### Issue 2: Model Not Available

**Error**: `Ollama connected but model llama3 not found`

**Fix**:
```bash
ollama pull llama3
ollama list  # Verify it appears
```

### Issue 3: Port Already in Use

**Error**: `Address already in use: 8000`

**Fix**:
```bash
# Use a different port
uvicorn main:app --reload --port 8001

# Or kill the process using port 8000
# Windows: netstat -ano | findstr :8000
# Linux/Mac: lsof -ti:8000 | xargs kill
```

### Issue 4: Slow Response

**Symptom**: Analysis takes > 2 minutes

**Fixes**:
1. Normal for first request (model loading)
2. Subsequent requests should be faster
3. Check your CPU/RAM (Ollama needs resources)
4. Try a smaller model: `ollama pull llama3:8b`

### Issue 5: Import Errors

**Error**: `ModuleNotFoundError: No module named 'llm'`

**Fix**:
```bash
# Make sure you're in the backend directory
cd backend

# Verify __init__.py files exist
ls llm/__init__.py
ls search/__init__.py

# Re-run from backend directory
python test_analyze_basic.py
```

## 📊 Test Scenarios to Try

### Scenario 1: Basic Analysis
```json
{
  "company_id": "abc-infra"
}
```

### Scenario 2: Material-Specific
```json
{
  "company_id": "abc-infra",
  "materials": ["Steel"]
}
```

### Scenario 3: With Question
```json
{
  "company_id": "abc-infra",
  "question": "What are the biggest risks to our steel supply chain?"
}
```

### Scenario 4: Regional Focus
```json
{
  "company_id": "abc-infra",
  "region": "Maharashtra",
  "materials": ["Steel", "Concrete"]
}
```

### Scenario 5: Industry Context
```json
{
  "company_id": "abc-infra",
  "industry": "construction",
  "question": "How do industry trends affect our procurement strategy?"
}
```

### Scenario 6: Full Analysis
```json
{
  "company_id": "abc-infra",
  "question": "Provide comprehensive procurement recommendations",
  "region": "Maharashtra",
  "materials": ["Steel", "Copper", "Concrete"],
  "industry": "infrastructure",
  "horizon": "next_quarter"
}
```

## 🎓 Understanding the Output

### Summary
- Concise 2-3 sentence overview
- Key insights and priorities
- Based on all provided data

### Recommended Actions
- Specific, actionable steps
- Per-material recommendations
- Justified by data (not hallucinated)

### Risks
- Risk level: low, medium, or high
- Specific drivers from signals
- Material-specific concerns

### Watchlist Materials
- Materials needing monitoring
- Not urgent but important
- Reason for watching

## 🚦 Next Steps

### Learn More
- Read `LLM_IMPLEMENTATION.md` for detailed architecture
- Explore `backend/llm/engine.py` for LLM logic
- Check `backend/search/industry.py` for industry intelligence

### Customize
- Add your own industry trends in `search/industry.py`
- Modify prompt in `llm/engine.py` -> `build_prisma_prompt()`
- Adjust LLM settings in `.env`

### Deploy
- See `DEPLOYMENT_CHECKLIST.md` for production setup
- Configure authentication
- Set up monitoring
- Add caching layer

## 📞 Need Help?

### Check Logs
```bash
# FastAPI logs show in terminal where server is running
# Look for errors or warnings

# Test with verbose output
python test_analyze_basic.py 2>&1 | tee test_output.log
```

### Health Checks
```bash
# Overall system
curl http://localhost:8000/health

# Analysis service
curl http://localhost:8000/analyze/health

# Signals service
curl http://localhost:8000/signals/health/check
```

### Debug Mode
```python
# In llm/config.py, add:
import logging
logging.basicConfig(level=logging.DEBUG)
```

## ✅ Success Checklist

- [ ] Ollama installed and running
- [ ] llama3 model downloaded
- [ ] Python dependencies installed
- [ ] FastAPI server started
- [ ] `/analyze/health` returns "connected"
- [ ] Test request returns valid JSON
- [ ] Summary contains material analysis
- [ ] Response time < 60 seconds
- [ ] All 5 test files pass

---

**You're ready to use PRISMA's AI-powered procurement recommendations!** 🎉

**Estimated Setup Time**: 5-10 minutes
**First Request Time**: 30-60 seconds (LLM processing)
**Subsequent Requests**: 20-40 seconds

