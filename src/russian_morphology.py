# coding=utf-8
__author__ = 'gisly'
from pymorphy import get_morph
morph = get_morph('D:\\LingM\\pymorphy\\ru.sqlite-json\\')

POS_CODES = {
             u'Г':'V',
             u'ИНФИНИТИВ':'V',
             u'С':'N',
             u'П':'Adj',
             u'КР_ПРИЛ':'Adj',
             
             u'СОЮЗ':'Conj',
             u'ЧИСЛ':'N',
             u'МС-П':'Det',
             u'Н':'Adv',
             u'ПРЕДЛ':'Prep',
             u'МС':'PronounToSee',
             
             u'ЧАСТ':'Adv',
             }



def getPOS(lemma):
    print lemma
    info = morph.get_graminfo(lemma.upper())[0]
    print info['class']
    return POS_CODES[info['class']]