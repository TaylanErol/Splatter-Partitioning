from collections import deque

import networkx as nx
import matplotlib.pyplot as plt
import random


def splatter_partitioning(graph, k):
    """
    Perform splatter partitioning on a graph using a breadth-first approach.

    :param graph: The graph to be partitioned.
    :type graph: networkx.Graph

    :param k: The number of partitions.
    :type k: int

    :return: A dictionary mapping each node to its assigned partition number.
    :rtype: dict
    """
    print("Starting splatter partitioning with breadth-first approach")

    # Initialize with K Partitions
    partitions = {node: None for node in graph.nodes()}
    initial_nodes = random.sample(list(graph.nodes()), k)
    for i, node in enumerate(initial_nodes):
        partitions[node] = i
        print(f"Initial node {node} assigned to partition {i}")

    # Initialize queues for each partition
    partition_queues = {i: deque([node]) for i, node in enumerate(initial_nodes)}

    # Breadth-first spreading of partitions
    unpartitioned_nodes = set(graph.nodes()) - set(initial_nodes)
    while unpartitioned_nodes:
        for partition, queue in partition_queues.items():
            if not queue:
                continue  # Skip empty queues

            current_node = queue.popleft()
            for neighbor in graph.neighbors(current_node):
                if partitions[neighbor] is None and neighbor in unpartitioned_nodes:
                    partitions[neighbor] = partition
                    queue.append(neighbor)
                    unpartitioned_nodes.remove(neighbor)
                    print(f"  Node {neighbor} assigned to partition {partition} from node {current_node}")

    # Refine Partitions
    print("Starting refinement of partitions")
    for refinement_iteration in range(10):  # Number of refinement iterations
        for node in graph.nodes():
            partition_members = [n for n in graph.nodes() if partitions[n] == partitions[node]]
            if len(partition_members) == 1:
                continue

            current_partition = partitions[node]
            neighbor_partitions = [partitions[n] for n in graph.neighbors(node) if partitions[n] != current_partition]

            initial_edge_count = sum(1 for neighbor in graph.neighbors(node) if partitions[neighbor] != current_partition)

            if neighbor_partitions:
                new_partition = random.choice(neighbor_partitions)
                partitions[node] = new_partition
                new_edge_count = sum(1 for neighbor in graph.neighbors(node) if partitions[neighbor] != new_partition)

                if new_edge_count < initial_edge_count:
                    print(f"  Refinement {refinement_iteration + 1}, Node {node}: Changed from partition {current_partition} to {new_partition}. Edge count reduced.")
                else:
                    partitions[node] = current_partition

    return partitions

# Rest of your code for initializing the graph and visualization remains the same


# Initialize the graph and parameters
G = nx.karate_club_graph()
pos = nx.kamada_kawai_layout(G)
k = 5  # Number of initial partitions

# Apply the splatter partitioning algorithm
partitions = splatter_partitioning(G, k)

# Creating a color map based on partitions
partition_colors = ['red', 'blue', 'green', 'yellow', 'purple']  # Add more colors if needed
color_map = [partition_colors[partitions[node] % len(partition_colors)] for node in G]

# Draw the graph
nx.draw(G, pos, node_color=color_map, edge_color='gray', with_labels=True, node_size=100)
plt.xticks([])
plt.yticks([])
plt.show()
