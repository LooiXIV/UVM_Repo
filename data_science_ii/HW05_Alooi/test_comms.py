#!/usr/bin/env python
# _*_UTF-8_*_
# test_nets.py
# <Alexander Looi>
# Last Modified: <March 16, 2017>

import nets
import os
from comms import comms_graph
from comms import 
from nose.tools import assert_equal, with_setup


#import py.test
# can import test modules here, but please no other third-party libraries

def test_nets_docstring():
    assert comms.__doc__ == "\nNETS CLASS DOCSTRING\n"

# FILL IN FROM HERE
# NODE FILL TESTS #
# testing a small network #
############################################################################

def Comm_setup():
    C = readcomms("NCAA_EdgeList_Conf", delimiter=',',with_graph = True)

def Comm_teardown():
    del C

############################################################################
@with_setup(setup = Comm_setup(), teardown = Comm_teardown)
# give a list of two communities to add for one node
def MultiCommAdd_test():
    C.add_nodes_to_comm("Navy", ["Con 1", "Con 2"])
    obs = C.CBN['Navy']
    exp = ["Con 1"]
    assert_equal(exp, obs)
# attempt to add two nodes to a single community
@with_setup(setup = Comm_setup(), teardown = Comm_teardown)
def MultiNodeAdd_test():
    C.add_nodes_to_comm(["Navy", "Army"], "Con 1")
    obs = C.CBN['Navy']
    exp = ["Con 1"]
    assert_equal(exp, obs)

# add a node that does not exist in a graph to a community
@with_setup(setup = Comm_setup(), teardown = Comm_teardown)
def AddNonExistNode_test():
    obs = C.add_nodes_to_comm("Marines", "Southeastern Conference")
    exp = False
    assert_equal(exp, obs)

# remove a node that doesn't exist from a community that does exist
@with_setup(setup = Comm_setup(), teardown = Comm_teardown)
def RemoveNonExistNode_test():
    obs = C.remove_node_from_comm('NoNode', 'Independent')
    exp = False
    assert_equal(exp, obs)

# remove an existing node from a community that doesn't exist
@with_setup(setup = Comm_setup(), teardown = Comm_teardown)
def RemoveNonComm_test():
    obs = C.remove_node_from_comm('Navy', 'NoComm')
    exp = False
    assert_equal(exp, obs)

# Calculate the modularity of an empty graph
def ModEmptyGraph_test():
    C = {}
    obs = C.modularity()
    exp = None
    assert_equal(exp, obs)

# give the Erdos Renyi model a single node with probability p=0.1 of a link.
def ERMSingleNode_test():
    
    C = ErdosRenyi(size=1, p=0.1)
    obs = C.G
    exp = {'NO':[]} 
    assert_equal(exp, obs)

# give the Erdos Renyi model no nodes
def ERMNoNodes_test():
    obs = ErdosRenyi(size=0, p=0.1)
    exp = None
    assert_equal(exp, obs)

# give the Erdos Renyi model no probability
def ERMNoProb_test():
    C = ErdosRenyi(size=10, p=0)
    obs = C.edges()
    exp = []
    assert_equal(exp, obs)

# Make one of the ER graphs in the Block model have 0 nodes
def BMERGIsNone_test():
    group_sizes = [0, 50, 25, 6]
    BM = BlockModel(list_group_sizes=group_sizes, p_in=0.7, p_btwn=0.1)
    obs = BM
    exp = False
    assert_equal(exp, obs)

# give 0 prob. betweeness between ER graphs
def BMERGpProbisZero_test():
    group_sizes = [5,5,5]
    BM = BlockModel(list_group_sizes=group_sizes, p_in=0.7, p_btwn=0)
    obs = len(list(BM.NIC.keys()))
    exp = 3
    assert_equal(exp, obs)

# take the modularity of an empty graph
def ModofEmptyGraph_test():
    C = comms_graph()
    obs = C.modularity
    exp = False
    assert_equal(exp, obs)

# take the modularity of a graph with no communities.
@with_setup(setup = Comm_setup(), teardown = Comm_teardown)
def ModNoComms_test():
    C.NIC = {}
    C.CBN = {}
    obs = C.modularity()
    exp = None
    assert_equal(exp, obs)

# return communities() of an empty graph
@with_setup(setup = Comm_setup(), teardown = Comm_teardown)
def CommOfEmptyGraph_test():
    C = comms_graph()
    obs = C.communities()
    exp = []
    assert_equal((exp, obs)

# build_CBN without NIC
@with_setup(setup = Comm_setup(), teardown = Comm_teardown)
def BuildNIC_test():
    C.NIC = {}
    C.CBN = {}
    obs = C.build_NIC
    exp = None
    assert_equal(exp, obs)

# build_NIC without CBN
@with_setup(setup = Comm_setup(), teardown = Comm_teardown)
def BuildCBN_test():
    C.NIC = {}
    C.CBN = {}
    obs = C.build_CBN
    exp = None
    assert_equal(exp, obs)

# remove a community that doesn't exist
@with_setup(setup = Comm_setup(), teardown = Comm_teardown)
def RemoveNonComm_test():
    obs = C.remove_comm('NotAComm')
    exp = False
    assert_equal(exp, obs)

# give remove_comm a list
@with_setup(setup = Comm_setup(), teardown = Comm_teardown)
def RemoveCommList():
    B = readcomms("NCAA_EdgeList_Conf", delimiter=',',with_graph = True)
    C.remove_comm(['Southeastern Conference'])
    obs = C.NIC
    B.remove_comm('Southeastern Conference')    
    exp = B.NIC
    assert_equal(exp, obs)

# give BlockModel a single value for list_group_size
def BMOneER_test():
    C = BlockModel(list_group_sizes=5, p_in=0.9, p_btwn=0.1)
    obs = len(list(C.NIC.keys))
    exp = 1
    assert_equal(exp, obs)


