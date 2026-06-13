import kmedoids_cpp

def clustering_medoids(dist:list[list[float]], num_medoids:int)->list[int]:
    """
    A mediator bewtween cpp and the main oython piepline. This allows the main python scripts to 
    handle the cpp process as if it was pythons 
    """
    medoids=[0]*num_medoids
    for i in range(num_medoids):
        medoids[i]=i
    result = kmedoids_cpp.run_kmedoids(dist, medoids)
    return result