#!/usr/bin/env python3
#_*_uft-8_*_

'''This orders Berlin Marathon data that has been pre-parsed by the parse_berlin.py script. This breaks down the data and reformats it into a 8 column X row table (where X is the number of rows for a particular year of data). Missing data will be replaced with 99999 values. Lastly, the data is sorted by finishing place of an individual.'''

import os
from bs4 import BeautifulSoup
import numpy as np
import re
import glob


berlin_files = glob.glob('*.txt')

years = [2016]

for y in years:

    berlin_file = open('Parsed{}BerlinMarathon.txt'.format(y), 'r')
    
    place = []
    name_place = []
    age_group = []
    gun_time = []
    net_time = []
    gender_place = []
    bib_num = []
    club = []

    for d in berlin_file:
        
        row = d.split(',')
        print(row)

        try:
            place.append(int(row[0]))
        except ValueError:
            place.append(99999)

        bib_num.append(row[1])
        name_place.append(' '.join(row[2:4]))
        age_group.append(row[4])
        club.append(row[6])
        gender_place.append(' ')
        net_time.append(row[-2])
    
    try:
        sorted_data = sorted(zip(place, gender_place, bib_num, 
            age_group, name_place, net_time))
    except TypeError:
        sorted_data = sorted(zip(place, gender_place, bib_num, 
            age_group, name_place, net_time))    
        
    out_data = open('BerlinData{}.txt'.format(y), 'w')

    for r in sorted_data:
        row = [str(e) if e != 99999 else 'NA' for e in r ]
        print(row)
        out_data.write(','.join(row)+'\n')

    out_data.close()

