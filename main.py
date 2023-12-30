from collections import deque

import networkx as nx
import matplotlib.pyplot as plt
import random


def calculate_modularity(graph, partitions):
    """
    Calculate the modularity of the graph for given partitions.

    :param graph: The graph.
    :type graph: networkx.Graph

    :param partitions: The partitioning of the graph.
    :type partitions: dict

    :return: The modularity value.
    :rtype: float
    """
    communities = {}
    for node, partition in partitions.items():
        communities.setdefault(partition, []).append(node)

    # Convert to list of lists for modularity calculation
    community_list = list(communities.values())
    return nx.algorithms.community.modularity(graph, community_list)


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

    for node in graph.nodes():
        if partitions[node] is None:
            partitions[node] = random.randint(0, k - 1)
            print(f"Node {node} was unassigned, randomly assigned to partition {partitions[node]}")

            # Refinement step based on modularity
            print("Starting refinement based on modularity")
            previous_modularity = calculate_modularity(graph, partitions)
            max_iterations = 10  # Limit the number of refinement iterations

            for iteration in range(max_iterations):
                improved = False
                new_partitions = {}

                for node in graph.nodes():
                    original_partition = partitions[node]
                    best_partition = original_partition
                    best_modularity = previous_modularity

                    # Check only a subset of neighbors to prevent over-concentration
                    neighbors_to_check = random.sample(list(graph.neighbors(node)), min(3, len(graph.neighbors(node))))
                    for neighbor in neighbors_to_check:
                        temp_partition = partitions[neighbor]
                        if temp_partition is None or temp_partition == original_partition:
                            continue

                        partitions[node] = temp_partition  # Temporarily change partition
                        new_modularity = calculate_modularity(graph, partitions)

                        # Apply a stricter criterion for changing partitions
                        if new_modularity > best_modularity + 0.01:  # Threshold for significant improvement
                            best_modularity = new_modularity
                            best_partition = temp_partition
                            improved = True

                        partitions[node] = original_partition  # Revert to original partition

                    if best_partition != original_partition:
                        new_partitions[node] = best_partition

                # Apply all partition changes in batch
                for node, partition in new_partitions.items():
                    partitions[node] = partition
                    print(
                        f"Iteration {iteration + 1}: Node {node} moved to partition {partition} for better modularity")

                if improved:
                    previous_modularity = best_modularity
                else:
                    break  # Stop if no improvements

        return partitions

# Rest of your code for initializing the graph and visualization remains the same


# Initialize the graph and parameters
G = nx.karate_club_graph()

k = 3  # Number of initial partitions

# Apply the splatter partitioning algorithm
partitions = splatter_partitioning(G, k)

# Creating a color map based on partitions
partition_colors = ['red', 'blue', 'green', 'yellow', 'purple']  # Add more colors if needed
color_map = [partition_colors[partitions[node] % len(partition_colors)] for node in G]

# Draw the graph
pos = nx.spring_layout(G)
nx.draw(G, pos, node_color=color_map, edge_color='gray', with_labels=True, node_size=100)
plt.xticks([])
plt.yticks([])
plt.show()
