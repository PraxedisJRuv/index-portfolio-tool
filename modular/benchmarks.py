import datetime
import pandas as pd
import numpy as np

def amount_of_periods(period: pd.Timedelta,start: datetime,end: datetime)->int:
    num_periods = (end - start) / period
    round_num_periods=(end - start)//period
    if num_periods!=round_num_periods:
        round_num_periods=round_num_periods+1
    return round_num_periods

def index_value(index_df: pd.DataFrame, period: pd.Timedelta, index_name:str)->pd.Series:
    index_v=index_df[f"{index_name}_Close"].resample(period).mean()
    return index_v

def index_returns(index_df: pd.DataFrame, period: pd.Timedelta, num_periods: int, index_name:str)->list[float]:
    index_v=index_value(index_df, period, index_name)
    index_r=[0]*num_periods
    for i in range(num_periods-1):
        index_r[i]=(index_v.iloc[i+1]/index_v.iloc[i])-1
    return index_r

def calc_dev_by_period(df: pd.DataFrame, tickers: list[str], period:pd.Timedelta)->list[float]:
    deviations_by_period=[]
    for company in tickers:
        deviation=(df[f"{company}_High"] - df[f"{company}_Low"]).resample(period).std()
        deviations_by_period.append(deviation)
    return deviations_by_period

def calc_vola(df: pd.DataFrame, period: pd.Timedelta, num_periods: int, tickers: list[str])->list[list[float]]:
    deviations_by_period=calc_dev_by_period(df,tickers, period)
    volatility_weight=[]
    for i in range(num_periods):
        volatility_weight.append([])
        desv_sum=0
        for j in range(len(tickers)):
            deviations_by_period[j].iloc[i]=1/deviations_by_period[j].iloc[i]
            desv_sum=desv_sum+deviations_by_period[j].iloc[i]
        for j in range(len(tickers)):
            volatility_weight[i].append(deviations_by_period[j].iloc[i]/desv_sum)
    return volatility_weight

def calc_EW(companies: list[str], num_periods: int)->list[list[float]]:
    ew_weight=[]
    num_periods
    weight=1/len(companies)
    for i in range(num_periods):
        ew_weight.append([])
        for j in range(len(companies)):
            ew_weight[i].append(weight)
    return ew_weight

def assign_by_cluster(medoids: list[int], tickers: list[str])->list[str]:
    cluster=[]
    for i in range(len(medoids)):
        cluster.append(tickers[medoids[i]])
    return cluster