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
             u'МС':'Pro',
             
             u'ЧАСТ':'Adv',
             u'ЧИСЛ-П':'Card',
              u'ПРИЧАСТИЕ':'PR',
              u'ДЕЕПРИЧАСТИЕ':'CV',
              u'ВВОДН':'Adv',
              u'МЕЖД':'Intj'
             }

DEFAULT_POS_CODE = 'V'



def getPOS(lemma):
    
    morphInfo =  morph.get_graminfo(lemma.upper())
    if morphInfo:
        info = morph.get_graminfo(lemma.upper())[0]
        return POS_CODES[info['class']]
    return DEFAULT_POS_CODE