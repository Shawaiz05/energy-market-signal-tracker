"""
Step 4: Forecasting Model
Builds a simple time-series forecast on TTF gas prices using
exponential smoothing (Holt-Winters) - a solid, explainable baseline.
"""

import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing


def load_price_data(path="energy_prices.csv"):
    df = pd.read_csv(path, index_col=0, parse_dates=True)
    return df


def forecast_series(series, periods=7):
    series = series.dropna().copy()
    # Normalize to UTC then strip timezone, then set a clean daily frequency
    idx = pd.to_datetime(series.index, utc=True).tz_localize(None)
    series.index = idx
    series = series[~series.index.duplicated(keep="last")]
    series = series.asfreq("D").ffill()

    model = ExponentialSmoothing(
        series,
        trend="add",
        seasonal=None,
        initialization_method="estimated",
    )
    fitted = model.fit()
    forecast = fitted.forecast(periods)
    return fitted, forecast


def main():
    df = load_price_data()
    ttf = df["TTF_Gas"]

    print(f"Loaded {len(ttf)} days of TTF gas price data")
    print(f"Current price: {ttf.iloc[-1]:.2f}")
    print(f"7-day price change: {ttf.iloc[-1] - ttf.iloc[-8]:.2f}\n")

    fitted, forecast = forecast_series(ttf, periods=7)

    print("7-day forecast:")
    for date, value in forecast.items():
        print(f"  {date.strftime('%Y-%m-%d')}: {value:.2f}")

    mae = (fitted.fittedvalues - fitted.model.endog).__abs__().mean()
    print(f"\nModel fit (Mean Absolute Error on training data): {mae:.2f}")

    forecast_df = forecast.reset_index()
    forecast_df.columns = ["date", "forecast_ttf_gas"]
    forecast_df.to_csv("forecast.csv", index=False)
    print("\nSaved forecast to forecast.csv")


if __name__ == "__main__":
    main()
