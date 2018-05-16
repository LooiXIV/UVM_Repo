#!/usr/bin/env python3

'''This script downloads Marathon times and results from the London Marathon website (indirectly from the website that does timing for the London Marathon). Each web page is stored as HTML data and stored a seperate text file. Additionally, each web page is further categorized as elite (ELIT) results or the masses (MAS). The only years available for down load are 2009 through to the present.'''

import threading
import urllib3 as ul
import numpy as np
import time
import os

min_page = 1
max_page = 50
page_ran = np.arange(min_page, max_page)

mean_int = 10

cat = ['ELIT', 'MAS']

years = np.arange(2014, 2017)

years = [2014]

counter = 1

tot_files = 2*len(years)*max_page
for y in years:

    for c in cat:
        
        if c == 'ELIT':
            page_ran = [1, 2]
            results = 25
        else:
            page_ran = np.arange(min_page, max_page)
            results == 1000

        for d in page_ran:
            if y == 2015:
                url_base = 'http://results-{}.virginlondonmarathon.com/{}/index.php?page={}&event=MAS&num_results={}&pid=search&search%6Bsex%5D=%25&search_sort=place_nosex&split=time_finish_netto'.format(y, y, d, results)
                out_file_name = 'All_Cats{}Page{}LondonMarathon.txt'.format(y, d)
            elif y == 2013:
                if c == 'ELIT':
                    url_base = 'http://results-{}.virginlondonmarathon.com/{}/index.php?page={}&event={}&pid=search&search%5Bsex%5D=%25&search_sort=place_nosex&split=time_finish_netto'.format(y, y, d, c)

                else:
                    url_base = 'http://results-2013.virginlondonmarathon.com/2013/index.php?page={}&event=MAS&num_results=1000&pid=search&search%5Bsex%5D=%25&search_sort=place_nosex&split=time_finish_netto'.format(d)

                out_file_name = '{}Cat{}Page{}LondonMarathon.txt'.format(y, c, d)

            elif y == 2014:
                if c == 'ELIT':
                    url_base = 'http://results-{}.virginmoneylondonmarathon.com/{}/?page={}&event={}&pid=search&search%5Bsex%5D=%25&search%5Bnation%5D=%25&search_sort=name'.format(y,y,d,c)
                else:
                    url_base = 'http://results-{}.virginmoneylondonmarathon.com/{}/?page={}&event={}&num_results=1000&pid=search&search%5Bsex%5D=%25&search%5Bnation%5D=%25&search_sort=name'.format(y, y, d, c)

                out_file_name = '{}Cat{}Page{}LondonMarathon.txt'.format(y, c, d)


            else:
                url_base = 'http://results-{}.virginmoneylondonmarathon.com/{}/?page={}&event={}&num_results=1000&pid=search&search%5Bsex%5D=%25&search%5Bnation%5D=%25&search_sort=name'.format(y, y, d, c)
                out_file_name = '{}Cat{}Page{}LondonMarathon.txt'.format(y, c, d)
        


            x = np.random.rand()
            wait = mean_int*x
            print(url_base)
            print('#'*60)
            print(out_file_name)
            print('pausing...', wait, 'seconds')
            print('on page ', counter, ' of ', tot_files)
            print('#'*60)

            time.sleep(wait)
    
            url = ul.PoolManager()

            page = url.request('GET', url_base)

            marathon_data = open(out_file_name, 'w')

            print(out_file_name)

            marathon_data.write(str(page.data))

            counter += 1

