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
        result = min(result, graph.get_edge_data(source, end)["capacity"])
        edges.append((source, end))
    return result, edges


def ford_fulkerson(graph: nx.DiGraph, source: int,
                   sink: int) -> Dict[Tuple[int, int], float]:
    edges = graph.edges
    num_edges = len(edges)
    flow = dict(edges)
    flow = {x: 0 for x in flow}
    for x, y in edges:
        pass

    residual_graph = graph.copy()

    while nx.has_path(residual_graph, source, sink):
        # choose a path
        path = next(nx.all_simple_paths(residual_graph, source, sink))

        # take the minimal additional flow of this path and the edges
        current_flow, current_edges = min_flow(residual_graph, path)

        # update flow values, remove edge and add with new capacity
        for edge in current_edges:

            # update flow values
            flow[edge] += current_flow
            vertice_from, vertice_to = edge

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

    return flow


graph = nx.DiGraph()
graph.add_edge(0, 7, capacity=10.9)
graph.add_edge(7, 6, capacity=5.6)
graph.add_edge(0, 6, capacity=2)
print(ford_fulkerson(graph, 0, 6))
