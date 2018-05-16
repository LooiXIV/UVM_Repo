#!/usr/bin/env python3

'''This Downloads Marathon time data from the Berlin Marathon starting in 2007 going to 2015. This downloads raw HTML data from the timing company that times the Berlin Marathon. For data before 2007 years consult the script that downloads data from MarathonGuide.com'''

import urllib3 as ul
import numpy as np
import time
import os

min_page = 1
max_page = 439
year = 2007
page_ran = np.arange(min_page, max_page+1)

mean_int = 5

# for all page numbers
for d in page_ran:

    x = np.random.rand()
    wait = mean_int*x
    print('pausing...', wait, 'seconds')
    print('on page ', d, ' of ', max_page)
    time.sleep(wait)
    
    url_base = 'http://results.scc-events.com/{}/?page={}&event=MAL&num_results=100&pid=search&search%5Bnation%5D=%25&search_sort=name'.format(year ,d)

    url = ul.PoolManager()

    page = url.request('GET', url_base)

    marathon_data = open('Year{}Page{}Berlin.txt'.format(year, d), 'w')

    marathon_data.write(str(page.data))

    marathon_data.close()

