"""This file is for creating the outputs and save them in sample_outputs folder"""
import json
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import json
import collections
import nltk


with open("../data/entity_pairs.json") as f:
  data = json.load(f)


with open("../data/summary_urls.json") as f:
  data_summary = json.load(f)

# Take the sentences from the json and format so that each sentence is followed
# by the respective link in markdown format.
summary_list = []
for key,value in data_summary.items():
    summary_list.append([key,"[link]","({})".format(value)])
with open('../sample_outputs/summary.md', 'w') as f:
    for i in summary_list:
        string = ''.join(i)
        f.write(string)


subject = (data["subject"])
object = (data["object"])
relation = (data["relation"])


print("Top 10 relations:")
print(pd.Series(relation).value_counts()[:10])


dataframe = pd.DataFrame({'source':subject, 'target':object, 'edge':relation})


print("\nSummary text with all the relevant links will be saved in sample_outputs folder")
relation_input = input("\nPlease enter one of the relations listed above to see the entitiy relations graphically\n")

# Create the network betweeen the requested nodes.
G=nx.from_pandas_edgelist(dataframe[dataframe['edge']==relation_input], "source", "target",
                          edge_attr=True, create_using=nx.MultiDiGraph())


plt.figure(figsize=(16,16))
pos = nx.spring_layout(G, k = 0.5) # k regulates the distance between nodes
nx.draw(G, with_labels=True, node_color='green', node_size=500, edge_cmap=plt.cm.Blues, pos = pos, font_size = 16)


plt.savefig('../sample_outputs/sample.png')
plt.show()
