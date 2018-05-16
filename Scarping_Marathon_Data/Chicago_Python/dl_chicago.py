#!/usr/bin/env python3

'''This script downloads the HTML code from the company that does the timing for the Chicago Marathon. The only available years that this can be done for are from 1992 to the present. All raw HTML code is exported by web page to a text file called Page{}ChicagoMarathon.txt where the {} references the web page number for the results for a particular year of the Chicago Marathon.'''

import urllib3 as ul
import numpy as np
import time
import os

min_page = 1
max_page = 671
page_ran = np.arange(min_page, max_page)

mean_int = 10
y = 2016

# loops through all the pages that have my marathon data
for d in page_ran:
    
    # pause for some random number of seconds
    # to avoid being black listed
    x = np.random.rand()
    wait = mean_int*x
    print('pausing...', wait, 'seconds')
    print('on page ', d, ' of ', max_page)
    time.sleep(wait)
    
    # format the url we want to get data from
    url_base = 'http://chicago-history.r.mikatiming.de/{}/?page={}&event=ALL_HISTORY&lang=EN_CAP&num_results=1000&pid=search&search%5Bnation%5D=%25&search_sort=name'.format(y, d)

    # create a url object
    url = ul.PoolManager()

    # use the url object to get the source html code from the web site
    page = url.request('GET', url_base)

    # open a file to store the future data
    marathon_data = open('Page{}ChicagoMarathon.txt'.format(d), 'w')

    # write the source url code to a data file
    marathon_data.write(str(page.data))



