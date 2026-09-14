"""
Step 1: Energy Market News Fetcher
Pulls recent headlines on UK/EU gas, power, and emissions markets from NewsAPI.
"""

import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("NEWSAPI_KEY")
BASE_URL = "https://newsapi.org/v2/everything"

KEYWORDS = [
    "TTF gas price",
    "EEX power price",
    "UK electricity market",
    "EU emissions trading",
    "European gas storage",
    "UK power grid",
]


def fetch_headlines(query, days_back=7, page_size=10):
    from_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")
    params = {
        "q": query,
        "from": from_date,
        "sortBy": "publishedAt",
        "language": "en",
        "pageSize": page_size,
        "apiKey": API_KEY,
    }
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    return response.json().get("articles", [])


def main():
    if not API_KEY:
        print("ERROR: Set NEWSAPI_KEY in a .env file first.")
        return

    all_articles = []
    for keyword in KEYWORDS:
        print(f"\nFetching: '{keyword}'...")
        try:
            articles = fetch_headlines(keyword)
            print(f"  Found {len(articles)} articles")
            for a in articles:
                all_articles.append({
                    "keyword": keyword,
                    "title": a["title"],
                    "description": a["description"],
                    "source": a["source"]["name"],
                    "published_at": a["publishedAt"],
                    "url": a["url"],
                })
        except requests.exceptions.RequestException as e:
            print(f"  Error fetching '{keyword}': {e}")

    print(f"\nTotal articles collected: {len(all_articles)}\n")

    for article in all_articles[:5]:
        print(f"[{article['keyword']}] {article['title']}")
        print(f"  Source: {article['source']} | {article['published_at']}\n")

    import csv
    with open("raw_headlines.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["keyword", "title", "description", "source", "published_at", "url"])
        writer.writeheader()
        writer.writerows(all_articles)
    print(f"Saved {len(all_articles)} articles to raw_headlines.csv")


if __name__ == "__main__":
    main()
