# 📊 Stock Analytics Platform

A production-style data pipeline and dashboard for analyzing stock market data.

## 🚀 Features

- Daily data ingestion using yfinance
- Data warehouse powered by DuckDB
- Transformations with dbt (staging → intermediate → fact models)
- Interactive dashboard built with Streamlit
- Technical indicators:
  - Moving averages
  - RSI
  - Bollinger Bands
  - Volatility
- Correlation heatmap across multiple tickers

## 🧱 Architecture

yfinance → DuckDB → dbt → Streamlit

## ⚙️ Tech Stack

- Python
- DuckDB
- dbt
- Streamlit
- Plotly

## ▶️ How to Run

```bash
uv sync
uv run dbt build
uv run streamlit run streamlit/app.py