import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from datetime import datetime
import benchmarks as bm
import portfolio as port
from optimization.Clustering.medoids.kmedoids import clustering_medoids
from optimization.Markowitz.usual.markowitz import markowitz_of_periods
from extraction import full_dataframe_extraction, index_dataframe_extraction, pdreader_full_dataframe_extraction

#Guardar en sesión
def save_to_state(key, value):
    st.session_state[key] = value

#Validar dependencia
def require_keys(keys):
    for k in keys:
        if k not in st.session_state:
            return False
    return True

#primer proceso
def run_process_1(tickers,index_name,period,start,end):
    num_periods = bm.amount_of_periods(period,start,end)

    df = full_dataframe_extraction(tickers,start,end)
    index = index_dataframe_extraction(index_name,start,end)

    vola = bm.calc_vola(df,period,num_periods,tickers)
    portafolio = port.portfolio_value(vola,df,period,num_periods,tickers)

    returns = np.array(port.portfolio_returns(portafolio,num_periods))
    index_returns = np.array(bm.index_returns(index,period,num_periods,index_name))

    st.session_state["p1"] = {
        "df": df,
        "returns": returns,
        "index_returns": index_returns,
        "num_periods": num_periods
    }


#segundo proceso
def run_process_2(tickers,num_medoids,period):
    p1 = st.session_state["p1"]

    correlation = port.general_metrizised_correlation_matrix(
        p1["df"],period,p1["num_periods"],tickers
    )

    medoids = clustering_medoids(correlation,num_medoids)
    tickers_clustered = bm.assign_by_cluster(medoids,tickers)

    vola_weight = bm.calc_vola(
        p1["df"],period,p1["num_periods"],tickers_clustered
    )

    portfolio = port.portfolio_value(
        vola_weight,p1["df"],period,p1["num_periods"],tickers_clustered
    )

    returns = np.array(port.portfolio_returns(portfolio,p1["num_periods"]))

    st.session_state["p2"] = {
        "returns": returns,
        "index_returns": p1["index_returns"],
        "num_periods": p1["num_periods"]
    }

#tercer proceso
def run_process_3(tickers,period):
    p1 = st.session_state["p1"]

    vola_weight = bm.calc_vola(p1["df"],period,p1["num_periods"],tickers)

    portfolio = port.portfolio_vlaue_by_asset(vola_weight,p1["df"],period,p1["num_periods"],tickers)

    portfolio_return = port.general_portfolio_returns(portfolio,p1["num_periods"])

    sigma = port.cov_matrix(p1["index_returns"],portfolio_return,p1["num_periods"])
    
    #This values need to be corrected, lambda also should be selectable
    alpha = np.random.randn(len(portfolio_return)).astype(np.float64)
    lamb = 10

    optimizados = markowitz_of_periods(sigma,vola_weight,alpha,lamb,p1["num_periods"])

    optimizado = port.portfolio_value(optimizados,p1["df"],period,p1["num_periods"],tickers)

    returns = np.array(port.portfolio_returns(optimizado,p1["num_periods"]))

    st.session_state["p3"] = {
        "returns": returns,
        "index_returns": p1["index_returns"],
        "num_periods": p1["num_periods"]
    }

#graph 
def metrics_and_chart(returns, index_returns, start, end, num_periods, key):

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

    fig = px.line(df_aux, x="Date", y=["Portfolio","Index"])

    #it is important to have the key, since otherwise streamlit might having some error
    st.plotly_chart(fig, use_container_width=True, key=f"{key}{1}")

