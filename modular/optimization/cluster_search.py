from typing import Any, Callable, Dict, List, Set, Tuple

Cluster = Set[str]
Clusterization = List[Set[str]]


def symmetric_difference_size(a: Cluster, b: Cluster) -> int:
    return len(a.symmetric_difference(b))


def match_clusters(
    clusterization_a: Clusterization,
    clusterization_b: Clusterization,
) -> Dict[int, int]:
    """
    Greedily matches each cluster in clusterization_a to a cluster in clusterization_b
    by minimizing symmetric difference size (1-to-1 when possible).

    When |A| > |B|, remaining unmatched A-clusters are assigned to the B-cluster
    with the greatest intersection.

    Returns a dict mapping A-cluster-index -> B-cluster-index.
    """
    available_b = set(range(len(clusterization_b)))
    matching: Dict[int, int] = {}

    for i, cluster_a in enumerate(clusterization_a):
        if not available_b:
            break
        best_j = min(
            available_b,
            key=lambda j: symmetric_difference_size(cluster_a, clusterization_b[j]),
        )
        matching[i] = best_j
        available_b.remove(best_j)

    # Second pass: assign unmatched A-clusters when |A| > |B|
    for i in range(len(clusterization_a)):
        if i not in matching:
            best_j = max(
                range(len(clusterization_b)),
                key=lambda j: len(clusterization_a[i] & clusterization_b[j]),
            )
            matching[i] = best_j

    return matching


def generate_path(
    clusterization_a: Clusterization,
    clusterization_b: Clusterization,
) -> List[Clusterization]:
    """
    Generates the full sequence of clusterization states going from clusterization_a
    to clusterization_b, where each step moves exactly one element between clusters.

    Intermediate states are indexed using clusterization_b's cluster ordering.
    Returns a list of length N+1, where N is the number of element moves required.

    Precondition: every element appears in exactly one cluster in both A and B,
    and the set of all elements is the same in both clusterizations.
    """
    matching = match_clusters(clusterization_a, clusterization_b)

    # Project clusterization_a onto B-cluster-index space
    n_b = len(clusterization_b)
    current: Clusterization = [set() for _ in range(n_b)]
    for i, cluster_a in enumerate(clusterization_a):
        current[matching[i]] |= cluster_a

    # Map each element to its target B-cluster index
    element_to_target: Dict[str, int] = {
        element: j
        for j, cluster_b in enumerate(clusterization_b)
        for element in cluster_b
    }

    # Collect elements that are not yet in their target cluster
    moves: List[Tuple[str, int, int]] = [
        (element, j, element_to_target[element])
        for j in range(n_b)
        for element in sorted(current[j])  # sorted for determinism
        if element in element_to_target and element_to_target[element] != j
    ]

    # Build path: one state snapshot per move
    path: List[Clusterization] = [[s.copy() for s in current]]
    for element, from_j, to_j in moves:
        current[from_j].discard(element)
        current[to_j].add(element)
        path.append([s.copy() for s in current])

    return path


def select_intermediate_steps(
    path: List[Clusterization],
    max_steps: int = 3,
) -> List[Clusterization]:
    """
    Selects up to max_steps equidistant intermediate states from the path,
    excluding the first (start) and last (end) states.

    If the total number of moves N <= max_steps, all intermediate states are returned.
    Otherwise, the states at positions N//4, N//2, and 3*N//4 in the path are returned.
    """
    n = len(path) - 1  # total number of moves

    if n <= max_steps:
        return path[1:-1]

    indices = [n // 4, n // 2, 3 * n // 4]
    return [path[i] for i in indices]


def cluster_search(
    clusterization_a: Clusterization,
    clusterization_b: Clusterization,
    metric: Callable[[Clusterization], Any],
    dist
) -> Dict[str, Any]:
    """
    Finds the path from clusterization_a to clusterization_b by single-element moves,
    selects up to 3 equidistant intermediate states, and evaluates the metric on each.

    Args:
        clusterization_a: Starting clusterization as a list of sets of strings.
        clusterization_b: Target clusterization as a list of sets of strings.
        metric: Function that takes a Clusterization and returns any comparable value.
                Evaluated only on intermediate steps, never on A or B themselves.

    Returns:
        A dict with:
            "total_steps":        total number of single-element moves in the path.
            "intermediate_steps": selected intermediate clusterization states.
            "metric_values":      metric evaluated on each intermediate step.
    """
    path = generate_path(clusterization_a, clusterization_b)
    intermediate_steps = select_intermediate_steps(path)
    metric_values = [metric(step,dist) for step in intermediate_steps]

    return {
        "total_steps": len(path) - 1,
        "intermediate_steps": intermediate_steps,
        "metric_values": metric_values,
    }
    
if __name__ == "__main__":
    # Example usage
    clusterization_a = [{0, 1, 3}, {2, 4}]
    clusterization_b = [{1}, {0, 2, 3, 4}]

    def example_metric(clusterization: Clusterization) -> int:
        return sum(len(cluster) for cluster in clusterization)
    
    def example_metric2(clusterization:Clusterization):
        distances=[[0,1,3,1,3],[1,0,4,1,3],[3,4,0,3,1],[1,1,3,0,5],[3,3,1,5,0]]
        for cluster in clusterization:
                dist=0
                for i in cluster:
                    i =int(i)
                    for j in cluster:
                        j=int(j)
                        dist=dist+distances[i][j]
        return dist
                    


    result = cluster_search(clusterization_a, clusterization_b, example_metric2)
    print(result)
