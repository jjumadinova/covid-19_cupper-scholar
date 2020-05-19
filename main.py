import pandas as pd
import glob
import os
import nltk
import re
#nltk.download('stopwords')

def summary_generator():
    meta_df = pd.read_csv('metadata.csv', dtype={
        'pubmed_id': str,
        'Microsoft Academic Paper ID': str,
        'doi': str
    },low_memory = False)

    meta_df.head()
    meta_df.info()



    print(type(meta_df['abstract'][1]))

    filtered = []
    for i in meta_df['abstract']:
        if isinstance(i, str):
            filtered.append(i)

    s = ' '.join(filtered)

    article_text = re.sub(r'\[[0-9]*\]', ' ', s)
    article_text = re.sub(r'\s+', ' ', s)

    formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )
    formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)

    sentence_list = nltk.sent_tokenize(s)

    stopwords = nltk.corpus.stopwords.words('english')

    word_frequencies = {}
    for word in nltk.word_tokenize(formatted_article_text):
        if word not in stopwords:
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
