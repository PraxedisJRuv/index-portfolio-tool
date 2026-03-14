import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from benchmarks import amount_of_periods
from main_module import end, start, period, returns

from datetime import datetime, timedelta
from extraction import full_dataframe_extraction
import benchmarks as bm
import portfolio as port
tickers = ["AAPL.US","MSFT.US"]
end=datetime.today()
start=end-timedelta(days=2*365)
df=full_dataframe_extraction(tickers, start, end)
period=pd.Timedelta("2W")
#ew=bm.calc_EW(tickers,period)
#print(ew)
vola=bm.calc_vola(df,tickers,period)
#print(vola)
portafolio=port.portfolio_value(vola,df,period,tickers)
#print(portafolio)
returns=port.portfolio_returns(portafolio,period)

st.set_page_config(layout="wide")

st.title("Portfolio Analytics Dashboard")

periods=amount_of_periods(period)
index_returns = np.random.normal(0.1, 0.1, periods)
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

tracking_error = np.std(active_returns) * np.sqrt(252)

volatility = np.std(returns) * np.sqrt(252)

sharpe = (np.mean(returns) * 252) / volatility

information_ratio = (np.mean(active_returns) * 252) / tracking_error

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