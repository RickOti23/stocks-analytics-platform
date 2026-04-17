import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from queries import get_ticker_data, get_correlation_data

# ── FULL UNIVERSE ────────────────────────────────────────
TICKERS = [
    "AAPL", "MSFT", "GOOGL", "META", "AMZN", "TSLA", "NVDA", "INTC", "AMD", "CSCO",
    "JPM", "BAC", "GS", "WFC", "MS", "JNJ", "PFE", "MRK", "UNH", "ABT",
    "HD", "NKE", "MCD", "SBUX", "LOW", "PG", "KO", "PEP", "WMT", "COST",
    "GE", "CAT", "BA", "UPS", "DE", "XOM", "CVX", "NEE", "DUK", "SLB",
    "NFLX", "PYPL", "ADBE", "CRM", "TMUS", "ORCL", "IBM", "QCOM", "INTU", "TXN","FX"
]


# ── DATA LOADERS ────────────────────────────────────────

@st.cache_data(ttl=3600)
def load_ticker(ticker: str, days: int):
    return get_ticker_data(ticker, days)


@st.cache_data(ttl=3600)
def load_correlations():
    return get_correlation_data()


# ── UI CONFIG ───────────────────────────────────────────

st.set_page_config(page_title="Stock Analytics", layout="wide")
st.title("Stock Analytics Dashboard")

col1, col2 = st.columns([2, 2])

with col1:
    ticker = st.selectbox("Select Ticker", TICKERS)

with col2:
    days = st.selectbox("Window", [90, 180, 365], index=2, format_func=lambda x: f"{x}d")


# ── LOAD DATA ───────────────────────────────────────────

df = load_ticker(ticker, days)

if df.empty:
    st.warning("No data found.")
    st.stop()

latest = df.iloc[-1]


# ── METRICS ─────────────────────────────────────────────

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("Close", f"${latest.close:.2f}")
c2.metric("Daily return", f"{latest.daily_return_pct:.2f}%")
c3.metric("RSI (14)", f"{latest.rsi_14:.1f}", delta=latest.rsi_signal)
c4.metric("Vol 7D", f"{latest.vol_7d_ann:.1f}%")
c5.metric("BB signal", latest.bb_signal)


# ── PRICE + MOVING AVERAGES ─────────────────────────────

st.subheader("Price & Moving Averages")

fig_ma = go.Figure()

fig_ma.add_trace(go.Scatter(x=df.trade_date, y=df.close, name="Close"))
fig_ma.add_trace(go.Scatter(x=df.trade_date, y=df.ma_7, name="MA 7"))
fig_ma.add_trace(go.Scatter(x=df.trade_date, y=df.ma_30, name="MA 30"))
fig_ma.add_trace(go.Scatter(x=df.trade_date, y=df.ma_200, name="MA 200"))

fig_ma.update_layout(height=350, margin=dict(t=10, b=10))

st.plotly_chart(fig_ma, use_container_width=True)

# ── DAILY RETURNS ───────────────────────────────────────

st.subheader("Daily Returns")

colors = ["green" if x >= 0 else "red" for x in df.daily_return_pct]

fig_ret = go.Figure()
fig_ret.add_trace(go.Bar(x=df.trade_date, y=df.daily_return_pct, marker_color=colors))

st.plotly_chart(fig_ret, use_container_width=True)


# ── BOLLINGER BANDS ─────────────────────────────────────

st.subheader("Bollinger Bands")

fig_bb = go.Figure()

fig_bb.add_trace(go.Scatter(x=df.trade_date, y=df.bb_upper, name="Upper"))
fig_bb.add_trace(go.Scatter(x=df.trade_date, y=df.bb_middle, name="Middle"))
fig_bb.add_trace(go.Scatter(x=df.trade_date, y=df.bb_lower, name="Lower", fill="tonexty"))
fig_bb.add_trace(go.Scatter(x=df.trade_date, y=df.close, name="Close"))

fig_bb.update_layout(height=300, margin=dict(t=10, b=10))

st.plotly_chart(fig_bb, use_container_width=True)


# ── RSI + VOLATILITY ────────────────────────────────────

col_rsi, col_vol = st.columns(2)

with col_rsi:
    st.subheader("RSI (14)")
    fig_rsi = go.Figure()
    fig_rsi.add_trace(go.Scatter(x=df.trade_date, y=df.rsi_14, name="RSI"))
    fig_rsi.update_yaxes(range=[0, 100])
    fig_rsi.update_layout(height=280)
    st.plotly_chart(fig_rsi, use_container_width=True)

with col_vol:
    st.subheader("Volatility")
    fig_vol = go.Figure()
    fig_vol.add_trace(go.Scatter(x=df.trade_date, y=df.vol_7d_ann, name="7D Vol"))
    fig_vol.add_trace(go.Scatter(x=df.trade_date, y=df.vol_30d_ann, name="30D Vol"))
    fig_vol.update_layout(height=280)
    st.plotly_chart(fig_vol, use_container_width=True)


# ── CORRELATION HEATMAP (FULLY DYNAMIC) ────────────────

st.subheader("30-Day Correlation Matrix")

corr_df = load_correlations()

if not corr_df.empty:
    row = corr_df.iloc[0]

    matrix = pd.DataFrame(index=TICKERS, columns=TICKERS, dtype=float)

    # diagonal = 1
    for t in TICKERS:
        matrix.loc[t, t] = 1.0

    # build ALL pairs dynamically (no hardcoding)
    from itertools import combinations

    for a, b in combinations(TICKERS, 2):
        col = f"corr_{a.lower()}_{b.lower()}"
        val = row.get(col)

        matrix.loc[a, b] = val
        matrix.loc[b, a] = val

    fig = px.imshow(
        matrix,
        zmin=-1,
        zmax=1,
        color_continuous_scale="RdBu",
        text_auto=".2f"
    )

    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)