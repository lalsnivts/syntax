# coding=utf-8
__author__ = 'gisly'
import os
import codecs

def getTextTitle(filename):
    return os.path.splitext(os.path.basename(filename))[0]

def saveDataToFile(data, folder, filename):
    fullFilename = os.path.join(folder, filename)
    with codecs.open(fullFilename, 'w', 'utf-8') as fout:
        fout.write(data)


    
    