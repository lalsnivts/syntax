# coding=utf-8
__author__ = 'gisly'
import re
import nltk
import morphology

SENTENCE_END = ur'[.!\?]'


PUNCT_LIST = u' .?!:;,()[]-"\'«»\r\n\\~'
PUNCT_REGEX = '[' + re.escape(PUNCT_LIST) + ']'


from pymorphy.contrib import tokenizers

def getFirstSentence(text):
    return re.split(SENTENCE_END, text)[0]

def getLastSentence(text):
    return re.split(SENTENCE_END, text)[-1]








def getLastPOSMethodPosition(POSMethod, sentence):
    return morphology.getLastPOSMethodPosition(POSMethod, tokenizeSentence(sentence))   
    
def getFirstPOSMethodPosition(POSMethod, sentence):
    return morphology.getFirstPOSMethodPosition(POSMethod, tokenizeSentence(sentence))


def getLastPOSPosition(POS, sentence):
    return morphology.getLastPOSPosition(POS, tokenizeSentence(sentence))   
    
def getFirstPOSPosition(POS, sentence):
    return morphology.getFirstPOSPosition(POS, tokenizeSentence(sentence))

def getFirstVerbPosition(sentence):
    return morphology.getFirstVerbPosition(tokenizeSentence(sentence)) 

def getLastVerbPosition(sentence):
    return morphology.getLastVerbPosition(tokenizeSentence(sentence)) 
    
def getFirstNounPosition(sentence):
    return morphology.getFirstNounPosition(tokenizeSentence(sentence))


def getLastNounPosition(sentence):
    return morphology.getLastNounPosition(tokenizeSentence(sentence))

def getLastWord(sentence):
    allWords = [word for word in tokenizers.extract_words(sentence)]
    if allWords:
        return allWords[-1]
    return None

def tokenizeSentence(sentence):
    return nltk.word_tokenize(sentence)


def tokenizeText(text):
    return [word for word in tokenizers.extract_words(text)]





def splitIntoTextSentencesIndices(text):
    sentences = nltk.sent_tokenize(text.replace('\r\n', '_.'))
    result = []
    for sentence in sentences:
        origSentence = sentence.replace('_.','\r\n')
        result.append((origSentence, text.find(origSentence)))
    return result


def tokenizeSentenceIntoWordsIndices(text):
    words = tokenizers.extract_tokens(text)
    result = []
    for word in words:
        result.append((word, text.find(word)))
    return result


def removePunctuation(text):
    return re.sub(PUNCT_REGEX, '', text)
