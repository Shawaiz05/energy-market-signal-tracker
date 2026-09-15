# ⚡ Energy Market Signal Tracker

An end-to-end research tool that turns unstructured energy market news into structured, actionable trading signals — combining AI-driven text analysis with real historical price data and short-term forecasting for UK/EU gas, power, and emissions markets.

Built to demonstrate a genuine "builder" workflow: automating the manual process of reading news and estimating market direction, the same problem faced daily by energy market analysts.

## 🔍 What It Does

1. **Collects real-time market news** — pulls recent headlines on TTF gas, EEX power, UK electricity, and EU emissions from NewsAPI.
2. **Structures unstructured text with AI** — uses the Gemini API to convert each headline into structured fields: event type, affected market, likely price direction, and confidence level.
3. **Pulls real historical price data** — TTF gas, Brent Crude, and US Nat Gas benchmarks via Yahoo Finance.
4. **Forecasts short-term price movement** — a Holt-Winters exponential smoothing model projects gas prices 7 days ahead.
5. **Visualizes everything in one dashboard** — an interactive Streamlit app with price/forecast charts, a live signal feed, volatility tracking, and a market correlation heatmap.

## 🛠️ Tech Stack

- **Data collection:** Python, NewsAPI, `requests`
- **AI structuring:** Google Gemini API (`google-genai`)
- **Price data:** `yfinance` (Yahoo Finance)
- **Forecasting:** `statsmodels` (Holt-Winters Exponential Smoothing)
- **Dashboard:** Streamlit, Plotly
- **Data handling:** Pandas

## 📁 Project Structure

- `fetch_news.py` — Step 1: pull raw news headlines
- `structure_signals.py` — Step 2: AI-structure headlines into signals
- `fetch_prices.py` — Step 3: pull historical price data
- `forecast.py` — Step 4: generate price forecast
- `dashboard.py` — Step 5: interactive Streamlit dashboard
- `raw_headlines.csv` — output of step 1
- `structured_signals.csv` — output of step 2
- `energy_prices.csv` — output of step 3
- `forecast.csv` — output of step 4
- `.env` — API keys (not committed)

## 🚀 Setup & Usage

Clone and enter the project:

    git clone <your-repo-url>
    cd energy-signal-tracker

Set up environment:

    python3 -m venv venv
    source venv/bin/activate
    pip install requests python-dotenv google-genai yfinance pandas statsmodels streamlit plotly

Add your API keys:

    echo "NEWSAPI_KEY=your_key_here" >> .env
    echo "GEMINI_API_KEY=your_key_here" >> .env

Run the pipeline in order:

    python3 fetch_news.py
    python3 structure_signals.py
    python3 fetch_prices.py
    python3 forecast.py

Launch the dashboard:

    streamlit run dashboard.py

## 📊 Dashboard Highlights

- **KPI cards** — latest TTF gas price, 7-day change, bullish signal count, high-confidence signal count
- **Price & Forecast tab** — actual vs. forecast price chart, related benchmark comparison
- **Market Signals tab** — filterable, color-coded feed of AI-structured news signals with reasoning
- **Signal Breakdown tab** — distribution of signals by direction and event type
- **Market Behavior tab** — rolling volatility, cross-market correlation heatmap, signal confidence trends

## 🎯 Why This Project

Built as a demonstration of the exact "builder" workflow that modern market analysis increasingly relies on: using AI tools not just conversationally, but programmatically, as part of a real data pipeline, to convert noisy, unstructured information into a decision-ready format, then validating and visualizing it responsibly.

## 👤 Author

**Mohammed Shawaiz Hussain**

[Portfolio](https://shawaiz05.github.io) · [GitHub](https://github.com/Shawaiz05) · [LinkedIn](https://www.linkedin.com/in/mohammed-shawaiz-hussain-4a12a32aa)
