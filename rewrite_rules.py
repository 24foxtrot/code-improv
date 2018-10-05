#!/usr/bin/env python3

from random import choice

# value of n for n-grams
N = 2
FILE = "README.md"

def real_words(f):
    '''extract and yield real-looking words from a file'''

    for line in f:
        for word in line.strip().split():
            if word and word[0].isalpha():
                yield word

def reprint_file(f, generator):
    '''print out a file, except with the real-looking words replaced with output from a generator'''

    for i, line in enumerate(f):

        # we can't change the first rule, and let's leave the title and description
        if not i or line.startswith('1. '):
            print(line.strip())

        # but we can change everything else in that file
        else:
            words = []
            for word in line.strip().split():
                if word and word[0].isalpha():
                    words.append(next(generator))
                else:
                    words.append(word)
            print(*words)

def build_ngrams(n, words):
    '''build a dictionary mapping n-minus-one words separated by spaces to a list of possible successor words'''

    ngrams = dict()
    predictor_words = []

    # saturate the predictor with the first few words
    for _ in range(n - 1):
        predictor_words.append(next(words))

    # store that word in the ngram table
    for word in words:
        key = ' '.join(predictor_words)
        try:
            ngrams[key].append(word)
        except KeyError:
            ngrams[key] = [word]

        # rotate the predictor words with the new word
        predictor_words.pop(0)
        predictor_words.append(word)

    return ngrams

def generate(ngrams):
    '''given an ngram dict generated by build_ngrams, '''

    while True:

        # seed generator with a random n-gram
        words = choice(list(ngrams.keys()))
        for word in words.split():
            yield word

        while True:
            try:
                word = choice(ngrams[words])
            except KeyError:
                # we've predicted ourselves into a corner, just start over
                break
            yield word
            _, _, words = words.partition(' ')
            words = ' '.join(words.split() + [word])

with open(FILE, 'r') as f:
    lines = f.readlines()

ngrams = build_ngrams(N, real_words(lines))
reprint_file(lines, generate(ngrams))