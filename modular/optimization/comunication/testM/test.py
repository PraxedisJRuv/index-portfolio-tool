import numpy as np
import markowitz_cpp

n = 5

Sigma = np.random.rand(n,n)
Sigma = Sigma @ Sigma.T   # hacerla PSD

wb = [0.1,0.03,0.7,0.07,0.1]
print(Sigma)
print(wb)
w = markowitz_cpp.optimize_portfolio(Sigma, wb)

print(w)
print("sum =", w.sum())