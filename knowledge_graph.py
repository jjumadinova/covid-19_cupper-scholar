from pycorenlp import StanfordCoreNLP

with open('summary.txt', 'r') as file:
    data = file.read()

nlp = StanfordCoreNLP("http://localhost:9000/")

output = nlp.annotate(data, properties={"annotators":"tokenize,ssplit,pos,depparse,natlog,openie",
                            "outputFormat": "json",
                             "openie.triple.strict":"true",
                             "openie.max_entailments_per_clause":"1"})

result = []
for i in output["sentences"]:
    result.append([i["openie"] for item in output])


def triple(result):
    for i in result:
        for n in i:
            for rel in n:
                relationSent=rel['subject'],rel['relation'],rel['object']
                print(relationSent)

triple(result)
