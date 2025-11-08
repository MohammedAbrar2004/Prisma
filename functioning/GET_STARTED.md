# 🚀 Get Started with PRISMA in 5 Minutes

## Step 1: Install (1 minute)

```bash
cd backend
pip install -r requirements.txt
```

## Step 2: Test Setup (30 seconds)

```bash
python test_setup.py
```

You should see:
```
✅ All tests passed!
```

## Step 3: Start Server (10 seconds)

```bash
uvicorn main:app --reload
```

You should see:
```
🚀 PRISMA Backend Starting...
Docs available at: http://localhost:8000/docs
```

## Step 4: Try It! (1 minute)

### Option A: In Browser
1. Open: http://localhost:8000/docs
2. Click on `GET /signals/{company_id}`
3. Click "Try it out"
4. Enter: `test-company`
5. Click "Execute"
6. See the results! 🎉

### Option B: In Terminal
```bash
curl http://localhost:8000/signals/test-company
```

### Option C: In Python
```python
import requests

response = requests.get("http://localhost:8000/signals/test-company")
data = response.json()

print(f"✅ Got {len(data['signals'])} signals!")
for signal in data['signals']:
    print(f"  • {signal['material']} in {signal['region']}: {signal['demand_direction']}")
```

## Step 5: Explore (2 minutes)

### Try Different Filters

**By Region:**
```bash
curl "http://localhost:8000/signals/test-company?region=Maharashtra"
```

**By Materials:**
```bash
curl "http://localhost:8000/signals/test-company?materials=Steel,Copper"
```

**Check API Health:**
```bash
curl http://localhost:8000/signals/health/check
```

## What You Just Did

✅ Installed PRISMA backend
✅ Validated the setup
✅ Started the API server
✅ Made your first API request
✅ Got real demand signals!

## What's Working

Right now, PRISMA is using **mock data** (realistic dummy signals).

This is perfect for:
- ✅ Testing
- ✅ Development
- ✅ Demos
- ✅ Learning the API

## Want Real Data?

To get real-time signals from external APIs:

1. **Get API Keys** (all free):
   - MetalpriceAPI: https://metalpriceapi.com/
   - CommodityAPI: https://commodityapi.com/
   - WeatherAPI: https://www.weatherapi.com/

2. **Configure**:
   ```bash
   cp env.example .env
   # Edit .env and add your keys
   ```

3. **Restart Server**:
   ```bash
   uvicorn main:app --reload
   ```

That's it! 🎉

## Example Output

```json
{
  "company_id": "test-company",
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
      ]
    }
  ],
  "data_sources": ["mock"]
}
```

## Understanding the Signals

**`demand_direction`**: What's happening?
- `increase` = Demand rising → Consider ordering more
- `decrease` = Demand falling → Reduce orders
- `stable` = Normal conditions → Continue as usual

**`demand_score`**: How risky? (0.0 to 1.0)
- 0.0-0.3 = Low risk
- 0.3-0.5 = Moderate
- 0.5-0.7 = Elevated
- 0.7-0.9 = High risk
- 0.9-1.0 = Critical

**`confidence`**: How sure are we? (0.0 to 1.0)
- 0.7-1.0 = High confidence
- 0.5-0.7 = Moderate
- 0.0-0.5 = Low confidence

**`drivers`**: Why is this happening?
- Human-readable reasons
- Multiple factors considered

## Next Steps

### Learn More
- 📖 [Full Documentation](README.md)
- 🔧 [Setup Guide](backend/SETUP.md)
- 📡 [API Guide](backend/API_GUIDE.md)
- ⚡ [Quick Reference](QUICK_REFERENCE.md)

### Build More
- Add forecast engine
- Integrate LLM reasoning
- Build frontend dashboard
- Upload requirements

### Deploy
- See [Deployment Checklist](backend/DEPLOYMENT_CHECKLIST.md)
- Configure for production
- Add authentication
- Set up monitoring

## Common Issues

**"Module not found"**
```bash
pip install -r requirements.txt
```

**"Port already in use"**
```bash
uvicorn main:app --reload --port 8001
```

**"Import error"**
```bash
# Make sure you're in backend/
cd backend
python main.py
```

## Getting Help

- 🐛 Issues? Check [SETUP.md](backend/SETUP.md)
- ❓ Questions? See [API_GUIDE.md](backend/API_GUIDE.md)
- 🚀 Quick help? See [QUICK_REFERENCE.md](QUICK_REFERENCE.md)

## Success! 🎉

You now have PRISMA running!

The External Signals Engine is:
- ✅ Collecting demand signals
- ✅ Analyzing external factors
- ✅ Providing risk scores
- ✅ Ready for integration

**Happy coding!** 🚀

---

**Time to complete:** 5 minutes
**Status:** Ready to use
**Next:** Explore the API at http://localhost:8000/docs

