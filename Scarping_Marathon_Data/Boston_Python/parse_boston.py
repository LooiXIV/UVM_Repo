#!/usr/bin/env python3
#_*_utf-8_*_

'''This script pre-parses the historical Boston Marathon data taken from the BAA website. This data comes as a pdf from the website. I then used the unix program pdftotext to convert to a text file. This scripte parses out the resulting text file and prints out a seperate text file with the data parsed into a file with X rows (number of individual entries in the file) and 6 columns. The end result is a single file with all Bostom Marathon results from 1897 to 2015 called ParsedBostonMarathonAll.txt. Lastly, some years the Marathon results are incorrect. These years include 2013 and 2015. '''

import os
import numpy as np
import re
import glob
import PyPDF2 as pdf

Boston_file = open('BostonMarathon.txt', 'rb')

c = 0
out_boston = open('ParsedBostonAll.txt', 'w')

# first read in the data create a list of lists and remove the 
# '\n' character
Boston_file = open('BostonMarathon.txt', 'rb')

pages = []
bos1_out = open('Boston_marathon_parsing1.txt', 'w')
for entry in Boston_file:
    e2 = entry.decode('latin-1')
    
    if e2[0] != '\n':
        pages.append(e2)
        bos1_out.write(e2)

bos1_out.close()


# Read in the list of lists that will be further parsed. 
page = []
pn = 0
pages = []
bos1_in = open('Boston_marathon_parsing1.txt', 'r')
for b in bos1_in:
    pages.append(b)


bos2_out = open('ParsedBostonMarathonAll.txt', 'w')
for p in pages:
    p2 = p.split(' ')
    p4 = [e.strip('\n') for e in p2]
    #p4 = [e.strip('\x0c') for e in p3]


    if '\x0c' in p[0]:

        if len(page) < 6:
            len_col = len(page[0])
            NA_val = (60*' UNKNOWN').split(' ')
            try:
                zipped_list = list(zip(page[0], NA_val, page[1], page[2], page[3], page[4]))
                #print(zipped_list)
            except IndexError:
                print('index error')
                print(page)
                break
        else:
            zipped_list = list(zip(page[0], page[1], page[2], page[3], page[4], page[5]))
        for r in zipped_list:
            print(r)
            bos2_out.write(','.join(r)+'\n')
        page = []
        page.append(p4)
        pn += 1
    else:
        page.append(p4)

bos2_out.close()


#####################################################################################################################################################################################
# There were a lot of formating problems with this data set and some entries/rows/columns had to be manually edited. The code below are all the instances I found where I had to hard code reformatting. 


names = "John Calisi Michael Sousa Paul Ryan Donnie Weeden Mark Palmer Chris Fehrnstrom Robert Cunningham Jeffrey Wall Daniel Mahoney Jay Civilinski Christopher Landry Gilmar Pazello Stephen Tillinghast Terrence Cunningham David Ferguson Dennis Njagi Shawn Stone Ken Gartner Frank Dicataldo John Brent Tom Amend Kevin Light Peter O\'Sullivan Mark Anderson Steve Pennie Philip Cargill Larry Skinner Christopher Krueger Don Greenough Thomas Cooper David Mcgillivray Bertil Lind Darryl Smith Claudio Sierra Louis Kaplan Geoff Grammel John Holmes Peter Shaughnessy Steven Hershberg Barrett Rollins James Larner FransonKwockSunTom"

fn = []; ln = []
name_list = np.array(names.split(' '))
len(('1 2 '*int((len(name_list))/2)).split(' '))

fn_bool = np.array(('1 2 '*int((len(name_list))/2)).split(' ')) == '1'

ln_bool = np.array(('1 2 '*int((len(name_list))/2)).split(' ')) != '1'

fn = ' '.join(name_list[fn_bool])
ln = ' '.join(name_list[ln_bool])


names_place = 'Jacob Ostergaard Denmark AlanB Barrett NewHampshire Joey Randall NewYork MatthewJ. Enna California Dylan Sutton California Richard Herbst Colorado VincentA Marino Ohio JustinN. Rosas Oregon Justin Bird Utah Pablo FernandezDeBobadillaFerrer Mexico Ed Kenny Michigan Dan McCray Ohio TimJ Fisler Pennsylvania BenjaminW. Petsch Tennessee Christian Blanc France DavidA. Sandham GreatBritain JohnP Anders Kansas ErnestoA. Burden NewHampshire BrianJ. McCourt NewJersey Edmond Tam NewYork TroyA.Sr. Jones Ohio Thomas Szumila Texas StevenD. Peterson Virginia Chris Marshall DistrictofColumbia JamesN. Chadwell Georgia JohnR.Jr. Harris Georgia Martin Quinn GreatBritain Alex Nagle Illinois SteveR. Seide Massachusetts Olov Berg Pennsylvania Adam Dunn Washington Robert(bobby)WJr. Spath Delaware Howard Shelanski DistrictofColumbia GiovanniSr. Busin Italy RonaldT. Stephens Virginia RobertC. Schroeder Wisconsin AndrewW. Chong Hawaii Matthew Searfus Washington FThomas Fisher California Jay Steele Michigan BrentJ Tisch Ohio KennethW. Chitwood Texas'

fn = []; ln = []; pl = []
name_list = np.array(names_place.split(' '))

vecs = ('1 2 3 '*int((len(name_list))/3)).split(' ')
fn_bool = np.array(vecs)[0:-1] == '1'

ln_bool = np.array(vecs)[0:-1] == '2'

pl_bool = np.array(vecs)[0:-1] == '3'

fn = ' '.join(name_list[fn_bool])
ln = ' '.join(name_list[ln_bool])
pl = ' '.join(name_list[pl_bool])

