# coding=utf-8
__author__ = 'gisly'

import xml.etree.ElementTree as ET
import file_utils

EAF_DELIMITER = '_'
TECHNICAL_DELIMITER = '#'

GLOSS_XPATH = ".//TIER[@TIER_ID='gl']/ANNOTATION/REF_ANNOTATION"
FON_XPATH = ".//TIER[@TIER_ID='fon']/ANNOTATION/REF_ANNOTATION"
FONWORD_XPATH = ".//TIER[@TIER_ID='fonWord']/ANNOTATION/REF_ANNOTATION"
EVENKI_XPATH = ".//TIER[@TIER_ID='ev']/ANNOTATION/ALIGNABLE_ANNOTATION"


ANNOTATION_VALUE_XPATH = '/ANNOTATION_VALUE'

ANNOTATION_REF_ATTRIBUTE = 'ANNOTATION_REF'
ANNOTATION_ID_ATTRIBUTE = 'ANNOTATION_ID'

EAF_EXT = '.eaf'

def getLocationByFilename(filename):
    filenameParts = filename.split(EAF_DELIMITER)
    return filenameParts[1].lower()



def getTextInfo(filename):
    root = getRoot(filename)
    sentences = getSentences(root)
    textInfo = []
    for sentence in sentences:
        textInfoSentence = dict()
        textInfoSentence['sentence'] = getAnnotationValueFromElement(sentence)
        textInfoSentence['morphology'] = getTokensBySentence(root, sentence)
        textInfo.append(textInfoSentence)
    return textInfo
        
        
    

def getTokensBySentence(root, sentence):
    sentenceId = getElementId(sentence)
    fonWords = getFonWordsById(root, sentenceId)
    morphInfos = []
    for fonWord in fonWords:
        morphInfo = dict()
        morphInfo['token'] = getAnnotationValueFromElement(fonWord)
        morphInfo['analysis'] = getAnalysis(root, fonWord)
        morphInfos.append(morphInfo)
    return morphInfos


def getAnalysis(root, fonWord):
    fonWordId = getElementId(fonWord)
    fons = getFonsById(root, fonWordId)
    analysis = []
    for fon in fons:
        fonId = getElementId(fon)
        gloss = getGlossById(root, fonId)
        analysis.append({'fon':getAnnotationValueFromElement(fon), 'gloss': getAnnotationValueFromElement(gloss)})
    return analysis
    
    
def getRoot(filename):
    tree = ET.parse(filename)
    return tree.getroot()


def getSentences(root):
    return root.findall(EVENKI_XPATH)


def getAnnotationValueFromElement(element):
    return element.find('.' + ANNOTATION_VALUE_XPATH).text.strip()


def getElementId(element):
    return element.attrib[ANNOTATION_ID_ATTRIBUTE]

def getFonWordsById(root, annotationId):    
    return root.findall(FONWORD_XPATH + "[@" + 
                      ANNOTATION_REF_ATTRIBUTE +  
                      "='" + annotationId+ "']");
        
        
def getFonsById(root, annotationId):
    return root.findall(FON_XPATH + "[@" + 
                      ANNOTATION_REF_ATTRIBUTE +  
                      "='" + annotationId+ "']");
                      
                      
def getGlossById(root, annotationId):
    return root.find(GLOSS_XPATH + "[@" + 
                      ANNOTATION_REF_ATTRIBUTE +  
                      "='" + annotationId+ "']");
                      



        