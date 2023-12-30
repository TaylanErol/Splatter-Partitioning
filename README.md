# Splatter Partitioning Python Script

## Overview
This Python script provides an implementation of the "Splatter Partitioning" algorithm on graph structures using NetworkX. The algorithm divides a graph into 'k' partitions or communities where 'k' is a user-defined parameter. It starts by randomly selecting 'k' nodes and allocates them to different partitions. Subsequently, it performs partitioning using a breadth-first approach. The script also has a modularity maximizing step where nodes can be moved between partitions to improve the global modularity score. In the end, it visualizes the graph with different colors distinguishing the partitions.

### Modules and Functionality
This script uses NetworkX for processing the graph and matplotlib for visualization. It includes two main functions - calculate_modularity() and splatter_partitioning().

* calculate_modularity(): Calculates the modularity of the graph given the current partitioning. This is used as a measure of the quality of the partitioning.

* splatter_partitioning(): Performs the splatter partitioning, with an optional refinement based on modularity.

### Usage

```python
G = nx.karate_club_graph()  # Initialize the graph
k = 3  # Number of initial partitions
partitions = splatter_partitioning(G, k)  # Apply the splatter partitioning algorithm
```
To visualize the final partitions on the graph, use matplotlib's pyplot. A color map is created based on partitions here for easier differentiation between partitions.

```python
partition_colors = ['red', 'blue', 'green', 'yellow', 'purple']  # Add more colors if needed
color_map = [partition_colors[partitions[node] % len(partition_colors)] for node in G]

# Draw the graph
pos = nx.spring_layout(G)
nx.draw(G, pos, node_color=color_map, edge_color='gray', with_labels=True, node_size=100)
plt.xticks([])
plt.yticks([])
plt.show()
```

## Karate Club Graph Partitioning Results
![alt text](https://raw.githubusercontent.com/TaylanErol/Splatter-Partitioning/master/myplot.png?token=GHSAT0AAAAAACKYRFWZKCTRRLXDYFUBXEWYZMP4B3Q)
