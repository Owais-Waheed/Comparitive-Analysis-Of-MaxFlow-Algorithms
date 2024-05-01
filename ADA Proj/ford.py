

class Graph:
    def __init__(self, V):
        self.V = V
        self.adj = [[] for _ in range(V)]
        self.count_residual_graphs = 0 # To count the number of residual graphs

    def addEdge(self, u, v, capacity):
        self.adj[u].append([v, capacity, len(self.adj[v])])
        self.adj[v].append([u, 0, len(self.adj[u]) - 1])

    def DFS(self, u, sink, visited, parent):
        visited[u] = True

        if u == sink:
            return True

        for index, (v, capacity, reverse_index) in enumerate(self.adj[u]):
            if not visited[v] and capacity > 0:
                parent[v] = (u, index)
                if self.DFS(v, sink, visited, parent):
                    return True

        return False

    def FordFulkersonMaxFlow(self, source, sink):
        parent = [-1] * self.V
        max_flow = 0

        while self.DFS(source, sink, [False] * self.V, parent):
            path_flow = float('Inf')
            s = sink

            while s != source:
                u, index = parent[s]
                path_flow = min(path_flow, self.adj[u][index][1])
                s = u

            s = sink
            while s != source:
                u, index = parent[s]
                self.adj[u][index][1] -= path_flow
                self.adj[s][self.adj[u][index][2]][1] += path_flow
                s = u

            max_flow += path_flow
            self.count_residual_graphs += 1

            parent = [-1] * self.V  # Reset parent array for next DFS

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
max_flow = g.FordFulkersonMaxFlow(source, sink)
print("Maximum flow:", max_flow)
print("Number of Residual Graphs:", g.count_residual_graphs)