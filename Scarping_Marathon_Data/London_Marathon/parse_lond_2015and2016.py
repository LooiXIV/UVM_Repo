#!/usr/bin/env python3

'''This script parses our the masses and the elite marathon data from 2015 to 2016. This is because the formating of the data set for these particular years is different from other years. Data is parsed into a single file called Parsed{}LondonMarathon.txt where the {} denotes the year a marathon was run. '''

import os
from bs4 import BeautifulSoup
import numpy as np
import re
import glob

os.getcwd()
#os.chdir('chicago_marathon')

year_parse = str(2014)

count = 1
line = []

mara_lond_out = open('Parsed{}LondonMarathon.txt'.format(year_parse), 'w')


all_pages = glob.glob('{}*'.format(year_parse))

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
            print(out_line)
            line = []    
        else:
            count += 1

mara_lond_out.close()


