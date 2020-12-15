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
SimilarLetterGroup = [{'\u0DD0','\u0DD1‍'},
                      {'\u0DDC','\u0DDD'},
                      {'\u0DD4','\u0DD6'},
                      {'\u0DD9','\u0DDA'},
                      {'අ','ආ','ඇ','ඈ'},
                      {'ඉ','ඊ','යි'},
                      {'උ','ඌ'},
                      {'එ','ඒ'},
                      {'ක','ඛ'},
                      {'ල','ළ'},
                      {'ප','ඵ'},
                      {'ග','ඝ'},
                      {'ච','ඡ'},
                      {'බ','භ','ඹ'},
                      
                      {'ඩ','ඪ','ද','ධ','ඳ'},
                      {'ජ','ඣ'},
                      {'න','ණ'},
                      {'ට','ඨ'},
                      {'ත','ථ'},
                      {'ස', 'ශ', 'ෂ'},
                      {''}]

def Preprocess(InputText):
    UniqueWordList = []
    tokenized_sent = [list(map(str.lower, nltk.word_tokenize(sent)))
                      for sent in nltk.sent_tokenize(text)]
    for sent in tokenized_sent:
        for word in sent:
            if word not in UniqueWordList and not word.isnumeric() and word not in special_chars:
                UniqueWordList.append(word);
    return UniqueWordList

def oneDArray(x):
    return list(chain(*x))

def GeneratePermutations(word):
    if 'න්' in word:
        newWord = word.replace('න්', 'ං')
        if newWord not in PermutationList:
            PermutationList.append(newWord)
    # ‌ෙ replace with ැ
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


def SelectBestSuggestion(unigram_model,PerList, word):
    for w in PerList:
        print(w, unigram_model[w])

if __name__ == '__main__':
    if os.path.isfile('adaderana.txt'):
        with io.open('adaderana.txt', encoding='utf8') as fin:
            text = fin.read()
    UniqueWordList = Preprocess(text)
    word = "සඳහා"
    GeneratePermutations(word)
    print(PermutationList)

