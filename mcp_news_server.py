import os
import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
NEWS_API_URL = "https://newsapi.org/v2/everything"

mcp = FastMCP("MCP News Server")

class NewsArticle(BaseModel):
    id: str
    title: str
    content: Optional[str]
    source: str
    domain: Optional[str]
    author: Optional[str]
    published_at: datetime
    url: str
    language: Optional[str]
    description: Optional[str]

class NewsSearchParams(BaseModel):
    q: Optional[str] = Field(None, description="Free-text search or keywords")
    topic: Optional[List[str]] = Field(None, description="List of topics/keywords")
    language: Optional[str] = Field(None, description="Content language (e.g., en, es)")
    source: Optional[str] = Field(None, description="Specific news source ID")
    author: Optional[str] = Field(None, description="Author name")
    start_date: Optional[datetime] = Field(None, description="Start of time range")
    end_date: Optional[datetime] = Field(None, description="End of time range")
    page_size: int = Field(10, description="Number of results per page")
    page: int = Field(1, description="Page number")

@mcp.tool(name="news.search", description="Search for news articles using NewsAPI.org with advanced filters.")
async def search_news(params: NewsSearchParams) -> List[NewsArticle]:
    if not NEWS_API_KEY:
        raise RuntimeError("NEWS_API_KEY not set in environment.")
    query = params.q or ""
    if params.topic:
        query = f"{query} {' '.join(params.topic)}".strip()
    api_params = {
        "apiKey": NEWS_API_KEY,
        "q": query or None,
        "language": params.language,
        "sources": params.source,
        "from": params.start_date.isoformat() if params.start_date else None,
        "to": params.end_date.isoformat() if params.end_date else None,
        "pageSize": params.page_size,
        "page": params.page,
    }
    # Remove None values
    api_params = {k: v for k, v in api_params.items() if v is not None}
    async with httpx.AsyncClient() as client:
        resp = await client.get(NEWS_API_URL, params=api_params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if data.get("status") != "ok":
            raise RuntimeError(f"NewsAPI error: {data.get('message', 'Unknown error')}")
        articles = []
        for a in data.get("articles", []):
            articles.append(NewsArticle(
                id=a.get("url", ""),
                title=a.get("title", ""),
                content=a.get("content"),
                source=a.get("source", {}).get("name", ""),
                domain=None,
                author=a.get("author"),
                published_at=datetime.fromisoformat(a.get("publishedAt", "1970-01-01T00:00:00Z").replace("Z", "+00:00")),
                url=a.get("url", ""),
                language=params.language,
                description=a.get("description"),
            ))
        return articles

if __name__ == "__main__":
    mcp.run() 