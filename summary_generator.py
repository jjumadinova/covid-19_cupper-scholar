import pandas as pd
import glob
import os
import nltk
import re
import heapq

# needs to be run only once
#nltk.download('stopwords')

def summary_generator():
    # represent the data from metadata file in pandas dataframe
    meta_df = pd.read_csv('metadata.csv', dtype={
        'pubmed_id': str,
        'Microsoft Academic Paper ID': str,
        'doi': str
    },low_memory = False)

    # display available coloumns that have information about the article
    meta_df.info()

    # Check if the abstract of the article is string data type
    filtered = []
    for i in meta_df['abstract']:
        if isinstance(i, str):
            filtered.append(i)

    s = ' '.join(filtered)

    # Filter the data from extra symbols
    article_text = re.sub(r'\[[0-9]*\]', ' ', s)
    article_text = re.sub(r'\s+', ' ', s)

    formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )
    formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)

    sentence_list = nltk.sent_tokenize(s)

    stopwords = nltk.corpus.stopwords.words('english')

    # Find the frequencies of the words
    word_frequencies = {}
    for word in nltk.word_tokenize(formatted_article_text):
        if word not in stopwords:
            # make sure that the word is not stopword
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1

    # compute the weighted frequencies.
    maximum_frequncy = max(word_frequencies.values())

    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)

    # Find the sentence scores for sentences that have less then 30 words. This
    # value can be modified based on the personal preference.
    sentence_scores = {}
    for sent in sentence_list:
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
                if len(sent.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word]
                    else:
                        sentence_scores[sent] += word_frequencies[word]


    # retrieve 150 sentences with the highest scores.
    summary_sentences = heapq.nlargest(150, sentence_scores, key=sentence_scores.get)

    summary = ' '.join(summary_sentences)
    print(summary)


    def is_empty(path):
        """Check if the path exitst and if file is empty"""
        return os.path.exists(path) and os.stat(path).st_size == 0


    empty = is_empty('summary.txt')

    if empty:
        # Open a file, if the file does not exist with mode `a` new one will be created
        file_object = open('summary.txt', 'a')
        # add the generated string to the file, input is the file with subtitles
        file_object.write(summary)
        # Close the file
        file_object.close()

# Needs to be called only once to generate the summary of the text, and save it in the
# specified file
#summary_generator()
