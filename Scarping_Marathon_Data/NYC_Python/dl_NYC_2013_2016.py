#!/bin/bin/env python
# _*_ coding: utf-8 _*_

'''This script uses Selenium to scrape 2011 to 2016 NYC marathon results data from the MarathonGuide website. Each webpage of data was saved as a text file which would be parsed later. '''

import os
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import time
import numpy.random
import numpy as np

# Setup
mean_int = 3

y = 2014

#url_base = 'http://www.marathonguide.com/results/browse.cfm?MIDD=472131103' # 2013 NYC
url_base = 'http://www.marathonguide.com/results/browse.cfm?MIDD=472141102' # 2014 NYC
dropdown_id = 'RaceRange'
button_id = 'SubmitButton'
subid = '1 - 100'


browser = webdriver.Chrome('/Users/looi/Downloads/chromedriver')
browser.get(url_base)

# Data getting
dropdown = browser.find_element_by_name(dropdown_id)
p = 1
options = dropdown.find_elements_by_tag_name('option')
num_its = len(options)

for n in np.arange(0, num_its):
    browser = webdriver.Chrome('/Users/looi/Downloads/chromedriver')

    browser.get(url_base)
    
    dropdown = browser.find_element_by_name(dropdown_id)
    option = dropdown.find_elements_by_tag_name('option')

    option[n].click()
    button = browser.find_element_by_name(button_id)
    button.click()

    raw_html = str(browser.page_source)
    page_file_out = open('year{}page{}NYC.txt'.format(y, p), 'w')
    page_file_out.write(raw_html)
    page_file_out.close()

    print('year{}page{}NYC.txt'.format(y, p))
    x = numpy.random.rand()
    wait = mean_int*x
    time.sleep(wait)
    p += 1
    
    browser.close()
