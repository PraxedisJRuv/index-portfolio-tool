import numpy as np
import kmedoids_cpp

dist = np.array([
    [1,0.5,0,0,0],
    [0.5,1,0,0,0],
    [0,0,1,0.5,0.5],
    [0,0,0.5,1,0],
    [0,0,0.5,0,1]
], dtype=float)

medoids = [0,1]

result = kmedoids_cpp.run_kmedoids(dist, medoids)

print(result)

"""
        {1,0.5,0,0,0},
        {0.5,1,0,0,0},
        {0,0,1,0.5,0.5},
        {0,0,0.5,1,0},
        {0,0,0.5,0,1}
"""