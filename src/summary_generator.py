import pandas as pd
import nltk
import re
import heapq
import json
import itertools

# Needs to be run only once
#nltk.download('stopwords')


meta_df = pd.read_csv('../data/metadata.csv', dtype={
    'pubmed_id': str,
    'Microsoft Academic Paper ID': str,
    'doi': str
},low_memory = False)

meta_df.head()
meta_df.info()

# Take abstracts from all the articles
filtered = []
for i in meta_df['abstract']:
    if isinstance(i, str):
        filtered.append(i)
    else:
        filtered.append("")

# take corresponding links to the articles
links = []
for i in meta_df['url']:
    links.append(i)

s = ' '.join(filtered)

# Tokenize each abstract
tokenized = []
for i in filtered:
    sent_list = nltk.sent_tokenize(i)
    tokenized.append(sent_list)


article_text = re.sub(r'\[[0-9]*\]', ' ', s)
article_text = re.sub(r'\s+', ' ', s)

formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )
formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)

# combine the urls and respective articles into a dictionary
data = dict(zip(links, tokenized))


sentence_list = nltk.sent_tokenize(s)

stopwords = nltk.corpus.stopwords.words('english')

# Find the word frequencies
def word_frequencies(article):
    word_freqs = {}
    for word in nltk.word_tokenize(article):
        if word not in stopwords:
            if word not in word_freqs.keys():
                word_freqs[word] = 1
            else:
                word_freqs[word] += 1
    return word_freqs

frequencies = word_frequencies(formatted_article_text)

maximum_frequncy = max(frequencies.values())

# Find the weights of the frequencies by dividing them by the maximum
for word in frequencies.keys():
    frequencies[word] = (frequencies[word]/maximum_frequncy)

# Find the scores for each sentences based on the frequencies of the words.
def sent_scores(sentences, word_freqs):
    sentence_scores = {}
    for sent in sentences:
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_freqs.keys():
                if len(sent.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_freqs[word]
                    else:
                        sentence_scores[sent] += word_freqs[word]
    return sentence_scores


scores = sent_scores(sentence_list, frequencies)

# Take top 150 sentences, this value is hard coded and can be anything depending on
# how large the summary needs to be.
summary_sentences = heapq.nlargest(150, scores, key = scores.get)

# Find the urls for the top 150 sentences, and store them as dictionary.
sent_link = {}
for i in summary_sentences:
    for key,value in data.items():
        if i in value:
            sent_link.update({i:key})


with open('../data/summary_urls.json', 'w') as outfile:
    json.dump(sent_link, outfile, indent=4)

print("here is summary")
summary = ' '.join(summary_sentences)
print(summary)
