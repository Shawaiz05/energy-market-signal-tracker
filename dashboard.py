"""
Step 5: Energy Market Signal Dashboard (Polished)
"""

import pandas as pd
import streamlit as st
import plotly.graph_objects as go

st.set_page_config(
    page_title="Energy Market Signal Tracker",
    layout="wide",
    page_icon="⚡"
)

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    div[data-testid="stMetric"] {
        background-color: #1c1f26;
        border: 1px solid #2a2e37;
        border-radius: 10px;
        padding: 15px;
    }
    h1 { color: #f0f0f0; }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ Energy Market Signal Tracker")
st.caption(
    "UK / EU Gas, Power & Emissions — AI-structured news signals + "
    "forecasting | Cobblestone-aligned research tool"
)
st.divider()


@st.cache_data
def load_data():
    signals = pd.read_csv("structured_signals.csv")

    prices = pd.read_csv(
        "energy_prices.csv",
        index_col=0,
        parse_dates=True
    )

    forecast = pd.read_csv(
        "forecast.csv",
        parse_dates=["date"]
    )

    # Fix mixed-timezone / plain Index issue
    prices.index = pd.to_datetime(
        prices.index,
        utc=True
    ).tz_localize(None)

    # Keep forecast dates timezone-naive too
    forecast["date"] = pd.to_datetime(
        forecast["date"],
        utc=True
    ).dt.tz_localize(None)

    return signals, prices, forecast


signals, prices, forecast = load_data()


# ============================================================
# KPI ROW
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "TTF Gas (€/MWh)",
        f"{prices['TTF_Gas'].iloc[-1]:.2f}"
    )

with col2:
    comparison_idx = -8 if len(prices) >= 8 else 0

    change = (
        prices["TTF_Gas"].iloc[-1]
        - prices["TTF_Gas"].iloc[comparison_idx]
    )

    pct = (
        change
        / prices["TTF_Gas"].iloc[comparison_idx]
    ) * 100

    st.metric(
        "7-Day Change",
        f"€{change:.2f}",
        delta=f"{pct:.1f}%"
    )

with col3:
    bullish = (
        signals["price_direction"]
        .astype(str)
        .str.lower()
        .eq("bullish")
        .sum()
    )

    st.metric(
        "Bullish Signals",
        f"{bullish}",
        delta=f"of {len(signals)} total"
    )

with col4:
    high_conf = (
        signals["confidence"]
        .astype(str)
        .str.lower()
        .eq("high")
        .sum()
    )

    st.metric(
        "High-Confidence Signals",
        f"{high_conf}"
    )


st.divider()


# ============================================================
# TABS
# ============================================================

tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Price & Forecast",
    "📰 Market Signals",
    "🔍 Signal Breakdown",
    "📊 Market Behavior"
])


# ============================================================
# TAB 1 — PRICE & FORECAST
# ============================================================

with tab1:

    fig = go.Figure()

    recent = prices["TTF_Gas"].tail(60)

    fig.add_trace(
        go.Scatter(
            x=recent.index,
            y=recent.values,
            mode="lines",
            name="TTF Gas (Actual)",
            line=dict(
                color="#00cc96",
                width=2
            )
        )
    )

    fig.add_trace(
        go.Scatter(
            x=forecast["date"],
            y=forecast["forecast_ttf_gas"],
            mode="lines+markers",
            name="7-Day Forecast",
            line=dict(
                color="#ff9f1c",
                width=2,
                dash="dash"
            )
        )
    )

    fig.update_layout(
        template="plotly_dark",
        height=450,
        xaxis_title="Date",
        yaxis_title="Price (€/MWh)",
        hovermode="x unified",
        legend=dict(
            orientation="h",
            y=1.1
        ),
        margin=dict(
            t=20,
            b=20
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        key="ttf_forecast_chart"
    )


    fig2 = go.Figure()

    for col, color in [
        ("Brent_Crude", "#636efa"),
        ("Nat_Gas_US", "#ef553b")
    ]:
        fig2.add_trace(
            go.Scatter(
                x=prices.index[-60:],
                y=prices[col].tail(60),
                mode="lines",
                name=col.replace("_", " ")
            )
        )

    fig2.update_layout(
        template="plotly_dark",
        height=300,
        title="Related Benchmarks",
        margin=dict(
            t=40,
            b=20
        )
    )

    st.plotly_chart(
        fig2,
        use_container_width=True,
        key="related_benchmarks_chart"
    )


# ============================================================
# TAB 2 — MARKET SIGNALS
# ============================================================

with tab2:

    direction_filter = st.multiselect(
        "Filter by price direction",
        options=signals["price_direction"].dropna().unique(),
        default=list(
            signals["price_direction"].dropna().unique()
        )
    )

    filtered = signals[
        signals["price_direction"].isin(direction_filter)
    ]

    for _, row in filtered.iterrows():

        direction = str(row["price_direction"]).lower()

        signal_icon = {
            "bullish": "🟢",
            "bearish": "🔴",
            "neutral": "⚪"
        }.get(
            direction,
            "⚪"
        )

        with st.container(border=True):

            st.markdown(
                f"**{signal_icon} {row['title']}**"
            )

            c1, c2, c3 = st.columns(3)

            c1.caption(
                f"Event: `{row['event_type']}`"
            )

            c2.caption(
                f"Market: `{row['affected_market']}`"
            )

            c3.caption(
                f"Confidence: `{row['confidence']}`"
            )

            st.caption(
                f"_{row['reasoning']}_"
            )


# ============================================================
# TAB 3 — SIGNAL BREAKDOWN
# ============================================================

with tab3:

    st.subheader("Signal Distribution")

    c1, c2 = st.columns(2)

    with c1:

        direction_counts = (
            signals["price_direction"]
            .value_counts()
        )

        fig3 = go.Figure(
            data=[
                go.Pie(
                    labels=direction_counts.index,
                    values=direction_counts.values,
                    hole=0.4
                )
            ]
        )

        fig3.update_layout(
            template="plotly_dark",
            height=350,
            title="By Price Direction"
        )

        st.plotly_chart(
            fig3,
            use_container_width=True,
            key="signal_direction_chart"
        )

    with c2:

        event_counts = (
            signals["event_type"]
            .value_counts()
        )

        fig4 = go.Figure(
            data=[
                go.Bar(
                    x=event_counts.values,
                    y=event_counts.index,
                    orientation="h"
                )
            ]
        )

        fig4.update_layout(
            template="plotly_dark",
            height=350,
            title="By Event Type"
        )

        st.plotly_chart(
            fig4,
            use_container_width=True,
            key="event_type_chart"
        )


# ============================================================
# TAB 4 — MARKET BEHAVIOR
# ============================================================

with tab4:

    st.subheader("How Volatile Has the Market Been?")

    st.caption(
        "Bigger swings day-to-day usually mean traders see "
        "more uncertainty ahead."
    )

    returns = (
        prices["TTF_Gas"]
        .pct_change()
        * 100
    )

    rolling_vol = returns.rolling(7).std()

    fig5 = go.Figure()

    fig5.add_trace(
        go.Scatter(
            x=prices.index[-90:],
            y=rolling_vol.tail(90),
            fill="tozeroy",
            line=dict(
                color="#ff6692"
            )
        )
    )

    fig5.update_layout(
        template="plotly_dark",
        height=300,
        yaxis_title="7-Day Volatility (%)",
        margin=dict(
            t=20,
            b=20
        )
    )

    st.plotly_chart(
        fig5,
        use_container_width=True,
        key="volatility_chart"
    )


    st.subheader("Do These Markets Move Together?")

    st.caption(
        "Values closer to 1 mean two markets tend to rise "
        "and fall together; closer to 0 means they move independently."
    )

    corr = prices[
        [
            "TTF_Gas",
            "Brent_Crude",
            "Nat_Gas_US"
        ]
    ].corr()

    fig6 = go.Figure(
        data=[
            go.Heatmap(
                z=corr.values,
                x=corr.columns,
                y=corr.columns,
                colorscale="RdYlGn",
                zmin=-1,
                zmax=1,
                text=corr.round(2).values,
                texttemplate="%{text}"
            )
        ]
    )

    fig6.update_layout(
        template="plotly_dark",
        height=350,
        margin=dict(
            t=20,
            b=20
        )
    )

    st.plotly_chart(
        fig6,
        use_container_width=True,
        key="correlation_heatmap"
    )


    st.subheader("News Confidence Over Time")

    st.caption(
        "Shows how many high vs. low-confidence signals "
        "the AI has flagged recently."
    )

    signals_copy = signals.copy()

    conf_counts = (
        signals_copy["confidence"]
        .astype(str)
        .str.lower()
        .value_counts()
        .reindex(
            ["high", "medium", "low"]
        )
        .fillna(0)
    )

    fig7 = go.Figure(
        data=[
            go.Bar(
                x=conf_counts.index,
                y=conf_counts.values,
                marker_color=[
                    "#00cc96",
                    "#ffa15a",
                    "#ef553b"
                ]
            )
        ]
    )

    fig7.update_layout(
        template="plotly_dark",
        height=300,
        yaxis_title="Number of Signals",
        margin=dict(
            t=20,
            b=20
        )
    )

    st.plotly_chart(
        fig7,
        use_container_width=True,
        key="confidence_chart"
    )


st.divider()

st.caption(
    "Data: NewsAPI, Yahoo Finance | "
    "AI structuring: Gemini | "
    "Forecast: Holt-Winters exponential smoothing | "
    "Built by Mohammed Shawaiz Hussain"
)
