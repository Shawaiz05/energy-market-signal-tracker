"""
Step 2: AI-Driven Signal Structuring
Uses Gemini to convert unstructured news headlines into structured
market signals: event type, region, price direction, confidence.
"""

import os
import csv
import json
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

GEMINI_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_KEY)
MODEL_NAME = "gemini-3.6-flash"

PROMPT_TEMPLATE = """You are an energy market analyst. Analyze this news headline and description, then respond with ONLY a valid JSON object (no markdown, no extra text) with these exact fields:

{{
  "event_type": "one of: supply_disruption, demand_shift, regulatory, geopolitical, weather, price_movement, other",
  "affected_market": "one of: UK_power, EU_gas, EU_power, EU_emissions, general",
  "price_direction": "one of: bullish, bearish, neutral",
  "confidence": "one of: high, medium, low",
  "reasoning": "one short sentence explaining the classification"
}}

Headline: {title}
Description: {description}
"""


def structure_article(title, description):
    """Send one article to Gemini and parse the structured response."""
    prompt = PROMPT_TEMPLATE.format(title=title, description=description or "N/A")
    try:
        response = client.models.generate_content(model=MODEL_NAME, contents=prompt)
        text = response.text.strip()
        # Strip markdown code fences if present
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        return json.loads(text.strip())
    except (json.JSONDecodeError, Exception) as e:
        print(f"  Failed to structure: {e}")
        return None


def main():
    if not GEMINI_KEY:
        print("ERROR: Set GEMINI_API_KEY in .env first.")
        return

    articles = []
    with open("raw_headlines.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        articles = list(reader)

    print(f"Loaded {len(articles)} articles. Structuring with Gemini...\n")

    structured = []
    for i, article in enumerate(articles):
        print(f"[{i+1}/{len(articles)}] {article['title'][:60]}...")
        result = structure_article(article["title"], article["description"])
        if result:
            structured.append({
                "title": article["title"],
                "source": article["source"],
                "published_at": article["published_at"],
                "url": article["url"],
                **result,
            })
            print(f"  -> {result['event_type']} | {result['price_direction']} | {result['confidence']}")
        time.sleep(1)  # be polite to the free tier rate limit

    print(f"\nSuccessfully structured {len(structured)}/{len(articles)} articles")

    with open("structured_signals.csv", "w", newline="", encoding="utf-8") as f:
        if structured:
            writer = csv.DictWriter(f, fieldnames=structured[0].keys())
            writer.writeheader()
            writer.writerows(structured)
    print("Saved to structured_signals.csv")


if __name__ == "__main__":
    main()
