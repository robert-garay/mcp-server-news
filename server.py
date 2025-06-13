from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum
import requests
import os
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
NEWS_API_URL = "https://newsapi.org/v2/everything"

app = FastAPI(title="MCP News Server", description="Retrieve news articles with powerful filtering.")

class Sentiment(str, Enum):
    positive = "positive"
    negative = "negative"
    neutral = "neutral"

class ContentType(str, Enum):
    article = "article"
    opinion = "opinion"
    video = "video"
    tweet = "tweet"

class NewsArticle(BaseModel):
    id: str
    title: str
    content: Optional[str]
    source: str
    domain: Optional[str]
    source_type: Optional[str]
    topic: Optional[List[str]]
    location: Optional[str]
    language: Optional[str]
    sentiment: Optional[Sentiment]
    credibility_score: Optional[float]
    content_type: Optional[ContentType]
    author: Optional[str]
    published_at: datetime
    engagement: Optional[dict]
    custom_tags: Optional[List[str]] = Field(default_factory=list)


def map_newsapi_to_article(article: dict) -> NewsArticle:
    return NewsArticle(
        id=article.get("url", ""),
        title=article.get("title", ""),
        content=article.get("content"),
        source=article.get("source", {}).get("name", ""),
        domain=None,  # NewsAPI does not provide domain directly
        source_type=None,
        topic=None,
        location=None,
        language=None,
        sentiment=None,
        credibility_score=None,
        content_type=ContentType.article,
        author=article.get("author"),
        published_at=datetime.fromisoformat(article.get("publishedAt", "1970-01-01T00:00:00Z").replace("Z", "+00:00")),
        engagement=None,
        custom_tags=[]
    )

@app.get("/articles", response_model=List[NewsArticle])
def get_articles(
    start_date: Optional[datetime] = Query(None, description="Start of time range"),
    end_date: Optional[datetime] = Query(None, description="End of time range"),
    source: Optional[str] = None,
    domain: Optional[str] = None,
    topic: Optional[List[str]] = Query(None),
    language: Optional[str] = None,
    author: Optional[str] = None,
    q: Optional[str] = Query(None, description="Free-text search"),
    page_size: int = 20,
    page: int = 1,
):
    if not NEWS_API_KEY:
        raise HTTPException(status_code=500, detail="NewsAPI key not configured.")
    params = {
        "apiKey": NEWS_API_KEY,
        "pageSize": page_size,
        "page": page,
    }
    if q:
        params["q"] = q
    if topic:
        params["q"] = " ".join(topic) if not q else f"{q} {' '.join(topic)}"
    if language:
        params["language"] = language
    if source:
        params["sources"] = source
    if author:
        params["q"] = f"{params.get('q', '')} {author}".strip()
    if start_date:
        params["from"] = start_date.isoformat()
    if end_date:
        params["to"] = end_date.isoformat()
    # NewsAPI does not support domain, location, sentiment, credibility, engagement, custom_tags, or content_type
    try:
        response = requests.get(NEWS_API_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data.get("status") != "ok":
            raise HTTPException(status_code=502, detail=f"NewsAPI error: {data.get('message', 'Unknown error')}")
        articles = [map_newsapi_to_article(a) for a in data.get("articles", [])]
        return articles
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=f"NewsAPI request failed: {str(e)}") 