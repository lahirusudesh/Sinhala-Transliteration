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

def GeneratePermutationsUsingEditDistance(word):
    UniqueWordList = []
    with open('UniqueWords.txt', 'r', encoding='utf-8', errors='ignore') as file1:
        UniqueWordList = json.load(file1)
    for uniqueword in UniqueWordList:
        distance  = nltk.edit_distance(uniqueword,word)
        if(distance <= 3):
            PermutationList.append(uniqueword)

if __name__ == '__main__':
    w1 = 'සකාච්චා'
    w2 = 'සාකච්ඡා'
    GeneratePermutationsByReplacing(w1)
    print(PermutationList)
    GeneratePermutationsUsingEditDistance(w1)
    print(PermutationList)



