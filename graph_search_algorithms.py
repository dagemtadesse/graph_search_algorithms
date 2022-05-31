from collections import deque
from graph_implementation  import Graph

def BFS(graph, start, target=None):
    visited = set([start])
    parent = Graph()
    queue = deque([start])
    
    while queue:
        current_node = queue.pop()
        if current_node == target:
            return parent 
        
        for adjacent in graph.adjacencies(current_node):
            if  not adjacent in visited:
                parent.remove_edges(adjacent)
                parent.add_edge(adjacent, current_node, directed=True)
                # parent[adjacent] = current_node
                visited.add(adjacent)
                queue.appendleft(adjacent)

    return parent

def DFS(graph, start, target=None):
    stack = [start]
    explored = set()
    parent = Graph()

    while len(stack) > 0:
        current = stack.pop()
        explored.add(current)
        if current == target:
            return parent
        
        for adjacent in graph.adjacencies(current):
            if not adjacent in explored:
                parent.remove_edges(adjacent)
                parent.add_edge(adjacent, current, directed=True)
                stack.append(adjacent)
    return parent


def dijkstra_search(graph, source, target=None, multiple=False):

    def min(cost_func, vertices):
        return sorted(vertices, key=lambda vertex: cost_func[vertex])[0]

    vertices = graph.vertices()
    cost = {}
    parent_graph = Graph()

    for vertex in vertices:
        cost[vertex] = float('inf')
    cost[source] = 0

    while vertices:
        current_node = min(cost, vertices)
        vertices.remove(current_node)

        for adjacent in graph.adjacencies(current_node):
            relax(cost, parent_graph, current_node, adjacent,
                  graph.weight(current_node, adjacent), multiple)

    return parent_graph


def relax(cost_map, parent: Graph, parent_node, node, weight, multiple=False):
    alter_cost = cost_map[parent_node] + weight

    if cost_map[node] > alter_cost:
        cost_map[node] = alter_cost
        parent.remove_edges(node)
        parent.add_edge(node, parent_node, directed=True)
        return True

    elif multiple and cost_map[node] == alter_cost:
        parent.add_edge(node, parent_node, directed=True)
        return True

    return False

def betweenness_score(graph, parent_graph, target, in_between_node):
    # traverse the parent graph using DFS algorithm and count the number of time the shortest paths
    # pass through the in_between_node and the total number of path
    stack = [target]
    total_paths = 0
    paths_containing_in_between_node = 0

    while stack:
        current = stack.pop()

        if current == in_between_node:
            # there's a path passing through the in_between_node
            paths_containing_in_between_node += 1

        parents = parent_graph.adjacencies(current)
        if parents is None or (parents == {}):
            # the path ended
            total_paths += 1
            continue

        for parent in parents.keys():
            stack.append(parent)

    return (paths_containing_in_between_node / total_paths) if total_paths != 0 else 0

def a_star_search(graph, heuristic, start, goal, multiple=False):

    def min(vertices):
        return sorted(vertices,
                      key=lambda vertex: heuristic(vertex, goal) + g_score[vertex])[0]

    open_set = [start]
    parent = Graph()
    g_score = {}

    for vert in graph.vertices():
        g_score[vert] = float('inf')
    g_score[start] = 0

    while len(open_set) > 0:
        
        current = min(open_set )
        if current == goal:
            return parent

        open_set.remove(current)
        for neighbor in graph.adjacencies(current):
            relaxed = relax(g_score, parent, current, neighbor,
                                 graph.weight(current, neighbor), multiple)
            
            if relaxed and neighbor not in open_set:
                open_set.append(neighbor)

    return parent

def calculate_cost(graph, parent_graph, current,):
    length = 0
    while True:
        parents = parent_graph.adjacencies(current)
        if not parents:
            break
        parent = list(parents)[0]
        length += graph.weight(parent, current)
        current = parent
        
    return length

def reconstruct_path(parent_graph: Graph, current):
    path = [current]
    while True:
        parents = parent_graph.adjacencies(current)
        if not parents:
            break
        current = list(parents)[0]
        path = [current] + path
    return path

def create_heuristic(graph):
    vertices = graph.vertices()
    h_values = {}
    
    if(vertices):
        parent_tree = dijkstra_search(graph, vertices[0])
        for vertex in vertices:
            cost = calculate_cost(graph, parent_tree, vertex)
            h_values[vertex] = cost

        def heuristic(current_node, goal):
            return abs(h_values[goal] - h_values[current_node])
        
        return heuristic