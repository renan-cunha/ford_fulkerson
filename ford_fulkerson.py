import networkx as nx
from typing import Tuple, Dict, List


class FordFulkerson:
    def __init__(self, graph: nx.DiGraph, source_vertice: int,
                 sink_vertice: int):
        self.graph = graph
        self.source_vertice = source_vertice
        self.sink_vertice = sink_vertice
        self.residual_graph = graph.copy()

        while nx.has_path(self.residual_graph, self.source_vertice,
                          self.sink_vertice):

            # choose a path
            path = next(nx.all_simple_paths(self.residual_graph,
                                            self.source_vertice,
                                            self.sink_vertice))

            # take the minimal additional flow of this path and the edges
            path_flow, path_edges = self.__min_flow(path)

            # update flow values, remove edge and add with new capacity
            for edge in path_edges:
                vertice_from, vertice_to = edge #(u,v)

                # update capacity value
                capacity = self.get_capacity(vertice_from, vertice_to)

                # remove edge
                self.residual_graph.remove_edge(vertice_from, vertice_to)

                # add edge with new capacity if it is greater than 0
                new_capacity = capacity - path_flow
                if new_capacity > 0:
                    self.residual_graph.add_edge(vertice_from, vertice_to,
                                                 capacity=new_capacity)

                # add anti parallel edge
                residual_graph_edges = self.residual_graph.edges
                if (vertice_to, vertice_from) in residual_graph_edges:
                    capacity = self.get_capacity(vertice_to, vertice_from)
                    self.residual_graph.remove_edge(vertice_to, vertice_from)
                else:
                    capacity = 0
                capacity += path_flow

                self.residual_graph.add_edge(vertice_to, vertice_from,
                                             capacity=capacity)

    def get_capacity(self, vertice_from: int, vertice_to: int) -> float:
        """Returns the capacity of an edge"""
        return self.residual_graph.get_edge_data(vertice_from,
                                                 vertice_to)['capacity']

    def get_flow(self) -> Dict[Tuple[int, int], float]:
        """Returns a dict with flow in each edge"""
        result = {}
        residual_graph_edges = self.residual_graph.edges
        graph_edges = self.graph.edges

        for residual_edge in residual_graph_edges:
            vertice_from, vertice_to = residual_edge
            edge = vertice_to, vertice_from
            if edge in graph_edges:
               result[edge] = self.get_capacity(vertice_from, vertice_to)

        return result

    def get_max_flow(self) -> float:
        """Return max float value"""
        residual_graph_edges = self.residual_graph.edges

        max_flow = 0.0
        for edge in residual_graph_edges:
            vertice_from, vertice_to = edge
            # inverted order in residual graph
            if vertice_to == self.source_vertice:
                max_flow += self.get_capacity(vertice_from, vertice_to)

        return max_flow

    def __min_flow(self, path_vertices: List[int]) -> Tuple[float,
                                                            List[Tuple[int, int]]]:
        """Returns the min additional flow of the path"""
        num_vertices = len(path_vertices)
        result = float("inf")
        edges: List[Tuple[int, int]] = []
        for i in range(num_vertices-1):
            source = path_vertices[i]
            end = path_vertices[i+1]
            result = min(result, self.residual_graph.get_edge_data(
                                                    source, end)['capacity'])
            edges.append((source, end))
        return result, edges


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
#graph.add_edge(0, 1, capacity=10)
#graph.add_edge(0, 3, capacity=10)
#graph.add_edge(1, 2, capacity=4)
#graph.add_edge(1, 3, capacity=2)
#graph.add_edge(1, 4, capacity=8)
#graph.add_edge(2, 5, capacity=10)
#graph.add_edge(3, 4, capacity=9)
#graph.add_edge(4, 2, capacity=6)
#graph.add_edge(4, 5, capacity=10)

ff = FordFulkerson(graph, 0, 7)
print(ff.get_max_flow())
print(ff.get_flow())
from networkx.algorithms.flow import maximum_flow
print(maximum_flow(graph, 0, 7))
