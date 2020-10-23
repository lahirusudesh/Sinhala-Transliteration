# -*- coding: utf-8 -*-
import json
import os
import io
import nltk
import string
import sys
import nltk
from nltk.util import ngrams
from nltk.lm import NgramCounter
from itertools import chain
sys.setrecursionlimit(10**8)
TrigramN = 4
BigramN = 3
# special characters
special_chars = string.punctuation
PermutationList = []
SimilarLetterGroup = [{'අ','ඇ','ඈ','ආ','එ','ඒ'},{'ක','ඛ'},{'ල','ළ'},{'ප','ඵ'},{'ග','ඝ'},{'ච','ඡ'},{'ෂ','ශ'},{'බ','භ'},{'ඉ','ඊ','යි'},{'ඩ','ඪ','ද','ධ','ඳ'},{'ජ','ඣ'},{'න','ණ'},{'ට','ඨ'},{'ත','ථ'}]

def GetTrigramCount(word,Trigram_counter_model):
    if word in Trigram_counter_model:
        return Trigram_counter_model[word]
    else:
        return 0
def GetBigramCount(word,Bigram_counter_model):
    if word in Bigram_counter_model:
        return Bigram_counter_model[word]
    else:
        return 0

def DivideTokenIntoNSyllableChunks(token, n):
    chunks = [token[i:i + n] for i in range(0, len(token))]
    return chunks

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
    if 'න්' in word:
        newWord = word.replace('න්','ං')
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
                            GeneratePermutations(new_word)
def SetUpUnigramModel():
    if os.path.isfile('combined.txt'):
        with io.open('combined.txt', encoding='utf8') as fin:
            text = fin.read()
    tokenized_text = [list(map(str.lower, nltk.word_tokenize(sent)))
                      for sent in nltk.sent_tokenize(text)]
    #print(tokenized_text)
    text_unigrams = [ngrams(sent, 1) for sent in tokenized_text]
    unigram_counter_model = NgramCounter(text_unigrams)
    return unigram_counter_model


def SelectBestSuggestion(unigram_model,Bigram_counter_model,Trigram_counter_model,word):
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
                    WordTrigramScore += GetTrigramCount(ThreeSyllableChunk,Trigram_counter_model)
                if WordTrigramScore > HighestTrigramScore:
                    HighestTrigramScore = WordTrigramScore
                    bestWord = w
    # bigram count
    if bestWord == word:
        HighestBigramScore = 0
        for w in PermutationList:
            TwoSyllableChunks = []
            if len(w) > 3:
                TwoSyllableChunks = DivideTokenIntoNSyllableChunks(w, BigramN)
                WordBigramScore = 0
                for TwoSyllableChunk in TwoSyllableChunks:
                    WordBigramScore += GetBigramCount(TwoSyllableChunk,Bigram_counter_model)
                if WordBigramScore > HighestBigramScore:
                    HighestBigramScore = WordBigramScore
                    bestWord = w
    return bestWord
def GenarateThreeSyllableChunks():
    a_file = open('threeSyllable.txt', 'r', encoding='utf-8', errors='ignore')
    x = a_file.read()
    return json.loads(x)

def GenarateTwoSyllableChunks():
    a_file = open('threeSyllable.txt', 'r', encoding='utf-8', errors='ignore')
    x = a_file.read()
    return json.loads(x)

if __name__ == '__main__':
    if os.path.isfile('adaderana.txt'):
        with io.open('adaderana.txt', encoding='utf8') as fin:
            text = fin.read()
    UniqueWordList = Preprocess(text)
    Unigram_counter_model = SetUpUnigramModel()
    Bigram_counter_model = GenarateThreeSyllableChunks()
    Trigram_counter_model = GenarateTwoSyllableChunks()
    wordlist = ["අර්තික","සාකාච්චා","සහබාගි","තිඩෙනෙකු", "අමාත්‍යන්ශ", "අසඩිතයින්ගෙ", "කරඉ"]
    for word in UniqueWordList:
    #for word in wordlist:
        PermutationList = []
        GeneratePermutations(word)
        BestSuggestion = SelectBestSuggestion(Unigram_counter_model,Bigram_counter_model,Trigram_counter_model,word)
        #f = a=open('myfile.txt', 'a', encoding='utf-8', errors='ignore')
        text = text.replace(word,BestSuggestion)
    print(text)