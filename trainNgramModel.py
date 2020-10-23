# -*- coding: utf-8 -*-
import os
import io
import json
import sys
import nltk
from itertools import chain

sys.setrecursionlimit(10 ** 8)
TrigramN = 4
BigramN = 3
ThreeSyllableChunksList = {}
TwoSyllableChunksList = {}


def DivideTokenIntoNSyllableChunks(token, n):
    chunks = [token[i:i + n] for i in range(0, len(token))]
    return chunks


def GetTrigramCount(word):
    a_file = open('threeSyllable.txt', 'r', encoding='utf-8', errors='ignore')
    x = a_file.read()
    ThreeSyllableChunksList = json.loads(x)
    print(y[word])


def GetBigramCount(word):
    a_file = open('twoSyllable.txt', 'r', encoding='utf-8', errors='ignore')
    x = a_file.read()
    y = json.loads(x)
    if word in y:
        return y[word]
    else:
        return 0


def GenarateThreeSyllableChunks(tokenized_sent):
    for sent in tokenized_sent:
        for token in sent:
            chunks = DivideTokenIntoNSyllableChunks(token, TrigramN)
            for chunk in chunks:
                if chunk in ThreeSyllableChunksList:
                    ThreeSyllableChunksList[chunk] += 1
                else:
                    ThreeSyllableChunksList[chunk] = 1


def GenarateTwoSyllableChunks(tokenized_sent):
    for sent in tokenized_sent:
        for token in sent:
            chunks = DivideTokenIntoNSyllableChunks(token, BigramN)
            for chunk in chunks:
                if chunk in TwoSyllableChunksList:
                    TwoSyllableChunksList[chunk] += 1
                else:
                    TwoSyllableChunksList[chunk] = 1

def oneDArray(x):
    return list(chain(*x))

def GenarateNGramModel():
    if os.path.isfile('combined.txt'):
        with io.open('combined.txt', encoding='utf8') as fin:
            text = fin.read()
    tokenized_text = [list(map(str.lower, nltk.word_tokenize(sent)))
                      for sent in nltk.sent_tokenize(text)]
    GenarateTwoSyllableChunks(tokenized_text)
    GenarateThreeSyllableChunks(tokenized_text)
    a_file = open('twoSyllable.txt', 'w', encoding='utf-8', errors='ignore')
    a_file.write(json.dumps(TwoSyllableChunksList))
    a_file.close()
    a_file = open('threeSyllable.txt', 'w', encoding='utf-8', errors='ignore')
    a_file.write(json.dumps(ThreeSyllableChunksList))
    a_file.close()

if __name__ == '__main__':
    GenarateNGramModel()