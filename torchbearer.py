"""
CS 460 – Algorithms: Final Programming Assignment
The Torchbearer

Student Name: Zakaria Abdullahi
Student ID:   820007650

INSTRUCTIONS
------------
- Implement every function marked TODO.
- Do not change any function signature.
- Do not remove or rename required functions.
- You may add helper functions.
- Variable names in your code must match what you define in README Part 5a.
- The pruning safety comment inside _explore() is graded. Do not skip it.

Submit this file as: torchbearer.py
"""

import heapq


# =============================================================================
# PART 1
# =============================================================================

def explain_problem():
    """
    Returns
    -------
    str
        Your Part 1 README answers, written as a string.
        Must match what you wrote in README Part 1.
    """
    return """ 
    A single shortest-path from S gives the cheapest path to each individual node, but the problem requires
        visiting all relics/nodes and then reaching the exit, meaning we need a full route.  
    Deciding in which order to visist the relics/nodes. Traversing in different orders produce different results 
         and we want the minimum overall cost.     
    Because the total cost depends on the sequence of relic/node visits, we must explore different possible orders
        to determine the minimum overall cost.
    """


# =============================================================================
# PART 2
# =============================================================================

def select_sources(spawn, relics, exit_node):
    """
    Parameters
    ----------
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    list[node]
        No duplicates. Order does not matter.
    """
    sources = []
    seen = set()

    for node in [spawn] + list(relics):
        if node not in seen:
            sources.append(node)
            seen.add(node)

    return sources


def run_dijkstra(graph, source):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
        graph[u] = [(v, cost), ...]. All costs are nonnegative integers.
    source : node

    Returns
    -------
    dict[node, float]
        Minimum cost from source to every node in graph.
        Unreachable nodes map to float('inf').
    """
    distances = {node: float("inf") for node in graph}
    distances[source] = 0

    pq = [(0, source)]

    while pq:
        current_dist, u = heapq.heappop(pq)

        if current_dist > distances[u]:
            continue

        for v, cost in graph.get(u, []):
            new_dist = current_dist + cost

            if new_dist < distances.get(v, float("inf")):
                distances[v] = new_dist
                heapq.heappush(pq, (new_dist, v))

    return distances


def precompute_distances(graph, spawn, relics, exit_node):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    dict[node, dict[node, float]]
        Nested structure supporting dist_table[u][v] lookups
        for every source u your design requires.
    """
    dist_table = {}
    sources = select_sources(spawn, relics, exit_node)

    for source in sources:
        distances = run_dijkstra(graph, source)
        dist_table[source] = {}

        for target in list(relics) + [exit_node]:
            dist_table[source][target] = distances.get(target, float("inf"))

    return dist_table


# =============================================================================
# PART 3
# =============================================================================

def dijkstra_invariant_check():
    """
    Returns
    -------
    str
        Your Part 3 README answers, written as a string.
        Must match what you wrote in README Part 3.

    """
    return """
        3A.) For nodes already finalized, their stored distance is the true cheapest distance from the source.
             For nodes not yet finalized, their stored distance is the current best known distance using paths that go through finalized nodes first.

        3B.) Initialization: The source starts with distance 0 becuase it costs nothing to reach itself. All other nodes start at infinity because no path has been found yet.
             Maintenance: Dijkstra chooses the unfinished node with the smallest known distance. Since all edge weights are nonnegative, any alternate path through another unfinished node cannot be cheaper later.
             Termination: When the algorithm finishes, every reachable finalized node has it's true shortest-path distance from the source. Unreachable nodes remain at infinity.

        3C.) Correct Dijkstra distances make the route planner compare relic orders using true minimum travel costs, so it's final route decision is based on those correct numbers.
    """


# =============================================================================
# PART 4
# =============================================================================

def explain_search():
    """
    Returns
    -------
    str
        Your Part 4 README answers, written as a string.
        Must match what you wrote in README Part 4.

    """
    return """
        The failure mode: Greedy can pick the nearest next relic, but the local choice may force a more expensive path later.
        Counter-example setup: Consider our graph example with source node S, exit node T, and relic nodes B,C, D. S->B=1, S->C=2, S->D=2, B->D=1, D->C=1, C->T=1, C->B=1, D->T=100.
        What greedy picks: Greedy starts at S and picks B first because S->B has a cost of 1 which is cheaper than our other options, S->C and S->D, which both have a cost of 2. It can then go from B->D->C->T for a total cost of 4.
        What optimal picks: The optimal route may opt to choose an order based on the whole remaining route, not just the nearest next relic.
        Why greedy loses: Greedy only minimizes the next step, while the problem needs the minimum total route across all relics and our exit.

        The algorithm must explore each possible order of relic vists because the total fuel cost depends on the routes order.
    """


# =============================================================================
# PARTS 5 + 6
# =============================================================================

def find_optimal_route(dist_table, spawn, relics, exit_node):
    """
    Parameters
    ----------
    dist_table : dict[node, dict[node, float]]
        Output of precompute_distances.
    spawn : node
    relics : list[node]
        Every node in this list must be visited at least once.
    exit_node : node
        The route must end here.

    Returns
    -------
    tuple[float, list[node]]
        (minimum_fuel_cost, ordered_relic_list)
        Returns (float('inf'), []) if no valid route exists.
    """
    def backtrack(current_node, collected_relics, fuel_cost, ordered_relic_list):
        if len(collected_relics) == len(relics):
            total_cost = fuel_cost + dist_table[current_node][exit_node]
            return total_cost, ordered_relic_list.copy()
        
        best_cost = float('inf')
        best_order = []

        for relic in relics:
            if relic not in collected_relics:

                 # choose
                collected_relics.add(relic)
                ordered_relic_list.append(relic)

                # explore
                route_cost, route_order = backtrack(relic, collected_relics, fuel_cost + dist_table[current_node][relic], ordered_relic_list)

                if route_cost < best_cost:
                    best_cost = route_cost
                    best_order = route_order
                    
                #backtrack
                ordered_relic_list.pop()
                collected_relics.remove(relic)

        return best_cost, best_order
    
    return backtrack(spawn, set(), 0, [])




def _explore(dist_table, current_loc, relics_remaining, relics_visited_order,
             cost_so_far, exit_node, best):
    """
    Recursive helper for find_optimal_route.

    Parameters
    ----------
    dist_table : dict[node, dict[node, float]]
    current_loc : node
    relics_remaining : collection
        Your chosen data structure from README Part 5b.
    relics_visited_order : list[node]
    cost_so_far : float
    exit_node : node
    best : list
        Mutable container for the best solution found so far.

    Returns
    -------
    None
        Updates best in place.

    TODO
    Implement: base case, pruning, recursive case, backtracking.

    REQUIRED: Add a 1-2 sentence comment near your pruning condition
    explaining why it is safe (cannot skip the optimal solution).
    This comment is graded.
    """
    pass


# =============================================================================
# PIPELINE
# =============================================================================

def solve(graph, spawn, relics, exit_node):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    tuple[float, list[node]]
        (minimum_fuel_cost, ordered_relic_list)
        Returns (float('inf'), []) if no valid route exists.

    TODO
    """
    pass


# =============================================================================
# PROVIDED TESTS (do not modify)
# Graders will run additional tests beyond these.
# =============================================================================

graph_1 = {
        'S': [('B', 1), ('C', 2), ('D', 2)],
        'B': [('D', 1), ('T', 1)],
        'C': [('B', 1), ('T', 1)],
        'D': [('B', 1), ('C', 1)],
        'T': []
    }
spawn = "S"
relics = ["B", "C", "D"]
exit_node = "T"

print(select_sources(spawn, relics, exit_node))
print(run_dijkstra(graph_1, spawn))
print(precompute_distances(graph_1, spawn, relics, exit_node))

# def _run_tests():
#     print("Running provided tests...")

#     # Test 1: Spec illustration. Optimal cost = 4.
#     graph_1 = {
#         'S': [('B', 1), ('C', 2), ('D', 2)],
#         'B': [('D', 1), ('T', 1)],
#         'C': [('B', 1), ('T', 1)],
#         'D': [('B', 1), ('C', 1)],
#         'T': []
#     }
#     cost, order = solve(graph_1, 'S', ['B', 'C', 'D'], 'T')
#     assert cost == 4, f"Test 1 FAILED: expected 4, got {cost}"
#     print(f"  Test 1 passed  cost={cost}  order={order}")

#     # Test 2: Single relic. Optimal cost = 5.
#     graph_2 = {
#         'S': [('R', 3)],
#         'R': [('T', 2)],
#         'T': []
#     }
#     cost, order = solve(graph_2, 'S', ['R'], 'T')
#     assert cost == 5, f"Test 2 FAILED: expected 5, got {cost}"
#     print(f"  Test 2 passed  cost={cost}  order={order}")

#     # Test 3: No valid path to exit. Must return (inf, []).
#     graph_3 = {
#         'S': [('R', 1)],
#         'R': [],
#         'T': []
#     }
#     cost, order = solve(graph_3, 'S', ['R'], 'T')
#     assert cost == float('inf'), f"Test 3 FAILED: expected inf, got {cost}"
#     print(f"  Test 3 passed  cost={cost}")

#     # Test 4: Relics reachable only through intermediate rooms.
#     # Optimal cost = 6.
#     graph_4 = {
#         'S': [('X', 1)],
#         'X': [('R1', 2), ('R2', 5)],
#         'R1': [('Y', 1)],
#         'Y': [('R2', 1)],
#         'R2': [('T', 1)],
#         'T': []
#     }
#     cost, order = solve(graph_4, 'S', ['R1', 'R2'], 'T')
#     assert cost == 6, f"Test 4 FAILED: expected 6, got {cost}"
#     print(f"  Test 4 passed  cost={cost}  order={order}")

#     # Test 5: Explanation functions must return non-placeholder strings.
#     for fn in [explain_problem, dijkstra_invariant_check, explain_search]:
#         result = fn()
#         assert isinstance(result, str) and result != "TODO" and len(result) > 20, \
#             f"Test 5 FAILED: {fn.__name__} returned placeholder or empty string"
#     print("  Test 5 passed  explanation functions are non-empty")

#     print("\nAll provided tests passed.")


# if __name__ == "__main__":
#     _run_tests()
