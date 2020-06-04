# covid-19_cupper-scholar
Repository to hold a research project conducted by Teona Bagashvili as a part of the Cupper Scholar program at Allegheny College in Spring 2020


## Necessary tools and libraries
networkx, pandas, matplotlib, nltk, heapq

The program is tested on Linux, with Pyhton 3.7.6 version

## Steps for running the program

- Navigate to `src` and run `python knowledge_graph.py`
- List of the top ten entity relations will be displayed on the terminal, type the one that you are interested in seeing graphically. For example type `is with`.
- Plot will show up as a separate window. The plot as well as the summary of the data with respective links will be saved in `sample_outputs` folder. The data is retrieved from Kaggle and contains up to 70,000 articles and papers on COVID-19.

## Steps for regenerating the summary and entity-pairs.

If you would like to change the length of the summary and regenerate the entity-pairs:

- Navigate to `src` and run `python summary_generator.py`, enter the number of sentences
you would like to have in the summary. Initially program used 150 sentences. Sentences will be
saved in `summary_urls.json` with respective links.

- To generate new entity pairs based on the new summary text. First open a separate terminal window and navigate to the directory where you installed Stanfor CoreNlp. And run:
```
cd stanford-corenlp-full-2018-10-05
java -mx6g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -timeout 5000

```
This will start the server. Don't close the terminal or close the server yet.

- In a separate terminal window navigate to `src` directory of this project and run
`python entity_extractor.py`. Generated Entity pairs will be saved in `entity_pairs.json`.

- Close the server that you started on the first terminal window with `Ctr c`.
