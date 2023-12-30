from collections import deque
import networkx as nx
import matplotlib.pyplot as plt
import random


def calculate_modularity(graph, partitions):
    communities = {}
    for node, partition in partitions.items():
        communities.setdefault(partition, []).append(node)

    community_list = list(communities.values())
    modularity = nx.algorithms.community.modularity(graph, community_list)
    return modularity


def splatter_partitioning(graph, k):
    partitions = {node: None for node in graph.nodes()}
    initial_nodes = random.sample(list(graph.nodes()), k)
    for i, node in enumerate(initial_nodes):
        partitions[node] = i

    partition_queues = {i: deque([node]) for i, node in enumerate(initial_nodes )}

    unpartitioned_nodes = set(graph.nodes()) - set(initial_nodes)
    while unpartitioned_nodes:
        for partition, queue in partition_queues.items():
            if not queue:
                continue

            current_node = queue.popleft()
            for neighbor in graph.neighbors(current_node):
                if partitions[neighbor] is None and neighbor in unpartitioned_nodes:
                    partitions[neighbor] = partition
                    queue.append(neighbor)
                    unpartitioned_nodes.remove(neighbor)

    for node in graph.nodes():
        if partitions[node] is None:
            partitions[node] = random.randint(0, k - 1)

    previous_modularity = calculate_modularity(graph, partitions)
    modularity_changes = False

    while not modularity_changes:
        modularity_changes = False
        for node in graph.nodes():
            best_partition = partitions[node]
            best_modularity = previous_modularity

            for p in range(k):
                partitions[node] = p
                new_modularity = calculate_modularity(graph, partitions)
                if new_modularity > best_modularity:
                    best_modularity = new_modularity
                    best_partition = p
                    modularity_changes = True

                partitions[node] = best_partition

        previous_modularity = calculate_modularity(graph, partitions)

    return partitions


G = nx.karate_club_graph()
k = 3
partitions = splatter_partitioning(G, k)
partition_colors = ['red', 'blue','green','yellow','purple']
color_map = [partition_colors[partitions[node] % len(partition_colors)] for node in G]
pos = nx.spring_layout(G)
nx.draw(G, pos, node_color=color_map, edge_color='gray', with_labels=True, node_size=100)
plt.show()