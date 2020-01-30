import os
import sys
import re
import pickle
import pandas as pd
from tqdm import tqdm

#------------------------------------------------------------------------
def parseText(lines):

    #Clean
    fulltext = ' '.join(lines)
    fulltext = fulltext.lower()
    fulltext = fulltext.replace("'","")
    fulltext = re.sub(r'[^a-zA-Z0-9_.]', ' ', fulltext)
    fulltext = fulltext.replace("     "," ")
    fulltext = fulltext.replace("    "," ")
    fulltext = fulltext.replace("   "," ")
    fulltext = fulltext.replace("  "," ")
    fulltext = fulltext.replace(","," ,")
    fulltext = fulltext.replace("."," .")

    #To List
    elements = fulltext.split(' ')
    wordlist = []
    for element in elements:
        if (len(element) > 1):
            wordlist.append(element)
        else:
            if element == 'a':
                wordlist.append(element)
            if element == '.':
                wordlist.append(element)
    
    #Return
    return wordlist

#------------------------------------------------------------------------
def processTextfile(filename,rawdir):

    #Init
    author = ''
    title = ''

    #Read file
    lines = []
    startindex = 0
    endindex = 0
    totallines = 0
    with open(rawdir + '/' + filename,'r',encoding='utf-8', errors='ignore' ) as f:
        for l,line in enumerate(f):
            totallines = totallines + 1
            if 'START OF THIS PROJECT GUTENBERG' in line:
                startindex = l
            if 'END OF THIS PROJECT GUTENBERG EBOOK' in line:
                endindex = l
            if 'START OF THE PROJECT GUTENBERG' in line:
                startindex = l
            if 'END OF THE PROJECT GUTENBERG EBOOK' in line:
                endindex = l
            lines.append(line.rstrip())

    if (totallines > 0 and startindex > 0 and endindex > startindex):
        #Get Author and Title
        for i in range(startindex):
            line = lines[i]
            if 'Author:' in line:
                elements = line.rstrip().split(': ')
                if (len(elements) > 1):
                    author = elements[1].lower()
                else:
                    author = 'unknown'
            if 'Title:' in line:
                elements = line.rstrip().split(': ')
                if (len(elements) > 1):
                    title = elements[1].lower()
                else:
                    title = 'unknown'

        #ParseText
        text = []
        text = parseText(lines[startindex+1:endindex])

        #Return
        return 1,author,title,text
    else:
        #Return
        return 0,author,title,[]
    
#------------------------------------------------------------------------
if __name__ == '__main__':
    
    #Data Directory
    cleandir = '/Volumes/3-1TB-LaCie/data/gutenberg/cleaned'
    rawdir = '/Volumes/3-1TB-LaCie/data/gutenberg/raw/'
    dbdir = '/Volumes/3-1TB-LaCie/data/gutenberg/database/'
    pickledir = '/Volumes/3-1TB-LaCie/data/gutenberg/pickle/'

    #Get all files
    txtfiles = []
    for root, dirs, files in os.walk(rawdir, topdown=False):
        for name in files:
            txtfiles.append(name)

    database = []
    D = {}
    for m,myfile in enumerate(txtfiles):
        success,author,title,text = processTextfile(myfile,rawdir)
        if (success > 0):
            database.append((myfile,author,title))
            print(m,myfile,author,title)
            if (len(author) > 0):
                fchar = author[0]
            else:
                author = 'unknown'
                fchar = 'u'
            if fchar in D:
                mydict = D[fchar]
                mydict[myfile] = text
                D[fchar] = mydict
            else:
                mydict = {}
                mydict[myfile] = text
                D[fchar] = mydict

    #To Pandas
    database = pd.DataFrame(database)
    database.columns = ['file','author','title']
    database.to_csv(dbdir + 'database.csv',index=False)

    #Store as pickle
    for i in tqdm(range(97,123)):
        char = chr(i)
        if char in D:
            mydict = D[char]            
            pickle.dump(mydict, open(pickledir + char + ".p", "wb"))