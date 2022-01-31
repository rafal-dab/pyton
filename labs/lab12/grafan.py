import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

# !!! Skrypt nadaje się tylko do grafów nieskierowanych !!!
fname = "CA-GrQc.txt"
G = nx.read_edgelist(fname)
print()
print("Wczytano sieć z pliku '" + fname + "'")
print()
print("Liczba wierzchołków:", G.number_of_nodes())
print("Liczba krawędzi:", G.number_of_edges())

degree_sequence = sorted((d for n, d in G.degree()), reverse=True)
dmax = degree_sequence[0]
dmin = degree_sequence[-1]
subG = [G.subgraph(c).copy() for c in nx.connected_components(G)]
print("Najwyższy stopień wierzchołka:", dmax)
print("Najniższy stopień wierzchołka:", dmin)
print("Liczba spójnych składowych:", len(subG))

subG_nodes = np.array([], dtype=int)
subG_paths = np.array([])
for s in subG:
    subG_nodes = np.append(subG_nodes, s.number_of_nodes())
    subG_paths = np.append(subG_paths, nx.average_shortest_path_length(s))
    #print(nx.is_connected(s), subG_nodes[-1], subG_paths[-1])

print()
print("Analiza składowych:")
nnodes, nn_counts = np.unique(subG_nodes, return_counts=True)
print("Liczba wierzchołków | Ilość składowych")
print("--------------------+-----------------")
for n, c in zip(nnodes, nn_counts):
    print("%19d | %16d" % (n, c))

print()
print("Analiza średnich najkrótszych ścieżek:")
npaths, np_counts = np.unique(subG_paths, return_counts=True)
print("Długość ścieżki | Ilość składowych")
print("----------------+-----------------")
for p, c in zip(npaths, np_counts):
    print("%15.4f | %16d" % (p, c))
print()
print("Średnia najkrótsza ścieżka we wszystkich składowych: %.4f" % (np.mean(subG_paths)))

fig = plt.figure("Analiza sieci", figsize=(12, 6))
axgrid = fig.add_gridspec(6, 12)

ax0 = fig.add_subplot(axgrid[:, 0:8])
options = {
    "node_color": "blue",
    "node_size": 10,
    "edge_color": "grey",
    "linewidths": 0.1,
    "width": 0.1,
}
pos = nx.spring_layout(G, seed=0)
nx.draw(G, pos, **options)
ax0.set_title("Sieć zaimportowana z pliku '" + fname + "'")
ax0.set_axis_off()

ax1 = fig.add_subplot(axgrid[:2, 8:])
ax1.bar(range(len(subG_nodes)), subG_nodes, width=1)
ax1.set_xlabel("Składowa")
ax1.set_ylabel("Liczba wierzchołków")
ax1.set_yscale('log')

ax2 = fig.add_subplot(axgrid[2:4, 8:])
ax2.bar(range(len(subG_paths)), subG_paths, width=1)
ax2.set_xlabel("Składowa")
ax2.set_ylabel("Średnia najkrótsza ścieżka")
ax2.set_yscale('log')

ax3 = fig.add_subplot(axgrid[4:, 8:])
nodes, counts = np.unique(degree_sequence, return_counts=True)
ax3.bar(nodes, counts, width=1)
ax3.set_title("Rozkład stopni wierzchołków")
ax3.set_xlabel("Stopień")
ax3.set_ylabel("Liczba wierzchołków")

fig.tight_layout()
plt.show()