import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import modular.benchmarks as bm
import modular.portfolio as port
from modular.optimization.Clustering.medoids.kmedoids import clustering_medoids
from modular.optimization.Markowitz.usual.markowitz import markowitz_of_periods
from modular.extraction import index_dataframe_extraction
from modular.optimization.cluster_search_utils import get_best_minimal_medoids_by_metric
from modular.optimization.Clustering.cluster.kmedoids import clustering_medoids as cluster_vector


#Save state
def save_to_state(key, value):
    st.session_state[key] = value

#validate dependency
def require_keys(keys):
    for k in keys:
        if k not in st.session_state:
            return False
    return True

#First process
def run_process_1(tickers:list[str], index_name:str, period:pd.Timedelta, start:datetime, end:datetime):
    num_periods = bm.amount_of_periods(period,start,end)
    
    df = pd.read_csv("C:/Users/praxy/OneDrive/Escritorio/Progra/Tests_for_live_index/Usable.csv", index_col=0, parse_dates=True)
    df=df.dropna()
    index = index_dataframe_extraction(index_name,start,end)

    ew = bm.calc_EW(tickers,num_periods)
    portafolio = port.portfolio_value(ew,df,period,num_periods,tickers)

    returns = np.array(port.portfolio_returns(portafolio,num_periods))
    index_returns = np.array(bm.index_returns(index,period,num_periods,index_name))

    st.session_state["p1"] = {
        "df": df,
        "returns": returns,
        "index_returns": index_returns,
        "num_periods": num_periods
    }


#segundo proceso
def run_process_2(tickers:list[str], num_medoids:int, period:pd.Timedelta):
    p1 = st.session_state["p1"]

    correlation = port.general_metrizised_correlation_matrix(
        p1["df"],period,p1["num_periods"],tickers
    )

    medoids = clustering_medoids(correlation,num_medoids)
    tickers_clustered = bm.assign_by_cluster(medoids,tickers)

    ew = bm.calc_EW(tickers_clustered, p1["num_periods"])

    portfolio = port.portfolio_value(
        ew,p1["df"],period,p1["num_periods"],tickers_clustered
    )

    returns = np.array(port.portfolio_returns(portfolio,p1["num_periods"]))

    st.session_state["p2"] = {
        "returns": returns,
        "index_returns": p1["index_returns"],
        "num_periods": p1["num_periods"]
    }

def run_process_3(tickers:list[str], num_medoids:int, period:pd.Timedelta):
    p1 = st.session_state["p1"]

    correlation = port.dev_matrix_from_df(
        p1["df"],period,p1["num_periods"],tickers
    )

    medoids = clustering_medoids(correlation,num_medoids)
    tickers_clustered = bm.assign_by_cluster(medoids,tickers)

    ew = bm.calc_EW(tickers_clustered, p1["num_periods"])

    portfolio = port.portfolio_value(
        ew,p1["df"],period,p1["num_periods"],tickers_clustered
    )

    returns = np.array(port.portfolio_returns(portfolio,p1["num_periods"]))

    st.session_state["p3"] = {
        "returns": returns,
        "index_returns": p1["index_returns"],
        "num_periods": p1["num_periods"]
    }

def run_process_4(tickers:list[str], num_medoids:int, period:pd.Timedelta):
    p1 = st.session_state["p1"]

    dist_corr= port.general_metrizised_correlation_matrix(        
        p1["df"],period,p1["num_periods"],tickers
    )

    dist_desv = port.dev_matrix_from_df(
        p1["df"],period,p1["num_periods"],tickers
    )

    clustering_corr = cluster_vector(dist_corr,num_medoids)
    clustering_desv =cluster_vector(dist_desv,num_medoids)
    
    medoids=get_best_minimal_medoids_by_metric(clustering_corr,clustering_desv,dist_corr)
    print(medoids)
    
    tickers_clustered = bm.assign_by_cluster(medoids,tickers)

    ew = bm.calc_EW(tickers_clustered, p1["num_periods"])

    portfolio = port.portfolio_value(
        ew,p1["df"],period,p1["num_periods"],tickers_clustered
    )

    returns = np.array(port.portfolio_returns(portfolio,p1["num_periods"]))

    st.session_state["p4"] = {
        "returns": returns,
        "index_returns": p1["index_returns"],
        "num_periods": p1["num_periods"]
    }

def run_process_5(tickers:list[str], period:pd.Timedelta, lambda_for_Markowitz:float):
    p1 = st.session_state["p1"]

    vola_weight = bm.calc_vola(p1["df"],period,p1["num_periods"],tickers)

    portfolio = port.portfolio_vlaue_by_asset(vola_weight,p1["df"],period,p1["num_periods"],tickers)

    portfolio_return = port.general_portfolio_returns(portfolio,p1["num_periods"])

    sigma = port.cov_matrix(p1["index_returns"],portfolio_return,p1["num_periods"])
    
    #This values need to be corrected, lambda also should be selectable
    alpha = np.random.randn(len(portfolio_return)).astype(np.float64)
    lamb = lambda_for_Markowitz

    optimizados = markowitz_of_periods(sigma,vola_weight,alpha,lamb,p1["num_periods"])

    optimizado = port.portfolio_value(optimizados,p1["df"],period,p1["num_periods"],tickers)

    returns = np.array(port.portfolio_returns(optimizado,p1["num_periods"]))

    st.session_state["p3"] = {
        "returns": returns,
        "index_returns": p1["index_returns"],
        "num_periods": p1["num_periods"]
    }

#graph 
def metrics_and_chart(returns:list[float], index_returns:list[float], start:datetime, end:datetime, num_periods:int, key):

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

    days_in_period =int(((end-start).days)-(((end-start).days)*.10))
    tracking_error = np.std(active_returns) * np.sqrt(days_in_period)
    volatility = np.std(returns) * np.sqrt(days_in_period)
    sharpe = (np.mean(returns) *days_in_period) / volatility
    information_ratio = (np.mean(active_returns) *days_in_period) / tracking_error

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Tracking Error", round(tracking_error,4))
    col2.metric("Volatility", round(volatility,4))
    col3.metric("Sharpe Ratio", round(sharpe,2))
    col4.metric("Information Ratio", round(information_ratio,2))

    fig = px.line(df_aux, x="Date", y=["Portfolio","Index"])

    #it is important to have the key, since otherwise streamlit might having some error
    st.plotly_chart(fig, use_container_width=True, key=f"{key}{1}")
