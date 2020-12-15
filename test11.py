import io
import json
import os
from string import punctuation
from nltk import word_tokenize, sent_tokenize
from nltk.lm.preprocessing import padded_everygram_pipeline
from nltk.lm import MLE

bestWordList = {}
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

def BestSuggestion(word1,word2,word,TrigramModel):
    bestword = word
    highestProbablity = 0
    for perWord in PermutationDict[word]:
        probability = TrigramModel.score(perWord, [word1,word2])
        if (probability > highestProbablity):
            bestword = perWord
    return bestword

def Padsent(TrigramModel):
    newsListOne = []
    text = ''
    if os.path.isfile('adaderana.txt'):
        with io.open('adaderana.txt', encoding='utf8') as fin:
            text = fin.read()
    tokenized_text = [list(map(str.lower, word_tokenize(sent)))
                      for sent in sent_tokenize(text)]
    opensent = ['<s>','<s>']
    closeSent = ['</s>','</s>']
    padded_sent = tokenized_text.copy()
    for i, sent in enumerate(padded_sent):
        padded_sent[i] = opensent + sent + closeSent
    print(tokenized_text)
    for sent in padded_sent:
        for i, word in enumerate(sent[2:-2]):
            if word not in punctuation and not word.isnumeric():
                bestWordList[word]= BestSuggestion(sent[i-2],sent[i-1],word,TrigramModel)

if __name__ == '__main__':
    with open('PermutationDictionary.txt', 'r', encoding='utf-8', errors='ignore') as file3:
        PermutationDict = json.load(file3)
    print(PermutationDict)
    TrigramModel = TrainNGramModel()
    Padsent(TrigramModel)
    print(bestWordList)