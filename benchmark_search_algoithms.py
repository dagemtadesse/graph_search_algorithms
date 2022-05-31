import timeit
from numpy import NaN
from load_graph_from_csv_file import roadMap
from graph_search_algorithms import BFS, DFS, a_star_search, calculate_cost, create_heuristic, dijkstra_search
# number of time each function is repeatedly  called to get the mean value
ITERATION = 10

def average(list): return sum(list) / len(list) if len(list) != 0 else NaN

def benchmark(graph, search_algorithm, arguments=None):
    searched_pairs = set()
    durations = []
    lengths = []

    for start in graph.vertices():
        for target in graph.vertices():
            if (start, target) in searched_pairs or (target, start) in searched_pairs:
                continue

            def test_function():
                if not arguments is None:
                    search_algorithm(graph, arguments, start, target)
                    return
                search_algorithm(graph, start, target)

            duration = timeit.Timer(
                test_function).timeit(number=ITERATION)

            duration /= ITERATION
            durations.append(duration)

            if not arguments is None:
                parent_tree = search_algorithm(graph, arguments, start, target)
            else:
                parent_tree = search_algorithm(graph, start, target)
            length = calculate_cost(graph, parent_tree, target)
            lengths.append(length)

            searched_pairs.add((start, target))

    return average(durations), average(lengths)


def test(h_func):
    for start in roadMap.vertices():
        for target in roadMap.vertices():
            dijkstra_result = dijkstra_search(roadMap, start, target)
            a_star_result = a_star_search(roadMap, h_func, start, target)

            dCost = calculate_cost(roadMap, dijkstra_result, target)
            aCost = calculate_cost(roadMap, a_star_result, target)

            assert(dCost == aCost)

if __name__ == '__main__':
    h_function = create_heuristic(roadMap)

    test(h_function)
    for algorithm in [BFS, DFS, dijkstra_search, a_star_search]:
        if(algorithm.__name__ == "a_star_search"):
            average_duration, average_lengths = benchmark(
                roadMap, algorithm, arguments=h_function)
        else:
            average_duration, average_lengths = benchmark(roadMap, algorithm,)
        print(algorithm.__name__)
        print("Average duration -> {}".format(average_duration))
        print("Average length between nodes-> {}".format(average_lengths))
