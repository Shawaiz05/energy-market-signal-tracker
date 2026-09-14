"""
Step 3: Historical Energy Price Data
Pulls real historical price data for European gas (Dutch TTF) and
related energy benchmarks using Yahoo Finance.
"""

import yfinance as yf
import pandas as pd

TICKERS = {
    "TTF_Gas": "TTF=F",
    "Brent_Crude": "BZ=F",
    "Nat_Gas_US": "NG=F",
}


def fetch_price_history(ticker, period="1y", interval="1d"):
    data = yf.Ticker(ticker).history(period=period, interval=interval)
    return data


def main():
    all_data = {}
    for name, ticker in TICKERS.items():
        print(f"Fetching {name} ({ticker})...")
        try:
            df = fetch_price_history(ticker)
            if df.empty:
                print(f"  No data returned for {ticker}")
                continue
            df = df[["Close"]].rename(columns={"Close": name})
            all_data[name] = df
            print(f"  Got {len(df)} days of data, latest close: {df[name].iloc[-1]:.2f}")
        except Exception as e:
            print(f"  Error fetching {ticker}: {e}")

    if not all_data:
        print("\nNo data collected. Check ticker symbols or internet connection.")
        return

    combined = pd.concat(all_data.values(), axis=1, join="outer")
    combined = combined.sort_index()
    combined.to_csv("energy_prices.csv")

    print(f"\nSaved combined price history to energy_prices.csv")
    print(f"Date range: {combined.index.min()} to {combined.index.max()}")
    print(f"\nLast 5 rows:")
    print(combined.tail())


if __name__ == "__main__":
    main()
