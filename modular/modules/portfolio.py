import pandas as pd
import numpy as np

def portfolio_value(benchmark: list[list[float]], df: pd.DataFrame, period: pd.Timedelta, num_periods: int, tickers: list[str])->list[float]:
    portfolio=[0]*num_periods
    for j in range(len(tickers)):
        valores=df[f"{tickers[j]}_Close"].resample(period).mean()
        for i in range(num_periods):
            portfolio[i]=portfolio[i]+benchmark[i][j]*valores.iloc[i]
    return portfolio

def general_portfolio_values(df: pd.DataFrame, period: pd.Timedelta, num_periods: int, tickers: list[str])->list[list[float]]:
    portfolio=[]
    for j in range(len(tickers)):
        portfolio.append([])
        valores=df[f"{tickers[j]}_Close"].resample(period).mean()
        for i in range(num_periods):
            portfolio[j].append(valores.iloc[i])
    return portfolio

def general_portfolio_returns_from_df(df: pd.DataFrame, period: pd.Timedelta, num_periods: int, tickers: list[str])->list[list[float]]:
    values=general_portfolio_values(df, period, num_periods, tickers)
    returns=[]
    for i in range(len(values)):
        returns.append([])
        for j in range(len(values[i])-1):
            returns[i].append((values[i][j+1]/values[i][j])-1)
    return returns

def portfolio_vlaue_by_asset(benchmark: list[list[float]], df: pd.DataFrame, period: pd.Timedelta, num_periods: int, tickers: list[str]):
    portfolio=[]
    for j in range(len(tickers)):
        valores=df[f"{tickers[j]}_Close"].resample(period).mean()
        portfolio.append([])
        for i in range(num_periods):
            portfolio[j].append(benchmark[i][j]*valores.iloc[i])
    return portfolio

def portfolio_returns(portfolio: list[list[float]], num_periods: int)->list[float]:
    port_return=[0]*num_periods
    for i in range(num_periods-1):
        port_return[i]=(portfolio[i+1]/portfolio[i])-1
    return port_return

def general_portfolio_returns(portfolio: list[list[float]], num_periods: int)->list[list[float]]:
    r=[]
    for j in range(len(portfolio)):
        r.append([])
        for i in range(num_periods-1):
            r[j].append((portfolio[j][i+1]/portfolio[j][i])-1)
    return r

def return_excess_vector(returns_vector: list[float], rf_by_period: float)->list[float]:
    excess=[]
    for i in returns_vector:
        excess.append(i-rf_by_period)
    return excess

def correlations_matrix_from_df(tickers: list[str], df: pd.DataFrame)->np.ndarray:
    import pandas as pd
    flag=True
    for ticker in tickers:
        df_temp=df[f"{ticker}_Close"]
        df_temp=pd.DataFrame(df_temp)
        if flag:
            data=df_temp
            flag =False
        else:
            data=data.join(df_temp)
    data=data.corr().to_numpy()
    return data

def metric_correlation_matrix(matrix: list[list[float]])->np.ndarray:
    import numpy as np
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            matrix[i][j]=2*(1-matrix[i][j])
    matriz=np.sqrt(matrix)
    return matriz

def general_metrizised_correlation_matrix(df: pd.DataFrame, period: pd.Timedelta, num_periods: int, tickers: list[str])->np.ndarray:
    import numpy as np
    portfolio=general_portfolio_values(df, period, num_periods,tickers)
    r=general_portfolio_returns(portfolio, num_periods)
    flag=True
    for i in range(len(r)):
        if flag:
            matriz=r[i]
            flag =False
        else:
            matriz=np.vstack([matriz,r[i]])
    matrix=np.corrcoef(matriz)
    matrix=metric_correlation_matrix(matrix)
    return matrix

def cov_matrix(index_returns: list[float], portfolio_returns: list[list[float]], num_periods: int)->np.ndarray:
    import numpy as np
    diferencia=[]
    for i in range(len(portfolio_returns)):
        diferencia.append([])
        for j in range(num_periods-1):
            diferencia[i].append(index_returns[j]-portfolio_returns[i][j])
    matrix=np.cov(diferencia)
    return matrix

def dev_matrix_from_df(df: pd.DataFrame, period: pd.Timedelta, num_periods: int, tickers: list[str])->list[list[float]]:
    values=general_portfolio_returns_from_df(df,period,num_periods,tickers)
    desv_returns_matrix=[]
    for i in range (len(values)):
        desv_returns_matrix.append([])
        for q in range(len(values)):
            suma=0
            for j in range(len(values[i])):
                suma=suma+(values[i][j]-values[q][j])**2
            desv_returns_matrix[i].append(suma)
    return desv_returns_matrix