import pandas as pd
import glob
import os
import nltk
import re
#nltk.download('stopwords')



meta_df = pd.read_csv('../data/metadata.csv', dtype={
    'pubmed_id': str,
    'Microsoft Academic Paper ID': str,
    'doi': str
},low_memory = False)

meta_df.head()
meta_df.info()


filtered = []
for i in meta_df['abstract']:
    if isinstance(i, str):
        filtered.append(i)
    else:
        filtered.append("")

# links to the articles
links = []
for i in meta_df['url']:
    links.append(i)

print(len(filtered))
print(len(links))

s = ' '.join(filtered)

article_text = re.sub(r'\[[0-9]*\]', ' ', s)
article_text = re.sub(r'\s+', ' ', s)

formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )
formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)
#
tokenized = []
for i in filtered:
    sent_list = nltk.sent_tokenize(i)
    tokenized.append(sent_list)


data = dict(zip(links, tokenized))


sentence_list = nltk.sent_tokenize(s)

stopwords = nltk.corpus.stopwords.words('english')
extra_words = ["Results","Methods","Abstract"]

word_frequencies = {}
for word in nltk.word_tokenize(formatted_article_text):
    if word not in stopwords:
        if word not in extra_words:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1

maximum_frequncy = max(word_frequencies.values())

for word in word_frequencies.keys():
    word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)


sentence_scores = {}
for sent in sentence_list:
    for word in nltk.word_tokenize(sent.lower()):
        if word in word_frequencies.keys():
            if len(sent.split(' ')) < 30:
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_frequencies[word]
                else:
                    sentence_scores[sent] += word_frequencies[word]

import heapq
summary_sentences = heapq.nlargest(150, sentence_scores, key=sentence_scores.get)

sent_link = {}
for i in summary_sentences:
    for key,value in data.items():
        if i in value:
            sent_link.update({i:key})

import json

with open('../data/summary_urls.json', 'w') as outfile:
    json.dump(sent_link, outfile, indent=4)


print(sent_link)



print("here is summary")
summary = ' '.join(summary_sentences)
print(summary)



#
#
# def is_empty(path):
#     """Check if the path exitst and if file is empty"""
#     return os.path.exists(path) and os.stat(path).st_size == 0
#
#
# empty = is_empty('../data/summary.txt')
#
# if empty:
#     # Open a file, if the file does not exist with mode `a` new one will be created
#     file_object = open('../data/summary.txt', 'a')
#     # add the generated string to the file, input is the file with subtitles
#     file_object.write(summary)
#     # Close the file
#     file_object.close()
