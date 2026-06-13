import markowitz_cpp
import numpy as np

def markowitz(Sigma: np.ndarray, wb:list[float], w_prev:np.ndarray, lambda_turnover:float):
    """
    This function is an intermiedate between the pybind module made for markowitz.cpp,
    so it can be implemented as a python function and imported as a module.
    """
    w_opt = markowitz_cpp.optimize_portfolio(Sigma, wb, w_prev, lambda_turnover)
    return w_opt
