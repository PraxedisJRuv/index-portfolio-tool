from copy import deepcopy
from typing import Any, List
import random

ENTITIES: List[str] = []
CLUSTERS: List[int] = []
MAX_ITER: int = 0
N_CLUSTERS: int = 3


def select_randomly(elements: List[Any], n_selections: int = 1):
    if n_selections == 1:
        return random.choice(elements)
    # prefer sampling without replacement when possible
    if n_selections <= len(elements):
        return random.sample(elements, k=n_selections)
    return random.choices(elements, k=n_selections)


def shuffle():
    random.shuffle


def step_process(
    entities: List[str],
    clusters: List[int],
    n_clusters: int,
    metrics: List[callable] | None = None,
    acceptance_criteria: callable | None = None,
):
    unique_cluster_ids = sorted(set(clusters))
    if not unique_cluster_ids:
        return clusters

    selected_clusters = select_randomly(unique_cluster_ids, n_clusters)

    selected_entity_indices: List[int] = []
    for cluster_id in selected_clusters:
        indices = [i for i, c in enumerate(clusters) if c == cluster_id]
        if not indices:
            continue
        chosen_idx = select_randomly(indices, 1)
        selected_entity_indices.append(chosen_idx)

    random.shuffle(selected_clusters)

    final_clusters = deepcopy(clusters)
    for idx, entity_idx in enumerate(selected_entity_indices):
        final_clusters[entity_idx] = selected_clusters[idx]

    results = []
    if metrics:
        for metric in metrics:
            results.append(metric(entities, final_clusters))

    if acceptance_criteria:
        accepted = acceptance_criteria(clusters, final_clusters, results)
        return final_clusters if accepted else clusters

    return final_clusters


def main():
    i = 0
    new_clusters: List[int] = deepcopy(CLUSTERS)
    while i < MAX_ITER:
        new_clusters = step_process(entities=ENTITIES, clusters=new_clusters, n_clusters=N_CLUSTERS)
        i += 1


if __name__ == "__main__":
    main()
