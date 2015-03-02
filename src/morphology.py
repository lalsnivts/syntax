# coding=utf-8
__author__ = 'gisly'
from pymorphy import get_morph
import tokenizer
import common_constants
morph = get_morph('D:\\LingM\\pymorphy\\ru.sqlite-json\\')

VERB = u'Г'
INFINITIVE = u'ИНФИНИТИВ'

NOUN = u'С'
ADJECTIVE = u'П'
ADVERB = u'Н'
PREPOSITION = u'ПРЕДЛ'
NUMERAL_ADJECTIVE = u'ЧИСЛ-П'
NUMERAL = u'Ч'
PREDICATIVE = u'ПРЕДК'

PARTICIPLE = u'ПРИЧАСТИЕ'
PARTICIPLE_BR = u'КР_ПРИЧАСТИЕ'


COMPARATIVE_DEGREE = u'сравн'


PAST_TENSE = u'прш'
PRESENT_TENSE = u'нст'
FUTURE_TENSE = u'буд'

PERFECTIVE_ASPECT = u'св'
IMPERFECTIVE_ASPECT = u'нс'

DELIM=','

DEVERBAL_ENDINGS = [u'ение', u'ание']

"""LIGHT_VERBS = [u'СОВЕРШИТЬ', u'СОВЕРШАТЬ', u'ПРОВЕСТИ', u'ПРОВОДИТЬ', u'СУЩЕСТВОВАТЬ']
COPULAR_VERBS = [u'ЯВЛЯТЬСЯ', u'БЫТЬ', u'ПРЕДСТАВИТЬ', u'СТАТЬ', u'СТАНОВИТЬСЯ']"""








def getPOSCode(word):
    if isFiniteVerb(word):
        return common_constants.VERB, [VERB]
    if isParticiple(word):
        if isBriefParticiple(word):
            return common_constants.BRIEF_PARTICIPLE, [PARTICIPLE]
        else:
            return common_constants.PARTICIPLE, [PARTICIPLE]
    if isNoun(word):
        return common_constants.NOUN, [NOUN]
        #return common_constants.OTHER, [NOUN]
    if isInfinitive(word):
        return common_constants.INFINITIVE, [INFINITIVE]
    
    if isCompAdjective(word):
        #return common_constants.COMP_ADJ, [ADJECTIVE]
        return common_constants.OTHER, [ADJECTIVE]
    
    
    return common_constants.OTHER, None



def getTense(word):
    if hasProperties(word, [PAST_TENSE]):
        return common_constants.TENSE_PAST
    
    if hasProperties(word, [PRESENT_TENSE]):
        return common_constants.TENSE_PRESENT
    
    if hasProperties(word, [FUTURE_TENSE]):
        return common_constants.TENSE_FUTURE
    
    return common_constants.FEATURE_NA


def getFirstPOSMethodPosition(POSMethod, wordList):
    for position, word in enumerate(wordList):
        if POSMethod(word):
            return word, position
    return None

def getLastPOSMethodPosition(POSMethod, wordList):
    lastVerbPosition = None
    for position, word in enumerate(wordList):
        if POSMethod(word):
            lastVerbPosition = (word, position - len(wordList))
    return lastVerbPosition

def getFirstPOSPosition(POS, wordList):
    for position, word in enumerate(wordList):
        if isPos(word, POS):
            return word, position
    return None

def getLastPOSPosition(POS, wordList):
    lastVerbPosition = None
    for position, word in enumerate(wordList):
        if isPos(word, POS):
            lastVerbPosition = (word, position - len(wordList))
    return lastVerbPosition

def getFirstVerbPosition(wordList):
    return getFirstPOSPosition(VERB, wordList)

def getLastVerbPosition(wordList):
    return getLastPOSPosition(VERB, wordList)


def getFirstNounPosition(wordList):
    return getFirstPOSPosition(NOUN, wordList)

def getLastNounPosition(wordList):
    return getLastPOSPosition(NOUN, wordList)

def getMorphoInfo(word):   
    info = morph.get_graminfo(word.upper())
    if not info:
        return None
    return [[info_variant['class'],info_variant['info'].split(DELIM), info_variant['method']] for info_variant in info]

"""def tryAddComplements(word, verbPosition, wordList):
    if (verbPosition < len(wordList) - 1):
        if isLightVerb(word):
            return ' ' + addLightVerbComplements(verbPosition + 1, wordList)
        elif isCopularVerb(word):
            return ' ' + addCopularComplements(verbPosition + 1, wordList)
        elif isPredicativeWord(word):
            return ' ' + addPredicativeComplements(verbPosition + 1, wordList)
    return '' 




def addLightVerbComplements(indexToStart, wordList):
    return addComplements(indexToStart, wordList, [NOUN])

def addCopularComplements(indexToStart, wordList):
    return addComplements(indexToStart, wordList, [ADJECTIVE, NUMERAL_ADJECTIVE, NOUN])

def addPredicativeComplements(indexToStart, wordList):
    return addComplements(indexToStart, wordList, [INFINITIVE])

def addComplements(indexToStart, wordList, COMPL_POS):
    complements = ''
    for i in range(indexToStart, len(wordList)):
        curWord = wordList[i]
        complements+=' '+curWord
        if isPos(curWord, COMPL_POS) and not isAdjective(curWord):
            return complements.strip()
    return complements.strip()"""

  
  
def isNotFromDictionary(word):
    info = getMorphoInfo(word)
    if not info:
        return True
    for info_variant in info:
        if 'predict' in info_variant[2]:
            return True
    return False
      
        
def isPos(word, POS_LIST):
    info = getMorphoInfo(word)
    if not info:
        return False
    for info_variant in info:
        if info_variant[0] in POS_LIST:
            return True
    return False

def isDeverbal(lemma):
    lemmaLower = lemma.lower()
    for ending in DEVERBAL_ENDINGS:
        if lemmaLower.endswith(ending):
            return True
    return False


def hasProperties(word, PROP_LIST):
    propSetToSearch = set(PROP_LIST)
    info = getMorphoInfo(word)
    if not info:
        return False
    for info_variant in info:
        propSet = set(info_variant[1])
        
        if propSet.issuperset(propSetToSearch):
            return True
    return False

def isPredicative(word):
    return isPos(word, [VERB, PREDICATIVE, PARTICIPLE, PARTICIPLE_BR]) or isCompAdjective(word)
    
def isVerb(word):
    return isPos(word, [VERB, PREDICATIVE, PARTICIPLE, PARTICIPLE_BR])

def isFiniteVerb(word):
    return isPos(word, [VERB])

def isInfinitive(word):
    return isPos(word, [INFINITIVE])

def isNoun(word):
    return isPos(word, [NOUN])

def isAdjective(word):
    return isPos(word, [ADJECTIVE, NUMERAL_ADJECTIVE, PARTICIPLE, PARTICIPLE_BR])

def isCompAdjective(word):
    return isAdjective(word) and hasProperties(word, [COMPARATIVE_DEGREE])  

def getLemmaSet(word):
    
    
    res = morph.get_graminfo(word.upper())
    lemmaSet =  morph.normalize(word.upper())
    if type(lemmaSet) == set:
        return lemmaSet
    return set(lemmaSet)

"""def isLightVerb(word):
    return isWordInList(word, LIGHT_VERBS)

def isCopularVerb(word):
    return isWordInList(word, COPULAR_VERBS)"""




def isParticiple(word):
    return isPos(word, [PARTICIPLE, PARTICIPLE_BR])

def isBriefParticiple(word):
    return isPos(word, [PARTICIPLE_BR])





def isWordInList(word, wordList):
    lemmata = getLemmaSet(word)
    for lemma in lemmata:
        if lemma in wordList:
            return True
    return False



def getLastLemma(text, POS_LIST = None):
    lastWord = tokenizer.getLastWord(text)
    if lastWord:
        return getLemmaByPosList(lastWord, POS_LIST)
    return None


def getFirstLemma(token):
    lemmata = getLemmaSet(token)
    if type(lemmata) == set:
        return lemmata.pop().lower()
    else:
        return lemmata.lower()

def getLemmaByPosList(token, POS_LIST = None):
    
    if filter is None:
        return getFirstLemma(token)

    info = morph.get_graminfo(token.upper())
    
    for res in info:
        if res['class'] in POS_LIST:
            return res['norm']
    return None
    
    
    return None



