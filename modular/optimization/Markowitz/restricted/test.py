import numpy as np
import markowitz_cpp

n = 5
T = 100  # periodos históricos

# Simular retornos
returns = np.random.randn(T,n) * 0.01

# Covarianza histórica
Sigma = np.cov(returns.T)

# Benchmark
wb = [0.1,0.03,0.7,0.07,0.1]

# Portafolio actual
w_prev = np.array([0.2,0.2,0.2,0.2,0.2])

# Turnover penalty
lambda_turnover = 0.05

# Optimizar
w_opt = markowitz_cpp.optimize_portfolio(Sigma, wb, w_prev, lambda_turnover)
print(type(Sigma))
print(type(wb))
print(type(w_prev))
print(wb)
print("w_opt =", w_opt)
print("suma =", w_opt.sum())
print("turnover =", np.sum(np.abs(w_opt - w_prev)))