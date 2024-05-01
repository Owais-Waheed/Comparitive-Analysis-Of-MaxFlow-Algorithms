
from collections import deque

class Graph:
    def __init__(self, V):
        self.V = V
        self.adj = [[] for _ in range(V)]
        self.count_residual_graphs = 0 

    def addEdge(self, u, v, capacity):
        self.adj[u].append([v, capacity, len(self.adj[v])])
        self.adj[v].append([u, 0, len(self.adj[u]) - 1])

    def BFS(self, source, sink, parent):
        visited = [False] * self.V
        queue = deque([source])
        visited[source] = True

        while queue:
            u = queue.popleft()

            for index, (v, capacity, reverse_index) in enumerate(self.adj[u]):
                if not visited[v] and capacity > 0:
                    queue.append(v)
                    visited[v] = True
                    parent[v] = (u, index)

                    if v == sink:
                        return True

        return False

    def EdmondsKarpMaxFlow(self, source, sink):
        parent = [-1] * self.V
        max_flow = 0

        while self.BFS(source, sink, parent):
            path_flow = float('Inf')
            s = sink

            while s != source:
                u, index = parent[s]
                path_flow = min(path_flow, self.adj[u][index][1])
                s = u

            # update capacities of the edges and reverse edges along the path
            s = sink
            while s != source:
                u, index = parent[s]
                self.adj[u][index][1] -= path_flow
                self.adj[s][self.adj[u][index][2]][1] += path_flow
                s = u

            max_flow += path_flow
            self.count_residual_graphs += 1

        return max_flow

# Example usage:
g = Graph(6)
g.addEdge(0, 1, 16)
g.addEdge(0, 2, 13)
g.addEdge(1, 2, 10)
g.addEdge(1, 3, 12)
g.addEdge(2, 1, 4)
g.addEdge(2, 4, 14)
g.addEdge(3, 2, 9)
g.addEdge(3, 5, 20)
g.addEdge(4, 3, 7)
g.addEdge(4, 5, 4)

source, sink = 0, 5
max_flow = g.EdmondsKarpMaxFlow(source, sink)
print("Maximum flow:", max_flow)
print("Number of Residual Graphs:", g.count_residual_graphs)