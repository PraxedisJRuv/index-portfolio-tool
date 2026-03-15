import pandas as pd
from datetime import datetime, timedelta
from extraction import full_dataframe_extraction, index_dataframe_extraction
import benchmarks as bm
import portfolio as port
tickers = ["AAPL.US","MSFT.US"]
index_name="^IPC"
end=datetime.today()
start=end-timedelta(days=2*365)
# por ahora por falla de stooq df=full_dataframe_extraction(tickers, start, end)
# index=index_dataframe_extraction(index, start, end)
df = pd.read_csv("C:/Users/praxy/OneDrive/Escritorio/Progra/Tests for live index/temporal.csv", index_col=0, parse_dates=True)
index=pd.read_csv("C:/Users/praxy/OneDrive/Escritorio/Progra/Tests for live index/index_t.csv", index_col=0, parse_dates=True)

period=pd.Timedelta("2W")
#ew=bm.calc_EW(tickers,period)
#print(ew)
vola=bm.calc_vola(df,tickers,period)
#print(vola)
portafolio=port.portfolio_value(vola,df,period,tickers)
#print(portafolio)
returns=port.portfolio_returns(portafolio,period)
#print(returns)
index_r=bm.index_returns(index,period,index_name)
print(index_r)
#import subprocess
#import sys
#import os

#if "STREAMLIT_SERVER_PORT" not in os.environ:
    #subprocess.run([
    #sys.executable, "-m", "streamlit", "run", "C:/Users/praxy/OneDrive/Escritorio/Progra/Tests for live index/modular/dashboard.py"
#])