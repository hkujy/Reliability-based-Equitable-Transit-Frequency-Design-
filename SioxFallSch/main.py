__author__ = 'Yu Jiang'
__version__ = '30-Jan-2021'
__email__ = 'yujiang@dtu.dk'
__status__ = 'complete, paper under second round review'
"""
    code for visualize sioux fall network
    references:
    http://avinashu.com/tutorial/pythontutorialnew/NetworkXBasics.html
"""
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
import matplotlib.colors as colors
import matplotlib.cm as cmx
import matplotlib as mpl

def make_proxy(clr, mappable, **kwargs):
    return Line2D([0, 1], [0, 1], color=clr, **kwargs)
def read_standard_node():
    """
        Read standard sioux fall nodes positions
    """
    f = open("SiouxFalls_node.tntp", "r",encoding='utf-8')
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
    """
        Read designed bus line data
    """
    f = open("stops.txt", "r",encoding='utf-8')
    line = f.readline()
    buslines = []
    while len(line):
        line = line.strip(';')
        # print(line)
        l = line.split()
        bl = []
        for s in range(0, len(l)-1):
            print(int(l[s]))
            bl.append(int(l[s]))
        buslines.append(bl)
        line = f.readline()
    return buslines
def add_one_line(_stops,_G,_nodes,_x,_y,_ns,_x_adjust,_y_adjust):
    """
        Add the edges of one line
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
    """
        main code for the plot
    """
    mpl.rc('font',family='Times New Roman')
    mycolors = ["blue","orange","green","red","purple","brown","pink","gray","olive","cyan",
            "darkorange","burlywood","wheat","slategray","palevioletred","lavenderblush",
            "maroon","sienna","seashell","saddlebrown"]
    # step 0: read the set of bus lines
    lines = read_lines()
    for l in lines:
        print(l)
    # step 1: read standard sioux fall network nodes
    (nodes, x, y) = read_standard_node()
    G = nx.MultiGraph()
    plt.figure(figsize=(12, 15))
    for i in range(0, len(nodes)):
        G.add_node(nodes[i], pos=(x[i], y[i]))
    node_pos = nx.get_node_attributes(G, 'pos')
    nx.draw_networkx_nodes(G,node_pos,node_size=500,node_color="orangered")
    nx.draw_networkx_labels(G,node_pos,font_family="Times New Roman",font_size=14)
    h = []
    for l in range(0,len(lines)):
        Gi = nx.MultiGraph()
        xad = pow(-1,l)*l*(0.1+0.01*l)
        yad = pow(-1,l)*l*(0.1+0.01*l)
        print(xad,yad)
        add_one_line(lines[l],_G=Gi,_nodes=nodes,_x=x,_y=y,_ns=l*24,_x_adjust=xad,_y_adjust=yad)
        node_pos = nx.get_node_attributes(Gi, 'pos')
        h.append(nx.draw_networkx_edges(Gi, node_pos, edge_color = mycolors[l],width = 2.0))
    proxies =[] 
    labels = []
    for i in range(0, len(lines)): 
        labels.append("Line "+str(i+1))
        proxies.append(make_proxy(mycolors[i], h[i], lw=2))
    plt.legend(proxies,labels,prop={"size":10})
    plt.axis('off')
    plt.savefig("Buslines.png",bbox_inches='tight',dpi=600)
    plt.close()

    #---------------------------------------------------------------------------
    # The following code plot and save individual bus lines
    for nl in range(0,len(lines)):
        G = nx.MultiGraph()
        plt.figure(figsize=(8, 12))
        for i in range(0, len(nodes)):
            G.add_node(nodes[i], pos=(x[i], y[i]))
        node_pos = nx.get_node_attributes(G, 'pos')
        nx.draw_networkx_nodes(G,node_pos,node_size=400,node_color="orangered")
        nx.draw_networkx_labels(G,node_pos,font_family="Times New Roman",font_size=14)
        Gi = nx.MultiGraph()
        add_one_line(lines[nl],_G=Gi,_nodes=nodes,_x=x,_y=y,_ns=0,_x_adjust=0,_y_adjust=0)
        node_pos = nx.get_node_attributes(Gi, 'pos')
        h=nx.draw_networkx_edges(Gi, node_pos, edge_color = mycolors[nl],width = 2.0)
        labels="Line "+str(nl+1)
        proxies = make_proxy(mycolors[nl], h, lw=2)
        plt.title("Line "+str(nl+1))
        plt.axis('off')
        plt.savefig("Line_"+str(nl+1)+".png",bbox_inches='tight',dpi=600)
        plt.close()
 

