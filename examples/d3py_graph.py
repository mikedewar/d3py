import d3py

import logging
logging.basicConfig(level=logging.DEBUG)

import networkx as nx

G=nx.Graph()
G.add_edge(1,2)

# use 'with' if you are writing a script and want to serve this up forever
with d3py.NetworkXFigure(G) as p:
    p += d3py.ForceLayout()
    p.show()
