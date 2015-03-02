# coding=utf-8
__author__ = 'gisly'

import tokenizer
import morphology

SPECIAL_WORDS = [u'СПЕЦВЫПУСК', u'ЭЖ']

def isRussian(text):
    words = tokenizer.tokenizeText(text)
    numOfWordsNotFromDict = 0
    for word in words:
        if (not isSpecial(word) and morphology.isNotFromDictionary(word)):
            numOfWordsNotFromDict += 1
    return numOfWordsNotFromDict <= (len(words)/2)

def isSpecial(word):
    return word in SPECIAL_WORDS