#!/usr/bin/env python
# _*_UTF-8_*_
# test_nets.py
# <Alexander Looi>
# Last Modified: <March 16, 2017>

import nets
import os
import time
from nets import Graph
from nets import read_adjmat
from nets import read_edgelist
from nets import subgraph
from nets import connected_nodes
from nets import relabel_nodes
from nose.tools import assert_equal, with_setup


#import py.test
# can import test modules here, but please no other third-party libraries

def test_nets_docstring():
    assert nets.__doc__ == "\nNETS CLASS DOCSTRING\n"

# FILL IN FROM HERE
# NODE FILL TESTS #
# testing a small network #
############################################################################
# test input of of graph on a small network
# These are some universal lists used for testing
Relationships = [['Alex','Julie'],['Julie','Alex'],['Alex','Michael'],['Michael','Alex'],['Julie','Michael'],['Michael','Julie'],['Mark','Michael'],['Michael','Mark'],['Jeff','Mark'],['Mark','Jeff'],['Ved','Michael'],['Michael','Ved'],['Alex','Ved'],['Ved','Alex'],['Ved','Jeff'],['Jeff','Ved'],['Ved','Rob'],['Rob','Ved'],['Julie','Rob'],['Rob','Julie'],['Rob','Jeff'],['Jeff','Rob']]
Friends = ['Alex', 'Julie', 'Rob', 'Ved', 'Michael', 'Mark', 'Jeff']

os.chdir('/Users/Looi/Desktop/MyRepo/HW04_Alooi/data')

# set up a graph to be tested
def Graph_setup():
    Friends = ['Alex', 'Julie', 'Rob', 'Ved', 'Michael', 'Mark', 'Jeff']
    Relationships = [['Alex','Julie'],['Julie','Alex'],['Alex','Michael'],['Michael','Alex'],['Julie','Michael'],['Michael','Julie'],['Mark','Michael'],['Michael','Mark'],['Jeff','Mark'],['Mark','Jeff'],['Ved','Michael'],['Michael','Ved'],['Alex','Ved'],['Ved','Alex'],['Ved','Jeff'],['Jeff','Ved'],['Ved','Rob'],['Rob','Ved'],['Julie','Rob'],['Rob','Julie'],['Rob','Jeff'],['Jeff','Rob']]
    G = Graph()    
    G.add_nodes_from(Friends)
    G.add_edges_from(Relationships)

# simple graph teardown
def Graph_teardown():
    del G

#NCAA setup
def NCAA_setup():
    NCAA = read_edgelist("NCAA_2005.edgelist", delimitedby= '" "')
    
#NCAA teardown
def NCAA_teardown():
    del NCAA
# End Setups and Tear downs
##################################################################
# add more than one node to "add_node"
def moreThanOne_test():
    G = Graph()
    G.add_node(['A', 'B'])
    obs = G.G
    exp = {'A':[]}
    assert_equal(exp, obs)

# give add_nodes_from a list of lists
def listOList_test():
    G = Graph()
    G.add_nodes_from([['A',],['B']])
    obs = G.G.keys()
    exp = {'A', 'B'} 
    assert_equal(exp, obs)

# give add_nodes_from an empty list #
def emptyNode_test():
    Friends = []
    G = Graph()
    G.add_nodes_from(Friends)
    obs = G.G
    exp = {}    
    assert_equal(exp, obs)

# the case where a graph is empty what is nodes()?
def emptySetNodes_test():
    G = Graph()
    obs = G.nodes()
    exp = set()
    # check nodes when the graph is empty
    assert_equal(exp, obs)

#@with_setup(setup=Graph_setup, teardown=Graph_teardown)
def numNode_test():
    # create a small graph
    G = Graph()    
    G.add_nodes_from(Friends)
    G.add_edges_from(Relationships)

    exp = {'Alex', 'Julie', 'Rob', 'Ved', 'Michael', 'Mark', 'Jeff'}
    obs = G.nodes()
    assert_equal(exp, obs)

#@with_setup(setup = Graph_setup, teardown = Graph_teardown)
def removeEmptyStr_test():
    # try to remove a node but user gives an empty string
    G = Graph()    
    G.add_nodes_from(Friends)
    G.add_edges_from(Relationships)
    G.remove_node('')
    exp = {'Alex', 'Julie', 'Rob', 'Ved', 'Michael', 'Mark', 'Jeff'}
    obs = G.nodes()
    assert_equal(exp, obs)

#@with_setup(setup = Graph_setup, teardown = Graph_teardown)
def removeEmptylst_test():
    G = Graph()    
    G.add_nodes_from(Friends)
    G.add_edges_from(Relationships)
    # try and remove an empty list
    G.remove_node(node=[])
    exp = {'Alex', 'Julie', 'Rob', 'Ved', 'Michael', 'Mark', 'Jeff'}
    obs = G.nodes()
    assert_equal(exp, obs)

#@with_setup(setup = Graph_setup, teardown = Graph_teardown)
def removeNodeSet_test():
    G = Graph()    
    G.add_nodes_from(Friends)
    G.add_edges_from(Relationships)
    # try to remove an empty set
    G.remove_node({})
    exp = {'Alex', 'Julie', 'Rob', 'Ved', 'Michael', 'Mark', 'Jeff'}
    obs = G.nodes()
    assert_equal(exp, obs)

#@with_setup(setup = Graph_setup, teardown = Graph_teardown)
def hasNodeEmpty_test():
    G = Graph()    
    G.add_nodes_from(Friends)
    G.add_edges_from(Relationships)
    # given an empty list to "has_node" should return empty list
    exp = False
    obs = G.has_node([])
    assert_equal(exp, obs)

#@with_setup(setup = Graph_setup, teardown = Graph_teardown)
def emptyEdges_test():
    G = Graph()    
    G.add_nodes_from(Friends)
    G.add_edges_from(Relationships)
    # test "edges" when given a string and not a list of strings
    obs = G.edges('Alex')    
    exp = [['Alex', 'Julie'], ['Alex', 'Michael'], ['Alex', 'Ved']]
    assert_equal(exp, obs)

#@with_setup(setup = Graph_setup, teardown = Graph_teardown)
def removeEdge_test():
    G = Graph()    
    G.add_nodes_from(Friends)
    G.add_edges_from(Relationships)
    exp = G.edges()
    # remove an edge but give an empty list
    G.remove_edge([])
    obs = G.edges()
    assert_equal(exp, obs)

#@with_setup(setup = Graph_setup, teardown = Graph_teardown)
def removeEdgeMorethan2_test():
    G = Graph()    
    G.add_nodes_from(Friends)
    G.add_edges_from(Relationships)
    # remove an edge but give three entries
    G.remove_edge(['Alex', 'Julie', 'Michael'])
    exp = 21
    obs = len(G.edges())
    assert_equal(exp, obs)

#@with_setup(setup = Graph_setup, teardown = Graph_teardown)
def removePartEdge_test():
    G = Graph()
    G.add_nodes_from(Friends)
    G.add_edges_from(Relationships)
    exp = G.edges()
    # remove an edge but give a single part of the edge
    G.remove_edge(['Alex'])
    obs = G.edges()
    assert_equal(exp, obs)

#@with_setup(setup = Graph_setup, teardown = Graph_teardown)
def addNoEdge_test():
    G = Graph()    
    G.add_nodes_from(Friends)
    G.add_edges_from(Relationships)
    exp = G.edges()
    # remove an edge but give an empty list
    G.remove_edge([])
    obs = G.edges()
    assert_equal(exp, obs)

#@with_setup(setup = Graph_setup, teardown = Graph_teardown)
def neighborsNoNode_test():
    G = Graph()    
    G.add_nodes_from(Friends)
    G.add_edges_from(Relationships)
    # give empty list
    obs = G.neighbors([])
    # need to figure how to capture standard out
    exp = False
    assert_equal(exp, obs)

#@with_setup(setup = Graph_setup, teardown = Graph_teardown)
def degreeNodeList():
    G = Graph()    
    G.add_nodes_from(Friends)
    G.add_edges_from(Relationships)
    # give and empty list
    obs = G.degree(node_L = [])
    exp = False
    assert_equal(exp, obs)

#@with_setup(setup = Graph_setup, teardown = Graph_teardown)
def clustCoefempty_test():
    G = Graph()    
    G.add_nodes_from(Friends)
    G.add_edges_from(Relationships)
    # give an empty list
    obs = G.clustering_coef(node_list = [])
    exp = {}
    assert_equal(exp, obs)

def info_test():
    # return info of an empty graph
    G = Graph()
    obs = G.info()
    exp = {'num_nodes':0, 'num_edgeSets':0, 'mean_degree':[], 'degree_std':[], 'orph_edges':[], 'orph_nodes':[]}    
    assert_equal(exp, obs)

#@with_setup(setup = Graph_setup, teardown = Graph_teardown)
def relabelNodesBlank_test():
    G = Graph()    
    G.add_nodes_from(Friends)
    G.add_edges_from(Relationships)
    Blank = ['', '', '', '', '', '', '']
    # give a blank list, a list with stuff, but they are all the same
    # and are empty character strings
    obs = relabel_nodes(G, Blank)
    exp = {'': ['', '', '']}
    assert_equal(exp, obs)

#@with_setup(setup = Graph_setup, teardown = Graph_teardown)
def relabelNodesUneven_test():
    G = Graph()    
    G.add_nodes_from(Friends)
    G.add_edges_from(Relationships)
    Notsame = ['A', 'B', 'C', 'D', 'E', 'F']
    obs = relabel_nodes(G, Notsame)
    exp = False
    # get standard out
    assert_equal(exp, obs)

def NotGraphDD_test():
    # case where graph is empty
    G_empt = Graph()
    obs = G_empt.degree_distribution() 
    exp = {} 
    # capture standard out
    assert_equal(exp, obs)

#@with_setup(setup = NCAA_setup, teardown = NCAA_teardown)    
def SourceNotSource_test():
    os.chdir('/Users/Looi/Desktop/MyRepo/HW04_Alooi/data')
    NCAA = read_edgelist("NCAA_2005.edgelist", delimitedby='" "')
    # case where originating node is not in a graph obj.
    obs = connected_nodes(NCAA,"Cornell") 
    exp = False
    # capture standard out
    assert_equal(exp, obs)

def SourceIsEdgeOnly_test():
    os.chdir('/Users/Looi/Desktop/MyRepo/HW04_Alooi/data')
    NCAA = read_edgelist("NCAA_2005.edgelist", delimitedby='" "')
    # case where originating node is not in a graph obj.
    obs = connected_nodes(NCAA, "Navy") 
    exp = False
    # capture standard out
    assert_equal(exp, obs)

def AdjMatReader_test():
    os.chdir('/Users/Looi/Desktop/MyRepo/HW04_Alooi/data')
    # read in an adjMat with a header
    MatH = read_adjmat('Test_adjMat.csv', delimitedby = ',', colnames = True)
    exp = {'n2': ['\ufeffn1'], 'n3': ['\ufeffn1', 'n4'], 'n4': ['\ufeffn1', 'n3'], '\ufeffn1': ['n2', 'n3', 'n4']}
    obs = MatH.G
    assert_equal(exp, obs)

def AdjMatReaderDelimiter_test():
    # read in an adjMat with incorrect delimiter
    MatH = read_adjmat('Test_adjMat.csv', delimitedby = '" "', colnames = True)
    obs = MatH
    exp = False
    assert_equal(exp, obs)

#@with_setup(setup = Graph_setup, teardown = Graph_teardown)
def subgraphNoneNode_test():
    G = Graph()    
    G.add_nodes_from(Friends)
    G.add_edges_from(Relationships)
    # A node in the subgraph list does not exist in "Nodes"
    sub_list = ['Alex', 'Michael', 'Julie', 'Matt']
    obs = subgraph(G, sub_list).G
    exp = {'Alex': ['Julie', 'Michael'],'Julie': ['Alex', 'Michael'],'Michael': ['Alex', 'Julie', 'Ved']}
    assert_equal(exp, obs)

def ClusteringCoefNodesDontExist_test():
    G = Graph()    
    G.add_nodes_from(Friends)
    G.add_edges_from(Relationships)
    obs = G.clustering_coef(['Lexa', 'Roy', 'Demmi'])
    exp = {}
    assert_equal(exp, obs)
    # create a graph with nodes but no edges
def SourceIsListConnectedNodes_test():
    os.chdir('/Users/Looi/Desktop/MyRepo/HW04_Alooi/data')
    NCAA = read_edgelist("NCAA_2005.edgelist", delimitedby='" "')
    # case where originating node is not in a graph obj.
    obs = set(connected_nodes(NCAA, ["TCU"]))
    exp = set(['TCU', 'Nebraska','Houston','Brigham Young','Hawaii','Boston College','Nevada','UNLV','San Diego St.','Virginia Tech','Virginia','Missouri'])
    # capture standard out
    assert_equal(exp, obs)
#Mat = read_adjmat('Adjmat_noheaders.csv', delimitedby = ',')
#MatH = read_adjmat('AdjMat_Header.csv', delimitedby = ',', colnames = True)


#G.clustering_coef('Alex')
#NCAA = read_edgelist("NCAA_2005.edgelist", delimitedby= '" "')
#cond = read_adjList("cond-mat.adjlist", delimitedby = " ", nodetype=None)
# make sure your test suite can be run from py.test or nosetests
