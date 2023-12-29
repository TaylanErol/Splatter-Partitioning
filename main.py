import matplotlib.pyplot as plt
import networkx as nx

num_nodes = 20
num_edge = 30

G = nx.dense_gnm_random_graph(num_nodes, num_edge, seed=45654516)

pos = nx.kamada_kawai_layout(G)

nx.draw(G, pos, node_color='skyblue', edge_color='gray', node_size=100)

plt.xticks([])
plt.yticks([])

plt.show()

