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

    with open('summary.txt', 'r') as file:
        s = file.read()


    # Filter the data from extra symbols
    text = re.sub(r'\[[0-9]*\]', ' ', s)
    text = re.sub(r'\s+', ' ', s)

    formated_text = re.sub('[^a-zA-Z]', ' ',text )
    formated_text = re.sub(r'\s+', ' ', formated_text)

    sentence_list = nltk.sent_tokenize(s)

    stopwords = nltk.corpus.stopwords.words('english')

    # Find the frequencies of the words
    word_freqs = {}
    for word in nltk.word_tokenize(formated_text):
        if word not in stopwords:
            # make sure that the word is not stopword
            if word not in word_freqs.keys():
                word_freqs[word] = 1
            else:
                word_freqs[word] += 1

    # compute the weighted frequencies, by dividing the frequencies of the words
    # by the word that has highest frequency
    for word in word_freqs.keys():
        word_freqs[word] = (word_freqs[word]/max(word_freqs.values()))

    # Find the sentence scores by adding the weighted frequencies of the words in each sentence.
    sentence_scores = {}
    for sent in sentence_list:
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_freqs.keys():
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_freqs[word]
                else:
                    sentence_scores[sent] += word_freqs[word]


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
