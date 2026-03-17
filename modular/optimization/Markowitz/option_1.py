#hay que instalar la librería, es open source. Hay que añadir OSPQ es rápido para QP financieros
#No me es de mucho interés trabajar con otro solver, además, trabajar con librerías es lento.
#Esta podría una muy buena opción para trabajar en otro proyecto de investigación pero no producción
import cvxpy as cp
import numpy as np
import pandas as pd

def optimizar_portafolio(cluster, op, periodo):

    w_b = []
    for i in range(len(cluster)):
        w_b.append(get_asignacion(cluster[i], op)[periodo])

    w_b = np.array(w_b)

    matriz_varianza = np.cov(matriz_retornos(cluster, op))

    tau_max = 0.10
    w_0 = w_b.copy()

    n = len(cluster)

    w = cp.Variable(n)
    u = cp.Variable(n)

    objective = cp.quad_form(w - w_b, matriz_varianza)

    constraints = [
        cp.sum(w) == 1,
        w >= 0,
        u >= w - w_0,
        u >= -(w - w_0),
        cp.sum(u) <= tau_max
    ]

    problem = cp.Problem(cp.Minimize(objective), constraints)
    problem.solve()

    w_opt = w.value

    turnover = np.sum(np.abs(w_opt - w_0))

    results = pd.DataFrame({
        "Asset": [f"Asset {i+1}" for i in range(n)],
        "w_current": w_0,
        "w_benchmark": w_b,
        "w_optimal": w_opt
    })

    print(results.round(4))
    print("Tracking Error Varianza:",
          (w_opt - w_b).T @ matriz_varianza @ (w_opt - w_b))
    print("Turnover:", turnover)