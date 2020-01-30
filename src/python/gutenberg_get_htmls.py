import os
import sys

#------------------------------------------------------------------------
if __name__ == '__main__':

    #Data Directory
    datadir = '/Volumes/3-1TB-LaCie/data/gutenberg/html'

    #Download all listing html files
    for i in range(97,123):
        char = chr(i)
        cmd = 'wget -O ' + datadir + '/' + char + '.html ' + 'https://www.gutenberg.org/browse/authors/' + char
        os.system(cmd)
