import duckdb
import pandas as pd
import os

# -----------------------------
# CONFIG
# -----------------------------
DB_PATH = os.getenv(
    "DUCKDB_PATH",
    r"C:\Users\user\Desktop\projects\stocks_engineering\stocks_dbt\Data_folder\stocks_data.duckdb"
)

# -----------------------------
# CONNECTION
# -----------------------------
def get_connection():
    return duckdb.connect(DB_PATH, read_only=True)

# -----------------------------
# QUERY BUILDERS
# -----------------------------
def ticker_query(ticker: str, days: int = 365) -> str:
    return f"""
        SELECT
            r.trade_date,
            r.ticker,
            r.close,
            r.volume,
            r.daily_return_pct,

            m.ma_7,
            m.ma_21,
            m.ma_30,
            m.ma_50,
            m.ma_200,

            v.vol_7d_ann,
            v.vol_30d_ann,
            v.vol_ratio,
            v.avg_vol_30d,

            rsi.rsi_14,
            rsi.rsi_signal,

            b.bb_upper,
            b.bb_middle,
            b.bb_lower,
            b.bb_pct_b,
            b.bb_signal

        FROM main.fct_prices r

        LEFT JOIN main.fct_moving_averages m
            USING (trade_date, ticker)

        LEFT JOIN main.fct_volatility v
            USING (trade_date, ticker)

        LEFT JOIN main.fct_rsi rsi
            USING (trade_date, ticker)

        LEFT JOIN main.fct_bollinger_bands b
            USING (trade_date, ticker)

        WHERE r.ticker = '{ticker}'
          AND r.trade_date >= CURRENT_DATE - INTERVAL {days} DAY
          AND r.daily_return_pct IS NOT NULL

        ORDER BY r.trade_date
    """

def correlation_query() -> str:
    return """
        SELECT *
        FROM main.fct_correlations
        WHERE trade_date >= CURRENT_DATE - INTERVAL 30 DAY
        ORDER BY trade_date DESC
        LIMIT 1
    """

# -----------------------------
# DATA ACCESS FUNCTIONS
# -----------------------------
def get_ticker_data(ticker: str, days: int = 365) -> pd.DataFrame:
    con = get_connection()
    df = con.execute(ticker_query(ticker, days)).df()
    con.close()
    return df


def get_correlation_data() -> pd.DataFrame:
    con = get_connection()
    df = con.execute(correlation_query()).df()
    con.close()
    return df