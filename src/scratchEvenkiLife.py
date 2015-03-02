# coding=utf-8
__author__ = 'gisly'

import time

import html_utils
import language_utils
import file_utils

import os
import re
import codecs


URL = 'http://www.evenkya.ru'
ENCODING = 'cp1251'
PAUSE_SEC = 10
MAX_PAGE_NUM = 100

URL_EV_LIFE = '/infoeg/life/'

RUSSIAN_CODE = 'ru'

FOLDER_TO_SAVE = '../resources'


DATE_PATTERN = ur'№\s*(?P<number>\d+(\/\d+)?(-\d+\s*)?(\s*\(\d+\s*?\)\s*)?(\s*\(\d+-\d+\s*?\)\s*)?)(\s+от)?\s*(?P<dateNum>\d+)\s*(?P<month>.+?)\s+(?P<year>\d\d\d\d)'
DATE_PATTERN_NO_NUM = ur'(?P<dateNum>\d+)\s*(?P<month>.+)\s+(?P<year>\d\d\d\d)'

DATE_PATTERN_NO_YEAR = ur'№\s*(?P<number>\d+(\/\d+)?(-\d+)?(\s*\(\d+-d+\s*?\)\s*)?)\s+от\s*(?P<dateNum>\d+)\s*(?P<month>.+)'

DATE_PATTERN_DDMMYYYY = ur'№\s*(?P<number>\d+(\/\d+)?(-\d+)?(\s*\(\d+\s*?\)\s*)?(\s*\(\d+-d+\s*?\)\s*)?)"\
(\s+от)?(\s+от)?\s*(?P<dateNum>\d+)\.(?P<month>\d\d)\.(?P<year>\d\d\d\d)'

MONTHS = {u'января':'01',
          u'февраля':'02',
          u'марта':'03',
          u'апреля':'04',
          u'мая':'05',
          u'июня':'06',
          u'июля':'07',
          u'августа':'08',
          u'сентября':'09',
          u'октября':'10',
          u'ноября':'11',
          u'декабря':'12'
          }


def downloadPagesInterval(pageFrom, pageTo):
    for i in range(pageFrom, pageTo + 1):
        print 'starting to process page ' + str(i)
        downloadPage(i)
    
    
def downloadPage(pageNumber):
    params = {'page':pageNumber}
    htmlData = html_utils.getHTMLData(URL + URL_EV_LIFE, ENCODING, params)
    processPage(htmlData)
    
def processPage(htmlData):
    allHeaders = html_utils.getHTMLTags(htmlData, "h3")
    htmlDataAfter = html_utils.createString(htmlData).strip()
    
    prevYear = 'XXXX'
    for i in range(0, len(allHeaders) - 1, 1):
        curHeader = allHeaders[i]
        nextHeader = allHeaders[i + 1]
        curHeaderText = html_utils.createString(curHeader).strip()
        
        
        
        if html_utils.normalize(curHeaderText).strip() == '':
            continue
        
        nextHeaderText = html_utils.createString(nextHeader).strip()
        
        
        
        
        
        htmlDataAfterNew = htmlDataAfter.split(curHeaderText)[-1]

        
        
        htmlDataParts = htmlDataAfterNew.split(nextHeaderText)
        htmlDataCur = htmlDataParts[0]
        
      
        htmlDataAfter = htmlDataParts[1]
        
        htmlDataCur_html = html_utils.getHtmlDataFromString(htmlDataCur)
        
        
        curDate, year = transformMagazineStyleDate(html_utils.normalize(curHeaderText), prevYear)
        
        prevYear = year
      
        allLinks = html_utils.getHTMLTags(htmlDataCur_html, "a")
        for link in allLinks:
            href = link.attrib['href']
            if isTextLink(href):
                linkData = processLink(href)
                if linkData:
                    file_utils.saveDataToFile(linkData, FOLDER_TO_SAVE, curDate + createFileName(href))
                    
            
def isTextLink(href):
    return href.startswith(URL_EV_LIFE) and len(href) > len(URL_EV_LIFE)

def processLink(href):
    if href == '/infoeg/life/.html':
        return None
    
    time.sleep(PAUSE_SEC)
    
    
    WHOLE_LINK = URL + href
    htmlData = html_utils.getHTMLData(WHOLE_LINK, ENCODING, {})
    contentTag = html_utils.getFirstHTMLTagByAttribute(htmlData, 'div', 'class', 'content')
    content = html_utils.normalize(html_utils.createString(contentTag)).strip()
    
    if not language_utils.isRussian(content):
        return content
    return None

def createFileName(href):
    return href.replace('/', '_')


def transformMagazineStyleDate(magazineStyleDate, prevYear):
    number, dateNum, month, year = extractFromDate(magazineStyleDate)
    number = number.replace('/', '[').replace('(', '[').replace(')', ']').replace(' ', '_')
    if year is None:
        year = prevYear
    return '_'.join([year, month, dateNum, number]), year

def extractFromDate(magazineStyleDate):
    magazineStyleDate = magazineStyleDate.replace('20009', '2009')
    magazineStyleDate = magazineStyleDate.replace(u'от  ноября', 'от 00 ноября')
    matchRes = re.search(DATE_PATTERN, magazineStyleDate)
    if matchRes:
        number = matchRes.group('number')
        dateNum = matchRes.group('dateNum')
        month = getMonth(matchRes.group('month'))
        year = matchRes.group('year')
        return number, dateNum, month, year
    else:
        matchRes = re.search(DATE_PATTERN_NO_NUM, magazineStyleDate)
        if matchRes:
            dateNum = matchRes.group('dateNum')
            month = getMonth(matchRes.group('month'))
            year = matchRes.group('year')
            return 'undefined', dateNum, month, year
        else:
            matchRes = re.search(DATE_PATTERN_NO_YEAR, magazineStyleDate)
            if matchRes:
                number = matchRes.group('number')
                dateNum = matchRes.group('dateNum')
                month = getMonth(matchRes.group('month').strip())
                return number, dateNum, month, None
            else:
                matchRes = re.search(DATE_PATTERN_DDMMYYYY, magazineStyleDate)
                if matchRes:
                    number = matchRes.group('number')
                    dateNum = matchRes.group('dateNum')
                    month = matchRes.group('month')
                    year = matchRes.group('year')
                    return number, dateNum, month, year
    raise Exception('wrong date!' + magazineStyleDate)

def getMonth(monthName):
    print monthName
    return MONTHS[monthName]


def countStats(folder, year = None):
    totalCount = 0
    for filename in os.listdir(folder):
        if not filename.endswith('.txt'):
            continue
        if year and not filename.startswith(str(year)):
            continue
        with codecs.open(os.path.join(folder, filename), 'r', 'utf-8') as fin:
            for line in fin:
                totalCount += len(re.findall("\s", line))
    return  totalCount 
        

print str(countStats('../resources'))  
totalSum = 0
for year in range(2002, 2011):
    curSum = countStats('../resources', year)
    print  str(curSum)  
    totalSum += curSum

print str(totalSum)  

#downloadPagesInterval(43, 50)
#print transformMagazineStyleDate(u'№ 50 (8356 ) от 12 сентября 2003 г.', '2002')

#print processLink('/infoeg/life/rezolyuciyatyn.html')