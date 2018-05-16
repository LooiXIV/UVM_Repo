#!/usr/bin/env python
# comms.py
# Alexander Looi
# Last Modified: March 26rd, 2017

"""COMMS
This module has all the components to create, manipulate and analyze communities for
a graph. In addition to manipulating and analyzing communities this module builds graphs. 
to associate with communities the user wishes to analyze and edit. Thus, this module 
requires the nets.py module to run work. There is one main class:
    
    The comms_graph object - This class allows a user to manually build communities
    for a network given existing nodes in a graph. There is also an option to auto-
    detect networks as well. Information on the methods within the comms_graph 
    class is in the the comms_graph docstring.
    
    There are four additional functions within this module.
    1) readcomms() - allows the user to read in a node to community file, or an
    edge list with a third column indicating the community a node in the first column
    belongs to
    
    2) writecomms() - writes a node to community list with the option to include an 
    edgelist.
    
    3) Erdos_Renyi() - creates an Erdos Renyi Graph with 'size' number of nodes and 
    probability 'p' of linking two nodes.
    
    4) BlockModel() - a net work of 'n' Erdos_Renyi Graphs with probability p_in of
    linking two nodes within a Erdos Renyi graph, and probability p_btwn of linking 
    two nodes between seperate Erdos Renyi graphs."""
import nets
from nets import Graph
import sys, os
import itertools
import csv
import random
import numpy as np

def readcomms(filename, delimiter="\t", with_graph = True):
    """Read community file
    This function can read two kinds of files:
    1) an edge list with another column showing the community that the first column
    of nodes belongs to (the originating node of an edge in the edge list). The first
    two columns are read in as an edge list and creates a graph. The third column is 
    read in with the first column, and builds a community of nodes according to the 
    communities in the third column. 
    2) Reads in a node to community list where the first column is the node, and the
    second column the community the node belongs to. This does not build a graph,
    and thus needs the 'read_edgelist' function from nets.py.
    
    When either file type are read in two community data structures are created. 
    1) The NIC data structure (Node in Community). This is a dictionary, where the
    dictionary key is the community name, and values associated with each community
    are node names.
    2) The CBN data structure (Community by node). This is another dictionary data
    structure where the node is the key and the community a node belongs to is the value
    for that node.
    
    Lastly, there are 3 inputs for this function:
        1) filename - the name of the file read in. This file can by an edge list
        with a third column denoting the community the node in the first column
        belongs to. Or it can be a node to community list. Here the first column is
        node and the second column is the community the node belongs to.
        2) delimiter - How data entries are seperated. All data in rows must use
        the same delimiter.
        3) with_graph - a boolean specifying if there is a graph attached to the
        data file (i.e. is the file an edgelist with a third column specifying
        communities)."""

    # open the comms file
    read_comms = open(filename, "r", errors="ignore")
    # create a community object, stores all communities
    net_com = comms_graph() # should also create a graph object
    # read the data line by line. building two dictionaries.
    if with_graph:
        #New_Graph = nets.read_edgelist(filename, delimitedby=delimiter)
        #net_com.G = New_Graph.G
        # build the communities and graph
        # reset the readline function back to the top
        #read_comms.seek(0)
        # Create a Graph "network" from class Graph()
        nodes = set() # an empty set to store nodes
        edge_list = [] # an edge list (list of lists)
        counter = 0 # Used to count the number of commented "junk" lines

        for ln, line in enumerate(read_comms):
            # make sure the line is read in as a string
            strline = line
            # Remove any blank spaces from the front and end of the string
            li=strline.strip()
            # make sure lines that begin with a "#" are not read in
            # make sure the line being read in does not have commented items
            if li.startswith("#"):
                counter = 0
            else:
                counter = counter + 1
                # remove any spaces that may occur after the "#"
                net_line = line.rstrip()
                # seperate out the lines using "delimitedby"
                node_edge_comm = net_line.split(delimiter)
                nodes.add(node_edge_comm[0])
                # initialize the first node if it's the 
                # first iteration/ first line actual of 
                # data in the network
                comm = node_edge_comm[2]
                node_c = node_edge_comm[0]
                edge_list.append(node_edge_comm[0:2])
                if counter == 1: 
                    prev_node = node_edge_comm[0]
                    counter = 100 
                # create a node, and neighbors entry
                # keep track of when the node changes
                prev_node = node_edge_comm[0]
                First_line = False
                net_com.add_node_to_comm(comm, node_c)
                
        # build the graph
        net_com.add_nodes_from(nodes)
        net_com.add_edges_from(edge_list)
        net_com.build_CBN()
    else:
        nodes = set() # an empty set to store nodes
        counter = 0 # Used to count the number of commented "junk" lines

        for ln, line in enumerate(read_comms):
            # make sure the line is read in as a string
            strline = line
            # Remove any blank spaces from the front and end of the string
            li=strline.strip()
            # make sure lines that begin with a "#" are not read in
            # make sure the line being read in does not have commented items
            if li.startswith("#"):
                counter = 0
            else:
                counter = counter + 1
                # remove any spaces that may occur after the "#"
                net_line = line.rstrip()
                # seperate out the lines using "delimitedby"
                node_edge_comm = net_line.split(delimiter)
                nodes.add(node_comm[0])
                # initialize the first node if it's the 
                # first iteration/ first line actual of 
                # data in the network
                comm = node_comm[1] # community
                node_c = node_comm[0] # node community
                if counter == 1: 
                    prev_node = node_edge_comm[0]
                    counter = 100 
                # create a node, and neighbors entry
                # keep track of when the node changes
                prev_node = node_comm[0]
                First_line = False
                # add the node to the community
                net_com.add_node_to_comm(comm, node_c)
                
        # build the community
        net_com.add_nodes_from(nodes)
        net_com.build_CBN()


    return(net_com)
#########################################################################################  
def writecomms(Graph, filename, delimiter = "\t", edge_list = False):
    """This function takes in a graph in 'dictionary form' and 
    writes it to a file of text. There are three values it 
    requires: 1) the Graph() class or network that the user 
    wants written, 2) a file name for the file that will be printed, 
    and 3) the desired delimiter that will seperate values. 
    
    The Graph() lass is specific to this particular module. 
    The actual graph object in the Graph() class must be in 
    dictionary form. Here the nodes are dictionary keys
    and values of keys are the other nodes the key node are linked
    to.

    The default setting will only create a node to community list. if
    edge_list = True then it was print a and edge list as well as the 
    community that first column node belongs to. 
    
    The file name can be made up of any alpha numeric combination.
    However, it must be utf-8 encoding.
    
    The delimiter default is a tab denoted by '\t'. However, 
    the user can specify any utf-8 alpha-numeric character.
    
    This does not return anything, but prints to a file through
    standard out."""
    network_file = open(filename, "w")
    
    # G has to be a dictionary object
    # loop through each dictionary key
    if edge_list:
        for n in Graph.G:
            # loop through each item in a dictionary
            for ne in Graph.G[n]:
                comm = C.CBN[n][0]
                # write each edge as a seperate line in the output file
                network_file.write(''.join([n,delimiter,ne,delimiter,comm,'\n']))
                # print to console to make sure things look okay
                print(n,delimiter,ne)
        # close the file
        network_file.close()
    else:
        for n in Graph.nodes():
            # loop through each item in a dictionary
            comm = C.CBN[n][0]
            # write each edge as a seperate line in the output file
            network_file.write(''.join([n,delimiter,comm,'\n']))
            # print to console to make sure things look okay
            print(n,delimiter,ne)
        # close the file
        network_file.close()
    
#########################################################################################  
class comms_graph(Graph):
    """COMMUNITY GRAPH
    
    This suite of modules provide all the tools to build, edit, and analyze
    a communities of nodes. This class inherits from Class NETS to build, 
    manipulate, and help with community analysis. There are two data structures
    in this class
    1) The NIC data structure (Node in Community). This is a dictionary, where the
    dictionary key is the community name, and values associated with each community
    are node names.
    2) The CBN data structure (Community by node). This is another dictionary data
    structure where the node is the key and the community a node belongs to is the value
    for that node.

    Additionally, there are several modules that allow for simple editing, building
    and analysis of communities of nodes. 
    1) communities - returns a list of all communities within a graph
    2) has_comm - returns true or false if a communities specified by the user exists.
    3) node_in_comm - returns the community a node belongs to, if it doesn't belong
        to a community it returns false
    4) build_CBN - builds the CBN data structure from data in the NIC data structure.
    5) build_NIC - builds the NIC data structure from the data in the CBN data structure.
    6) add_node_to_comm - Adds a node to a community specified by the user. for both
        data structures if the community doesn't exist, it is created and the user 
        specified node is added.
    7) remove_node_from_comm - removes a node from a community from both data structures.
        Does not delete or remove communities even if a community is empty.
    8) remove_comm - deletes a community from both data structures regardless if
        nodes are present in the community.
    9) configuration_model - Builds the configuration model, a hypothetical null model
        usually used to test significance to communities in a graph.
    10) modularity - Calculates modularity. How well is the graph partitioned?
    11) comm_part - A greedy single node or multi node algorithm, used to partition
        graphs.
    """    
    def __init__(self):
        """INIT
        1) Inherit the graph class from nets
        2) Create the CBN and NIC data structures.
        """
        Graph.__init__(self)
        self.CBN = {} # nodes are the key, community the value. 
        self.NIC = {} # communities are the key, nodes the values.

    ############################################################
    def communities(self):
        """communities()
        Returns a list of communities of a graph
        Needs no user input. If there are no communities associated with the graph
        then the module returns false."""
        communities = [] # set a list to store all communities
        # loop through all communties in the dictionary
        if bool(self.NIC):
            return(False)
        for comm in self.NIC:
            # append the community name to the comms list
            communities.append(comm)
        # return the comms list
        return(communities)

    ############################################################
    def has_comm(self, comm):
        """has_comm(comm)

        If a community is present in a graph, then return true,
        else return false. There is one user specified input needed.
        1) comm - community to check existance in graph."""
        # check to see if there is an empty list
        # if it's an empty list return false
        if bool(comm):
            # check to see if the commmunity exists in the comm obj
            if comm in self.NIC:
                return(True)
            else:
                # return false if the community doesn't exist
                return(False)
        else:
            return(False)

    ############################################################    
    def node_in_comm(self, node):
        """node_in_comm(node)
        
        Returns the community or communities that the node belongs
        to. If the node does not exist as part of any community
        the method will return false.
        
        1) node - The node to search communities in the graph."""
        if isinstance(node, list):
            node = node[0]
        if node in self.CBN:
            return(self.CBN[node])
        else:
            return(False)

    ############################################################
    def build_CBN(self):
        """build_CBN()
        After communities as been added to the NIC data strucutre, this 
        builds another community reference system. CBN has nodes as the 
        keys in the data structure. It is recommended that you use build_CBN
        only after you've finished creating communities and adding nodes
        to those communities. No user input is needed because the CBN
        is built through the NIC."""
        self.CBN = {}
        for c in self.NIC.keys():
            # for each community, set the nodes as a key
            # communities that nodes belong to become the
            # associated values
            for n in self.NIC[c]:
                # when node n is in more than one community
                #print(n, c)
                if n in self.CBN:
                    self.CBN[n].append(c)
                else:
                    # when node n is only in one community
                    self.CBN[n] = [c]

    ############################################################
    def build_NIC(self):
        """build_NIC()
        Build a NIC community data structure from the CBN"""
        self.NIC = {}
        nodes = list(self.CBN.keys())
        for n in nodes:
            comm = self.CBN[n][0]
            if comm not in self.NIC: 
                self.NIC[comm] = [n]
            else: 
                self.NIC[comm].append(n)
        self.build_CBN()
        
    ############################################################
    def add_node_to_comm(self, comm, node):
        """add_node_to_com(comm, node)
        
        Add a community and populate with one node. If a community already
        exists but the node being added does not exist within the community,
        then just add the node. This only adds one community and node pair
        at a time. There are two user inputs:
        1) comm - The community to add
        2) node - the node that is added to community 'comm'
        """
        
        # check to see if the comm entry is a single entry
        # if it's a list only use the first value
        if isinstance(comm, list) and bool(comm):
            comm = comm[0]
        elif bool(comm) == False:
            print("variable 'comm' is empty")
            return(False)
        # check to see if the node entry is a single entry
        # if it's a list only use the first value
        if isinstance(node, list) and bool(node):
            node = node[0]
        elif bool(node) == False:
            print("variable 'node' is empty")
            return(False)
        # see if the community already exists, if it does
        # add a node to the community, if it doesn't have the community
        # add the community as a key and add the associated
        # node to the new community
        if self.has_comm(comm):
            if node in self.NIC[comm]:
                # check to see if the node exists in the NIC community,
                # if it does, return false, for both the CBN and
                # NIC data structures
                self.CBN[node] = [comm]         
                return(False)
            else: 
                # if the node does not exist in NIC but the community
                # exists in NIC add the node to the community
                self.NIC[comm].append(node)
        # check to see if the community exists and if the node
        # is present in the community
        elif self.has_comm(comm) and node not in self.NIC[comm]:
            # if the community is empty, add the node to the community
            if bool(self.NIC[comm]) == False:
                self.NIC[comm] = [node]
            else:
                # if the community has nodes in it, append the node
                # to a list of nodes in the community.
                self.NIC[comm].append(node)
        else: # if the community does not exist add the community and node
            self.NIC[comm] = [node]
            # also add to the CBN data structure
        # add the node and community to the CBN data structure
        self.CBN[node] = [comm]
    ############################################################
    def remove_comm(self, comm):
        """remove_comm(comm)
        
        Removes a community from a graph from both the CBN and NIC data
        structure regardless if the communities are empty. There is one
        input needed.
        1) comm - the community to be removed."""
        # check to see if the comm var is empty
        if bool(comm) == False:
            print("this list is empty")
        elif self.has_comm(comm):
            nodes = self.NIC[comm][0]
            for n in nodes:
                self.CBN[n].remove(comm)
            del self.NIC[comm]
        else:
            print(comm, "cannot be removed because it does not exist as a community")
            return(False)

    ############################################################
    def remove_node_from_comm(self, comm, node):
        """remove_node_from_comm(comm, node)

        Remove a node from community that it is in. If there are no nodes 
        remaining in a community, the community will still remain. There are
        two pieces of input needed:
        1) comm - The community to look in
        2) node - The node to remove from community comm."""
        # check to see if node is a single char var or a list
        if isinstance(node, list):
            node = node[0]
        if isinstance(comm, list):
            comm = comm[0]

        if node in self.CBN and comm in self.NIC:
            print(node)
            if node in self.NIC[comm]:
                # the community the node to be deleted is associated with
                # delete the node from the communty key
                self.NIC[comm].remove(node)
                # delete the community from the node key
                self.CBN[node].remove(comm)
            else:
                print("node", node, "does not exist in community", comm)
                return(False)
        else:
            return(False)

    ############################################################
    def configuration_model(self):
        """configuration_model()
        Build a configuration model using the degree distribution
        of the current graph."""
        DD = self.degree_distribution()
        # build a second dictionary from DD where each node is a key
        # and the value is the node's degree distribution.
        keys_DD = DD.keys()
        cm_DD = {}
        num_edges = 0
        # loop through all degrees and find all the nodes with that
        # degree
        for nn in keys_DD:
            # grab each node with a particular degree
            nodes = DD[nn]
            # put that node with its degree into a dictionary where
            # the node is the key, and its degree is the value
            # there should only be 1 value for each key
            for d in nodes:
                num_edges = num_edges + nn
                cm_DD[d] = [nn]

        # loops through all the nodes, and randomly 
        # connect them with other nodes, creating a 
        # new randomly generated graph. 
        nodes = list(cm_DD.keys())
        num_nodes = len(nodes)
        edge_listCM = []
        # create a graph and add all nodes
        CMG = Graph()
        CMG.add_nodes_from(nodes)
        choices = list(range(0,num_nodes))
        NN_remain = len(choices)
        while NN_remain > 0:
            #print(choices)
            # randomly choose a "originating node"
            pick_n1 = random.choice(choices)
            node1 = nodes[pick_n1]
            C_index1 = choices.index(pick_n1)
            # randomly choose another node for the
            # "orginating node" to connect to 
            # ("connecting node")
            if C_index1 == len(choices)-1:
                choices2 = choices[0:C_index1]
            elif C_index1 == 0:
                choices2 = choices[1:len(choices)+1]
            else:
                P1 = choices[0:C_index1]
                P2 = choices[C_index1+1:len(choices)]
                choices2 = P1+P2 

            pick_n2 = random.choice(choices2)            
            node2 = nodes[pick_n2]
            # create an edge
            edge = [node1, node2]
            rev_edge = [node2, node1]
            # add the node to the graph
            EB1 = CMG.add_edge(edge)
            #EB2 = CMG.add_edge(rev_edge)
            #print(EB1, EB2)
            
            # if the edge sets did not exist then remove a degree
            # from the two randomly choosen nodes, remove a node from
            # NN_remain if the degree of a node reaches 0. If
            # the edge set already existed then choose another edge set
            if EB1:
                node_val1 = [cm_DD[node1][0]-1]
                node_val2 = [cm_DD[node2][0]-1]
                #print(node_val1, node_val2)
                cm_DD[node1] = node_val1
                cm_DD[node2] = node_val2
                if cm_DD[node1][0] == 0:
                    #print(choices)
                    #print("P1", pick_n1)                    
                    #print(choices)
                    choices.remove(pick_n1)
                if cm_DD[node2][0] == 0:
                    #print(choices2)                    
                    #print("P2", pick_n2)                    
                    choices.remove(pick_n2)
                    #print(choices)
            NN_remain = len(choices)
            #print(NN_remain)
            #print(NN_remain, choices)
            #print(cm_DD) 
        #num_edges = num_edges/2
        #for e in num_edges:
            #random.random()
        #return(cm_DD)
        return(CMG.G)

    ############################################################
    def modularity(self):
        """modularity()
        
        calculate the modularity of a graph. No user input required."""
        # calculate the total number of edges in a graph "M"        
        M = len(self.edges())
        Mat_sum = []
        # loop through all nodes and all the other nodes they share a
        # connection with.
        nodes = self.nodes()
        for n in nodes:
            # edges of node "n"
            N_edges = self.G[n]
            # determine community of node "v"
            C_v = self.CBN[n][0]
            for e in nodes:
                k_v = self.degree(n)[n][0]
                k_w = self.degree(e)[e][0]
                # determine community of node "w"
                C_w = self.CBN[e][0]
                # determine if the nodes share a link
                edge_t = [n,e]
                if self.has_edge(edge_t):
                    #print(edge_t)
                    Avw = 1
                else:
                    Avw = 0
                # determine if they are in the same community
                if C_v == C_w:
                    delta = 1
                else:
                    delta = 0
                    #print(C_v, C_w)                    
                # compute a single element of the sum
                Mat_cell = (Avw-(k_v*k_w)/(2*M))*delta                  
                Mat_sum.append(Mat_cell)

        Q = sum(Mat_sum)/(2*M)
        return(Q)

    ############################################################
    def comm_find(self, multi = False):
        """comm_find(multi=T or F)
        
        partitions nodes in a graph using a greedy algorithm. This can either
        work node by node or by groups of nodes that belong the same 
        community. Here we try and maximize modularity. There is one piece of 
        user input.
        
        1) multi - Default False. True if the user wants the algorithm to 
            include groups of nodes from the same community in calculating"""
        self.NIC = {}
        self.CBN = {}
        # get nodes and assign a single community to each
        nodes = list(self.nodes())
        num_nodes = [str(i) for i in range(0,len(nodes))]
        node_comms = ["C" + nn for nn in num_nodes]
        for nn,n in enumerate(nodes):
            self.add_node_to_comm(node_comms[nn], n)
        self.build_CBN()
        # start at the first node_comm individual, look at all their neighbors
        # and add the node to the originating community where the modularity
        # increases the most.
        max_m = self.modularity() # initialize max_modularity parm to optimize
        for on in nodes:
            neighbors = self.G[on]
            org_comm = np.copy(self.CBN[on])[0]
            
            for nv, neigh in enumerate(neighbors):                
                # if the neighboring node belongs to a larger community
                # bring in all nodes from that community.
                comm = np.copy(self.CBN[neigh])[0]
                nodes_in_comm = self.NIC[comm]                
                num_nodes_comm = len(nodes_in_comm)
                
                # if a node belongs to a larger community include all 
                # those nodes.
                if num_nodes_comm > 1 and multi == True:
                    for cn in nodes_in_comm:
                        self.remove_node_from_comm(comm, cn)                        
                        self.add_node_to_comm(org_comm, cn)
                    # calculate the modularity
                    # find the node that gives the max modularity
                    if new_modularity > max_m:
                        max_node = neigh
                        max_m = new_modularity
                        remove_comm = comm
                        del self.NIC[remove_comm]
                else:
                    # remove the node from its community
                    self.remove_node_from_comm(comm, neigh)
                    # add node to the originating node's community
                    self.add_node_to_comm(org_comm, neigh)
                    
                    # Calculate the modularity of the new communities.
                    new_modularity = self.modularity()
                    # find the node that gives the max modularity
                if new_modularity > max_m:
                    max_node = neigh
                    max_m = new_modularity
                    remove_comm = comm
                    del self.NIC[remove_comm]
    
#########################################################################################
def Erdos_Renyi(size, p):
    """Erdos_Renyi(size, p)
    Create an Erdos Renyi Graph. Create a graph with 'size' number of nodes
    with probability p of a connection between any two nodes. There are two
    required inputs:
        1) size - the size in number of nodes of the graph.
        2) p - the probability p of a connection between any two nodes. p must
            be a number between 0 and 1."""
    # Create nodes of length size
    if size < 1:
        print("cannot have a network less than one node")
        return(False)

    numbers = list(range(1,size+1))
    n_num = [str(i) for i in numbers]    
    all_nodes_names = ["N" + nn for nn in n_num]
    # Create an Erdos Renyi graph obj
    ERG = comms_graph()
    ERG.add_nodes_from(all_nodes_names)

    # loop through all the nodes in graph ERG with probability "p" of making a 
    # connection. If a connection is made, assume the graph is non-directional
    # and make the opposite connection as well
    #if p > 1:
    #    print("p cannot be greater than 1.0")
    #    break
    # loop through all nodes, this is the originating node
    for n in all_nodes_names:
        org_edge = n
        # loop through all nodes that can be connected to
        for e in all_nodes_names:
            # there is probability 'p' of making a connection
            con_edge = e
            edge1 = [org_edge, con_edge]
            edge2 = [con_edge, org_edge]
            if ERG.has_edge(edge1) == False and ERG.has_edge(edge2) == False:
                if random.random() < p:
                    # connect the two nodes in both directions
                    ERG.add_edge(edge1)
                    ERG.add_edge(edge2)
    return(ERG)
#########################################################################################
def BlockModel(list_group_sizes, p_in, p_btwn):
    
    """BlockModel(list_group_sizes, p_in, P_btwn)
    
    Create a block model. This will create several Erdos Renyi graphs
    specified by the number of entries in 'list_group_sizes', and values.
    nodes within each Erdos Renyi graph have probability p_in of being
    connected. Between Erdos Renyi graphs there is probability p_btwn of
    two nodes from seperate graphs of being connected. There are three
    required inputs:
        1) list_group_sizes - a list of integers specifying the size
            of each Erdos Renyi graph to create. There can be any number
            of integers, as well as any number as the integers.
        2) p_in - the probability two nodes will connect within an 
            Erdoes Renyi graph.
        3) p_btwn - the probability two nodes from seperate Erdos Renyi
            graphs will connect."""
    All_comms = {}
    for cn, c in enumerate(list_group_sizes):
        # Create a name for the community
        comm_name = "C"+str(cn)
        # create an ER graph
        C = Erdos_Renyi(size=c,p=p_in)
        All_comms[comm_name] = C
    # relabel all nodes
    new_nodes_num = list(range(0,sum(list_group_sizes)))
    new_node_names = ["T"+str(i) for i in new_nodes_num]
    comms = list(All_comms.keys())
    start = 0
    Block_graph = comms_graph()
    # put nodes into communities
    for cn, c_rename in enumerate(comms):
        # grab the appropriate number of new node names for the 
        # ER graph.
        end = sum(list_group_sizes[0:1+cn])
        comm_node_names = new_node_names[start:end]
        #print(len(comm_node_names))
        start = end
        # assign node from each ER graph to a community
        # after relabeling.
        # relabel the nodes        
        All_comms[c_rename].relabel_nodes(comm_node_names)
        # assign newly relabelled nodes to a community in a
        # large graph which houses the block graph
        block_nodes = All_comms[c_rename].nodes()
        Block_graph.add_nodes_from(block_nodes)
        ERG_edges = All_comms[c_rename].edges()
        Block_graph.add_edges_from(ERG_edges)
        for bn in block_nodes:
            Block_graph.add_comm_node(c_rename, bn)
            # add edges for each newly added node
            Block_graph.G[bn] = All_comms[c_rename].G[bn]
        # build the CBN community data structure
        Block_graph.build_CBN()
    # Connect ER graphs using betweeness. Loop through all
    # nodes not in the current community. There is a prob.
    # p_btwn of two nodes from differing communities to connect
    for c in comms:
        # grab all nodes from the current community
        current_comm = Block_graph.NIC[c]
        other_comms = []
        for oc in comms:
            if oc != c:
                # grab all nodes from other communities
                other_comms = other_comms + Block_graph.NIC[oc]

        # start linking nodes between communities
        for n in current_comm:
            for en in other_comms:
                if p_btwn > random.random():
                    Block_graph.add_edge([n,en])

    return(Block_graph)

#########################################################################################
