#!/usr/bin/env python3

'''This script parses the Marathon results data scraped from the MarathonGuide website. Data are stored in text files labelled NYC_MG_parsed{}.txt where {} represents the year of a NYC marathon result. '''

import os
from bs4 import BeautifulSoup
import numpy as np
import re
import glob
import json
import pickle

os.getcwd()

years = [2014]

# a method to collect data from 
# the soup obj. It starts after
# a key word, and collection stops
# after a certain key word
def collect(dat_list, s, e):
    # intially set the collection mode to false
    col = False
    # Create a list to hold all the collected data
    list_col = []
    for d in dat_list:
        if col:
            list_col.append(d)

        if d == s:
            col = True
            continue
        elif d == e:
            col = False
            break
    return list_col[0:-2]

# a method to step through a list of marathon results
# and parse through creating a seperate row for each
# marathon result.
def get_dat(data, file_write):
    rm_bl_list = list(filter(None, data))
    row = []
    num_row = 0
    for r in rm_bl_list:
        if r == 'BQ' or r == '\xa0':
            num_row += 1
            out_row = ', '.join(row)+'\n'
            print(num_row, out_row)
            file_write.write(out_row)
            row = []
        else:
            e = re.sub(r'\\xa0.*?\\xa0', '/', r)
            row.append(e)
            

for y in years:
    # get all files from a particular year
    year_files = glob.glob('year{}*'.format(y))
    # open a file to write to to contain all the results
    # from a particular year
    NYC_MG = open('NYC_MG_parsed{}.txt'.format(y), 'w')
    # loop through all the files of a particular year.

    for f in year_files:
        # print the file name of the file being opened
        print('#'*60)
        print(f)
        print('#'*60, '\n')

        # open the file to parse
        mara_NYC = open(f, 'r')
        # create a soup object using file 'f'
        # the year and page of the NYC marathon
        soup = BeautifulSoup(mara_NYC, 'html.parser')
        # find the tables in the soup obj.
        table = soup.find_all('table')
        
        # if the table is empty go to the next file 
        if bool(table)==False:
            continue
        
        # find the index of the soup_table obj
        # that has the data.
        for t in table:
            soup2 = BeautifulSoup(str(t), 'html.parser')
            try:
                if str(soup2.find_all('b')[0]) == '<b>Marathon Results</b>':
                    #print(c, soup2.find_all('b')[0])
                    break
            except IndexError:
                pass
        
        # remove the html code
        ele = re.sub(r'\<.*?\>', '', str(t))
        # split string elements on the new line character
        # creating a single list
        ele3 = ele.split('\n')

        # the starting string that tells the "collector"
        # when to start collecting data.
        start_col = 'State, Country AG Time* BQ*'
        # the ending strings to tell the "collector" when
        # to stop collecting data.
        end_col = '*AG Time = Age-Graded Equivalent Time.  '
        
        # Collect all the raw data in a long list
        ele4 = collect(ele3, start_col, end_col)
        # prase the list into seperate rows. 
        get_dat(ele4, NYC_MG)

    # close the file being written to.
    NYC_MG.close()
