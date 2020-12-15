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
from math import sqrt
from math import floor
from nltk import word_tokenize, sent_tokenize
from nltk.lm.preprocessing import padded_everygram_pipeline
from nltk.lm import MLE
sys.setrecursionlimit(10**6)
# special characters
special_chars = string.punctuation
PermutationList = []
PermutationDic = {'a':['a','A']}
SimilarLetterGroup = [{'ක','ඛ'},
                      {'ග','ඝ'},
                      {'ච','ඡ'},
                      {'ජ','ඣ'},
                      {'ට','ඨ'},
                      {'ත','ථ'},
                      {'ද','ධ'},
                      {'ඩ','ඪ'},
                      {'ප','ඵ'},
                      {'බ','භ'},
                      {'න','ණ'},
                      {'ල','ළ'},
                      {'ෂ','ශ','ෂ'},
                      {'ඤ','ඥ'},
                      ]

UniqueWordListInTest = []
WordListInTest = []
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
        if(distance <= floor(sqrt(len(word))) and uniqueword not in PermutationList):
            PermutationList.append(uniqueword)

def Preprocess(InputText):
    tokenized_sent = [list(map(str.lower, nltk.word_tokenize(sent)))
                      for sent in nltk.sent_tokenize(InputText)]
    for sent in tokenized_sent:
        for word in sent:
            if not word.isnumeric() and word not in special_chars:
                WordListInTest.append(word)
                if word not in UniqueWordListInTest:
                    UniqueWordListInTest.append(word)

def TrainNGramModel():
    newsListOne = []
    text = ''
    with open("combined.txt", 'r', encoding='utf-8', errors='ignore') as outfile:
        newslist = json.load(outfile)
    for news in newslist:
        newsListOne.extend(news)
    text = ' '.join([str(elem) for elem in newsListOne])
    tokenized_text = [list(map(str.lower, word_tokenize(sent)))
                      for sent in sent_tokenize(text)]
    n = 3
    train_data, padded_sents = padded_everygram_pipeline(n, tokenized_text)

    model = MLE(n)  # Lets train a 3-grams maximum likelihood estimation model.
    model.fit(train_data, padded_sents)
    return model


if __name__ == '__main__':
    if os.path.isfile('adaderana.txt'):
        with io.open('adaderana.txt', encoding='utf8') as fin:
            text = fin.read()

    with open('UniqueWords.txt', 'r', encoding='utf-8', errors='ignore') as file1:
        UniqueWordListInCorpus = json.load(file1)
    file1.close()
    with open('WordsList.txt', 'r', encoding='utf-8', errors='ignore') as file2:
        WordListInCorpus = json.load(file2)
    file2.close()
    Preprocess(text)
    nGramModel = TrainNGramModel()
    for uniqueword in UniqueWordListInTest:
        PermutationList.clear()
        GeneratePermutationsByReplacing(uniqueword)
        GeneratePermutationsUsingEditDistance(uniqueword,UniqueWordListInCorpus)
        PermutationListCopy = PermutationList.copy()
        PermutationDic[uniqueword] = PermutationListCopy
    with open('PermutationDictionary.txt', 'w', encoding='utf-8', errors='ignore') as file3:
        json.dump(PermutationDic,file3)