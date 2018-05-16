#!/usr/bin/env python3

'''This script parses london marathon data only for the year of 2009. This is because this year of logged results was different from all other years and thus need to be parsed seperately. Additionally, the end result was stored in a text file called Parsed{}LondonMarathon.txt where the {} denote the year of the marathon.'''

import os
from bs4 import BeautifulSoup
import numpy as np
import re
import glob

os.getcwd()
#os.chdir('chicago_marathon')

year_parse = 2009

mara_lond_out = open('Parsed{}LondonMarathon.txt'.format(year_parse), 'w')

all_pages = glob.glob('All_Cats{}*'.format(year_parse))

for p in all_pages:

    file_mara = open(p, 'r')
    
    print('#'*60)
    print(p)
    print('#'*60)

    soup = BeautifulSoup(file_mara, 'html.parser')

    table = soup.find_all('td')

    count = 0
    row = []
    row_num = 1
    for t in table:
        ele = re.sub(r'\<.*?\>', '', str(t))

        if count == 7:
            print(row_num, row)
            mara_lond_out.write(','.join(row)+'\n')
            count = 0
            row = []
            row_num += 1
        else:
            row.append(ele)
        count += 1
            
