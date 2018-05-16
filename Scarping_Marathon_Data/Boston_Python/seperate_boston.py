#!/usr/bin/env python3
#_*_utf-8_*_

'''This script separates out the all the different finishing times of the Boston Marathon for every year there is data present. The resulting file is a text file called ParsedBoston{}.txt where the {} represents the specific year the marathon was run. '''

import os
import numpy as np
import re
import glob

Boston_file = open('BostonMarathonAllParsed.txt', 'r')

uni_years = set()

new_file = False

for r in Boston_file:
    row = r.split(',')
    year = row[0].strip('\x0c')
    row[0] = year
    try:
        new_year = int(year)
        if new_year not in uni_years:
            new_file = True
        else:
            new_file = False
    except ValueError:
        new_file = False

    if new_file:
        print('#'*60)
        print('ParsedBoston{}.txt'.format(new_year))
        print('#'*60)
        out_year = open('ParsedBoston{}.txt'.format(new_year), 'w')
        old_year = new_year
        uni_years.add(new_year)
        out_year.write(','.join(row))
        print(row)
    else:
        try:
            out_year.write(','.join(row))
            print(row)
        except NameError:
            pass

