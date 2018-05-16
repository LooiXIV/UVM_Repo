# !usr/env/python 3
# _*_utf-8_*_

'''Compare the distribution parameters for the Boston Chicago, and NYC marathons.'''

import numpy as np
import pickle
import scipy.stats as stats
import matplotlib.pyplot as plt
import glob
# Make sure all the correct files at accessible
all_pkls = glob.glob('*.pkl')
print(all_pkls)
Mara_params = {'Boston': {}, 'Chicago': {}, 'NYC': {}}

# load pickled data into a dictionary
for f in Mara_params.keys():
    opened_file = open(f+'MVSK.pkl', 'rb')
    in_pkl = pickle.load(opened_file)
    Mara_params[f] = in_pkl

ylabs = ['mean', 'variance', 'skew']

# make a box and whisker plot/ violin plots
# compare mean, skew and variance of the three marathons

fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(18,6))
c=0
fig_labs = ['A', 'B', 'C']
for p in ylabs:
    Bost_plt = [e.tolist() for e in Mara_params['Boston'][p]]
    NYC_plt = [e.tolist() for e in Mara_params['NYC'][p]]
    Chic_plt = [e.tolist() for e in Mara_params['Chicago'][p]]
    
    
    print(p, 'Bost_plt, NYC_plt', stats.ttest_ind(Bost_plt, NYC_plt)[-1])
    print(p, 'Bost_plt, Chic_plt', stats.ttest_ind(Bost_plt, Chic_plt)[-1])
    print(p, 'Chic_plt, NYC_plt', stats.ttest_ind(Chic_plt, NYC_plt)[-1])

    
    

    axes[c,].boxplot([Bost_plt, NYC_plt, Chic_plt], 
            showmeans=True, widths=1)
    axes[c,].set_xticklabels(['Boston', 'New York', 'Chicago'], fontsize=17)
    axes[c,].set_xlim(0, 4)
    axes[c,].set_ylabel(p, fontsize=20)
    axes[c,].text(3.5, np.max(Bost_plt+NYC_plt+Chic_plt), fig_labs[c], fontsize=20)

    c+=1
plt.tight_layout()
plt.show()
plt.close()




