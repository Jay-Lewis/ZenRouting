__author__ = 'Justin'

import matplotlib.pyplot as plt
import networkx as nx
G=nx.dodecahedral_graph()
nx.draw(G)  # networkx draw()
plt.draw()  # pyplot draw()
plt.show()