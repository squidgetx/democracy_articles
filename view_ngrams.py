"""
Python script to view ngrams related to given words
"""
import datasets 
import json
import nltk
from nltk.tokenize import word_tokenize
from squidtools import util
from random import sample

WORDS = [
    'democracy',
    'republic'
]

def process_article(a):
    text = a['article']
    headline = a['headline']
    fulltext = (headline + '\n' + text).lower()
    tokens = word_tokenize(fulltext)
    bgs = list(nltk.bigrams(tokens))
    tgs = list(nltk.trigrams(tokens))
    result = {}

    for w in WORDS:
        wbgs = [b for b in bgs if w in b]
        wtgs = [t for t in tgs if w in t]
        bfdist = nltk.FreqDist(wbgs)
        tfdist = nltk.FreqDist(wtgs)
        result[f"{w}_bigrams"] = bfdist
        result[f"{w}_trigrams"] = tfdist

    return result

df = json.load(open('relevant_articles.10000.json', 'rt'))
bigrams = {}
trigrams = {}

for w in WORDS:
    bigrams[w] = nltk.FreqDist()
    trigrams[w] = nltk.FreqDist()

for year in df:
    # Not every year in the dataset
    articles = df[year]
    print(f"{len(articles)} articles found for year {year}")
    ngrams = [process_article(a) for a in articles]
    for w in WORDS:
        bigramskey = f"{w}_bigrams"
        trigramskey = f"{w}_trigrams"
        for a in ngrams:
            bigrams[w].update(a[bigramskey])
            trigrams[w].update(a[trigramskey])
for w in WORDS:
    print(bigrams[w].most_common(n=50))
    print(trigrams[w].most_common(n=50))
