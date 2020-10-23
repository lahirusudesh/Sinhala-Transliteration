import os
import io
import nltk
ThreeSyllableChunks = {}
def DivideTokenIntoThreeSyllableChunks(token):
    n = 4
    chunks = [token[i:i+n] for i in range(0,len(token))]
    return chunks

if __name__ == '__main__':
    if os.path.isfile('combined.txt'):
        with io.open('combined.txt', encoding='utf8') as fin:
            text = fin.read()
    tokenized_sent = [list(map(str.lower, nltk.word_tokenize(sent)))
                      for sent in nltk.sent_tokenize(text)]
    for sent in tokenized_sent:
        for token in sent:
            chunks= DivideTokenIntoThreeSyllableChunks(token)
            for chunk in chunks:
                if chunk in ThreeSyllableChunks:
                    ThreeSyllableChunks[chunk] += 1
                else:
                    ThreeSyllableChunks[chunk] = 1
    print(ThreeSyllableChunks[''])