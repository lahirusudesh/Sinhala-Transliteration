#Sylables are created in this module
# -*- coding: utf-8 -*-
import os
import io
import nltk
import string
import sys
import nltk
from nltk.util import ngrams
from nltk.lm import NgramCounter
from itertools import chain
sys.setrecursionlimit(10**7)
TrigramN = 4
BigramN = 3
# special characters
special_chars = string.punctuation
PermutationList = []
SimilarLetterGroup = [{'ක','ඛ'},{'ල','ළ'},{'ප','ඵ'},{'ග','ඝ'},{'ච','ඡ'},{'ෂ','ශ'},{'බ','භ'},{'ඩ','ඪ'},{'ද','ධ'},{'ජ','ඣ'},{'න','ණ'},{'ට','ඨ'},{'ත','ථ'}]
ThreeSyllableChunksList = {}
TwoSyllableChunksList = {}
def DivideTokenIntoNSyllableChunks(token,n):
    chunks = [token[i:i+n] for i in range(0,len(token))]
    return chunks

def GetTrigramCount(word):
    if word in ThreeSyllableChunksList:
        return ThreeSyllableChunksList[word]
    else:
        return 0
def GetBigramCount(word):
    if word in TwoSyllableChunksList:
        return TwoSyllableChunksList[word]
    else:
        return 0
def GenarateThreeSyllableChunks():
    if os.path.isfile('combined.txt'):
        with io.open('combined.txt', encoding='utf8') as fin:
            text = fin.read()
    tokenized_sent = [list(map(str.lower, nltk.word_tokenize(sent)))
                      for sent in nltk.sent_tokenize(text)]
    for sent in tokenized_sent:
        for token in sent:
            chunks= DivideTokenIntoNSyllableChunks(token,TrigramN)
            for chunk in chunks:
                if chunk in ThreeSyllableChunksList:
                    ThreeSyllableChunksList[chunk] += 1
                else:
                    ThreeSyllableChunksList[chunk] = 1

def GenarateTwoSyllableChunks():
    if os.path.isfile('combined.txt'):
        with io.open('combined.txt', encoding='utf8') as fin:
            text = fin.read()
    tokenized_sent = [list(map(str.lower, nltk.word_tokenize(sent)))
                      for sent in nltk.sent_tokenize(text)]
    for sent in tokenized_sent:
        for token in sent:
            chunks= DivideTokenIntoNSyllableChunks(token,BigramN)
            for chunk in chunks:
                if chunk in TwoSyllableChunksList:
                    TwoSyllableChunksList[chunk] += 1
                else:
                    TwoSyllableChunksList[chunk] = 1

def Preprocess(InputText):
    UniqueWordList = []
    tokenized_sent = [list(map(str.lower, nltk.word_tokenize(sent)))
                      for sent in nltk.sent_tokenize(InputText)]
    for sent in tokenized_sent:
        for word in sent:
            if word not in UniqueWordList and not word.isnumeric() and word not in special_chars:
                UniqueWordList.append(word);
    return UniqueWordList

def oneDArray(x):
    return list(chain(*x))

def GeneratePermutations(word):
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
                            GeneratePermutations(new_word)
def SetUpUnigramModel():
    if os.path.isfile('combined.txt'):
        with io.open('combined.txt', encoding='utf8') as fin:
            text1 = fin.read()
    tokenized_text = [list(map(str.lower, nltk.word_tokenize(sent))) for sent in nltk.sent_tokenize(text1)]
    #print(tokenized_text)
    text_unigrams = [ngrams(sent, 1) for sent in tokenized_text]
    unigram_counter_model = NgramCounter(text_unigrams)
    return unigram_counter_model


def SelectBestSuggestion(unigram_model, word):
    highestUnigramFrequency = 0
    bestWord = word
    #Unigram count
    for w in PermutationList:
        wordUnigramFrequency = unigram_model[w]
        if (wordUnigramFrequency > highestUnigramFrequency):
            highestUnigramFrequency = wordUnigramFrequency
            bestWord = w
    #trigram count
    if bestWord == word:
        HighestTrigramScore = 0
        for w in PermutationList:
            ThreeSyllableChunks = []
            if len(w) > TrigramN:
                ThreeSyllableChunks = DivideTokenIntoNSyllableChunks(w,TrigramN)
                WordTrigramScore = 0
                for ThreeSyllableChunk in ThreeSyllableChunks:
                    WordTrigramScore += GetTrigramCount(ThreeSyllableChunk)
                if WordTrigramScore > HighestTrigramScore:
                    HighestTrigramScore = WordTrigramScore
                    bestWord = w
    # bigram count
    if bestWord == word:
        HighestBigramScore = 0
        for w in PermutationList:
            TwoSyllableChunks = []
            if len(w) > BigramN:
                TwoSyllableChunks = DivideTokenIntoNSyllableChunks(w, BigramN)
                WordBigramScore = 0
                for TwoSyllableChunk in TwoSyllableChunks:
                    WordBigramScore += GetBigramCount(TwoSyllableChunk)
                if WordBigramScore > HighestBigramScore:
                    HighestBigramScore = WordBigramScore
                    bestWord = w
    return bestWord

if __name__ == '__main__':
    if os.path.isfile('adaderana.txt'):
        with io.open('adaderana.txt', encoding='utf8') as fin:
            text = fin.read()
    UniqueWordList = Preprocess(text)
    unigram_counter_model = SetUpUnigramModel()
    GenarateThreeSyllableChunks()
    GenarateTwoSyllableChunks()
    wordlist = ["අර්තික","සාකාච්චා","සහබාගි","තිඩෙනෙකු", "අමාත්‍යන්ශ", "අසඩිතයින්ගෙ", "කරඉ"]
    for word in UniqueWordList:
    #for word in wordlist:
        PermutationList = []
        GeneratePermutations(word)
        BestSuggestion = SelectBestSuggestion(unigram_counter_model,word)
        #f = a=open('myfile.txt', 'a', encoding='utf-8', errors='ignore')
        text = text.replace(word,BestSuggestion)
    print(text)