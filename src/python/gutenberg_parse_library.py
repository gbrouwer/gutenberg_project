import os
import sys
from tqdm import tqdm

#------------------------------------------------------------------------
if __name__ == '__main__':

   #Data Directory
    htmldir = '/Volumes/3-1TB-LaCie/data/gutenberg/html'
    rawdir = '/Volumes/3-1TB-LaCie/data/gutenberg/raw/'

    #Download all listing html files
    links = []
    for i in range(97,123):
        char = chr(i)
        htmlfile = htmldir + '/' + char + '.html'
        with open(htmlfile,'r') as f:
            for line in f:
                if 'class="pgdbetext"' in line:
                    if '(English)' in line:
                        index = line.find('href')
                        elements = line[index:].split('>')
                        elements = elements[0].split('"')
                        elements = elements[1].split('/')
                        links.append(elements[2])
    
    #Get Files    
    for index in tqdm(links):
        remotefile = 'http://www.gutenberg.org/cache/epub/' + index + '/pg' + index + '.txt'
        cmd = 'wget -q -O ' + rawdir + index + '.txt ' + remotefile
        os.system(cmd)