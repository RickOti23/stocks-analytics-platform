import yfinance as yf
import pandas as pd
import duckdb as db
import os as os
import datetime as dt

def extract():

    tickers =  ["AAPL", "MSFT", "GOOGL", "META", "AMZN", "TSLA", "NVDA", "INTC", "AMD", "CSCO","JPM", "BAC", "GS", "WFC", "MS", "JNJ", "PFE", "MRK", "UNH", "ABT",
                "HD", "NKE", "MCD", "SBUX", "LOW", "PG", "KO", "PEP", "WMT", "COST",
                "GE", "CAT", "BA", "UPS", "DE", "XOM", "CVX", "NEE", "DUK", "SLB",
                "NFLX", "PYPL", "ADBE", "CRM", "TMUS", "ORCL", "IBM", "QCOM", "INTU", "TXN"
                ]
    dfs= []
    for ticker in tickers:
        obj = yf.Ticker(ticker)
        df = obj.history(start="2020-01-01",interval="1d",end="2025-12-31")
        df["Ticker"] = ticker
        df.index = pd.to_datetime(df.index).date
        df["Date"] = df.index
        
        dfs.append(df)

    df = pd.concat(dfs,ignore_index=True)

    #CREATE FOLDER
    data_folder = "Data_folder"
    os.makedirs(data_folder,exist_ok=True)

    #SAVE CSV
    csv_path = os.path.join(data_folder,"stocks.csv")
    print(f"Loading data to {data_folder}")
    df.to_csv(csv_path)


    #DUCKDB CONNECTION
    db_path = os.path.join(data_folder,"stocks_data.duckdb")
    conn = db.connect(db_path)

    conn.register("df",df)

    #I need to create a schema

    conn.execute(
        """CREATE TABLE IF NOT EXISTS stocks 
        AS SELECT * FROM df"""
    )
    print(f"Loading data to {db_path}")

    return df

if __name__ == "__main__":
    df = extract()
    print(f"Loaded daa of {df.shape[0]} rows to duckdb")