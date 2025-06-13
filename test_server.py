import pytest
from fastapi.testclient import TestClient
from server import app
from datetime import datetime, timedelta

client = TestClient(app)

def test_get_articles_by_topic():
    response = client.get("/articles", params={"topic": "tech"})
    assert response.status_code == 200
    articles = response.json()
    assert any("tech" in a["topic"] for a in articles)

def test_get_articles_by_sentiment():
    response = client.get("/articles", params={"sentiment": "positive"})
    assert response.status_code == 200
    articles = response.json()
    assert all(a["sentiment"] == "positive" for a in articles)

def test_get_articles_by_relative_period():
    response = client.get("/articles", params={"relative_period": "24h"})
    assert response.status_code == 200
    articles = response.json()
    now = datetime.now().timestamp()
    for a in articles:
        published = datetime.fromisoformat(a["published_at"]).timestamp()
        assert now - published <= 24 * 3600

def test_get_articles_by_multiple_filters():
    params = {
        "topic": "tech",
        "sentiment": "positive",
        "min_credibility": 0.9,
        "location": "USA",
        "language": "en",
        "content_type": "article",
        "author": "Jane Doe",
        "min_views": 1000,
        "custom_tags": "featured"
    }
    response = client.get("/articles", params=params)
    assert response.status_code == 200
    articles = response.json()
    assert len(articles) > 0
    for a in articles:
        assert "tech" in a["topic"]
        assert a["sentiment"] == "positive"
        assert a["credibility_score"] >= 0.9
        assert a["location"] == "USA"
        assert a["language"] == "en"
        assert a["content_type"] == "article"
        assert a["author"] == "Jane Doe"
        assert a["engagement"]["views"] >= 1000
        assert "featured" in a["custom_tags"]

def test_get_articles_by_engagement_metrics():
    response = client.get("/articles", params={"min_views": 1000, "min_shares": 50, "min_likes": 200})
    assert response.status_code == 200
    articles = response.json()
    for a in articles:
        assert a["engagement"]["views"] >= 1000
        assert a["engagement"]["shares"] >= 50
        assert a["engagement"]["likes"] >= 200

def test_get_articles_by_custom_tags():
    response = client.get("/articles", params={"custom_tags": "2024"})
    assert response.status_code == 200
    articles = response.json()
    assert all("2024" in a["custom_tags"] for a in articles)

def test_get_articles_by_author():
    response = client.get("/articles", params={"author": "Jane Doe"})
    assert response.status_code == 200
    articles = response.json()
    assert all(a["author"] == "Jane Doe" for a in articles)

def test_get_articles_no_results():
    response = client.get("/articles", params={"topic": "nonexistent", "author": "nobody"})
    assert response.status_code == 200
    articles = response.json()
    assert articles == []

def test_response_structure():
    response = client.get("/articles")
    assert response.status_code == 200
    articles = response.json()
    for a in articles:
        assert set(a.keys()) == {"id", "title", "content", "source", "domain", "source_type", "topic", "location", "language", "sentiment", "credibility_score", "content_type", "author", "published_at", "engagement", "custom_tags"} 