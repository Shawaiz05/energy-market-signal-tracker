⚡ Energy Market Signal Tracker

AI-assisted market intelligence for UK/EU energy markets, combining unstructured news signals, commodity price data, and short-term TTF gas forecasting in one interactive dashboard.

Built as a portfolio project for the Cobblestone Energy Junior Market Analyst application.

🚀 Live Demo

Streamlit App: https://energy-market-signal-tracker.streamlit.app/

GitHub: https://github.com/Shawaiz05/energy-market-signal-tracker

🎯 Project Objective

Energy markets react to a mixture of quantitative market data and rapidly changing information such as supply disruptions, weather, geopolitical developments, infrastructure events, and policy changes.

This project demonstrates a workflow for turning that unstructured information into structured market intelligence and combining it with quantitative price analysis.

The pipeline:

NewsAPI
   ↓
Raw Energy Headlines
   ↓
Google Gemini
   ↓
Structured Market Signals
   ↓
Historical Commodity Prices ──→ TTF Forecast
   ↓                              ↓
   └──────────────→ Streamlit Dashboard

🧠 What the System Does

1. Collects energy-market news

fetch_news.py uses NewsAPI to collect relevant UK/EU headlines covering areas such as:

Natural gas

Electricity / power

Emissions

Energy supply

European energy markets

The collected headlines are saved to:

raw_headlines.csv

The current development run collected 49 real articles.

2. Converts unstructured news into structured signals

structure_signals.py uses the Google Gemini API to analyse each headline and produce structured fields including:

Field

Purpose

event_type

Classifies the market event

affected_market

Identifies the affected energy market

price_direction

Bullish, bearish, or neutral

confidence

AI confidence level

reasoning

Explanation for the classification

Output:

structured_signals.csv

This demonstrates the core AI workflow:

unstructured text → structured market insight

3. Collects historical commodity prices

fetch_prices.py uses yfinance to retrieve daily market data for:

TTF Gas

Brent Crude

US Natural Gas

Output:

energy_prices.csv

The development dataset contains approximately 251 trading days of historical data.

4. Forecasts TTF gas prices

forecast.py applies Holt-Winters exponential smoothing to the TTF gas price series and generates a 7-day forecast.

Output:

forecast.csv

The development evaluation produced an MAE of approximately €0.83/MWh on TTF prices around €82/MWh.

This corresponds to roughly 1% of the price level. The metric should be interpreted as a model evaluation result, not as proof of trading profitability.

5. Interactive market dashboard

dashboard.py combines the outputs into a Streamlit application.

The dashboard includes:

Current TTF gas price

7-day price change

Bullish signal count

High-confidence signal count

TTF historical price chart

7-day forecast

Related commodity benchmarks

AI-structured market signals

Signal distribution

Event-type breakdown

TTF volatility

Cross-market correlation

AI confidence distribution

📊 Dashboard

The application is organized into four main sections:

Price & Forecast

Visualizes recent TTF gas prices alongside the 7-day Holt-Winters forecast and related commodity benchmarks.

Market Signals

Displays the AI-structured news signals with filtering by price direction.

Signal Breakdown

Shows the distribution of bullish, bearish, and neutral signals and the types of market events detected.

Market Behavior

Explores TTF volatility, relationships between TTF gas, Brent crude and US natural gas, and AI signal-confidence distribution.

🏗️ Project Structure

energy-market-signal-tracker/
│
├── dashboard.py
├── fetch_news.py
├── structure_signals.py
├── fetch_prices.py
├── forecast.py
│
├── raw_headlines.csv
├── structured_signals.csv
├── energy_prices.csv
├── forecast.csv
│
├── requirements.txt
├── .gitignore
└── README.md

⚙️ Tech Stack

Component

Technology

Language

Python 3.11

News collection

NewsAPI

AI structuring

Google Gemini

Market data

Yahoo Finance / yfinance

Forecasting

Statsmodels Holt-Winters

Data processing

Pandas, NumPy

Visualization

Plotly

Dashboard

Streamlit

Version control

Git / GitHub

🔧 Local Setup

1. Clone the repository

git clone https://github.com/Shawaiz05/energy-market-signal-tracker.git
cd energy-market-signal-tracker

2. Create a virtual environment

python3 -m venv venv
source venv/bin/activate

3. Install dependencies

pip install -r requirements.txt

4. Configure API keys

The news and AI scripts expect API keys to be supplied through environment variables rather than hard-coded into the source code.

Example:

export NEWSAPI_KEY="your_newsapi_key"
export GEMINI_API_KEY="your_gemini_api_key"

Do not commit API keys to GitHub.

5. Run the pipeline

Collect news:

python fetch_news.py

Structure the news with Gemini:

python structure_signals.py

Fetch market prices:

python fetch_prices.py

Generate the TTF forecast:

python forecast.py

Launch the dashboard:

streamlit run dashboard.py

📈 Forecasting Methodology

The forecasting component currently uses Holt-Winters exponential smoothing on historical TTF gas prices.

The model produces a short-term 7-day forecast.

The project currently reports:

TTF price level: ~€82/MWh
MAE: ~€0.83/MWh

MAE is calculated as:

MAE = mean(|actual price - predicted price|)

The reported MAE is useful for evaluating forecast error, but it should not be interpreted as a guarantee of future performance or profitability.

🔍 Why This Project Matters

The project focuses on a practical market-analyst workflow:

Unstructured information
        ↓
Information extraction
        ↓
Structured market signal
        ↓
Quantitative market data
        ↓
Forecast / market context
        ↓
Decision-support dashboard

Rather than treating news analysis and quantitative analysis as separate tasks, the system puts them into one workflow.

⚠️ Limitations

This is a research and portfolio project, not a production trading system.

Current limitations include:

News classification depends on the quality and context of the source headline.

Gemini output can contain classification errors.

NewsAPI coverage is not a complete representation of the energy-information universe.

Holt-Winters is a relatively simple time-series forecasting approach.

The current forecast does not incorporate weather, storage levels, LNG flows, pipeline flows, demand forecasts, outages, or other fundamental energy-market variables.

MAE alone does not establish trading profitability.

The current system is designed primarily for short-term market context and decision support.

These limitations provide clear directions for future development.

🔮 Future Development

Potential next steps include:

Add weather and temperature data

Add European gas storage levels

Add LNG and pipeline-flow data

Add power prices and carbon prices to forecasting

Introduce forecast confidence intervals

Compare Holt-Winters against naive and other forecasting baselines

Build a composite market-signal score

Add historical signal-performance analysis

Automate scheduled data refreshes

Add database storage instead of CSV-only persistence

Add model monitoring and evaluation over time

👨‍💻 Author

Mohammed Shawaiz Hussain

GitHub: https://github.com/Shawaiz05

📌 Disclaimer

This project is for research, educational, and portfolio purposes. It is not financial advice and does not constitute a recommendation to buy or sell any commodity, security, or derivative.
