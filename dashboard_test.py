import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(layout="wide")

st.title("Portfolio Analytics Dashboard")

# Simulated Data

dates = pd.date_range("2022-01-01", periods=300)

portfolio_returns = np.random.normal(0.0008, 0.01, 300)
index_returns = np.random.normal(0.0006, 0.009, 300)

portfolio_value = (1 + portfolio_returns).cumprod()
index_value = (1 + index_returns).cumprod()

active_returns = portfolio_returns - index_returns

df = pd.DataFrame({
    "Date": dates,
    "Portfolio": portfolio_value,
    "Index": index_value,
    "Portfolio Returns": portfolio_returns,
    "Index Returns": index_returns,
    "Active Returns": active_returns
})

# Metrics

tracking_error = np.std(active_returns) * np.sqrt(252)

volatility = np.std(portfolio_returns) * np.sqrt(252)

sharpe = (np.mean(portfolio_returns) * 252) / volatility

information_ratio = (np.mean(active_returns) * 252) / tracking_error

col1, col2, col3, col4 = st.columns(4)

col1.metric("Tracking Error", round(tracking_error,4))
col2.metric("Volatility", round(volatility,4))
col3.metric("Sharpe Ratio", round(sharpe,2))
col4.metric("Information Ratio", round(information_ratio,2))

# Portfolio vs Index Chart

fig = px.line(df, x="Date", y=["Portfolio","Index"],
              title="Portfolio vs Index")

st.plotly_chart(fig, use_container_width=True)

# Tracking Error Chart

fig2 = px.line(df, x="Date", y="Active Returns",
               title="Active Returns")

st.plotly_chart(fig2, use_container_width=True)

# Drawdown

cum = (1 + portfolio_returns).cumprod()
peak = np.maximum.accumulate(cum)
drawdown = (cum - peak) / peak

df["Drawdown"] = drawdown

fig3 = px.area(df, x="Date", y="Drawdown",
               title="Portfolio Drawdown")

st.plotly_chart(fig3, use_container_width=True)

assets = ["AAPL","MSFT","GOOG","AMZN","NVDA"]

portfolio_weights = np.array([0.25,0.20,0.15,0.25,0.15])
index_weights = np.array([0.20,0.25,0.20,0.20,0.15])

active_weights = portfolio_weights - index_weights

vols = np.array([0.25,0.22,0.24,0.30,0.35])

tracking_contribution = (active_weights**2) * vols

te_df = pd.DataFrame({
    "Asset":assets,
    "Active Weight":active_weights,
    "Contribution":tracking_contribution
})

fig = px.bar(te_df,
             x="Asset",
             y="Contribution",
             title="Tracking Error Contribution")

st.plotly_chart(fig)

st.sidebar.header("Adjust Portfolio Weights")

weights = []

for asset in assets:
    w = st.sidebar.slider(asset,0.0,0.5,0.2)
    weights.append(w)

weights = np.array(weights)
weights = weights / weights.sum()

window = 60

df["Rolling TE"] = df["Active Returns"].rolling(window).std() * np.sqrt(252)

fig = px.line(df, x="Date", y="Rolling TE",
              title="Rolling Tracking Error")

st.plotly_chart(fig)