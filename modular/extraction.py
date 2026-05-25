import pandas as pd
import requests
from io import StringIO
import time
import random
import os

api_key=os.getenv("AK_STOOQ")

def full_dataframe_extraction(tickers,start, end):
    flag=True
    for ticker in tickers:
        url=f"https://stooq.com/q/d/l/?s={ticker}&d1={start:%Y%m%d}&d2={end:%Y%m%d}&i=d&apikey={api_key}"
        print(url)
        df_temp=(pd.read_csv(url,parse_dates=["Date"])
            .set_index("Date")
            .sort_index())
        df_temp.columns = [f"{ticker}_Open", f"{ticker}_High", f"{ticker}_Low", f"{ticker}_Close", f"{ticker}_Volume"]
        if flag:
            data=df_temp
            flag =False
        else:
            data=data.join(df_temp)
    return data

def index_dataframe_extraction(index,start, end):
    url=f"https://stooq.com/q/d/l/?s={index}&d1={start:%Y%m%d}&d2={end:%Y%m%d}&i=d&apikey={api_key}"
    data=(pd.read_csv(url,parse_dates=["Date"])
        .set_index("Date")
        .sort_index())
    data.columns = [f"{index}_Open", f"{index}_High", f"{index}_Low", f"{index}_Close", f"{index}_Volume"]
    return data

"""
This functions using pdreader were used since the other fucntions were having an error
the error was there wasn't a Date column to organize the data, but reviewing it more deeply
it seems stooq was returning empty files, and with pandas_datareader it was the same.
More detail in some errors.txt
"""

#it seems the main issue is Stooq requieres APIKEY, it's free, but need to be get manually every once in a while it seems.

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": "https://stooq.com/",
}

def fetch_stooq(ticker: str, start, end) -> pd.DataFrame:
    url = (
        f"https://stooq.com/q/d/l/"
        f"?s={ticker}&d1={start:%Y%m%d}&d2={end:%Y%m%d}&i=d&apikey={api_key}"
    )
    resp = requests.get(url, headers=HEADERS, timeout=15)
    print(resp.status_code)
    print(resp.text[:500]) 
    resp.raise_for_status()

    # Stooq devuelve una página de error sin levantar excepción HTTP
    if "No data" in resp.text or len(resp.text.strip()) < 30:
        raise ValueError(f"Stooq didn't return any for {ticker}")

    df = (
        pd.read_csv(StringIO(resp.text), parse_dates=["Date"])
        .set_index("Date")
        .sort_index()
    )
    df.columns = [f"{ticker}_{c}" for c in df.columns]
    return df

def full_robust_dataframe_extraction(tickers, start, end, delay=(1.0, 2.5)):
    frames = []
    for i, ticker in enumerate(tickers):
        print(f"[{i+1}/{len(tickers)}] Downloading{ticker}...")
        try:
            frames.append(fetch_stooq(ticker, start, end))
        except Exception as e:
            print(f"    Error at {ticker}: {e}")
        if i < len(tickers) - 1:
            time.sleep(random.uniform(*delay))   #random pause

    return frames[0].join(frames[1:]) if frames else pd.DataFrame()



def pdreader_full_dataframe_extraction(indexs,start, end):
    import pandas_datareader.data as web
    data = web.DataReader(indexs, 'stooq', start, end)
    data.columns = [f"{ticker} {col}" for col, ticker in data.columns]
    data = data.sort_index()
    return data

def fetch_with_retry(ticker, start, end, retries=3):
    import time
    for i in range(retries):
        try:
            df = web.DataReader(ticker, 'stooq', start, end)
            if not df.empty:
                return df
        except Exception:
            pass
        time.sleep(1.5) 
    print(f"Failed after retries: {ticker}")
    return None

def preventive_pdreader_extraction(indexs, start, end):
    data = None
    flag = True

    for ticker in indexs:
        df = fetch_with_retry(ticker, start, end)

        if df is None:
            continue

        df = df.sort_index()
        df.columns = [f"{ticker} {col}" for col in df.columns]

        if flag:
            data = df
            flag = False
        else:
            data = data.join(df, how="outer")

    return data