import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from extraction import full_dataframe_extraction, index_dataframe_extraction
import benchmarks as bm
import portfolio as port
from optimization.Clustering.medoids.kmedoids import clustering_medoids
from optimization.Markowitz.usual.markowitz import markowitz,markowitz_of_periods
tickers = ["AAPL.US","MSFT.US","ADBE.US","AMZN.US","PEP.US"]
index_name="^NDX"
end=datetime(2026,3,15)
start=datetime(2024,3,17)
# por ahora por falla de stooq df=full_dataframe_extraction(tickers, start, end)
# index=index_dataframe_extraction(index, start, end)
df = pd.read_csv("C:/Users/praxy/OneDrive/Escritorio/Progra/Tests_for_live_index/temporal.csv", index_col=0, parse_dates=True)
index=pd.read_csv("C:/Users/praxy/OneDrive/Escritorio/Progra/Tests_for_live_index/index_t.csv", index_col=0, parse_dates=True)
period=pd.Timedelta("2W")
num_periods=bm.amount_of_periods(period,start,end)
#portfolio=port.general_portfolio_values(df,period,num_periods,tickers)
#print(portfolio)
#print(port.general_portfolio_returns(portfolio,num_periods))

correlation=port.general_metrizised_correlation_matrix(df,period,num_periods,tickers)
num_medoids=2
medoids=clustering_medoids(correlation,num_medoids)

tickers=bm.assign_by_cluster(medoids,tickers)
vola_weight=bm.calc_vola(df,period,num_periods,tickers)
portfolio=port.portfolio_vlaue_by_asset(vola_weight,df,period,num_periods,tickers)

portfolio_return=port.general_portfolio_returns(portfolio,num_periods)
index_return=bm.index_returns(index,period,num_periods,index_name)

sigma=port.cov_matrix(index_return,portfolio_return,num_periods)

alpha = np.random.randn(len(portfolio_return)).astype(np.float64)
lamb = 0.1
optimizados=markowitz_of_periods(sigma,vola_weight,alpha,lamb,num_periods)
optimizado=port.portfolio_value(optimizados,df,period,num_periods,tickers)
optimizado=port.portfolio_returns(optimizado,num_periods)
print(optimizado)
#ew=bm.calc_EW(tickers,period)
#print(ew)
def debugeando():
    vola=bm.calc_vola(df,tickers,period,num_periods)
    print(vola)
    portafolio=port.portfolio_value(vola,df,period,num_periods,tickers)
    print(portafolio)
    returns=port.portfolio_returns(portafolio,num_periods)
    print(returns)
    index_r=bm.index_returns(index,period,num_periods,index)
    print(index_r)
#import subprocess
#import sys
#import os

#if "STREAMLIT_SERVER_PORT" not in os.environ:
    #subprocess.run([
    #sys.executable, "-m", "streamlit", "run", "C:/Users/praxy/OneDrive/Escritorio/Progra/Tests for live index/modular/dashboard.py"
#])