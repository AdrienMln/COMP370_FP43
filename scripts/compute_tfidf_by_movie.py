import pandas as pd
from pathlib import Path
import re
from collections import Counter
import math
import os
import json

def load_stopwords(stopwords_path):
    with open(stopwords_path, 'r') as f:
        stopwords_list = [line.strip() for line in f]
    return set(stopwords_list)

TSV_FILENAME = 'all_movie_articles.tsv'
NUM_ARTICLES = 0
STOPWORDS = load_stopwords(Path(__file__).parent.parent/'stopwords.txt')
CATEGORY_TOP_WORDS_PATH = 'top10_words_by_movie.json'
MOVIE_NAMES = ''.join(['The Hunger Games: The Ballad of Songbirds & Snakes', 'The Marvels', 'Saltburn', 'Priscilla', 'The Holdovers', 'Thanksgiving'])

def load_tsv(tsv_name):
    return pd.read_csv(tsv_name, sep='\t')

def remove_stopwords(text, stopwords_set):
    words = text.split()
    filtered_words = [word for word in words if word.lower() not in stopwords_set]
    return ' '.join(filtered_words)

def remove_punctuation(text):
    return re.sub(r'[()\[\],.\-\?!:;#&\'"]', '', text).replace('“', '').replace('”','').replace('‘', '').replace('’', '').replace('–', '').replace('—', '')

def fix_text(df: pd.DataFrame):
    df['Fixed Title'] = df['Article Title'].apply(lambda title: remove_punctuation(title))
    df['Fixed Title'] = df['Fixed Title'].apply(lambda title: remove_stopwords(title, STOPWORDS))
    df['Fixed Description'] = df['Description'].apply(lambda description: remove_punctuation(description))
    df['Fixed Description'] = df['Fixed Description'].apply(lambda description: remove_stopwords(description, STOPWORDS))
    return df

def compute_idf(word, df: pd.DataFrame, num_articles):
    num_articles_that_mention = sum([1 for i, article in df.iterrows() if word in article['Fixed Description'] or word in article['Fixed Title']])
    return math.log(num_articles/num_articles_that_mention)

def compute_top_words(tfidf_scores, n):
    lst = sorted(tfidf_scores, key=lambda x: x[1], reverse=True)
    return list(filter(lambda word: word[0] not in MOVIE_NAMES, lst))[:n]


def write_to_json(json_path, data):
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=3)

def main():
    top_words = {}
    file_path = Path(__file__).parent.parent/'data'/TSV_FILENAME
    df = load_tsv(file_path)

    NUM_ARTICLES = len(df) # setting global variable for use in tfidf

    fixed_df = fix_text(df)
    total_word_counter = Counter()
    for index, article in fixed_df.iterrows():
        total_word_counter.update(article['Fixed Title'].split())
        total_word_counter.update(article['Fixed Description'].split())

    articles_by_movie = fixed_df.groupby(by=['Movie'])
    for movie, group in articles_by_movie:
        group_word_counter = Counter()
        for i, article in group.iterrows():
            # first pass to collect term frequencies for each of the words
            group_word_counter.update(article['Fixed Description'].split())
            group_word_counter.update(article['Fixed Title'].split())

        group_words = []
        for word in group_word_counter:
            tf = group_word_counter[word]
            idf = compute_idf(word, fixed_df, NUM_ARTICLES)
            group_words.append((word, tf*idf))

        top_words_group = compute_top_words(group_words, 10)
        top_words[movie[0]] = [word for word, _ in top_words_group]

    top_words_path = Path(__file__).parent.parent/'data'/CATEGORY_TOP_WORDS_PATH
    write_to_json(top_words_path, top_words)

if __name__ == '__main__':
    main()