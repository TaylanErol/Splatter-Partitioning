from collections import deque, defaultdict
import networkx as nx
import matplotlib.pyplot as plt
import random

def calculate_modularity(graph, partitions):
    communities = defaultdict(list)
    for node, partition in partitions.items():
        communities[partition].append(node)
    return nx.algorithms.community.modularity(graph, communities.values())

def splatter_partitioning(graph, k):
    partitions = {node: None for node in graph.nodes()}
    partition_sizes = [0] * k
    border_nodes = defaultdict(set)

    # Initialize partitions and border nodes
    initial_nodes = random.sample(list(graph.nodes()), k)

    for i, node in enumerate(initial_nodes):
        partitions[node] = i
        partition_sizes[i] += 1
        for neighbor in graph.neighbors(node):
            border_nodes[i].add(node)

    unpartitioned_nodes = set(graph.nodes()) - set(initial_nodes)
    while unpartitioned_nodes:
        for partition, nodes in border_nodes.items():
            for current_node in list(nodes):
                for neighbor in graph.neighbors(current_node):
                    if partitions[neighbor] is None and neighbor in unpartitioned_nodes:
                        partitions[neighbor] = partition
                        partition_sizes[partition] += 1
                        unpartitioned_nodes.remove(neighbor)
                        for neighbor_neighbor in graph.neighbors(neighbor):
                            if partitions[neighbor_neighbor] != partition:
                                border_nodes[partition].add(neighbor)

    previous_modularity = calculate_modularity(graph, partitions)
    modularity_changes = True

    while modularity_changes:
        modularity_changes = False
        for partition, nodes in border_nodes.items():
            for node in list(nodes):
                if partition_sizes[partitions[node]] == 1:
                    continue  # Protect small partitions

                current_partition = partitions[node]
                best_partition = current_partition
                best_modularity = previous_modularity

                for p in range(k):
                    if p != current_partition:
                        partitions[node] = p
                        new_modularity = calculate_modularity(graph, partitions)
                        if new_modularity > best_modularity:
                            best_modularity = new_modularity
                            best_partition = p
                            modularity_changes = True

                if best_partition != current_partition:
                    partition_sizes[current_partition] -= 1
                    partition_sizes[best_partition] += 1
                    border_nodes[best_partition].add(node)
                    border_nodes[current_partition].remove(node)
                partitions[node] = best_partition

        previous_modularity = calculate_modularity(graph, partitions)

    return partitions

# Example usage
G = nx.karate_club_graph()
k = 3
partitions = splatter_partitioning(G, k)
partition_colors = ['red', 'blue', 'green', 'yellow', 'purple']
color_map = [partition_colors[partitions[node] % len(partition_colors)] for node in G]
pos = nx.spring_layout(G)
nx.draw(G, pos, node_color=color_map, edge_color='gray', with_labels=True, node_size=100)
plt.show()
