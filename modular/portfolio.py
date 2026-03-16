from benchmarks import amount_of_periods

def portfolio_value(benchmark, df, period, tickers):
    periods=amount_of_periods(period)
    portfolio=[0]*periods
    for j in range(len(tickers)):
        valores=df[f"{tickers[j]} Close"].resample(period).mean()
        for i in range(periods):
            portfolio[i]=portfolio[i]+benchmark[i][j]*valores[i]
    return portfolio

def general_portfolio_values(df, period, tickers):
    periods=amount_of_periods(period)
    portfolio=[]
    for j in range(len(tickers)):
        portfolio.append([])
        valores=df[f"{tickers[j]} Close"].resample(period).mean()
        for i in range(periods):
            portfolio[j].append(valores[i])
    return portfolio

def portfolio_vlaue_by_asset(benchmark, df, period, tickers):
    periods=amount_of_periods(period)
    portfolio=[]
    for j in range(len(tickers)):
        valores=df[f"{tickers[j]} Close"].resample(period).mean()
        portfolio.append([])
        for i in range(periods):
            portfolio[j].append(benchmark[i][j]*valores[i])
    return portfolio

def portfolio_returns(portfolio,period):
    periods=amount_of_periods(period)
    port_return=[0]*periods
    for i in range(periods-1):
        port_return[i]=(portfolio[i+1]/portfolio[i])-1
    return port_return

def general_portfolio_returns(portfolio,period):
    periods=amount_of_periods(period)
    r=[]
    for j in range(len(portfolio)):
        r.append([])
        for i in range(periods-1):
            r[j].append((portfolio[j][i+1]/portfolio[j][i])-1)
    return r
  
def correlations_matrix_from_df(tickers, df):
    import pandas as pd
    flag=True
    for ticker in tickers:
        df_temp=df[f"{ticker} Close"]
        df_temp=pd.DataFrame(df_temp)
        if flag:
            data=df_temp
            flag =False
        else:
            data=data.join(df_temp)
    data=data.corr().to_numpy()
    return data

def metric_correlation_matrix(matrix):
    import numpy as np
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            matrix[i][j]=2*(1-matrix[i][j])
    matrix=np.sqrt(matrix)
    return matrix

def general_metrizised_correlation_matrix(df, period, tickers):
    import numpy as np
    portfolio=general_portfolio_values(df, period, tickers)
    r=general_portfolio_returns(portfolio, period)
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

def turnover(portfolio,index):
    turnover=(portfolio-index).std()
    return turnover