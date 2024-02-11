import nltk
import string
from nltk.tokenize import word_tokenize, sent_tokenize

foreign_bigrams = {
    'republic': set([
        "french",
        "dominican",
        "argentine",
        "irish",
        "german",
        "mexican",
        "soviet",
        "cuban",
        "china",
        "cuba"
    ]), 
    'democracy': set()
}

def check_sentence(sentence, word):
    if word not in sentence:
        return False
    tokens = word_tokenize(sentence)
    bgs = nltk.bigrams(tokens)
    tgs = nltk.trigrams(tokens)
    # Count instances of bad bgs and bad tgs
    bad_bgs = [b for b in bgs if word in b and foreign_bigrams[word].intersection(b)]
    bad_tgs = [t for t in tgs if t[0] == word and t[1] == 'of' and t[2] in foreign_bigrams[word]]
    count = tokens.count(word) 
    total = count - len(bad_bgs) - len(bad_tgs)
    return total > 0

def get_sentences(a):
    text = a['article']
    headline = a['headline']
    fulltext = (headline + '\n' + text).lower()
    sentences = sent_tokenize(fulltext)

    processed = []
    for i, s in enumerate(sentences):
        republic = check_sentence(s, 'republic')
        democracy = check_sentence(s, 'democracy')
        sent = {
            'sentence_text': s,
            'mentions_republic': republic,
            'mentions_democracy': democracy,
            'article_id': a['article_id'],
            'sentence_idx': i
        }
        processed.append(sent)
    return processed

def wc(a):
    text = a['article']
    headline = a['headline']
    fulltext = (headline + '\n' + text).lower()
    tokens = word_tokenize(fulltext)
    tokens_no_punct = [t for t in tokens if t not in string.punctuation]
    return len(tokens_no_punct)

def check_article_naive(a, word):
    text = a['article']
    headline = a['headline']
    fulltext = (headline + '\n' + text).lower()
    return word in fulltext

def check_article_naive_words(a, words):
    for w in words:
        if check_article_naive(a, w):
            return True
    return False