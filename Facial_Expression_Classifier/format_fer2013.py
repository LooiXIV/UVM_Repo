#!/bin/bin/env python
# _*_ coding: utf-8 _*_

'''This script reformats the facial emotion data set from a 2013 kaggle challenge. The original data set is a csv format. Each image is converted to a numpy array where each array is stored in a dictionary and seperated into testing and training data.'''

import os
import numpy as np
import csv
import pickle
from sklearn.preprocessing import OneHotEncoder

file_name = 'fer2013.csv'

cat = []
TrainOrTest = []
pict = []

dims = 48

# read in the data
with open(file_name, 'r') as fer_2013_file:
    next(fer_2013_file)
    for r in fer_2013_file:
    
        row_split = r.split(',')

        cat.append(row_split[0])
        
        picture = np.array(row_split[1].split(' '))
        
        pict.append(picture.astype(np.float32))

        TrainOrTest.append(row_split[2].strip('\n'))

Train_Test = [r.strip('\n') for r in TrainOrTest]

# reformat image data
ref_pict = []
for p in pict:
    ref_pict.append(p.reshape((dims, dims)))

enc = OneHotEncoder()
enc.fit(cat)

oneHot_cat = enc.transform(cat).toarray()


training_i = []
testing_i = []
training_l = []
testing_l = []

for i, l, c in zip(np.asarray(pict), cat, Train_Test):
    if c == 'Training':
        training_i.append(i)
        training_l.append(l)
    else:
        testing_i.append(i)
        testing_l.append(l)


fer_2013 = {'training':np.asarray(training_i, dtype=np.float32), 
        'testing':np.asarray(testing_i, dtype=np.float32), 
        'testing_labs':np.asarray(testing_l, dtype=np.uint8), 
        'training_labs':np.asarray(training_l, dtype=np.uint8)}

pklfer2013 = open('fer2013.pkl', 'wb')
pickle.dump(fer_2013, pklfer2013)
