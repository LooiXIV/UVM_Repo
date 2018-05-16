#!/usr/bin/env python3
#_*_uft-8_*_
import os
import re
import numpy as np
import glob


years = np.arange(1970, 2012)

years = [1999]
# get the file

for y in years:
 
    #y = 2011
    NYC_file = open('NYC{}.txt'.format(y), 'r')

    NYC_new = open('ParsedNYC{}.txt'.format(y), 'w')
    
    for r in NYC_file:
    
        row = r.split(',')
 
        if row[0] == 'First Name':
            header = row
            NetTime = any([h for h in header if h == 'NetTime'])
            continue

        place = row[8]
        gen_pl = row[9]
        name = ' '.join([row[0], row[1]])
        CoR = row[6]

        gen_age = list(row[2])
        gender = gen_age[0]
        age = ''.join(gen_age[1:3])

        name_CoR = ' '.join([name, CoR])

        # sort out the time
        if NetTime:
            try:
                time = row[12]
                #time = row[12]
            except ValueError:
                pass
                #time = row[11]
        else:
            time = row[11]

        new_row = [place, gen_pl, gender, age, name_CoR, time]
        print(new_row)

        NYC_new.write(','.join(new_row)+'\n')

    NYC_file.close()
    NYC_new.close()
