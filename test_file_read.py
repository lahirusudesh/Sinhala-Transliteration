import os
import io
import nltk
from nltk.lm.preprocessing import padded_everygram_pipeline
from nltk.lm import MLE

if __name__ == '__main__':
    if os.path.isfile('adaderana.txt'):
        with io.open('adaderana.txt', encoding='utf8') as fin:
            text = fin.read()
    tokenized_text = [list(map(str.lower, nltk.word_tokenize(sent)))
                      for sent in nltk.sent_tokenize(text)]
    # Preprocess the tokenized text for 3-grams language modelling
    n = 3
    train_data, padded_sents = padded_everygram_pipeline(n, tokenized_text)
    model = MLE(n)
    model.fit(train_data, padded_sents)
    print(model.generate(10, random_seed=5))