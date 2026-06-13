#This functions as a mediator bewtween cpp and the main oython piepline
#This allows the main python scripts to handle the cpp process as if it was pythons 
import markowitz_cpp
import numpy as np

def markowitz(Sigma:np.ndarray, wb:list[float], alpha:float, lamb:float)->list[float]:
    w = markowitz_cpp.optimize_portfolio(Sigma, wb, alpha, lamb)
    return w

def markowitz_of_periods(Sigma:np.ndarray, wb:list[float], alpha:float, lamb:float, num_periods:int)->list[list[float]]:
    wt=[]
    for i in range(num_periods):
        wt.append(markowitz(Sigma,wb[i],alpha,lamb))
    return wt