import json
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import json
import collections
import nltk

with open("../data/file.json") as f:
  data = json.load(f)

with open("../data/summary_urls.json") as f:
  data_summary = json.load(f)

summary_list = []
for key,value in data_summary.items():
    summary_list.append([key,"[link]","({})".format(value)])

with open('../sample_outputs/summary.md', 'w') as f:
    for i in summary_list:
        string = ''.join(i)

        f.write(string)
        print(string)

subject = (data["subject"])
object = (data["object"])
relation = (data["relation"])

print("Top 10 relations:")
print(pd.Series(relation).value_counts()[:10])


kg_df = pd.DataFrame({'source':subject, 'target':object, 'edge':relation})


relation_input = input("\nPlease enter one of the relations listed above\n")

G=nx.from_pandas_edgelist(kg_df[kg_df['edge']==relation_input], "source", "target",
                          edge_attr=True, create_using=nx.MultiDiGraph())

plt.figure(figsize=(16,16))
pos = nx.spring_layout(G, k = 0.5) # k regulates the distance between nodes
nx.draw(G, with_labels=True, node_color='green', node_size=500, edge_cmap=plt.cm.Blues, pos = pos, font_size = 16)

plt.savefig('../sample_outputs/sample.png')
plt.show()
