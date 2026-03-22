import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime
import benchmarks as bm
import portfolio as port
from optimization.Clustering.medoids.kmedoids import clustering_medoids
from optimization.Markowitz.usual.markowitz import markowitz,markowitz_of_periods

st.set_page_config(layout="wide")
st.title("Portfolio Analytics Dashboard")

#las 5 siguientes variables deberían poder elegirse, las 2 primeras de un multiselect. En este caso son unas pocas fijas
tickers = ["AAPL.US","MSFT.US","ADBE.US","AMZN.US","PEP.US"]
index_name="^NDX"
end=datetime(2026,3,15)
start=datetime(2024,3,17)
period=pd.Timedelta("2W")

#Aquí comienza el procesado de las anteriores variables que deberían ser inputs
num_periods=bm.amount_of_periods(period,start,end)

df = pd.read_csv("C:/Users/praxy/OneDrive/Escritorio/Progra/Tests_for_live_index/temporal.csv", index_col=0, parse_dates=True)
index=pd.read_csv("C:/Users/praxy/OneDrive/Escritorio/Progra/Tests_for_live_index/index_t.csv", index_col=0, parse_dates=True)

vola=bm.calc_vola(df,period,num_periods,tickers)
portafolio=port.portfolio_value(vola,df,period,num_periods,tickers)
returns=port.portfolio_returns(portafolio,num_periods)
returns=np.array(returns)
index_returns=bm.index_returns(index,period,num_periods,index_name)
index_returns=np.array(index_returns)

dates = pd.date_range(start, end, num_periods)
portfolio_value = (1 + returns).cumprod()
index_value = (1 + index_returns).cumprod()
active_returns = returns - index_returns

df_aux = pd.DataFrame({
    "Date": dates,
    "Portfolio": portfolio_value,
    "Index": index_value,
    "Portfolio Returns": returns,
    "Index Returns": index_returns,
    "Active Returns": active_returns
})

tracking_error = np.std(active_returns) * np.sqrt(252)
volatility = np.std(returns) * np.sqrt(252)
sharpe = (np.mean(returns) *252) / volatility
information_ratio = (np.mean(active_returns) *252) / tracking_error

col1, col2, col3, col4 = st.columns(4)

col1.metric("Tracking Error", round(tracking_error,4))
col2.metric("Volatility", round(volatility,4))
col3.metric("Sharpe Ratio", round(sharpe,2))
col4.metric("Information Ratio", round(information_ratio,2))

fig = px.line(df_aux, x="Date", y=["Portfolio","Index"],
              title="Portfolio vs Index")
st.plotly_chart(fig, use_container_width=True)


#este proceso debe seleccionarse dando un botón
correlation=port.general_metrizised_correlation_matrix(df,period,num_periods,tickers)
num_medoids=2 #Esto debe de poder escogerse
medoids=clustering_medoids(correlation,num_medoids)
tickers=bm.assign_by_cluster(medoids,tickers)
vola_weight=bm.calc_vola(df,period,num_periods,tickers)
portfolio=port.portfolio_value(vola_weight,df,period,num_periods,tickers)

returns=port.portfolio_returns(portfolio,num_periods)
returns=np.array(returns)

portfolio_value = (1 + returns).cumprod()

active_returns = returns - index_returns

df_aux = pd.DataFrame({
    "Date": dates,
    "Portfolio": portfolio_value,
    "Index": index_value,
    "Portfolio Returns": returns,
    "Index Returns": index_returns,
    "Active Returns": active_returns
})

tracking_error = np.std(active_returns) * np.sqrt(252)
volatility = np.std(returns) * np.sqrt(252)
sharpe = (np.mean(returns) *252) / volatility
information_ratio = (np.mean(active_returns) *252) / tracking_error

col1, col2, col3, col4 = st.columns(4)

col1.metric("Tracking Error", round(tracking_error,4))
col2.metric("Volatility", round(volatility,4))
col3.metric("Sharpe Ratio", round(sharpe,2))
col4.metric("Information Ratio", round(information_ratio,2))

fig = px.line(df_aux, x="Date", y=["Portfolio","Index"],
              title="Portfolio clusterized vs Index")
st.plotly_chart(fig, use_container_width=True)


#tercer proceso, Markowitz
vola_weight=bm.calc_vola(df,period,num_periods,tickers)
portfolio=port.portfolio_vlaue_by_asset(vola_weight,df,period,num_periods,tickers)
portfolio_return=port.general_portfolio_returns(portfolio,num_periods)
sigma=port.cov_matrix(index_returns,portfolio_return,num_periods)

alpha = np.random.randn(len(portfolio_return)).astype(np.float64)
lamb = 10
optimizados=markowitz_of_periods(sigma,vola_weight,alpha,lamb,num_periods)
optimizado=port.portfolio_value(optimizados,df,period,num_periods,tickers)
optimizado=port.portfolio_returns(optimizado,num_periods)
returns=np.array(optimizado)

portfolio_value = (1 + returns).cumprod()

active_returns = returns - index_returns

df_aux = pd.DataFrame({
    "Date": dates,
    "Portfolio": portfolio_value,
    "Index": index_value,
    "Portfolio Returns": returns,
    "Index Returns": index_returns,
    "Active Returns": active_returns
})

tracking_error = np.std(active_returns) * np.sqrt(252)
volatility = np.std(returns) * np.sqrt(252)
sharpe = (np.mean(returns) *252) / volatility
information_ratio = (np.mean(active_returns) *252) / tracking_error

col1, col2, col3, col4 = st.columns(4)

col1.metric("Tracking Error", round(tracking_error,4))
col2.metric("Volatility", round(volatility,4))
col3.metric("Sharpe Ratio", round(sharpe,2))
col4.metric("Information Ratio", round(information_ratio,2))

fig = px.line(df_aux, x="Date", y=["Portfolio","Index"],
              title="Portfolio optimized vs Index")
st.plotly_chart(fig, use_container_width=True)
