from benchmarks import amount_of_periods

def portfolio_value(benchmark, df, period, tickers):
    periods=amount_of_periods(period)
    portfolio=[0]*periods
    for j in range(len(tickers)):
        valores=df[f"{tickers[j]} Close"].resample(period).mean()
        for i in range(periods):
            portfolio[i]=portfolio[i]+benchmark[i][j]*valores[i]
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

def turnover(portfolio,index):
    turnover=(portfolio-index).std()
    return turnover