import io
import json
import os
import nltk
import os
import io
import nltk
import string
import sys
import nltk
from nltk.util import ngrams
from nltk.lm import NgramCounter
from itertools import chain
sys.setrecursionlimit(10**6)
# special characters
special_chars = string.punctuation
PermutationList = []
SimilarLetterGroup = [{'ක','ඛ'},
                      {'ග','ඝ'},
                      {'ච','ඡ'},
                      {'ජ','ඣ'},
                      {'ට','ඨ'},
                      {'ත','ථ'},
                      {'ද','ධ'},
                      {'ප','ඵ'},
                      {'බ','භ'},
                      {'න','ණ'},
                      {'ල','ළ'},
                      {'ෂ','ශ','ෂ'},
                      {'ඤ','ඥ'}
                      ]

def oneDArray(x):
    return list(chain(*x))

def GeneratePermutationsByReplacing(word):
    if 'න්' in word:
        newWord = word.replace('න්', 'ං')
        if newWord not in PermutationList:
            PermutationList.append(newWord)
    LetterList = list(word)
    OneDSimilar = oneDArray(SimilarLetterGroup)
    for i in range(len(LetterList)):
        if LetterList[i] in OneDSimilar:
            for similar_l in SimilarLetterGroup:
                if LetterList[i] in similar_l:
                    for l in similar_l:
                        LetterList[i] = l
                        new_word = "".join(LetterList)
                        if new_word not in PermutationList:
                            PermutationList.append(new_word)
                            GeneratePermutationsByReplacing(new_word)

def GeneratePermutationsUsingEditDistance(word, UniqueWordListInCorpus):
    for uniqueword in UniqueWordListInCorpus:
        distance  = nltk.edit_distance(uniqueword,word)
        if(len(word)>3 and distance < 2 and uniqueword not in PermutationList):
            PermutationList.append(uniqueword)

def Preprocess(InputText):
    UniqueWordList = []
    tokenized_sent = [list(map(str.lower, nltk.word_tokenize(sent)))
                      for sent in nltk.sent_tokenize(InputText)]
    for sent in tokenized_sent:
        for word in sent:
            if word not in UniqueWordList and not word.isnumeric() and word not in special_chars:
                UniqueWordList.append(word)
    return UniqueWordList

if __name__ == '__main__':
    if os.path.isfile('adaderana.txt'):
        with io.open('adaderana.txt', encoding='utf8') as fin:
            text = fin.read()
    with open('UniqueWords.txt', 'r', encoding='utf-8', errors='ignore') as file1:
        UniqueWordListInCorpus = json.load(file1)
    UniqueWordListInTest = Preprocess(text)

    for uniqueword in UniqueWordListInTest:
        PermutationList.clear()
        GeneratePermutationsByReplacing(uniqueword)
        print(PermutationList)
        GeneratePermutationsUsingEditDistance(uniqueword,UniqueWordListInCorpus)
        print(PermutationList)



