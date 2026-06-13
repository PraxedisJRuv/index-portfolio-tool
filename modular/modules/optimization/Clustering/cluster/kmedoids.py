import cluster_module_cpp

def clustering_medoids(dist:list[list[float]], num_medoids:list[int])->list[int]:
    medoids=[0]*num_medoids
    for i in range(num_medoids):
        medoids[i]=i
    result = cluster_module_cpp.run_clustering(dist, medoids)
    return result

def evaluate_objective_f(dist:list[list[float]], clusterization:list[int])->float:
    obj=0
    for i in range (len(clusterization)):
        obj=dist[i][clusterization[i]]
    return obj