"""
Build a dataset of random articles and sentences from the American Stories dataset.
"""
import datasets 
import json
import nltk
import string
from nltk.tokenize import word_tokenize, sent_tokenize
from squidtools import util
from random import sample

from lib import wc, get_sentences, check_article_naive_words

words = [
    'democracy',
    'republic'
]

df = datasets.load_from_disk('american_stories.dataset')
years = range(1774, 1964)
records = []
sentences = []

for year in years:
    # Not every year in the dataset
    if str(year) not in df:
        continue
    articles = df[str(year)]
    print(f"{len(articles)} articles found for year {year}")
    for a in articles:
        if check_article_naive_words(articles, words):
            article = {
                'article_id': a['article_id'],
                'word_count': wc(a),
                'year': year,
                'date': a['date'],
                'newspaper': a['newspaper_name'],
                'edition': a['edition'],
                'page': a['page'],
            }
            article_sentences = get_sentences(a)
        
            article['mentions_democracy'] = any((s['mentions_democracy'] for s in article_sentences))
            article['mentions_republic'] = any((s['mentions_republic'] for s in article_sentences))
            records.append(article)
            sentences.extend(article_sentences)


util.write_tsv(records, 'articles.target.tsv')
util.write_tsv(sentences, 'sentences.target.tsv')
