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

    print('result: ', result)
    return result, edges


def ford_fulkerson(graph: nx.DiGraph, source: int,
                   sink: int) -> Dict[Tuple[int, int], float]:
    edges = graph.edges
    num_edges = len(edges)
    flow = dict(edges)
    flow = {x: 0 for x in flow}
##    print('flow: ', flow)
    for x, y in edges:
        pass

    residual_graph = graph.copy()
    max_flow = 0
    while nx.has_path(residual_graph, source, sink):
        
        # choose a path
        path = next(nx.all_simple_paths(residual_graph, source, sink))
        print('path: ',path)
        
        # take the minimal additional flow of this path and the edges
        current_flow, current_edges = min_flow(residual_graph, path)
        max_flow += current_flow
        
        # update flow values, remove edge and add with new capacity
        for edge in current_edges:

            # update flow values
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
        print('max_flow: ', max_flow)
            

    return max_flow


graph = nx.DiGraph()
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


print(ford_fulkerson(graph, 0, 7))
