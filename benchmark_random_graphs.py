import string
import random
import matplotlib.pyplot as plt
from benchmark_search_algoithms import benchmark, create_heuristic
from graph_search_algorithms import BFS, DFS, a_star_search, dijkstra_search

from graph_implementation import Graph

NODE_SIZE = 20
MAX_EDGE_COUNT = 4

def generate_graph_data(node_size):
    graph = Graph()
    
    for _ in range(node_size):
        node = "".join(random.choice(string.ascii_uppercase) for i in range(5))
        graph.add_node(node)
        
    for vertex in graph.vertices():
        max_edge = random.randint(1, MAX_EDGE_COUNT)
        for _ in range(max_edge):
            not_vertex = filter(lambda vert: vert != vertex, graph.vertices())
            right = random.choice(list(not_vertex))
            graph.add_edge(vertex, right, random.randint(50, 100))
        
    return graph    
    
    
if __name__ == "__main__":
    durations = []
    costs = []
    
    for i in range(1, 5):
        generatedGraph = generate_graph_data(NODE_SIZE * i)
        h_function = create_heuristic(generatedGraph)
        
        lapDuration = []
        lapCost = []
        for algorithm in [BFS, DFS, dijkstra_search, a_star_search]:
            if(algorithm.__name__ == "a_star_search"):
                average_duration, average_lengths = benchmark(
                    generatedGraph, algorithm, arguments=h_function)
            else:
                average_duration, average_length = benchmark(generatedGraph, algorithm,)
            lapDuration.append(average_duration)
            lapCost.append(average_length)
        durations.append(lapDuration)
        costs.append(lapCost)
        
    zippedDurations = list(zip(*durations))
    zippedLength =list(zip(*costs))
    
    algorithm_names = ['BFS', 'DFS', 'dijkstra\'s search', 'a* search']
    
    fig, axs = plt.subplots(2)
    fig.suptitle('Average search duration(1st) and Average path length (2nd)')
    
    x = [1, 2, 3, 4]
    for i in range(len(zippedDurations)):
        axs[0].plot(x, zippedDurations[i], label = algorithm_names[i])
        axs[1].plot(x, zippedLength[i], label = algorithm_names[i])
        
    plt.legend()
    plt.show()
    
