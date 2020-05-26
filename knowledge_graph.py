import json
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

print(pd.Series(relation).value_counts()[:50])


kg_df = pd.DataFrame({'source':subject, 'target':object, 'edge':relation})

G=nx.from_pandas_edgelist(kg_df[kg_df['edge']=="is in"], "source", "target",
                          edge_attr=True, create_using=nx.MultiDiGraph())

plt.figure(figsize=(16,16))
pos = nx.spring_layout(G, k = 1) # k regulates the distance between nodes
nx.draw(G, with_labels=True, node_color='skyblue', node_size=1500, edge_cmap=plt.cm.Blues, pos = pos)
plt.show()
