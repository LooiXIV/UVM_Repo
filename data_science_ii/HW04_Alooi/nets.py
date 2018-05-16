#!/usr/bin/env python
#!/usr/bin/env python
# nets.py
# Alexander Looi
# Last Modified: March 3rd, 2017

"""
This is a series of functions to read and write networks in various forms.
There are three types of raw network data files that this program can read
1) Edge list
2) Adjacency List
3) Adjacency Matrix
Files that are successful read will be returned as a Graph object. 
Graph objects can be manipulated and analyzed using methods within
the graph object.

Graph objects have the following methods:
        1) nodes - returns a set of nodes in the Graph object.
        2) add_node - adds a single node to the graph given a 
            character string.
        3) add_nodes_from - add a list of nodes to the graph given a list
        4) remove_node - remove a single node from the graph given
            a character string.
        5) has_node - checks to see if a graph has a node given a str input
        6) edges = returns a list of all edge sets in a graph in list form
        7) remove_edge - remove an edge in a graph given a character string
        8) has_edge - check to see if a graph has an edge set
        9) add_edges_from - given a list of edge sets add the edges to the
            graph.
        10) neighbors - given a node or a graph return the number of neighbors
            a node has.
        11) number_of_nodes - return the number of nodes in a graph obj.
        12) number_of_edges - return the number of edges in a graph obj.
        13) degree - find the degree of a node, either for the entire graph
            or a specific node.
        14) clustering_coef - find the clustering coefficient given a list
            of nodes in the graph.
        15) info - returns general info about the graph
These methods give both the ability to create a new graph object and manipulate
the graph object.
"""
import sys, os
import collections
import itertools
import csv, json
# NOTE - no more imports are allowed!

def write_edgelist(Graph, filename, delimiter="\t"):
    """This function takes in a graph in 'dictionary form' and 
    writes it to a file of text. There are three values it 
    requires: 1) the Graph() class or network that the user 
    wants written, 2) a file name for the file that will be printed, 
    and 3) the desired delimiter that will seperate values. 
    
    The Graph() lass is specific to this particular module craete
    by Alexander Looi. The actual graph object in the Graph() class
    must be in dictionary form. Here the nodes are dictionary keys
    and values of keys are the other nodes the key node are linked
    to.
    
    The file name can be made up of any alpha numeric combination.
    However, it must be utf-8 encoding.
    
    The delimiter default is a tab denoted by '\t'. However, 
    the user can specify any utf-8 alpha-numeric character.
    
    This does not return anything, but prints to standard out."""
    network_file = open(filename, "w")
    
    # G has to be a dictionary object
    # loop through each dictionary key
    for n in Graph.G:
        # loop through each item in a dictionary
        for ne in Graph.G[n]:
            # write each edge as a seperate line in the output file
            network_file.write(n,delimiter,ne)
            # print to console to make sure things look okay
            print(n,delimiter,ne)
    # close the file
    network_file.close()

#########################################################################################

def read_edgelist(filename, delimitedby="\t"):
    """This reads an edge list and converts to a Graph() object/class.
    The edge list must be formated into two columns. The first column
    stores origin nodes, stores destination nodes. This way the edge list
    is read left to right (origin to destination). This method takes in 
    Three variable types: 1) filename, 2) delimitedby, and 3) nodetype.
    
    The filename is the name of the edge list file. The encoding of the
    file must be in UTF-8.
    
    The delimiter can be any alpha numeric character. However, the default
    is tab denoted by '\t'. Unless the user specifies the delimiter tab
    will be assumed to be the default delimiter.
    
    The nodetype,
    
    This returns a graph object.""" # what is node type?
    read_net = open(filename, "r", errors = "ignore")
    # need case where file does not exist.

    # read the data in line by line keeping track of the nodes.
    
    # Create a Graph "network" from class Graph()
    network = Graph() # Create a Graph object
    nodes = set() # an empty set to store nodes
    edge_list = [] # an edge list (list of lists)
    counter = 0 # Used to count the number of commented "junk" lines
    for ln, line in enumerate(read_net):
        # make sure the line is read in as a string
        strline = line
        # Remove any blank spaces from the front and end of the string
        li=strline.strip()
        # make sure lines that begin with a "#" are not read in
        #all_edges = []
        # make sure the line being read in does not have commented items
        if li.startswith("#"):
            counter = 0
        else:
            counter = counter + 1
            # remove any spaces that may occur after the "#"
            net_line = line.rstrip()

            # seperate out the lines using "delimitedby"
            node_edge = net_line.split(delimitedby)
            #print(node_edge[0])
            nodes.add(node_edge[0])
            # take the first element from each list as the "node"
            #nodes.add(node_edge[0])
            # create a list of neighbors for each node
            #neighbors.append(node_edge[1])
            # initialize the first node if it's the 
            # first iteration/ first line actual of 
            # data in the network
            edge_list.append(node_edge)
            if counter == 1: 
                prev_node = node_edge[0]
                counter = 100 
            # create a node, and neighbors entry
            #if node_edge[0] != prev_node:
                #network[prev_node] = neighbors
                # reset the neighbors for the new node
                #neighbors = []
            # keep track of when the node changes
            prev_node = node_edge[0]
            First_line = False
    
    network.add_nodes_from(nodes)
    network.add_edges_from(edge_list)
    read_net.close()
    return(network)
#########################################################################################
def relabel_nodes(graph, N_names):
    """Relabels node names of a network (keys in the dictioanry) as well 
    as the names of nodes that nodes link to (edges/values in dictionary). 
    This method takes two objects, a Graph(), and a list of new node names
    
    1) graph - A Graph() object from this module, where Graph.G() is a 
    network as a dictionary.

    2) N_names - a list of new node names, each new node name must be a string
    where all new node name entries are in list form. Additionally, the number
    of new node names has to be the same as the number of nodes in the original
    graph. Lastly, the node names in N_name will replace corresponding node names 
    in the graph object. Example, if a network Net1 has nodes {Node1, Node2} to be
    replaced with [N_a, N_a], Net1 will be {N_1, N_b}
    
    This function will replace the original graph object used as input and 
    return essentially the same graph object except with replaced node names"""

    if len(graph.G) != len(N_names):
        print("Input graph and list of node names are not the same length")
        return(False)
    else: 
        # n_n = node number; o_n = original node name
        # convert to keys in the dictionary to a list
        original_nodels = list(graph.G.keys())
        # loop through all the original nodes and replace them with
        # the node name in N_names.
        #print(original_nodels)
        #print(graph.G.keys())
        for n_n, o_n in enumerate(original_nodels):
            #print("node to replace", o_n, "with", N_names[n_n])
            #print(o_n, "is now", N_names[n_n])
            # replace the edges by looping through each key again
            # and replacing the appropriate edges
            #print(n_n, o_n)
            #print("Original Nodes",original_nodels)
            for e_n in original_nodels:
                #print(e_n)
                # loop through all the edges for a node
                org_edges = graph.G[e_n]
                #print("looking for", o_n, "in", org_edges)
                for n_e, e in enumerate(org_edges):
                    #print(n_e, e)
                    # if there is a match for the original node name 
                    # replace it with the new node name
                    #print(o_n, e)
                    if o_n == e:
                        org_edges[n_e] = N_names[n_n]
                        #print(N_names[n_n])
                # replace the node values
                #print(org_edges)
                graph.G[e_n] = org_edges
            # replace the key
            graph.G[N_names[n_n]] = graph.G.pop(o_n)
            # update the "original" nodes list by replacing item that was
            # replaced in the dictionary
            original_nodels[n_n] = N_names[n_n]
    return(graph.G)

#########################################################################################
def connected_nodes(graph, source):
    """This method returns a list of nodes that a source/input node are connected to.
    The basic input is a graph and a source node.
    
    1) Graph() - a graph object with a network G.
    
    2) a source node as a character string.
    
    returns a list of nodes that the source nodes share connections with"""

    # need a case where source node does not exist as a node.

   # first look at all the nieghbors of the source node and get the source node's
    # neighbors. 
    # Put those nodes in a variable called "nodes visted"
    # get the all the neighbors of neighboring nodes excluding those in nodes
    # already visited.
    # Do this until there are not more unique nodes to visit (that are "visitable")
    # find the neighbors of node "source"
    if isinstance(source, list):
        source = source[0]
    if graph.has_node(source):
        neighbors = graph.G[source]
        source = [source]
    else:
        print("Node does not exist")
        return(False)
        
    # find the number of neighbors to visit
    # as long as this is greater than 1 the function will continue running
    num_nodes = len(neighbors)
    # now that the original "source node" has been visited
    # create a list of visted nodes
    # initialize visited nodes with source
    visited_nodes = source
    while num_nodes > 0:
        num_nodes = 0
        # now that we have visited the source node, the neighbors are the new
        # source nodes.
        source = neighbors
        # reset neighbors
        neighbors = []
        # the new source nodes have been "visited"
        #visited_nodes = visited_nodes + source
        
        # get a list of all neighbors for the new list of source nodes
        for sc in source:
            #print(sc)
            # get all the neighbors of source sc
            if graph.has_node(sc):
                neighbors = neighbors + graph.G[sc]
            else:
                print(sc, 'is an orphaned edge')
        # find all unique values by using "set" then coer. to a list so that 
        # it becomes iterable

        neighbors = list(set(neighbors))
        # which nodes in neighbors have already been visited
        for n in neighbors:
            #print(n)
            if n not in visited_nodes:
                visited_nodes = visited_nodes + [n]
                num_nodes = num_nodes + 1 
    return(visited_nodes)

#########################################################################################
def read_adjList(filename, delimitedby = '\t', nodetype=None):
    """A function to read an adjecency list from a text file. Then uses
    the input to create a graph object. There are two main inputs, a filename
    and a delimiter (delimitedby).
    
    1) filename - the name of adjlist file. The formatting of this file is similar to
    a dictionary. Here the originating node is in the first column. Nodes that the
    originating node are connected to are in subsequent columns. Number of columns per
    row can vary depending on the number of connections
    
    2) delimitedby - a character string telling the program who columns in rows (nodes and
    edges in a row of the file) are seperated. The default is '\t', but any alpha numeric
    character can be used"""
    read_net = open(filename, "r")
    G = Graph()
    for l in read_net:
        # split up the nodes and edges by the delimiter
        node_edges = l.split(delimitedby)
        # collect the node which is always in position "0"
        # add the node to the network
        node = node_edges[0]
        G.add_node(node)
        # remove new line character from the last entery in a line
        node_edges[-1] = node_edges[-1].rstrip("\n")
        #print(node) # print the node
        #print(node_edges[1:len(node_edges)])
        # return all the edges associated with a node
        edges = node_edges[1:len(node_edges)]
        G.G[node] = edges # create a new node/key in a dictionary
        # give the key values/edges/links to other nodes
    return(G)
#########################################################################################
def read_adjmat(filename, delimitedby='\t', nodetype=None, colnames=False):
    # still need to get to the point where it can except headers and 
    # row names.
    """Read an adjcency matrix that is not directed. The columns and rows
    HAVE to be transpose of each other. If on the column names are given when 
    colnames = True, then the adj matrix file is assumed to symetrical. Requried
    inputs are filename, a delimiter, and an indication if there are column names/
    a header
    
    1) filename - the name of the adjmatrix file. The file should be a square
    matrix (unless there is a header). The contents of cells should be numerics
    only, this method will not be able to interpret other kinds of characters
    
    2) delimitedby - the delimiter of cells. This must be consistent through
    the entire file. The default is '\t', but any alpha numeric character can be 
    used.
    
    3) colnames - true or false, if there are column names or headers/specific node
    names. The default is false (assuming there are no column names). This method
    is unable to autodetect column names so be careful."""
    read_mat = open(filename, "r")
    G = Graph()
    if colnames == False:
        need_node_names = True
    else:
        need_node_names = False
    # read through the rows in this case each row is a node
    # a 1 denotes that there is a link between two nodes
    for ln, l in enumerate(read_mat):
        print(l)
        # split the contents of each row using the user defined
        # delimiter
        row = l.split(delimitedby)
        # remove the \n character if it exists
        row[-1] = row[-1].rstrip("\n")

        # use the column names if there is a header
        # if there are column names (header) use those 
        # instead of doing a generic node naming
        if colnames:
            # make sure to only grab the first line for use in 
            # naming nodes if colnames = True
            if ln == 0:
                all_node_names = row
                #print(all_node_names)
                continue
            else:
                # because the column names will take up the first
                # row the ln now has to be off set to make sure 
                # future subsetting of nodes and edges is correct
                ln = ln - 1
        # in the case where there are no node names, 
        # create generic node names.
        elif need_node_names:
            numbers = list(range(1,len(row)+1))
            n_num = [str(i) for i in numbers]
            all_node_names = ["node_" + nn for nn in n_num]
            
        #print(all_node_names)
        #print(ln)
        node_name = all_node_names[ln]
        # add the node as a key to a dictionary
        G.add_node(node_name)
        # add the edges the node has
        # create a list of edges
        edges = []
        for cn,c in enumerate(row):
            #print(node_name, c, cn)
            # convert cell value to a float so it can be evaluated
            # the nodes are linked if the cell value in an adj mat is greater than 0.
            try:
                cell_val = float(c) # need to be able to catch non-numeric characters
            except:
                # break out of the loop if there are none numeric
                # characters in adj mat.
                print("cell value is not a float or int")
                return(False)
                break
            if cell_val > 0:
                # start linking nodes, node row number n with node col number c
                # if there are columns use those
                link_node = all_node_names[cn]
                # add all edges to a list which will be "attached" to a key/node
                # in the network.
                edges.append(link_node)
                #print(edges)
        # add the edges to the node/key
        #print(node_name,edges)
        G.G[node_name] = edges
        #print(row)
    return(G)

############################################################
def subgraph(graph, Nodes):
    """Creates a sub graph given a 1) graph object and 2) a list of nodes.
    The sub graph() is a smaller graph made up of nodes in 'Nodes'
    using the Nodes and edges found in the graph object 'graph'.
    The graph object returned will only have nodes and edges specified
    in Nodes.
    
    1) graph - this is a Graph() object specified in this module
    
    2) Nodes - a list of character strings specifying the nodes to make
    a sub graph. The nodes in 'Nodes', need to names in the original 
    graph object."""
    # make a new graph with the nodes in "Nodes"
    newG = Graph()
    for n in Nodes:
        # add nodes to the new graph if they exist in "graph"
        if graph.has_node(n):
            newG.add_node(n)
            # add the edges (all edges)
            edges = graph.G[n]
            # remove edges not in the subgraph
            for e in edges:
                # if the nodes 
                if e not in Nodes:
                    #print(e)
                    edges.remove(e)
            newG.G[n] = edges
        else:
            print("Node", n, "Does not exist")
    
    return(newG)

#########################################################################################  
class Graph(object):
    """A Graph class to create, store and manipulate a network. 'self' is
    the key variable. Within self there is a variable 'G'. G is a dictionary 
    that stores nodes as dictionary keys. Values for each key are nodes that 
    each the key node shares links with. Direction of links go from the key 
    node to the value node. Next there are 16 methods within Graph which
    have a variety of functions:
    
        1) nodes - returns a set of nodes in the Graph object.
        2) add_node - adds a single node to the graph given a 
            character string.
        3) add_nodes_from - add a list of nodes to the graph given a list
        4) remove_node - remove a single node from the graph given
            a character string.
        5) has_node - checks to see if a graph has a node given a str input
        6) edges = returns a list of all edge sets in a graph in list form
        7) remove_edge - remove an edge in a graph given a character string
        8) has_edge - check to see if a graph has an edge set
        9) add_edges_from - given a list of edge sets add the edges to the
            graph.
        10) neighbors - given a node or a graph return the number of neighbors
            a node has.
        11) number_of_nodes - return the number of nodes in a graph obj.
        12) number_of_edges - return the number of edges in a graph obj.
        13) degree - find the degree of a node, either for the entire graph
            or a specific node.
        14) clustering_coef - find the clustering coefficient given a list
            of nodes in the graph.
        15) info - returns general info about the graph"""
        
    
    def __init__(self):
        """Initialize the variables within the class. The only variable to
        initialize is self, and a dictionary within self. This dictionary
        is the network/graph G."""
        # this is a graphs adjacency list for a particular node
        # put in "dictionary" form. Makes sure the "values" are sets
        # That way there is no "self linking"
        self.G = {} # node --> set neighbors (start from this, *hint hint*)
        # A node taken from the adjacency list. 
        #self.nodes = set()
        # edge or link for a node linking the node to other nodes. 
        #self.edges = []

        # should I have code here that creates a graph given an input of data?
    ############################################################
    def nodes(self):
        """returns a set() of all nodes in the graph"""
        nodes = []
        for node in self.G:
            nodes.append(node)
        return(set(nodes))
        # pass
        # may need a test to see what happens when a data structure
        # other than a dictionary is passed to nodes
    ############################################################
    def add_node(self, node):
        # a function to add a single node to 
        """Add a node to graph 'G' if a list is given then use
        the first element"""
        if isinstance(node, list) and bool(node):
            node = node[0]
        if node not in self.G and bool(node): # don't erase an existing node
            self.G[node] = []
        elif bool(node) == False:
            self.G = None
        else:# if the node already exists make sure the user knows
            print("node already exists")
    ############################################################    
    def add_nodes_from(self, L_nodes):
        """ add nodes to a graph obj from a list of nodes """
        #L_nodes = list(itertools.chain(*L_nodes))
        # takes a list of strings and adds them as individual nodes
        for addN in L_nodes:
            self.add_node(addN)
                #if addN not in self.G:
                #    self.G[addN] = []
                #else: 
                #    print(addN, "already exists as a node")
    ############################################################
    def remove_node(self, node):
        """Remove a single node 'node' from graph 'G' """
        # does the node exist in G?
        if bool(node) == False:
            print("this is empty")
        elif node in self.G:
            # First have to remove neighbors 
            # (other nodes linked to the node being removed        
            node_neighbors = self.G[node]
            # loop through al the node neighbors to remove the neighbors
            for n in node_neighbors:
                self.G[n].remove(node)
            # finally remove the node
            del self.G[node]
        else:
            # if is no node present inform the user.
            #return(False)
            print(node, "cannot be removed since it does not exist")
    ############################################################            
    def has_node(self, node):
        """Check to see if a graph has a node 'node_name.'
        1) only input is 'node'. Method will return false
        if the node does not exist and will return true
        if the node does exist."""
        if bool(node):
            if node in self.G: 
                return(True)
            else:
                return(False)
        else:
            return(False)
    ############################################################
    def edges(self,nodes=None):
        """Return all the edges/links.
        The function will have to go into each key, 
        then print the 'key' node and the other
        nodes that the 'key' shares links with.
        Essentially returns an edge list. If given
        a list of nodes it will return all edges
        for that list of nodes"""
        edges = []
        if nodes is None:
            nodes = self.G.keys()
        elif isinstance(nodes, str):
            nodes = [nodes]
        # loop through all nodes 
        for node in nodes:
            # loop through all values associated with a node key
            # pair the key node with each edge (key values)
            # into a two item list where the originating node is
            # is the first item and the second item is the node
            # being connected to
            # put thoses two piece lists into a larger list. 
            for edge in self.G[node]:
                edges.append([node, edge])
        return(edges)
    ############################################################
    def has_edge(self, edge_set):
        # edge should be a list
        # currently this will only work for a undirected network
        # write a test to test the case where an input "edge" is only
        # a single element
        """ Given a graph and an edge set determine if the 
        edge exists and return return true if the edge set exists
        and false if it doesn't exist.
        1) only input is 'edge_set.' This is a two item list
        where the first item is the originating node (N1) and the
        second item is the node that is being connected to (N2). note
        that this only considers the direction N1 to N2."""
        if edge_set[0] in self.G and edge_set[1] in self.G[edge_set[0]]:
            return(True)
        else:
            return(False)
    ############################################################
    def add_edge(self, edge_set):
        """given a single two element list create a link between two nodes.
        Only 1 single edge_set can be implemented with this method.
        
        1) There is only one input, edge_set, a two item list of two nodes
        to be connected. the first item in 'edge_set' is the originating
        node (N1) and the second is the node destination node (N2).
        
        Will inform user if a node or an edge set is not possible"""
        # first check to see if the edge set already exists
        node = edge_set[0]
        # make sure the node exists, but it's not already linked to the same node
        # proposed in edge_set
        if edge_set[0] in self.G and edge_set[1] not in self.G[edge_set[0]]:
            self.G[edge_set[0]].append(edge_set[1])
        elif edge_set[0] not in self.G or edge_set[1] not in self.G[edge_set[0]]:
            print("Node or node being linked to does not exist in graph")
        elif edge_set[0] in self.G and edge_set[1] in self.G[edge_set[0]]:
            print(edge_set[0], edge_set[1], "edge already exists")
    ############################################################
    def remove_edge(self, edge_set):
        """ given an edgeset check if it exists, if it does
        remove the edge.
        1) only input is 'edge_set.' This is a two item list
        where the first item is the originating node (N1) and the
        second item is the node that is being connected to (N2). note
        that this only considers the direction N1 to N2."""
        if len(edge_set) >= 2:
            if edge_set[0] in self.G and edge_set[1] in self.G[edge_set[0]]:
                self.G[edge_set[0]].remove(edge_set[1])
            else:
                print("edge set does not exist")
        else:
            print("edge set does not have enough entries")
            return(False)
    ############################################################
    def add_edges_from(self, edges_L):
        """ Add edges from a n x 2 matrix (a list of 2 element lists). The first item
        is the originating node, and the second column is the destination node or a 
        list of edge_sets. Order of the edge_sets does not matter.
        
        1) only 1 input, a list of 2 elemenet lists.
        
        If an edge set or node does not exist the user will be informed"""
        for e in edges_L:
            self.add_edge(e)
            #if e[0] in self.G and e[1] not in self.G[e[0]]:
            #    self.G[e[0]].append(e[1])
            #else:
            #    print("edge already exists")
    ############################################################
    def neighbors(self, node):
        """Return all the neighbors of a node: Takes a character string to 
        reference a single node, and returns all the neighbors of that node
        
        1) only 1 input, a character string 'node', can't be a single element
        list.
        
        If the node does not exist informs the user."""
        # check to see if the node exists in the network
        # if it doesn't inform the user.
        if bool(node) and isinstance(node, list):
            node = node[0]
        elif isinstance(node, list):
            print("This is an empty list")
            return(False)
        if node in self.G:
            return(self.G[node])
        else:
            print("Node does not exist")
            return(False)
    ############################################################
    def number_of_nodes(self):
        """ return the total number of nodes in a network.
        no input, if the network is empty returns '0'."""
        # check to see if the network is empty, if it is, inform the user.
        if bool(self.G):
            return(len(self.G.keys()))
        else:
            return(0)
    ############################################################
    def number_of_edges(self):
        """Get a count of nodes and edges currently in the graph. No
        user inputs, if the network is empty return '0'"""
        if bool(self.G):
            tot_len = 0
            # loops through each node
            for n in self.G.keys():
                tot_len = len(self.G[n]) + tot_len
            return(tot_len)
        else:
            return(0)
    ############################################################
    def degree(self,node_L=None):
        """Return a dictionary mapping a node to number of neighbors,
        for all nodes or an optional list of nodes
        
        1) One optional input 'node_L' - a list of nodes as
        a character string. If none, this will return all the number
        of neighbors of every node in the graph.
        
        If the network is empty the user will be informed"""
        # At this point must be in list form.
        # an if statement to catch character strings
        if isinstance(node_L,str):
            node_L = [node_L]
        # store the resulting dictionary of degrees in a dictionary
        degree = {}
        # check to see if the network is populated, if not
        # inform the user
        if bool(self.G):
            # if the user inputed their own list of nodes use their list
            # if not, then use all nodes in the network
            if node_L is None:
                all_nodes = self.G.keys()
            else:
                all_nodes = node_L
            # loop through all nodes, and calculated the list length
            # of each node
            for n in all_nodes:
                # create a node
                degree[n] = []
                # next add a item
                num_links = len(self.G[n])
                # add the degree to the dictionary
                degree[n].append(num_links)
        else:
            # inform the user the network is empty
            print("This network is empty")
            return(False)
        return(degree)
    ############################################################
    def clustering_coef(self,node_list):
        """Returns the clustering coef. of a node or a list of nodes 
        in dictionary form. 
        
        1) only 1 input, node_list - node_list can either be a single
        character string or a list of character strings. If a node
        does not exist the user will be informed but the method will
        continue to process items in list 'node_list.'"""
        # node_l is a list of nodes
        CC_dict = {}
        if bool(self.G) is False:
            print("Network is empty")
            return(False)
        else:
            if isinstance(node_list,str):
                node_list = [node_list]
            # go through all the nodes in node_list
            for n in node_list:
                if self.has_node(n):
                    # get the neighbors of the nodes
                    # Find the neighbors of the neighbors of node "n"            
                    N_neighbors = self.neighbors(n)
                    # find the degree of node "n"
                    K_i = self.degree(n)[n][0]
                    #print(K_i)
                    T_i = 0
                    #print(N_neighbors)
                    for neighbor in N_neighbors:
                        # NsOfN neighbor of neighbors, get all neighbors
                        # of a neighbor of the original node
                        NsOfN = self.neighbors(neighbor)
                        # find the total number of shared connections that
                        # the node neighbor has with the node 
                        T_isub = len(set(N_neighbors) & set(NsOfN))/2
                        # need to catch a none type?
                        # in a undirected graph it should always double count...?
                        #print(T_isub)
                        # sum connections
                        T_i = T_i + T_isub
                        #print(T_i)
                        #print(neighbor)
                        #print(set(N_neighbors) & set(NsOfN))
                        #print(set(N_neighbors), set(NsOfN))
                        #print()
                    # calculate the Clustering Coef.
                    #print('T_i',T_i)
                    #print('T_isub',T_isub)
                    numer = 2*(T_i)
                    denom = (K_i*(K_i-1))
                    #print(numer)
                    #print(denom)
                    C_i = numer/denom
                    CC_dict[n] = C_i
                    #print('C_i',C_i)
                else:
                    print("Node does not exist")
        return(CC_dict)
    ############################################################
    def info(self):
        """This returns general stats about the graph. 
        1) num_nodes - total number of nodes
        2) num_edgeSets - total number of edges
        3) mean_degree - mean degree of nodes in the graph
        4) degree_std - standard deviation of edges per node
        5) orph_edges - a list of edges that are not nodes
        6) orph_node - a list of nodes that have no edges
        
        All info is returned in dictionary form"""

        info = {'num_nodes':[], 'num_edgeSets':[], 'mean_degree':[], 'degree_std':[], 'orph_edges':[]}     
        # return number of nodes
        num_nodes = len(self.nodes())
        info['num_nodes'] = num_nodes
        # total number of edges
        num_edgeSets = len(self.edges())
        info['num_edgeSets'] = num_edgeSets
        # mean number of edges per node
        if num_nodes == 0:
            mean_degree = []
        else:   
            mean_degree = num_edgeSets/num_nodes
        info['mean_degree'] = mean_degree
        # standard deviation/vairance of degrees distribution
        # loop through all nodes and find the difference between
        # observed number of nodes and mean number of nodes
        tot_diff = 0
        #diff_list = []
        if bool(self.G): 
            for d in list(self.degree()):
                d_num = self.degree(d)[d][0]
                #print(d_num)
                #print(mean_degree)
                diff = (d_num - mean_degree)**2
                tot_diff = diff + tot_diff
            std = tot_diff/num_nodes
        else:
            std = []
        info['degree_std'] = std
        # return a list of orphaned edges, these do not appear as their own node
        orph_edge = []
        all_nodes = list(self.nodes())
        # loop through all the nodes and see which edges are not nodes in the network
        for e in self.edges():
            if e[1] not in all_nodes:
                orph_edge.append(e[1])
        all_orph_edges = set(orph_edge)
        # If there are no orphand edges set value equal to None
        if bool(all_orph_edges):
            info['orph_edges'] = all_orph_edges
        else:
            info['orph_edges'] = []
        # return a list of nodes with no edges
        orph_node = []
        for n in all_nodes:
            if bool(self.G[n]) == False:
                orph_node.append(n)
        if bool(orph_node) == False:
            info['orph_nodes'] = []
        return(info)

    ############################################################
    def degree_distribution(self):
        """Take a graph obj. and return data for a degree distribution of a graph/
        network. The format is essentially a 'reverse dictionary' with degree as a
        dictionary key and nodes as key values. 
    
        This function only needs a graph 
        object as input. 
    
        It will return a dictionary with the degree distribution."""
        # get graph keys and convert from set to a list
        nodes = list(self.G.keys())
        degree_dict = self.degree()
        distri = dict()
        # loop through each node
        # for each new degree add a new key for a degree number
        # nodes in this case become dictionary values
        for n in nodes:
            if degree_dict[n][0] in distri:
                distri[degree_dict[n][0]].append(n)
            else:
                distri[degree_dict[n][0]] = [n] 
        return(distri)
        
#########################################################################################
