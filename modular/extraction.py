import pandas as pd

def full_dataframe_extraction(indexs,start, end):
    flag=True
    for index in indexs:
        url=f"https://stooq.com/q/d/l/?s={index}&d1={start:%Y%m%d}&d2={end:%Y%m%d}&i=d"
        df_temp=(pd.read_csv(url,parse_dates=["Date"])
            .set_index("Date")
            .sort_index())
        df_temp.columns = [f"{index} Open", f"{index} High", f"{index} Low", f"{index} Close", f"{index} Volume"]
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