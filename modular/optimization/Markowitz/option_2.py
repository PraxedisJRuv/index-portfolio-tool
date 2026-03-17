#option with scipy
#Se ve simple y amigable, probablemente la pruebe pero, nuevamente, en algo de investigación
#Donde requiere estar ajustando muchas opciones diversas.
from scipy.optimize import minimize
import numpy as np

def objective(w, Sigma, wb):
    diff = w - wb
    return diff.T @ Sigma @ diff


def optimizar_portafolio(cluster, op, periodo):

    w_b = np.array([get_asignacion(cluster[i], op)[periodo]
                   for i in range(len(cluster))])

    Sigma = np.cov(matriz_retornos(cluster, op))

    n = len(cluster)
    tau_max = 0.10
    w0 = w_b.copy()

    cons = [
        {'type': 'eq', 'fun': lambda w: np.sum(w) - 1},
    ]

    bounds = [(0, 1)] * n

    res = minimize(objective, w0,
                   args=(Sigma, w_b),
                   bounds=bounds,
                   constraints=cons)

    return res.x