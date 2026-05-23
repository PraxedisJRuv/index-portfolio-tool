from modular.optimization.cluster_search import cluster_search

def clusterization_make(clustering):
    """
    Makes result from cpp into a list[set()] 
    that cluster search can use
    """
    medoids=list(set(clustering))
    clusterization=[]
    for i in medoids:
        aux_set=set()
        for j in range(len(clustering)):
            if clustering[j]==i:
                aux_set.add(j)
        clusterization.append(aux_set)
    print(clusterization)
    return clusterization

def dist_based_metric(clusterization, dist):
    """
    Evaluate the clustering regarding a distance
    """
    total=0
    for cluster in clusterization:
        cluster=list(cluster)
        min =1000000000
        for i in range(len(cluster)):
            sum=0
            for j in range(len(cluster)):
                sum=sum+dist[cluster[i]][cluster[j]]
            if sum<=min:
                min=sum
        total=total+min
    return total

def get_medoids(clusterization, dist):
     """ 
     Get the medoids of a cluster_search() step
     """
     medoids=[]
     for cluster in clusterization:
        cluster=list(cluster)
        min =1000000000
        for i in range(len(cluster)):
            sum=0
            for j in range(len(cluster)):
                sum=sum+dist[cluster[i]][cluster[j]]
            if sum<=min:
                min=sum
                medoid=i
        medoids.append(medoid)
     print(medoids)
     return medoids

def get_minimal_intermediate_steps(result):
     """
     Gets the step with the least metric, in this case, distance
     """
     optimal=result["metric_values"][0]
     index=0
     for i in range(len(result["metric_values"])):
        if result["metric_values"][0]<=optimal:
             optimal=result["metric_values"][i]
             index=i
     print(index)
     return index

def get_best_medoids(clusterization, dist):
    index=get_minimal_intermediate_steps(clusterization)
    best=clusterization["intermediate_steps"][index]
    medoids=get_medoids(best,dist)
    return(medoids)

def get_best_minimal_medoids_by_metric(clustering_a, clustering_b, distance):
    clusterization_a=clusterization_make(clustering_a)
    clusterization_b=clusterization_make(clustering_b)
    results=cluster_search(clusterization_a,clusterization_b,dist_based_metric,distance)
    print(results)
    medoids=get_best_medoids(results,distance)
    print(medoids)
    return medoids