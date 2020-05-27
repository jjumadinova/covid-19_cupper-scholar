from pycorenlp import StanfordCoreNLP

with open('../data/summary.txt', 'r') as file:
    data = file.read()

nlp = StanfordCoreNLP("http://localhost:9000/")

output = nlp.annotate(data, properties={"annotators":"tokenize,ssplit,pos,depparse,natlog,openie",
                            "outputFormat": "json",
                             "openie.triple.strict":"true",
                             "openie.max_entailments_per_clause":"1"})

result = []
for i in output["sentences"]:
    result.append([i["openie"] for item in output])


subject = []
relation = []
object = []
for i in result:
    for n in i:
        for rel in n:
            subject.append(rel['subject'])
            relation.append(rel['relation'])
            object.append(rel['object'])


import json

lists = ['subject', 'relation', 'object']

data = {listname: globals()[listname] for listname in lists}
with open('file.json', 'w') as outfile:
    json.dump(data, outfile, indent=4)
