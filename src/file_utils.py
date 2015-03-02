# coding=utf-8
__author__ = 'gisly'
import os

def getTextTitle(filename):
    return os.path.splitext(os.path.basename(filename))[0]
    
    