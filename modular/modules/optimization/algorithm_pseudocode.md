# Cluster Search Algorithm — Pseudocode

## Types

```
Cluster          = Set<String>
Clusterization   = List<Cluster>
Step             = (element: String, from_cluster: Int, to_cluster: Int)
Path             = List<Clusterization>
```

A **step** is defined as removing one element from a cluster and inserting it into a different cluster, producing a new valid clusterization.

---

## 1. Symmetric Difference Distance

```
FUNCTION symmetric_difference_size(a: Cluster, b: Cluster) -> Int
    RETURN |a △ b|   // cardinality of the symmetric difference
END FUNCTION
```

---

## 2. Cluster Matching (Greedy)

Maps each cluster in `A` to the most similar cluster in `B` using symmetric difference as the distance measure.

```
FUNCTION match_clusters(A: Clusterization, B: Clusterization) -> Map<Int, Int>
    available ← {0, 1, ..., |B| - 1}
    matching  ← {}

    // First pass: 1-to-1 greedy matching
    FOR i FROM 0 TO |A| - 1:
        IF available is empty: BREAK
        best_j ← argmin_{j ∈ available} symmetric_difference_size(A[i], B[j])
        matching[i] ← best_j
        available.remove(best_j)

    // Second pass: unmatched A-clusters (only when |A| > |B|)
    FOR i FROM 0 TO |A| - 1:
        IF i NOT IN matching:
            best_j ← argmax_{j ∈ 0..|B|-1} |A[i] ∩ B[j]|
            matching[i] ← best_j

    RETURN matching
END FUNCTION
```

**Edge cases:**
| Condition | Behaviour |
|-----------|-----------|
| `\|A\| == \|B\|` | Clean 1-to-1 matching; every B-cluster gets exactly one A-cluster. |
| `\|A\| < \|B\|` | Some B-clusters have no A-counterpart; they start empty and receive elements via moves. |
| `\|A\| > \|B\|` | After the first pass, unmatched A-clusters are merged into the B-cluster with the most overlap. |

---

## 3. Path Generation

Transforms `A` into `B` by moving one element at a time.
States are represented using B-cluster indices (0 to `|B| - 1`).

```
FUNCTION generate_path(A: Clusterization, B: Clusterization) -> Path
    matching ← match_clusters(A, B)

    // Project A into B-cluster-index space
    current ← [∅, ∅, ..., ∅]   // |B| empty sets
    FOR i FROM 0 TO |A| - 1:
        j ← matching[i]
        current[j] ← current[j] ∪ A[i]

    // Build element → target-B-cluster map
    element_to_target ← {}
    FOR j FROM 0 TO |B| - 1:
        FOR EACH element IN B[j]:
            element_to_target[element] ← j

    // Identify elements that are not yet in their target cluster
    moves ← []
    FOR j FROM 0 TO |B| - 1:
        FOR EACH element IN current[j]:
            target_j ← element_to_target[element]
            IF target_j ≠ j:
                moves.append( (element, from=j, to=target_j) )

    // Build path: one state snapshot per move
    path ← [ copy(current) ]
    FOR EACH (element, from_j, to_j) IN moves:
        current[from_j].remove(element)
        current[to_j].add(element)
        path.append( copy(current) )

    RETURN path   // path[0] ≈ A (in B-index space), path[-1] = B
END FUNCTION
```

**Total steps:** `|path| - 1` = number of elements whose cluster assignment differs between A and B (after matching).

**Precondition:** every element appears in exactly one cluster in both A and B, and the set of all elements is identical in both clusterizations.

---

## 4. Intermediate Step Selection

Selects up to 3 equidistant intermediate states, excluding the start and end.

```
FUNCTION select_intermediate_steps(path: Path, max_steps: Int = 3) -> List<Clusterization>
    N ← |path| - 1   // total number of moves

    IF N ≤ max_steps:
        RETURN path[1 .. N-1]          // all true intermediates (excludes start and end)
    ELSE:
        indices ← [N//4, N//2, 3*N//4]
        RETURN [path[i] FOR i IN indices]
END FUNCTION
```

**Boundary guarantees (when N > 3):**
- `N//4 ≥ 1` → never the start state.
- `3*N//4 < N` → never the end state.

---

## 5. Main Function: `cluster_search`

```
FUNCTION cluster_search(
    A      : Clusterization,
    B      : Clusterization,
    metric : Clusterization → Any
) -> Dict

    path               ← generate_path(A, B)
    intermediate_steps ← select_intermediate_steps(path)
    metric_values      ← [ metric(step) FOR step IN intermediate_steps ]

    RETURN {
        "total_steps":        |path| - 1,
        "intermediate_steps": intermediate_steps,
        "metric_values":      metric_values
    }
END FUNCTION
```

**Notes:**
- `metric` is evaluated **only** on the selected intermediate steps — never on `A` or `B` themselves.
- If `A == B`, `total_steps = 0` and both lists are empty.

---

## 6. Worked Example

```
A = [ {"alice", "bob", "carol"},   {"dave", "eve"} ]
B = [ {"alice", "bob"},            {"carol", "dave", "eve"} ]
```

### Step 1 — `match_clusters(A, B)`

```
symmetric_difference_size( A[0], B[0] ) = |{carol}|             = 1
symmetric_difference_size( A[0], B[1] ) = |{alice, bob, dave, eve}| = 4
symmetric_difference_size( A[1], B[0] ) = |{alice, bob, dave, eve}| = 4
symmetric_difference_size( A[1], B[1] ) = |{carol}|             = 1

Greedy first pass:
  i=0: best available B-cluster for A[0] is B[0] (cost 1)  →  matching[0] = 0
  i=1: best available B-cluster for A[1] is B[1] (cost 1)  →  matching[1] = 1

matching = { 0: 0, 1: 1 }
```

### Step 2 — `generate_path`

```
current[0] ← A[0] = {"alice", "bob", "carol"}
current[1] ← A[1] = {"dave", "eve"}

element_to_target:
  alice→0,  bob→0,  carol→1,  dave→1,  eve→1

Moves from current:
  current[0]: alice stays (→0), bob stays (→0), carol moves (→1)
  current[1]: dave stays (→1), eve stays (→1)

moves = [ ("carol", from=0, to=1) ]

path[0] = [ {"alice","bob","carol"},  {"dave","eve"} ]           ← initial (= A)
path[1] = [ {"alice","bob"},          {"carol","dave","eve"} ]   ← final   (= B)
```

### Step 3 — `select_intermediate_steps`

```
N = 1  →  N ≤ 3  →  return path[1:-1] = []
```

No intermediate states exist: a single move takes us directly from A to B.

### Result

```json
{
  "total_steps": 1,
  "intermediate_steps": [],
  "metric_values": []
}
```
