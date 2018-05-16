#!/usr/bin/env python
# comms.py
# Alexander Looi
# Last Modified: April 3rd, 2017

"""Block model Running
This script uses the nets, and comms scripts/classes to build a block model
and calculate a variety of modularity values for models of varying size, p_in,
and p_btwn values. Values are stored in three numpy arrays. Each array corresponds
to a different block model node quantity. The rows corresponde to p_in values
and the colmuns correspond to p_btwn values."""

#C.configuration_model()
import time
from comms import comms_graph
from comms import Erdos_Renyi
from comms import BlockModel
import numpy as np
# loop through varying number of nodes per ERG with three levels of
# p_in and p_btwn
num_nodes_rang = [5,50,75]
p_in_rang = np.arange(0.01, 1, 0.1)
p_btwn_rang = np.arange(0.01, 1, 0.1)
NN_names = ["low_nodes", "mid_nodes", "high_nodes"]

D = {}

start_time = time.time()
# rows ---> p_in
# columns ^ p_btwn
for it_num,nnr in enumerate(num_nodes_rang):
    D[NN_names[it_num]] = np.zeros(shape=[len(p_in_rang), len(p_btwn_rang)])
    for pin, pir in enumerate(p_in_rang):
        for pbn,pbr in enumerate(p_btwn_rang):
            nodes_inG = num_nodes_rang[it_num]
            groups = [nodes_inG, nodes_inG, nodes_inG, nodes_inG]
            TBM = BlockModel(list_group_sizes=groups, p_in=pir, p_btwn=pbr)
            D[NN_names[it_num]][pin,pbn] = TBM.modularity()

# calculate time to run block models
end_time = time.time()

print("--- %s seconds ---" % (end_time - start_time))
# plot as a heat map the three as a heat map.
import matplotlib.pyplot as plt
# a is the data
for p in range(0,3):
    fig, axis = plt.subplots()
    hm = axis.pcolor(D[NN_names[p]],cmap = plt.cm.Blues)
    #hm = plt.imshow(D[NN_names[p]], cmap = plt.cm.Blues, interpolation='nearest')
    plt.xlabel('p_btwn')
    plt.ylabel('p_in')
    plt.colorbar(hm)
    axis.set_xticklabels([0.0,0.2,0.4,0.6,0.8,1.0])
    axis.set_yticklabels([0.0,0.2,0.4,0.6,0.8,1.0])
    plt.show()

# used for quick testing of an individual block model
nodes_inG = 10
groups = [nodes_inG, nodes_inG, nodes_inG, nodes_inG, nodes_inG, nodes_inG]
TBM = BlockModel(list_group_sizes=groups, p_in=0.99, p_btwn=0.000001)
TBM.modularity()

##################################################################
# quickly reading in an edgelist and it's associated community.
C = readcomms("NCAA_EdgeList_Conf", delimiter=',',with_graph = True)
