# -*- coding: utf-8 -*-
import json
import sys
import csv
import nltk

sys.setrecursionlimit(10**9)
consonants= []
consonantsUni= []
vowels= []
vowelsUni= []
vowelModifiersUni= []
specialConsonants= []
specialConsonantsUni= []
specialCharUni= []
specialChar= []

vowelsUni.extend(['ඌ','ඕ','ඕ','ආ','ආ','ඈ','ඈ','ඈ','ඊ','ඊ','ඊ','ඊ','ඒ','ඒ','ඒ','ඌ','ඌ','ඖ','ඇ'])

vowels.extend(['oo','o','oe','aa','a\\)','Aa','A\\)','ae','ii','i\\)','ie','ee','ea','e\\)','ei','uu','u\\)','au','/\a'])

vowelModifiersUni.extend(['ූ','ෝ','ෝ','ා','ා','ෑ','ෑ','ෑ','ී','ී','ී','ී','ේ','ේ','ේ','ූ','ූ','ෞ','ැ'])

vowelsUni.extend(['අ','ඇ','ඉ','එ','උ','ඔ','ඓ'])

vowels.extend(['a','A','i','e','u','o','I'])

vowelModifiersUni.extend(['','ැ','ි','ෙ','ු','ො','ෛ'])

nVowels=26;

specialConsonantsUni.extend(['ං','ඃ','ඞ','ඍ'])

specialConsonants.extend(["\n","\h","\R"])
# special characher Repaya
specialConsonantsUni.append('ර්'+'\u200D')
specialConsonantsUni.append('ර්'+'\u200D')

specialConsonants.append("/R")
specialConsonants.append("\r")

consonantsUni.extend(['ච','ත','ශ','ඥ'])

consonants.extend(['ch','th','sh','gn'])

consonantsUni.extend(['ක','ක','ග','ජ','ට','ද','න','ප','බ','ම','ය','ර','ල', 'ව','ව','ස','හ'])

consonants.extend(['k','c','g','j','t','d','n','p','b','m','y','r','l','v','w','s','h'])

consonantsUni.append('ර')
consonants.append('r')

specialCharUni.append('ෲ')
specialChar.append('ruu')
specialCharUni.append('ෘ')
specialChar.append('ru')

def LoadEnglishWordList():
    with open("english.txt","r",encoding='utf-8', errors='ignore') as f_en:
        english_words = json.load(f_en)
        return english_words

def Translate(text):
    # special consonents
    for i in range (0,len(specialConsonants)):
        text = text.replace(specialConsonants[i], specialConsonantsUni[i])
    # consonents + special
    for i in range (0,len(specialCharUni)):
        for j in range(0,len(consonants)):
            s = consonants[j] + specialChar[i]
            v = consonantsUni[j] + specialCharUni[i]
            r = s
            text = text.replace(r, v)
    # consonants + Rakaransha + vowel modifiers
    for j in range(0,len(consonants)):
        for i in range(0,len(vowels)):
            s = consonants[j] + "r" + vowels[i]
            v = consonantsUni[j] + "්‍ර" + vowelModifiersUni[i]
            r = s
            # r = new RegExp(s, "g")
            text = text.replace(r, v)

        s = consonants[j] + "r"
        v = consonantsUni[j] + "්‍ර‍"
        r = v
        text = text.replace(r, v)


    # constants with vowels modifiers
    for i in range(0,len(consonants)):
        for j in range(0,nVowels):
            s = consonants[i]+vowels[j]
            v = consonantsUni[i] + vowelModifiersUni[j]
            r = s
            text = text.replace(r, v)



    # Hal kirima
    for i in range(0, len(consonants)):
        r = consonants[i]
        text = text.replace(r, consonantsUni[i]+"්")


    # adding vowels
    for i in range(0,len(vowels)):
        r = vowels[i]
        text = text.replace(r, vowelsUni[i])

    return text

if __name__ == '__main__':
    print(Translate("lahiro)‍‍‍‍,laahiru, kramaya"))
    output = []
    eng = LoadEnglishWordList()
    print(eng)
    with open('data.csv', 'rt')as f:
        data = csv.DictReader(f)
        for row in data:
            sent = row['content'].lower()
            words = nltk.wordpunct_tokenize(sent)
            for i in range(len(words)):
                if words[i] not in eng or not words[i].isalpha():
                    words[i] = Translate(words[i])
            print(' '.join(word for word in words))