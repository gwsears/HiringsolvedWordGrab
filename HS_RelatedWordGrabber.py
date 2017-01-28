# This program is meant to take a file with a list of words and get a list of words from the Hiring Solved keyword
# synonym tool.  Input will be a text file with one word per line.  Output is going to be a .csv file with the keyword
# in the first column and the related words and their scores in alternating columns after that.

import requests
import csv
from random import randint
from time import sleep

# Set the parameters here:
keywordInputFile = 'keywords.txt' # Path and name of the input file.
keywordOutputFile = 'relatedwords.csv' # Path and name for output file.
numSynonyms = 2 # How many synonyms the program should fetch.
maxDelay = 15 # How many seconds at most should the program wait to fetch the next keyword. 0 turns off delay
filterHiringSolved = True # Set if HS's filter is used.  I don't know what the filter actually does.

def getHiringSolvedRelatedWords(keyword,size,filter):
    # Takes Keyword as string, size as integer, and filter as Boolean
    # Returns a dictionary with {keyword:json of related words}
    HS_baseURL = 'https://hiringsolved.com/api/v2/related?q='
    targetURL = HS_baseURL + keyword + '&size=' + str(size) + '&filter='  + str(filter).lower()
    print('Looking up ' + keyword + '...')
    try:
        r = requests.get(targetURL, auth=('user','pass'))
        relatedWords = r.json()
        print(relatedWords)
    except Exception:
        print('Unable to get ' + keyword + '!')
        return
    return {keyword:relatedWords}

def loadKeywordList(file):
    # Takes local file path as input
    openfile = open(file)
    openList = openfile.readlines()
    openfile.close()
    returnList = []
    for item in openList:
        returnList = returnList + [item.strip()]
    return returnList

keywordDict = {}
for item in loadKeywordList(keywordInputFile):
    keywordDict.update(getHiringSolvedRelatedWords(item,numSynonyms,filterHiringSolved))
print(keywordDict)