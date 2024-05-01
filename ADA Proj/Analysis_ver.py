import time
import sys
import matplotlib.pyplot as plt
from random_graph import generate_random_graph
from ford import Graph as FordGraph
from edmond import Graph as EdmondsGraph
from dinics import Graph as DinicsGraph

sys.setrecursionlimit(10**6)

def generate_graph(num_nodes, num_edges, max_capacity):
    # Create a random graph and save it to a file
    file_name = f"random_graph_{num_nodes}.txt"
    generate_random_graph(num_nodes, num_edges, max_capacity, file_name)
    return file_name

def load_graph(file_name, graph_class, num_nodes):
    # Load the graph from the specified file into the given graph class instance
    graph = graph_class(num_nodes)
    with open(file_name, 'r') as f:
        lines = f.readlines()[1:]  # Skip the first line (num_nodes num_edges)
        for line in lines:
            u, v, capacity = map(int, line.split())
            graph.addEdge(u, v, capacity)
    return graph

def measure_execution_time(graph, algorithm_name):
    # Measure the execution time for the specified algorithm on the given graph
    source, sink = 0, graph.V - 1  # Source is 0, Sink is V - 1
    start_time = time.time()

    if algorithm_name == "ford":
        max_flow = graph.FordFulkersonMaxFlow(source, sink)
    elif algorithm_name == "edmond":
        max_flow = graph.EdmondsKarpMaxFlow(source, sink)
    elif algorithm_name == "dinics":
        max_flow = graph.DinicMaxFlow(source, sink)
    else:
        raise ValueError("Invalid algorithm name. Supported options: 'ford', 'edmond', 'dinics'")

    execution_time = time.time() - start_time
    return graph.count_residual_graphs, execution_time,max_flow

def main():
    num_vertices_range = range(1000, 10001, 1000)
    num_edges_factor = 10
    max_capacity = 100

    ford_execution_times = []
    edmonds_execution_times = []
    dinics_execution_times = []
    ford_paths = []
    edmonds_paths = []
    dinics_paths = []
    ford_max_flows = []
    edmonds_max_flows = []
    dinics_max_flows = []

    for num_vertices in num_vertices_range:
        num_edges = num_edges_factor * num_vertices
        # num_edges_factor = num_edges_factor * 2 

        # Generate a random graph and load it into separate graph instances
        file = generate_graph(num_vertices, num_edges, max_capacity)
        

        # Measure execution time and max flow for Ford-Fulkerson Algorithm
        ford_graph = load_graph(file, FordGraph, num_vertices)
        ford_count, ford_time , ford_flow = measure_execution_time(ford_graph, "ford")
        ford_execution_times.append(ford_time)
        ford_paths.append(ford_count)
        ford_max_flows.append(ford_flow)

        # Measure execution time and max flow for Edmonds-Karp Algorithm
        edmonds_graph = load_graph(file, EdmondsGraph, num_vertices)
        edmonds_count, edmonds_time , edmond_flow = measure_execution_time(edmonds_graph, "edmond")
        edmonds_execution_times.append(edmonds_time)
        edmonds_paths.append(edmonds_count)
        edmonds_max_flows.append(edmond_flow)

        # Measure execution time and max flow for Dinic's Algorithm
        dinics_graph = load_graph(file, DinicsGraph, num_vertices)
        dinics_count, dinics_time , dinic_flow= measure_execution_time(dinics_graph, "dinics")
        dinics_execution_times.append(dinics_time)
        dinics_paths.append(dinics_count)
        dinics_max_flows.append(dinic_flow)

        print(f"Finished measuring execution times for {num_vertices} vertices.")

    # Print or further analyze the collected execution times and max flows
    print("Execution times for Ford-Fulkerson Algorithm:", ford_execution_times)
    print("Execution times for Edmonds-Karp Algorithm:", edmonds_execution_times)
    print("Execution times for Dinic's Algorithm:", dinics_execution_times)

    print("Number of residual graphs for Ford-Fulkerson Algorithm:", ford_paths)
    print("Number of layered networks for Edmonds-Karp Algorithm:", edmonds_paths)
    print("Number of layered networks for Dinic's Algorithm:", dinics_paths)

    
    # Plotting
    plt.plot(num_vertices_range, ford_execution_times, label="Ford-Fulkerson")
    plt.plot(num_vertices_range, edmonds_execution_times, label="Edmonds-Karp")
    plt.plot(num_vertices_range, dinics_execution_times, label="Dinic's")

    plt.xlabel("Number of Vertices")
    plt.ylabel("Execution Time (seconds)")
    plt.title("Execution Time vs. Number of Vertices (Edge Factor = 10)")
    plt.legend()
    plt.grid(True)
    plt.show()

        # Plotting
    bar_width = 0.3
    index = range(len(num_vertices_range))

    plt.bar(index, ford_paths, bar_width, label='Ford-Fulkerson')
    plt.bar([i + bar_width for i in index], edmonds_paths, bar_width, label='Edmonds-Karp')
    plt.bar([i + 2 * bar_width for i in index], dinics_paths, bar_width, label='Dinic\'s')

    plt.xlabel('Number of Vertices')
    plt.ylabel('Number of Paths')
    plt.title('Number of Paths vs. Number of Vertices (Edge Factor = 10)')
    plt.xticks([i + bar_width for i in index], num_vertices_range)
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()

