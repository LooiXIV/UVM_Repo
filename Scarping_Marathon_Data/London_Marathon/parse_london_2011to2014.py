#!/usr/bin/env python3

'''This script parses out the raw London Marathon HTML data for the years of 2011 to 2014. All data are stored in a single text file called Parsed{}LondonMarathon.txt.'''

import os
from bs4 import BeautifulSoup
import numpy as np
import re
import glob

os.getcwd()

year_parse = str(2014)

count = 1
line = []

mara_lond_out = open('Parsed{}LondonMarathon.txt'.format(year_parse), 'w')


all_pages = glob.glob('All_Cats{}*'.format(year_parse))

for p in all_pages:
    mara_lond = open(p, 'r')
    soup = BeautifulSoup(mara_lond, 'html.parser')
    table = soup.find_all('td')

    header = soup.find_all('th')
    col_len = len(header)
    header_line = []
    for h in header:
        header_line.append(re.sub(r'\<.*?\>', '', str(h)))
    
    for e in table:
        
        ele = re.sub(r'\<.*?\>', '', str(e))
        ele = re.sub('» ', '', ele)
        ele = re.sub('no results found.', '', ele)
        ele = ele.strip('\\n')
        
        line.append(ele)
        if ele == 'No results found.':
            continue
             
        if count == col_len:
            line
            count = 1
            out_line = ','.join(line)
            mara_lond_out.write(out_line+'\n')
            #print(header_line)
            print(line)
            line = []    
        else:
            count += 1

mara_lond_out.close()
