from nltk.util import pad_sequence
from nltk.util import bigrams
from nltk.util import ngrams
from nltk.util import everygrams
from nltk.lm.preprocessing import pad_both_ends
from nltk.lm.preprocessing import flatten
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.lm.preprocessing import padded_everygram_pipeline
from nltk.lm import MLE
import os
import io #codecs


if __name__ == '__main__':
    text = ['ධිර පරීක්ෂණ පෞද්ගලික අංශයෙන් සිදුකිරීම']
    tokenizer = RegexpTokenizer('\s+', gaps=True)
    words = tokenizer.tokenize(text[0])

    padded_sent = list(pad_sequence(words,
                      pad_left=True, left_pad_symbol="<s>",
                      pad_right=True, right_pad_symbol="</s>",
                      n=2))
    all_grams = list(everygrams(padded_sent, max_len=2))
    #bi = list(bigrams(words))
    # Preprocess the tokenized text for 3-grams language modelling
    n = 3
    train_data, padded_sents = padded_everygram_pipeline(n, words)
    model = MLE(n)
    model.fit(train_data, padded_sents)
    print(len(model.vocab))
    print(model.vocab.lookup(padded_sent))
    print(model.counts)
    print(padded_sent)
