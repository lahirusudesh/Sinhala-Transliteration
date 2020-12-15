import os
import io #codecs
import json
from nltk import word_tokenize, sent_tokenize
from nltk.lm.preprocessing import padded_everygram_pipeline
from nltk.lm import MLE

if __name__ == '__main__':
    newsListOne = []
    text = ''
    with open("combined.txt", 'r', encoding='utf-8', errors='ignore') as outfile:
        newslist = json.load(outfile)
    for news in newslist:
        newsListOne.extend(news)
    text = ' '.join([str(elem) for elem in newsListOne])
    tokenized_text = [list(map(str.lower, word_tokenize(sent)))
                      for sent in sent_tokenize(text)]
    print(tokenized_text)
    n = 3
    train_data, padded_sents = padded_everygram_pipeline(n, tokenized_text)

    model = MLE(n)  # Lets train a 3-grams maximum likelihood estimation model.
    model.fit(train_data, padded_sents)
    print(padded_sents)
    print(model.counts[['<s>', '<s>']]['තවත්'])
    print(model.score('කොවිඩ්', ['<s>','<s>']))