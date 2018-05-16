#!/usr/bin/env python3

'''This script parses out the raw HTML data downloaded from the timing company that times the Berlin Marathon. This condenses all the downloaded HTML into the displayed rows and columns presented on the web site.'''

import os
from bs4 import BeautifulSoup
import numpy as np
import re
import glob

os.getcwd()

year_parse = str(2016)

count = 1
line = []

mara_lond_out = open('Parsed{}BerlinMarathon.txt'.format(year_parse), 'w')


all_pages = glob.glob('Year{}*'.format(year_parse))

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
        if ele == 'Keine Ergebnisse gefunden.':
            continue
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


