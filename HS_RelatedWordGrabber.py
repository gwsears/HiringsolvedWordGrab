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
        waiter(maxDelay)
    except Exception:
        print('Unable to get ' + keyword + '!')
        waiter(maxDelay/2)
        return
    return {keyword:relatedWords}

def loadKeywordList(file):
    # Takes local file path as input
    # Returns a list of keywords
    openfile = open(file)
    openList = openfile.readlines()
    openfile.close()
    returnList = []
    for item in openList:
        returnList = returnList + [item.strip()]
    return returnList

def waiter(seconds):
    # Add a delay between pulls in seconds
    # If seconds is given as 0 or less then it adds no delay
    if seconds >> 0:
        waitT = randint(1,seconds)
        print('Waiting ' + str(waitT) + ' seconds...')
        sleep(waitT)

# Start up dictionary to store our keywords and words related to them.
keywordDict = {}
# Puts the keywords and related words into keywordDict.
keywordList = loadKeywordList(keywordInputFile)
for item in keywordList:
    keywordDict.update(getHiringSolvedRelatedWords(item,numSynonyms,filterHiringSolved))

print("Here's your dictionary!")
print(keywordDict)
print(keywordDict[keywordList[0]])

#def ouputCSVversion1(HSDictionary):
#    csvfile = open(keywordOutputFile, 'w+', encoding='utf-8', newline='')
#    outputWriter = csv.writer(csvfile, dialect='excel')
#    toprow = ['keyword']
#    for x in range(1, numSynonyms):
#        toprow = toprow + ['related word', 'score']
#    outputWriter.writerow(toprow)
#    for keyword in HSDictionary:
