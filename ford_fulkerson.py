import networkx as nx
from typing import Tuple, Dict, List


def min_flow(graph: nx.DiGraph,
             path_vertices: List[int]) -> Tuple[float, List[Tuple[int, int]]]:
    """Returns the min additional flow of the path"""
    num_vertices = len(path_vertices)
    result = float("inf")
    edges: List[Tuple[int, int]] = []
    for i in range(num_vertices-1):
        source = path_vertices[i]
        end = path_vertices[i+1]
        result = min(result, graph.get_edge_data(source, end)['capacity'])
        edges.append((source, end))

    return result, edges


def ford_fulkerson(graph: nx.DiGraph, source: int,
                   sink: int) -> int:
    edges = graph.edges
    flow = dict(edges)
    flow = {x: 0 for x in flow}

    residual_graph = graph.copy()

    max_flow = 0
    while nx.has_path(residual_graph, source, sink):
        
        # choose a path
        path = next(nx.all_simple_paths(residual_graph, source, sink))

        # take the minimal additional flow of this path and the edges
        current_flow, current_edges = min_flow(residual_graph, path)
        max_flow += current_flow
        
        # update flow values, remove edge and add with new capacity
        for edge in current_edges:

            # update flow values
            if edge not in flow:
                flow[edge] = 0
            flow[edge] += current_flow

            vertice_from, vertice_to = edge #(u,v)

            # update capacity value
            capacity = residual_graph.get_edge_data(vertice_from,
                                                    vertice_to)['capacity']

            capacity -= current_flow

            # remove edge
            residual_graph.remove_edge(vertice_from, vertice_to)

            # add edge with new capacity if it is greater than 0
            if capacity > 0:
                residual_graph.add_edge(vertice_from, vertice_to,
                                        capacity=capacity)

            #add flow edge
            residual_graph.add_edge(vertice_to, vertice_from, capacity=flow[edge])

            if (vertice_to, vertice_from) in edges:
                residual_graph.remove_edge(vertice_to, vertice_from)

    return max_flow


graph = nx.DiGraph()

# Ex. 1
graph.add_edge(0, 1, capacity=13)
graph.add_edge(0, 3, capacity=10)
graph.add_edge(0, 5, capacity=10)
graph.add_edge(1, 2, capacity=24)
graph.add_edge(2, 4, capacity=1)
graph.add_edge(2, 7, capacity=9)
graph.add_edge(3, 1, capacity=5)
graph.add_edge(3, 5, capacity=15)
graph.add_edge(3, 6, capacity=7)
graph.add_edge(4, 6, capacity=6)
graph.add_edge(4, 7, capacity=13)
graph.add_edge(5, 6, capacity=15)
graph.add_edge(6, 7, capacity=16)

#Ex. 2
# graph.add_edge(0, 1, capacity=10)
# graph.add_edge(0, 3, capacity=10)
# graph.add_edge(1, 2, capacity=4)
# graph.add_edge(1, 3, capacity=2)
# graph.add_edge(1, 4, capacity=8)
# graph.add_edge(2, 5, capacity=10)
# graph.add_edge(3, 4, capacity=9)
# graph.add_edge(4, 2, capacity=6)
# graph.add_edge(4, 5, capacity=10)

print(ford_fulkerson(graph, 0, 7))
