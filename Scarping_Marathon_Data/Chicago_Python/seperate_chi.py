#!/usr/bin/env python3
#_*_uft-8_*_

'''This script takes the parsed by column chicago marathon data called ParsedChicagoMarathon.txt and seperates the data into 11 columns where each year the Chicago Marathon was run gets its own text file. The resulting files are labelled as ParsedChicago{}.txt where the {} denotes the year of Chicago Marathon results.'''

import os
from bs4 import BeautifulSoup
import numpy as np
import re

chi_file = open('ParsedChicagoMarathon.txt', 'r')


chi_data = {}

for r in chi_file:
    year = r.split(',')[0]
    try:
        chi_data[year].append(r)
    except KeyError:
        chi_data[year] = [r]

for mara_year in chi_data.keys():

    y = []
    place = []
    gender_place = []
    div_place = []
    name_place = []
    div = []
    age = []
    HALF = []
    time = []
    cat = []
    gender = []
    
    for d in chi_data[mara_year]:
        
        row = d.split(',')
 
        if row[1].lower() != 'marathon':
            continue

        try:
            place.append(int(row[2]))
            gender_place.append(int(row[3]))
            div_place.append(int(row[4]))

        except ValueError:
            place.append(9999999)
            gender_place.append(9999999)
            div_place.append(9999999)

        cat.append(row[1])
        name_place.append(''.join(row[5:-6]))
        div.append(row[-4])
        age.append(row[-3])
        HALF.append(row[-2])
        time.append(row[-1])
        gender.append('')
    
    try:
        sorted_data = sorted(zip(place, 
        gender_place, age, name_place, time))
    except TypeError:
        sorted_data = sorted(zip(place, 
        gender_place, age, name_place, time))
    out_data = open('ParsedChicago{}.txt'.format(mara_year), 'w')

    for r in sorted_data:
        row = [str(e) if e != 99999 else 'DNF' for e in r ]
        out_data.write(','.join(row))

    out_data.close()
