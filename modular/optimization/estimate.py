import modular.portfolio as port
import modular.benchmarks as bm
from datetime import datetime
import pandas as pd
import numpy as np
from scipy import stats

def full_estimate_returns(index_returns, portfolio_returns_by_asset, rf_annual, num_periods):
    rf_period=(1+rf_annual)**(1/num_periods)-1
    
    excess_rm=port.return_excess_vector(index_returns, rf_period)

    excess_rm.pop()

    market_premium=np.array(excess_rm).mean()*num_periods

    results = {"alpha": {}, "beta": {}, "r2": {}}

    for i in range(len(portfolio_returns_by_asset)):
        excess_ri = port.return_excess_vector(portfolio_returns_by_asset[i],rf_period)
        beta, alpha, r, _, _ = stats.linregress(
                np.array(excess_rm),
                np.array(excess_ri)
            )
        results["alpha"][i] = alpha * num_periods     
        results["beta"][i]  = beta
        results["r2"][i]    = r ** 2
    
    alphas = results["alpha"]
    betas  = results["beta"]
    r2     = results["r2"]
    
    print(alphas)
    print(betas)
    print(r2)
    mu=[]
    for i in range(len(portfolio_returns_by_asset)):
        mu.append(rf_annual + betas[i] * market_premium + alphas[i])
    
    return mu


def estimate_returns(index_returns, portfolio_returns_by_asset, rf_annual, num_periods):
    rf_period=(1+rf_annual)**(1/num_periods)-1
    
    excess_rm=port.return_excess_vector(index_returns, rf_period)

    excess_rm.pop()

    market_premium=np.array(excess_rm).mean()*num_periods

    results = {"alpha": {}, "beta": {}, "r2": {}}

    for i in range(len(portfolio_returns_by_asset)):
        excess_ri = port.return_excess_vector(portfolio_returns_by_asset[i],rf_period)
        beta, alpha = stats.linregress(
                np.array(excess_rm),
                np.array(excess_ri)
            )
        results["alpha"][i] = alpha * num_periods     
        results["beta"][i]  = beta
    
    alphas = results["alpha"]
    betas  = results["beta"]

    mu=[]
    for i in range(len(portfolio_returns_by_asset)):
        mu.append(rf_annual + betas[i] * market_premium + alphas[i])
    
    return np.array(mu)