import networkx as nx
import numpy as np

'''
k_shortest() finds the "k" shortest paths 
and returns their lengths as well 
'''


def k_shortest(graph, src, terminal, K):
    G = nx.DiGraph()
    for i in range(len(graph)):
        for j in range(len(graph[i])):
            G.add_edge(i, j, weight=graph[i][j])

    k_paths = [[]]
    k_length = [0]

    # returns the shortest path using simple dijkstra
    k_length[0], k_paths[0] = nx.single_source_dijkstra(
        G, src, terminal, weight='weight')

    for i in range(1, K):
        best_path = []
        best_weight = float('inf')
        # finds the common root paths
        for t in range(i):
            common_root_path = list(range(len(k_paths)))
            graph_copy = graph.copy()
            root_path = []
            current_weight = 0

            for j in range(0, len(k_paths[t]) - 1):
                # spur node: node about which we 
                # see the deviations in the path
                spur_node = k_paths[t][j]
                if len(root_path):
                    current_weight+=graph[root_path[-1]][spur_node]
                root_path.append(spur_node)
                

                for y in range(len(graph_copy)):
                    graph_copy[y][spur_node] = float("inf")

                common_root_path = list(
                    filter(lambda x: k_paths[x][j] == spur_node, common_root_path))

                # done nodes are the onces already visited
                done_nodes = map(lambda x: k_paths[x][j + 1], common_root_path)

                for x in done_nodes:
                    graph_copy[spur_node][x] = float('inf')

                G_copy = nx.DiGraph()
                for m in range(len(graph_copy)):
                    for n in range(len(graph_copy[i])):
                        G_copy.add_edge(m, n, weight = graph_copy[m][n])

                curr_length, candidate_path = nx.single_source_dijkstra(
                    G_copy, spur_node, terminal, weight = 'weight')
                # print(i,j,curr_length,candidate_path,root_path,current_weight)
                curr_length += current_weight

                # print()

                if curr_length <= best_weight:
                    best_weight = curr_length
                    best_path = root_path[:-1] + candidate_path
                graph_copy[spur_node] = [float("inf")] * len(graph_copy[spur_node])

        # updates the k_paths with the shortest
        # best candidate path 

        k_paths.append(best_path)
        k_length.append(best_weight)

    return k_length, k_paths

# edges=np.ones((5,5))*float('inf')
# edges[0][1]=1
# edges[1][3]=2
# edges[1][2]=2
# edges[2][3]=2
# edges[4][3]=2
# edges[0][4]=2
# print(k_shortest(edges, 0, 3, 3))

