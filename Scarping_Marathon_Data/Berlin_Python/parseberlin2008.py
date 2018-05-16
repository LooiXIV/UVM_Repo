#!/usr/bin/env python3
#_*_uft-8_*_
import os
from bs4 import BeautifulSoup
import numpy as np
import re
import glob

years = [2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016]
years = [2008]
berlin_files = glob.glob('*.txt')



for y in years:

    berlin_file = open('Parsed{}BerlinMarathon.txt'.format(y), 'r')
    
    place = []
    name_place = []
    age_group = []
    gun_time = []
    net_time = []
    gender_place = []
    bib_num = []
    
    for d in berlin_file:
        
        row = d.split(',')
        #print(row)

        try:
            place.append(int(row[0]))
        except ValueError:
            place.append(99999)

        bib_num.append(row[2])
        gender_place.append(row[1])
        name_place.append(' '.join(row[3:-5]))
        age_group.append(row[-5])
        net_time.append(row[-2])
    
    try:
        sorted_data = sorted(zip(place, gender_place, bib_num, 
            age_group, name_place, net_time))
    except TypeError:
        sorted_data = sorted(zip(place, gender_place, bib_num, 
            age_group, name_place, net_time))
    out_data = open('ParsedBerlinData{}.txt'.format(y), 'w')

    for r in sorted_data:
        row = [str(e) if e != 99999 else 'NA' for e in r ]
        print(row)
        out_data.write(','.join(row)+'\n')

    out_data.close()



