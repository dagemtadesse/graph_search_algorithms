import timeit
import functools
from pprint import pprint
from graph_implementation import Graph
from graph_search_algorithms import a_star_search, betweenness_score, calculate_cost, dijkstra_search, create_heuristic
from load_graph_from_csv_file import roadMap


def closeness_centrality(graph: Graph, targetNode, useAStar=False, heuristic_func=None):
    distances = []
    for node in graph.vertices():
        if node == targetNode:
            continue
        if not useAStar:
            parent_tree = dijkstra_search(graph, targetNode, node)
        else:
            parent_tree = a_star_search(
                graph, heuristic_func, targetNode, node)

        distance = calculate_cost(graph, parent_tree, node)
        distances.append(distance)

    return 1 / sum(distances)


def betweenness_centrality(graph: Graph, node, useAStar=False, heuristic_func=None):
    total_b_score = 0

    vertices = graph.vertices()
    for index, startNode in enumerate(vertices):
        for targetNode in vertices[index + 1:]:
            if targetNode == node or startNode == node:
                continue

            if not useAStar:
                parent_graph = dijkstra_search(
                    graph, startNode, target=targetNode, multiple=True)
            else:
                parent_graph = a_star_search(
                    graph, heuristic_func, startNode, targetNode,)

            b_score = betweenness_score(graph, parent_graph, targetNode, node)
            total_b_score += b_score

    return total_b_score


if __name__ == "__main__":

    durations = {"dijkstra_closeness": 0, "a_star_closeness": 0,
                 "dijkstra_betweenness": 0, "a_star_betweenness": 0}

    centrality = {"dijkstra_closeness": {}, "a_star_closeness": {},
                  "dijkstra_betweenness": {}, "a_star_betweenness": {}}

    h_function = create_heuristic(roadMap)

    def dijkstra_closeness(vertex):
        score = closeness_centrality(roadMap, vertex)
        centrality["dijkstra_closeness"][vertex] = score

    def a_star_closeness(vertex):
        score = closeness_centrality(
            roadMap, vertex, useAStar=True, heuristic_func=h_function)
        centrality["a_star_closeness"][vertex] = score

    def dijkstra_betweenness(vertex):
        score = betweenness_centrality(roadMap, vertex)
        centrality["dijkstra_betweenness"][vertex] = score

    def a_star_betweenness(vertex):
        score = betweenness_centrality(
            roadMap, vertex, useAStar=True, heuristic_func=h_function)
        centrality["a_star_betweenness"][vertex] = score

    for vertex in roadMap.vertices():
        durations["dijkstra_closeness"] += timeit.Timer(
            functools.partial(dijkstra_closeness, vertex)).timeit(number = 1)
        durations["dijkstra_betweenness"] += timeit.Timer(
            functools.partial(dijkstra_betweenness, vertex)).timeit(number = 1)
        
        durations["a_star_closeness"] += timeit.Timer(
            functools.partial(a_star_closeness, vertex)).timeit(number = 1)
        durations["a_star_betweenness"] += timeit.Timer(
            functools.partial(a_star_betweenness, vertex)).timeit(number = 1)
       
    pprint(roadMap.vertices()) 
    # print("durations")
    # pprint(durations)
    # print("centrality scores")
    # pprint(centrality)
