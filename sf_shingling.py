#!/usr/bin/env python
# coding: utf-8

# Needed Libraries
def warn(*args, **kwargs):
    pass
import warnings
# Silly workaround to get rid of Sklearn deprication warnings.
warnings.warn = lambda *a, **b : None
import mmh3
from nltk import ngrams
import numpy as np
import pandas
import random
import argparse
from tqdm import tqdm

# Functions and Classes

def generate_random_seeds(n, seed=5):
    random.seed(seed)
    return random.sample(range(1, n+1), n)

def jaccard_similarity(set_a, set_b):
    return len(set_a.intersection(set_b)) / len(set_a.union(set_b))

class ShingledText:
    def __init__(self, text, random_seed=5, shingle_length=5, minhash_size=200):
        split_text = text.split()
        if len(split_text) < shingle_length:
            raise ValueError(u'input text is too short for specified shingle length of {}'.format(shingle_length))

        self.minhash = []
        self.shingles = ngrams(split_text, shingle_length)

        for hash_seed in generate_random_seeds(minhash_size, random_seed):
            min_value = float('inf')
            for shingle in ngrams(split_text, shingle_length):
                value = mmh3.hash(' '.join(shingle), hash_seed)
                min_value = min(min_value, value)
            self.minhash.append(min_value)

    def similarity(self, other_shingled_text):
        return jaccard_similarity(set(self.minhash),
                set(other_shingled_text.minhash))

def apply_shingled(row,urls,shingles):

    url = row['address']
    urli = urls.index(url)
    urlsh = shingles[urli]
    high = 0.0
    match = ""
    start = 0

    if not urlsh:
        row['Sim Score'] = 0.0
        row['Sim Match'] = ""
        return row

    for i, sh in enumerate(shingles):

        if not urli == i and sh:
            sim = jaccard_similarity(set(urlsh), set(sh))
            if sim > high:
                high = sim
                match = urls[i]

    row['Sim Score'] = high
    row['Sim Match'] = match

    return row


def main(args):

    print('Loading file: {}'.format(args.in_file))
    df = pandas.read_csv(args.in_file)

    if df.columns[0] == 'Internal - HTML':
        df = pandas.read_csv(args.in_file, skiprows=1)

    df.columns = [c.lower() for c in df.columns]

    content_col = args.content_column.lower()

    #Easy way to get rid of NaN values
    df = df[df[content_col] == df[content_col]]
    df.reset_index(drop=True, inplace=True)

    urls = []
    shingles = []

    print('Building content shingles.')
    # Build content shingles list
    for i, row in tqdm(df.iterrows(), total=df.shape[0]):

        text = row[content_col]
        url = row['address']
        default = "Maecenas vestibulum euismod dui id scelerisque."

        if isinstance(text, str) and len(text.split()) > 5:
            urls.append(url)
            shingles.append( ShingledText(text).minhash)
        else:
            urls.append(url)
            shingles.append(ShingledText(default).minhash)

    print('Applying scores to data.')
    df_comp = df.apply(apply_shingled, args=(urls,shingles), axis=1)

    print('Saving to file: {}'.format(args.out_file))
    df_comp.to_csv(args.out_file, encoding='utf-8' )


'''
 Example Usage:

    -i : Input filename
    -o : Output filename
    -c : Column from Screaming Frog that contains your extracted content.

    Example invocation:
    python sf_shingling.py -i internal_html_ap.csv -o output_html_ap.csv -c "BodyContent 1"

'''

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--in_file', type=str, required=True, help='Input Screaming Frog CSV filename')
    parser.add_argument('-o', '--out_file', type=str, required=True, help='Output CSV filename')
    parser.add_argument('-c', '--content_column', type=str, required=True, help='The name of the column holding the extracted content.')

    args = parser.parse_args()

    main(args)
