import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from benchmarks import amount_of_periods
#from main_module import end, start, period, returns

from datetime import datetime, timedelta
#from extraction import full_dataframe_extraction
import benchmarks as bm
import portfolio as port
tickers = ["AAPL.US","MSFT.US"]
index_name="^IPC"
end=datetime.today()
start=end-timedelta(days=2*365)
#df=full_dataframe_extraction(tickers, start, end)
df = pd.read_csv("C:/Users/praxy/OneDrive/Escritorio/Progra/Tests for live index/temporal.csv", index_col=0, parse_dates=True)
index=pd.read_csv("C:/Users/praxy/OneDrive/Escritorio/Progra/Tests for live index/index_t.csv", index_col=0, parse_dates=True)
period=pd.Timedelta("2W")
#ew=bm.calc_EW(tickers,period)
#print(ew)
vola=bm.calc_vola(df,tickers,period)

portafolio=port.portfolio_value(vola,df,period,tickers)

returns=port.portfolio_returns(portafolio,period)
returns=np.array(returns)

index_returns=bm.index_returns(index,period,index_name)
index_returns=np.array(index_returns)

st.set_page_config(layout="wide")

st.title("Portfolio Analytics Dashboard")

periods=amount_of_periods(period)
dates = pd.date_range(start, end, periods)

portfolio_value = (1 + returns).cumprod()
index_value = (1 + index_returns).cumprod()
active_returns = returns - index_returns

df = pd.DataFrame({
    "Date": dates,
    "Portfolio": portfolio_value,
    "Index": index_value,
    "Portfolio Returns": returns,
    "Index Returns": index_returns,
    "Active Returns": active_returns
})

tracking_error = np.std(active_returns)

volatility = np.std(returns)

sharpe = (np.mean(returns)) / volatility

information_ratio = (np.mean(active_returns)) / tracking_error

col1, col2, col3, col4 = st.columns(4)

col1.metric("Tracking Error", round(tracking_error,4))
col2.metric("Volatility", round(volatility,4))
col3.metric("Sharpe Ratio", round(sharpe,2))
col4.metric("Information Ratio", round(information_ratio,2))

fig = px.line(df, x="Date", y=["Portfolio","Index"],
              title="Portfolio vs Index")
st.plotly_chart(fig, use_container_width=True)


fig2 = px.line(df, x="Date", y="Active Returns",
               title="Active Returns")
st.plotly_chart(fig2, use_container_width=True)

peak = np.maximum.accumulate(portfolio_value)
drawdown = (portfolio_value - peak) / peak

df["Drawdown"] = drawdown

fig3 = px.area(df, x="Date", y="Drawdown",
               title="Portfolio Drawdown")
st.plotly_chart(fig3, use_container_width=True)