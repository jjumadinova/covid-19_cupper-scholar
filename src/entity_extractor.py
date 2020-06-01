"""This file is for generating entity-relation pairs with Stanford Core NLP"""

from pycorenlp import StanfordCoreNLP
import json


with open("../data/summary_urls.json") as f:
    summary = json.load(f)

summary_list = []
for key,value in summary.items():
    summary_list.append(key)

data = ''.join(summary_list)

nlp = StanfordCoreNLP("http://localhost:9000/")


output = nlp.annotate(data, properties={"annotators":"tokenize,ssplit,pos,depparse,natlog,openie",
                            "outputFormat": "json",
                             "openie.triple.strict":"true",
                             "openie.max_entailments_per_clause":"1"})

# Retrieve entities and rtheir relations.
result = []
for i in output["sentences"]:
    result.append([i["openie"] for item in output])

# Represent subject, object, relation as lists and then add to json file for later
# use to make graph.
subject = []
relation = []
object = []
for i in result:
    for n in i:
        for rel in n:
            subject.append(rel['subject'])
            relation.append(rel['relation'])
            object.append(rel['object'])


lists = ['subject', 'relation', 'object']


data = {listname: globals()[listname] for listname in lists}
with open('../data/entitiy_pairs.json', 'w') as outfile:
    json.dump(data, outfile, indent=4)
