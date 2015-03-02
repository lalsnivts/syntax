# coding=utf-8
__author__ = 'gisly'
import os
import codecs
import re
import file_utils
import eaf_utils
import russian_morphology


TEXT_EXTENSION = 'txt'
WORD_EXTENSION = 'w'
MORPH_EXTENSION = 'm'
SYNTACTIC_EXTENSION = 'a'




WORD_START = '<?xml version="1.0" encoding="UTF-8"?>\
<lalswdata xmlns="http://ufal.mff.cuni.cz/pdt/pml/">\
    <head>\
        <schema href="lalswschema.xml" />\
    </head>\
    <meta>-</meta>\
    <doc id="DOC_ID" source_id="DOC_TEXT_NAME">\
        <docmeta></docmeta>'
        
WORD_END = '</doc>\
</lalswdata>'


WORD_ELEMENT = '<w id="w-DOC_ID-sSENTENCE_NUMwTOKEN_NUM">\
                <token>TOKEN_CONTENT</token>\
                </w>'




MORPH_START = '<?xml version="1.0" encoding="UTF-8"?>\
                <lalsmdata xmlns="http://ufal.mff.cuni.cz/pdt/pml/">\
                  <head>\
                    <schema href="lalsmschema.xml" />\
                    <references>\
                      <reffile id="w" name="wdata" href="WORD_FILENAME" />\
                    </references>\
                  </head>\
                  <meta>\
                    <lang>ev</lang>\
                    <annotation_info>ANNOTATION</annotation_info>\
                  </meta>'
                  
                  
                  

WORD_SENTENCE_START  = '<para>'
WORD_SENTENCE_END  = '</para>'
                  
MORPH_SENTENCE_START = '<s id="m-DOC_ID-sSENTENCE_NUM">'
MORPH_SENTENCE_END = '</s>'

MORPH_ELEMENT = '<m id="m-DOC_ID-sSENTENCE_NUMwTOKEN_NUM">\
      <src.rf>TODO</src.rf>\
      <w.rf>w#w-DOC_ID-sSENTENCE_NUMwTOKEN_NUM</w.rf>\
      <form>FORM</form>\
      <lemma>LEMMA</lemma>\
      <tag>TAG</tag>\
      <!--<analysis>ANALYSIS</analysis>-->\
    </m>'
    
    
MORPH_ELEMENT_SLIP = '<m id="m-DOC_ID-sSENTENCE_NUMwTOKEN_NUM">\
      <src.rf>TODO</src.rf>\
      <w.rf>w#w-DOC_ID-sSENTENCE_NUMwTOKEN_NUM</w.rf>\
      <form>FORM</form>\
      <form_change>true</form_change>\
      <tag>TAG</tag>\
    </m>'


MORPH_END = '</lalsmdata>'



SYNT_START = '<?xml version="1.0" encoding="UTF-8"?>\
<lalsdata xmlns="http://ufal.mff.cuni.cz/pdt/pml/">\
    <head>\
        <schema href="lals_schema.xml" />\
        <references>\
            <reffile id="m" name="mdata" href="MORPH_FILENAME" />\
            <reffile id="w" name="wdata" href="WORD_FILENAME" />\
        </references>\
    </head>\
    <meta>\
        <annotation_info>\
            <desc>ANNOTATION</desc>\
        </annotation_info>\
    </meta>\
    <trees>'
    
SYNT_SENTENCE_START = '<LM id="a-DOC_ID-sSENTENCE_NUM"><s.rf>m#m-DOC_ID-sSENTENCE_NUM</s.rf><children>'
SYNT_ELEMENT = '<nonterminal id="a-a-DOC_ID-sSENTENCE_NUMwTOKEN_NUM">\
                    <cat>CATEGORY</cat>\
                    <children>\
                        <terminal id="a-DOC_ID-sSENTENCE_NUMwTOKEN_NUM">\
                            <m.rf>m#m-DOC_ID-sSENTENCE_NUMwTOKEN_NUM</m.rf>\
                            <ord>TOKEN_NUM</ord>\
                        </terminal>\
                    </children>\
                </nonterminal>'
                
SYNT_SENTENCE_END = '</children></LM>'    
    
SYNT_END = '</trees></lalsdata>'



PARTICIPLE_CODES = ['PANT', 
                    'PPOST']
  
  


def convertElanFileToPML(elanFilename, pmlFolder, metaDescription):
    baseElanFilename = file_utils.getTextTitle(elanFilename)
    text_filename = createOutputFilename(pmlFolder, baseElanFilename, TEXT_EXTENSION)
    word_filename = createOutputFilename(pmlFolder, baseElanFilename, WORD_EXTENSION)
    morph_filename = createOutputFilename(pmlFolder, baseElanFilename, MORPH_EXTENSION)
    syntactic_filename = createOutputFilename(pmlFolder, baseElanFilename, SYNTACTIC_EXTENSION)
    print word_filename
    with codecs.open(text_filename, 'w', 'utf-8' ) as text_out:
        with codecs.open(word_filename, 'w', 'utf-8' ) as word_out:
            with codecs.open(morph_filename, 'w', 'utf-8' ) as morph_out:
                with codecs.open(syntactic_filename, 'w', 'utf-8' ) as synt_out:  
                    wordStart = WORD_START.replace('DOC_ID', baseElanFilename)\
                                          .replace('DOC_TEXT_NAME', os.path.basename(text_filename))
                    word_out.write(wordStart)
                    
                    
                    
                    morphStart = MORPH_START.replace('WORD_FILENAME', os.path.basename(word_filename))
                    syntStart = SYNT_START.replace('WORD_FILENAME', os.path.basename(word_filename))\
                                           .replace('MORPH_FILENAME', os.path.basename(morph_filename))
                    
                    
                    morph_out.write(morphStart)
                    synt_out.write(syntStart)
                    writeConversionToFiles(elanFilename, text_out, word_out, morph_out, synt_out, baseElanFilename) 
                    word_out.write(WORD_END)
                    morph_out.write(MORPH_END)
                    synt_out.write(SYNT_END)
    
def writeConversionToFiles(elanFilename, text_out, word_out, morph_out, synt_out, baseElanFilename):
    textInfo = eaf_utils.getTextInfo(elanFilename) 
    for sentenceNum in range(0, len(textInfo)):
        sentenceInfo = textInfo[sentenceNum]
        word_out.write(WORD_SENTENCE_START)
        
        text_out.write(sentenceInfo['sentence'] + '\r\n')
        morphInfo = sentenceInfo['morphology']
        morphSentenceStart = MORPH_SENTENCE_START\
                               .replace('DOC_ID', baseElanFilename)\
                               .replace('SENTENCE_NUM', str(sentenceNum))
        morph_out.write(morphSentenceStart)
        
        
        syntSentenceStart = SYNT_SENTENCE_START\
                               .replace('DOC_ID', baseElanFilename)\
                               .replace('SENTENCE_NUM', str(sentenceNum))
        
        synt_out.write(syntSentenceStart)
        for tokenNum in range(0, len(morphInfo)):
            morphInfoElement = morphInfo[tokenNum]
 
            wordElement = createTokenElement(morphInfoElement['token'], baseElanFilename, sentenceNum, tokenNum)
            word_out.write(wordElement)
            
            
            if u'bisōn' in wordElement:
                aa = 9

            morphElement, isSlip = createMorphElement(morphInfoElement, baseElanFilename, sentenceNum, tokenNum)
            morph_out.write(morphElement)
            
            if not isSlip:
                syntElement = createSyntElement(morphInfoElement, baseElanFilename, sentenceNum, tokenNum)
                synt_out.write(syntElement)
            
        synt_out.write(SYNT_SENTENCE_END)
        morph_out.write(MORPH_SENTENCE_END)
        word_out.write(WORD_SENTENCE_END)
    
    
    
def createTokenElement(token, docId, sentenceNum, tokenNum):
    return WORD_ELEMENT.replace('TOKEN_CONTENT', token)\
                       .replace('DOC_ID', docId)\
                       .replace('SENTENCE_NUM', str(sentenceNum))\
                       .replace('TOKEN_NUM', str(tokenNum))
                       
def createMorphElement(morphInfoElement, docId, sentenceNum, tokenNum):
    token = morphInfoElement['token']
    lemma = morphInfoElement['analysis'][0]['fon']
    analysisToPrint = '-'.join([(analysisElement['fon']+'=' + analysisElement['gloss']) for analysisElement in morphInfoElement['analysis']])
    isSlip = (analysisToPrint.endswith('SLIP'))
    morphElement = fillInMorphElement(docId, sentenceNum, tokenNum, token, lemma, analysisToPrint, isSlip)
    return morphElement, isSlip
        
    
                               

def fillInMorphElement(docId, sentenceNum, tokenNum, token, lemma, analysisToPrint, isSlip):
    if isSlip:
        return MORPH_ELEMENT_SLIP.replace('DOC_ID', docId)\
                               .replace('SENTENCE_NUM', str(sentenceNum))\
                               .replace('TOKEN_NUM', str(tokenNum))\
                               .replace('FORM', token)\
                               .replace('TAG', analysisToPrint)
    return MORPH_ELEMENT.replace('DOC_ID', docId)\
                               .replace('SENTENCE_NUM', str(sentenceNum))\
                               .replace('TOKEN_NUM', str(tokenNum))\
                               .replace('FORM', token)\
                               .replace('LEMMA', lemma)\
                               .replace('TAG', analysisToPrint)
                               
                               
def createSyntElement(morphInfoElement, docId, sentenceNum, tokenNum):
    lemmaGloss = morphInfoElement['analysis'][0]['gloss']
    if isPronoun(lemmaGloss):
        pos = 'N'
    elif isPossessivePronoun(lemmaGloss):
        pos = 'Adj'
    elif isSlip(lemmaGloss):
        pos = 'SLIP'
    elif isNeg(lemmaGloss):
        pos = 'NEG'
    elif isRfl(lemmaGloss):
        pos = 'RFL'
    else:
        pos = analyzePos(lemmaGloss, morphInfoElement['analysis'])
    category = pos + 'P'
    return SYNT_ELEMENT.replace('DOC_ID', docId)\
                               .replace('SENTENCE_NUM', str(sentenceNum))\
                               .replace('TOKEN_NUM', str(tokenNum))\
                               .replace('CATEGORY', category)
                               
def isPronoun(lemmaGloss):
    return re.match('\d', lemmaGloss) is not None

def isPossessivePronoun(lemmaGloss):
    return lemmaGloss.startswith('PS')    


def isSlip(lemmaGloss):
    return lemmaGloss.endswith('SLIP')   


def isNeg(lemmaGloss):
    return lemmaGloss.endswith('NEG')  


def isRfl(lemmaGloss):
    return lemmaGloss.endswith('RFL')                             
                               
def analyzePos(lemmaGloss, morphAnalysis):
    russianLemmaGloss = russian_morphology.getPOS(lemmaGloss)
    if russianLemmaGloss != 'V':
        return russianLemmaGloss
    elif isParticiple(morphAnalysis):
        return 'PR' 
    elif isConverb(morphAnalysis):
        return 'CV'
    return russianLemmaGloss


def isParticiple(morphAnalysis):
    for element in morphAnalysis:
        if isParticipleGloss(element['gloss']):
            return True
    return False


def isParticipleGloss(elementGloss):
    for participleCode in PARTICIPLE_CODES:
        if elementGloss == participleCode:
            return True
    return False


def isConverb(morphAnalysis):
    for element in morphAnalysis:
        if element['gloss'].startswith('CV'):
            return True
    return False
        
    
    
def createOutputFilename(folder, baseName, extension):
    return os.path.join(folder, baseName + '.' + extension)


convertElanFileToPML("D://ForElan/ForSIL/2011 Hantayskoye Ozero Turskaya Minna Dmitriyevna L/2011_Hantayskoye_Ozero_Turskaya_Minna_Dmitriyevna_L_transliterated.eaf", 
                     "D://Nivts//Syntax//nivts_treebank", "")