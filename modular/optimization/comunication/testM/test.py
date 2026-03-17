import numpy as np
import markowitz_cpp

n = 5

Sigma = np.random.rand(n,n)
Sigma = Sigma @ Sigma.T   # hacerla PSD

wb = np.ones(n)/n

w = markowitz_cpp.optimize_portfolio(Sigma, wb)

print(w)
print("sum =", w.sum())