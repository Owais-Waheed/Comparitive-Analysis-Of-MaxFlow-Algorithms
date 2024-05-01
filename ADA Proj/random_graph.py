import random

def generate_random_graph(num_nodes, num_edges, max_capacity, file_name):
    with open(file_name, 'w') as f:
        f.write(f"{num_nodes} {num_edges}\n")
        for _ in range(num_edges):
            source = random.randint(0, num_nodes - 1)
            target = random.randint(0, num_nodes - 1)
            while target == source:
                target = random.randint(0, num_nodes - 1)
            capacity = random.randint(1, max_capacity)
            f.write(f"{source} {target} {capacity}\n")

# Example usage
generate_random_graph(5, 7, 10, "random_graph.txt")
