"""
Python script to count articles per year per newspaper
and provide word counts for each group.
"""

import datasets 
import json
import nltk
import statistics
from nltk.tokenize import word_tokenize
from squidtools import util
from random import sample
import string

from lib import wc

df = datasets.load_from_disk('american_stories.dataset')
years = range(1774, 1964)
records = []

for year in years:
    # Not every year in the dataset
    if str(year) not in df:
        continue
    print(year)
    newspapers = {}
    articles = df[str(year)]
    for a in articles:
        np =  a['newspaper_name']
        if np not in newspapers:
            newspapers[np] = {
                'count': 0,
                'wcs': []
            }
        newspapers[np]['count'] += 1
        newspapers[np]['wcs'].append(wc(a))
    for np in newspapers:
        records.append({
            'year': year,
            'newspaper': np,
            'n_articles': newspapers[np]['count'],
            'total_words': sum(newspapers[np]['wcs'])
        })

util.write_tsv(records, 'summary_counts.tsv')

print(f"Wrote {len(records)} articles to summary_counts.tsv")