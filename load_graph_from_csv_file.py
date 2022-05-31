from  graph_implementation import Graph
import sys
from graph_search_algorithms import a_star_search, dijkstra_search, BFS, DFS, reconstruct_path

def read_graph(file_path):
    graph = Graph()

    with open(file_path) as file:
        def capitalize(strNode): return strNode.capitalize()
        while(True):
            line = file.readline()
            if len(line) == 0:
                break

            left, right, weight = line[:-1].split(',')
            nodes = map(capitalize, [left, right])
            graph.add_edge(*nodes, weight= int(weight))
            
    return graph

path = sys.argv[1] if len(sys.argv) > 1 else 'graph.csv'
roadMap = read_graph(path)

if __name__ == "__main__":
    
    if len(sys.argv) < 2:
        print("Please provide the path to the graph")
        print("using default graph.csv")
    
    print(roadMap.adjacencies('Bucharest'), "\n\n")
    
    dijkstra_result = dijkstra_search(roadMap, 'Oradea', 'Bucharest')
    print("Dijkstra", reconstruct_path(dijkstra_result, 'Bucharest'), "\n\n")
    
    a_star_result = a_star_search(roadMap, lambda x, y: 0, 'Oradea', "Bucharest")
    print("A*", reconstruct_path(a_star_result, "Bucharest"), "\n\n")
    
    bfs_result = BFS(roadMap, 'Oradea', "Bucharest")
    print("BFS", reconstruct_path(bfs_result, "Bucharest"), "\n\n")
    
    dfs_result = DFS(roadMap, 'Oradea', "Bucharest")
    print("DFS", reconstruct_path(dfs_result, "Bucharest"), "\n\n")
    
    
    
