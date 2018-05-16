#!/usr/bin/env python3


'''This script takes the raw HTML data scraped from the Chicago Marathon timing website and parses the data into a single text file. This resulting text file has 12 columns and X rows where X is the total number of athletes in the data set.'''

import os
from bs4 import BeautifulSoup
import numpy as np
import re
import glob

os.getcwd()

count = 1

# open a file to write parsed data to
mara_chicago = open('ParsedChicagoMarathon.txt', 'w')

# find all the pages I want to parse data from
all_pages = glob.glob('Page*')
line = []

# loop through all the available pages in the directory
# and scrape all the necessary data from it.
for p in all_pages:

    # open a file with a specific page of marathon
    # time data.
    marathon_page = open(p, 'r')

    # Create a soup object from the source text data 
    # (the html code we are trying to parse)
    soup = BeautifulSoup(marathon_page, 'html.parser')
    
    # find all the <td/> <td> entries 
    # this is where the marathon times/ results are
    table = soup.find_all('td')

    # clean up the data in the <td> areas
    for e in table:
        ele = re.sub(r'\<.*?\>', '', str(e))
        ele = re.sub('» ', '', ele)
        line.append(ele)
    
        if count == 12:
            count = 1
            out_line = ','.join(line)
            mara_lond_out.write(out_line+'\n')
            line = []    
        else:
            count += 1

mara_chicago.close()
