# Google Programmable Search Engine Setup

## Quick Setup

1. **Get API Key**: https://developers.google.com/custom-search/v1/overview
   - Create project in Google Cloud Console
   - Enable Custom Search API
   - Create credentials (API Key)

2. **Create Search Engine**: https://programmablesearchengine.google.com/
   - Click "Add" → "Search entire web"
   - Copy the Search Engine ID

3. **Add to `.env`**:
   ```
   GOOGLE_SEARCH_API_KEY=your_api_key_here
   GOOGLE_SEARCH_ENGINE_ID=your_engine_id_here
   ```

## How It Works

When you upload company requirements JSON:
1. System extracts industry and materials
2. Searches Google for: `"{industry} industry {materials} materials demand trends 2025"`
3. Converts search results to knowledge signals
4. Feeds enriched data to LLM

## Free Tier Limits

- 100 free searches per day
- Sufficient for MVP/testing

## Fallback

If Google Search not configured, system uses hardcoded industry trends.

