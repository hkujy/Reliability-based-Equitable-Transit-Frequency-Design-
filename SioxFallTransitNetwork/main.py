"""
    code for visualize sioux fall network
    references:
    http://avinashu.com/tutorial/pythontutorialnew/NetworkXBasics.html
"""

import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
# For color mapping
import matplotlib.colors as colors
import matplotlib.cm as cmx
import matplotlib as mpl

def make_proxy(clr, mappable, **kwargs):
    return Line2D([0, 1], [0, 1], color=clr, **kwargs)

def read_standard_node():
    """
        read standard sioux fall nodes positions
    """
    f = open("SiouxFalls_node.tntp", "r")
    line = f.readline()
    line = f.readline()
    nodes = []
    x = []
    y = []
    while len(line):
        line = line.strip(';')
        l = line.split()
        node = int(l[0])
        pos1 = float(l[1])/1000
        pos2 = float(l[2])/1000
        line = f.readline()
        nodes.append(node)
        x.append(pos1)
        y.append(pos2)
    f.close()
    return nodes,x,y

def read_lines():
    # read bus lines of the node index
    f = open("stops.txt", "r")
    line = f.readline()
    buslines = []
    while len(line):
        line = line.strip(';')
        l = line.split()
        bl = []
        for s in range(0, len(l)-1):
            print(int(l[s]))
            bl.append(int(l[s]))
        buslines.append(bl)
        node = int(l[0])
        pos1 = float(l[1])/1000
        pos2 = float(l[2])/1000
        line = f.readline()
 
    return buslines

def standard():
    G3 = nx.DiGraph()
    f = open("SiouxFalls_flow.tntp", "r")
    line = f.readline()
    line = f.readline()
    while len(line):
        l = line.split()
        fromnode = int(l[0])
        to = int(l[1])
        volume = float(l[2])
        cost = int(float(l[3]))
        G3.add_edge(fromnode, to, weight=cost)
        line = f.readline()
    f.close()
    print(G3.number_of_edges())

    f = open("SiouxFalls_node.tntp", "r")
    line = f.readline()
    line = f.readline()
    while len(line):
        line = line.strip(';')
        l = line.split()
        node = int(l[0])
        pos1 = float(l[1])/10000
        pos2 = float(l[2])/10000
        G3.add_node(node, pos=(pos1, pos2))
        line = f.readline()
    f.close()
    print(G3.number_of_nodes())

    plt.figure(figsize=(8, 12))
    # plt.figure()
    # The positions of each node are stored in a dictionary
    node_pos = nx.get_node_attributes(G3, 'pos')
    # The edge weights of each arcs are stored in a dictionary
    arc_weight = nx.get_edge_attributes(G3, 'weight')
    # Determine the shortest path
    # If the node is in the shortest path, set it to red, else set it to white color
    # node_col = ['white' if not node in sp else 'red' for node in G3.nodes()]
    # If the edge is in the shortest path set it to red, else set it to white color
    # edge_col = ['black' if not edge in red_edges else 'red' for edge in G3.edges()]
    # Draw the nodes
    # nx.draw_networkx(G3, node_pos,node_color= node_col, node_size=450)
    nx.draw_networkx(G3, node_pos, node_size=600)
    # Draw the node labels
    # nx.draw_networkx_labels(G3, node_pos,node_color= node_col)
    # Draw the edges
    # nx.draw_networkx_edges(G3, node_pos,edge_color= edge_col)
    h1 = nx.draw_networkx_edges(G3, node_pos, edge_color="green")
    # Draw the edge labels
    # nx.draw_networkx_edge_labels(G3, node_pos,edge_color= edge_col, edge_labels=arc_weight)
    nx.draw_networkx_edge_labels(G3, node_pos, edge_labels=arc_weight)
    # Remove the axis
    plt.axis('off')
    # Show the plot

    G4 = nx.DiGraph()
    f = open("SiouxFalls_flow.tntp", "r")
    line = f.readline()
    line = f.readline()
    while len(line):
        l = line.split()
        fromnode = int(l[0])+24
        to = int(l[1]) + 24
        volume = float(l[2])
        cost = int(float(l[3]))
        G4.add_edge(fromnode, to, weight=cost)
        line = f.readline()
    f.close()

    f = open("SiouxFalls_node.tntp", "r")
    line = f.readline()
    line = f.readline()
    while len(line):
        line = line.strip(';')
        l = line.split()
        node_2 = int(l[0]) + 24
        pos1_2 = float(l[1])*1.01/1000
        pos2_2 = float(l[2])*1.01/1000
        G4.add_node(node_2, pos=(pos1_2, pos2_2))
        line = f.readline()
    f.close()
    node_pos = nx.get_node_attributes(G4, 'pos')
    # The edge weights of each arcs are stored in a dictionary
    arc_weight = nx.get_edge_attributes(G4, 'weight')
    # nx.draw_networkx(G4, node_pos, node_size=600,node_color = node_col)
    h2 = nx.draw_networkx_edges(G4, node_pos, edge_color="red")
    # nx.draw_networkx_edge_labels(G4, node_pos,edge_labels=arc_weight)

    # generate proxies with the above function
    clrs = ["green", "red"]
    proxies = [make_proxy(clr, h2, lw=2) for clr in clrs]
    # and some text for the legend -- you should use something from df.
    labels = ["Green", "red"]
    plt.legend(proxies, labels)
    plt.show()

def add_one_line(_stops,_G,_nodes,_x,_y,_ns,_x_adjust,_y_adjust):
    """
        add the edges of one line
    """
   # step 0: add nodes
    for i in range(0, len(_nodes)):
        node =  _nodes[i] + int(_ns)   # shift the nodes number
        x = _x[i] + float(_x_adjust)
        y = _y[i] + float(_y_adjust)
        _G.add_node(node, pos=(x, y))
    # step 1: add edges
    for i in range(0, len(_stops)-1):
        fromnode = _stops[i] +int(_ns)
        tonode = _stops[i+1] +int(_ns)
        _G.add_edge(fromnode, tonode)

    return


if __name__ == "__main__":
    
    mpl.rc('font',family='Times New Roman')
    mycolors = ["blue","orange","green","red","purple","brown","pink","gray","olive","cyan"]
    # step 0: read the set of bus lines
    lines = read_lines()
    for l in lines:
        print(l)
    # step 1: read standard sioux fall network nodes
    (nodes, x, y) = read_standard_node()
    # G = nx.DiGraph()
    G = nx.MultiGraph()
    plt.figure(figsize=(8, 12))
    for i in range(0, len(nodes)):
        G.add_node(nodes[i], pos=(x[i], y[i]))
    node_pos = nx.get_node_attributes(G, 'pos')
    # nx.draw_networkx(G, node_pos, node_size=500)
    # nx.draw_networkx_nodes(G,node_pos,node_size=500,node_color="lightsalmon")
    nx.draw_networkx_nodes(G,node_pos,node_size=400,node_color="orangered")
    nx.draw_networkx_labels(G,node_pos,font_family="Times New Roman",font_size=14)

    # line 0
    h = []
    # for l in range(0,len(lines)):
    for l in range(0,10):
        Gi = nx.MultiGraph()
        # add_one_line(lines[0],_G=G,_nodes=nodes,_x=x,_y=y,_ns=0,_x_adjust=0.0,_y_adjust=0.0)
        xad = pow(-1,l)*l*(0.1+0.05*l)
        yad = pow(-1,l)*l*(0.1+0.05*l)
        print(xad,yad)
        add_one_line(lines[l],_G=Gi,_nodes=nodes,_x=x,_y=y,_ns=l*24,_x_adjust=xad,_y_adjust=yad)
        node_pos = nx.get_node_attributes(Gi, 'pos')
        h.append(nx.draw_networkx_edges(Gi, node_pos, edge_color = mycolors[l],width = 2.0))
    
    proxies =[] 
    labels = []
    for i in range(0, 10): 
        labels.append("Line "+str(i+1))
        proxies.append(make_proxy(mycolors[i], h[i], lw=2))
    # and some text for the legend -- you should use something from df.
    plt.legend(proxies,labels,prop={"size":10})

 
    # G1 = nx.MultiGraph()
    # add_one_line(lines[1],_G=G1,_nodes=nodes,_x=x,_y=y,_ns=0,_x_adjust=0.1,_y_adjust=0.1)
    # node_pos = nx.get_node_attributes(G1, 'pos')
    # h1 = nx.draw_networkx_edges(G1, node_pos, edge_color = mycolors[1])
    plt.axis('off')
    plt.savefig("Buslines.png",bbox_inches='tight',dpi=600)
    # plt.show()
    plt.close()

#########################################################################
    # save each individual figure

    for nl in range(0,10):
        G = nx.MultiGraph()
        plt.figure(figsize=(8, 12))
        for i in range(0, len(nodes)):
            G.add_node(nodes[i], pos=(x[i], y[i]))
        node_pos = nx.get_node_attributes(G, 'pos')
        nx.draw_networkx_nodes(G,node_pos,node_size=400,node_color="orangered")
        nx.draw_networkx_labels(G,node_pos,font_family="Times New Roman",font_size=14)
        Gi = nx.MultiGraph()
        # add_one_line(lines[0],_G=G,_nodes=nodes,_x=x,_y=y,_ns=0,_x_adjust=0.0,_y_adjust=0.0)
        add_one_line(lines[nl],_G=Gi,_nodes=nodes,_x=x,_y=y,_ns=0,_x_adjust=0,_y_adjust=0)
        node_pos = nx.get_node_attributes(Gi, 'pos')
        h=nx.draw_networkx_edges(Gi, node_pos, edge_color = mycolors[l],width = 2.0)
        labels="Line "+str(nl+1)
        proxies = make_proxy(mycolors[nl], h, lw=2)
        # plt.legend(proxies,labels,prop={"size":10})
        plt.title("Line "+str(nl+1))
        plt.axis('off')
        plt.savefig("Line_"+str(nl+1)+".png",bbox_inches='tight',dpi=600)
        plt.close()
 

