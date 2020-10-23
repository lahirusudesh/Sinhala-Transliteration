from nltk.util import ngrams
import os
import io
import nltk
from nltk.util import ngrams
from nltk.lm import NgramCounter
#text_unigrams = [ngrams(sent, 1) for sent in text]

if __name__ == '__main__':
    if os.path.isfile('combined.txt'):
        with io.open('combined.txt', encoding='utf8') as fin:
            text = fin.read()
    tokenized_text = [list(map(str.lower, nltk.word_tokenize(sent)))
                      for sent in nltk.sent_tokenize(text)]
    #print(tokenized_text)
    text_unigrams = [ngrams(sent, 1) for sent in tokenized_text]
    uingram_counts = NgramCounter(text_unigrams)
    print(unigram_counts['අද'])