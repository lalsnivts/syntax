# coding=utf-8
__author__ = 'gisly'
import Tkinter
from Tkinter import END

import tkFileDialog
import os
import elan_to_pml

class PmlUtils(object):
    folder = os.getcwd()
    filename = ''


    DESCRIPTION_WIDTH = 200
    RESULT_WIDTH = 200
    FILENAME_WIDTH = 100
    
   
    def __init__(self):
        self.init()

    def init(self):
        self.root=Tkinter.Tk()

        self.addControls()

        self.root.mainloop()

    def chooseFile(self):
        self.filename = tkFileDialog.askopenfilename(defaultextension='.eaf',
                                                filetypes=[('Eaf file','*.eaf'), ('All files','*.*')],
                                                initialdir = self.folder)
        if len(self.filename) > 0:
            self.folder = os.path.dirname(self.filename)
            self.saveFilenameText(self.filename)
            
        
    def convertFile(self):
        originalTierName = self.originalTierEntry.get()
        description = self.descriptionEntry.get()
        
        
            
        if len(self.filename ) > 0\
                and len(originalTierName) > 0\
                and len(description) > 0:
            
                outputFolder = os.path.dirname(self.filename)
                self.printResult("")
                
                
                try:
                    elan_to_pml.convertElanFileToPML(self.filename, outputFolder, 
                                                                    description, originalTierName)
                    self.printSuccess('sucess')
                except Exception, e:
                    self.printError('Error occurred:' + str(e))
                      
                
        elif len(self.filename) == 0:
            self.printError(u"Выберите файл .eaf")
        elif len(originalTierName) == 0:
            self.printError(u"Введите название слоя с оригинальным текстом")
        elif len(description) == 0:
            self.printError(u"Введите описание")
            
    
    def printError(self, resultText):
        self.printResult(resultText)
        self.resultEntry['bg'] = 'red'
        
    def printSuccess(self, resultText):
        self.printResult(resultText)
        self.resultEntry['bg'] = 'green'
    
    def printResult(self, resultText):
        self.resultEntry.delete(0, END)
        self.resultEntry.insert(0, resultText)
        self.resultEntry['bg'] = 'red'
        
    def saveFilenameText(self, filename):
        self.filenameText.configure(state='normal')
        self.filenameText.delete(0, END)
        self.filenameText.insert(0, filename)
        self.filenameText.configure(state='disabled')
                
    def addControls(self):
        self.frame = Tkinter.Frame(self.root)
        self.frame.pack()
        
        
        self.addFileChooser()
        
        self.addTierNameEntry()
        self.addDescriptionEntry()
        self.addResultLabel()
        self.addConversionButton()
        
        
   
        
    def addFileChooser(self):
        self.loadButton = Tkinter.Button(self.frame, text = u"Выберите файл .eaf", command=self.chooseFile,
                                        )
        self.loadButton.grid(row=0, column=0)
        
        self.filenameText = Tkinter.Entry(self.frame, state='disabled', width = self.FILENAME_WIDTH)
        self.filenameText.grid(row=0, column=1)
        
    def addConversionButton(self):
        self.conversionButton = Tkinter.Button(self.frame, text = u"Конвертировать", command=self.convertFile,
                                        )
        self.conversionButton.grid(row=0, column=2)
        
    def addTierNameEntry(self):
        originalTierLabel = Tkinter.Label(self.frame, text = u"Введите имя слоя для языка (например, ket)")
        originalTierLabel.grid(row=1, column=0)
        
 
        self.originalTierEntry = Tkinter.Entry(self.frame)
        self.originalTierEntry.grid(row=1, column=1)
        
    def addDescriptionEntry(self):
        descriptionLabel = Tkinter.Label(self.frame, text = u"Введите описание текста в свободной форме")
        descriptionLabel.grid(row=2, column=0)
        
        self.descriptionEntry = Tkinter.Entry(self.frame, width = self.DESCRIPTION_WIDTH)
        self.descriptionEntry.grid(row=2, column=1)
        
    def addResultLabel(self):
        resultLabel = Tkinter.Label(self.frame, text = u"Результат обработки")
        resultLabel.grid(row=3, column=0)
        
        self.resultEntry = Tkinter.Entry(self.frame, width = self.RESULT_WIDTH)
        self.resultEntry.grid(row=3, column=1)
        
        

PmlUtils()