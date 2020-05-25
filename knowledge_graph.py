from pycorenlp import StanfordCoreNLP

nlp = StanfordCoreNLP("http://localhost:9000/")

text = 'Mark Robert is the founder of 3trucks. 3trucks was founded in 2010'

output = nlp.annotate(text, properties={"annotators":"tokenize,ssplit,pos,depparse,natlog,openie",
                            "outputFormat": "json",
                             "openie.triple.strict":"true",
                             "openie.max_entailments_per_clause":"1"})


result = [output["sentences"][0]["openie"] for item in output]
for i in result:
    for rel in i:
        relationSent=rel['subject'],rel['relation'],rel['object']
        print(relationSent)
