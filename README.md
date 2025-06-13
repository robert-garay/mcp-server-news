# MCP News Server

A simple, clean, and powerful FastAPI server for retrieving news article data with advanced filtering capabilities.

## Features
- Filter news articles by:
  - Time Range (start/end dates, relative periods like last 24h, past week)
  - Source (outlet, domain, type)
  - Topic/Keywords (free-text or categories)
  - Location (country, city, region)
  - Language
  - Sentiment (positive, negative, neutral)
  - Credibility Score
  - Content Type (article, opinion, video, tweet, etc.)
  - Author
  - Engagement Metrics (views, shares, likes)
  - Custom Tags
- Elegant, extensible codebase
- Mock data for demonstration and testing

## Setup
1. **Clone the repository**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the server:**
   ```bash
   uvicorn server:app --reload
   ```

## Usage
- Access the API docs at: [http://localhost:8000/docs](http://localhost:8000/docs)
- Example request:
  ```bash
  curl 'http://localhost:8000/articles?topic=tech&sentiment=positive&relative_period=24h'
  ```
- Supports all filter parameters as query strings.

## Testing
Run the tests with:
```bash
pytest test_server.py
```

---
**MCP News Server** – for powerful, flexible news data retrieval. 