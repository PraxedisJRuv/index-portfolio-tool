import pandas as pd

def full_dataframe_extraction(tickers,start, end):
    flag=True
    for ticker in tickers:
        url=f"https://stooq.com/q/d/l/?s={ticker}&d1={start:%Y%m%d}&d2={end:%Y%m%d}&i=d"
        print(url)
        df_temp=(pd.read_csv(url,parse_dates=["Date"])
            .set_index("Date")
            .sort_index())
        df_temp.columns = [f"{ticker} Open", f"{ticker} High", f"{ticker} Low", f"{ticker} Close", f"{ticker} Volume"]
        if flag:
            data=df_temp
            flag =False
        else:
            data=data.join(df_temp)
    return data

def index_dataframe_extraction(index,start, end):
    url=f"https://stooq.com/q/d/l/?s={index}&d1={start:%Y%m%d}&d2={end:%Y%m%d}&i=d"
    data=(pd.read_csv(url,parse_dates=["Date"])
        .set_index("Date")
        .sort_index())
    data.columns = [f"{index} Open", f"{index} High", f"{index} Low", f"{index} Close", f"{index} Volume"]
    return data


#This functions using pdreader were used since the other fucntions were having an error
#the error was there wasn't a Date column to organize the data, but reviewing it more deeply
#it seems stooq was returning empty files, and with pandas_datareader it was the same.
#More detail in some errors.txt

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